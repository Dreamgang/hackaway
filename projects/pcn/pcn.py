import numpy as np
import cv2
import torch

from models import PCN1, PCN2, PCN3

EPS = 1e-5
net_ = [None, None, None]
minFace_ = 20 * 1.4
scale_ = 1.414
stride_ = 8
classThreshold_ = [0.37, 0.43, 0.97]
nmsThreshold_ = [0.8, 0.8, 0.3]
angleRange_ = 45
stable_ = 0
period_ = 30
trackThreshold_ = .95
augScale_ = 0.15


class Window:
    def __init__(self, x, y, width, angle, score):
        self.x = x
        self.y = y
        self.width = width
        self.angle = angle
        self.score = score

class Window2:
    def __init__(self, x, y, w, h, angle, scale, conf):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.angle = angle
        self.scale = scale
        self.conf = conf


# notation
list_win2 = [Window2(1,1,1,1,1,1,1)]

def rotate_point(x, y, centerX, centerY, angle):
    x -= centerX
    y -= centerY
    theta = -angle * np.pi / 180
    rx = int(centerX + x * np.cos(theta) - y * np.sin(theta))
    ry = int(centerY + x * np.sin(theta) + y * np.cos(theta))
    return rx, ry


def draw_line(img, pointlist):
    thick = 2
    cyan = (0, 255, 255)
    blue = (0, 0, 255)
    cv2.line(img, pointlist[0], pointlist[1], cyan, thick)
    cv2.line(img, pointlist[1], pointlist[2], cyan, thick)
    cv2.line(img, pointlist[2], pointlist[3], cyan, thick)
    cv2.line(img, pointlist[3], pointlist[0], blue, thick)

def draw_face(img, face:Window):
    x1 = face.x
    y1 = face.y
    x2 = face.width + face.x -1
    y2 = face.width + face.y -1
    centerX = (x1 + x2) // 2
    centerY = (y1 + y2) // 2
    lst = (x1, y1), (x1, y2), (x2, y2), (x2, y1)
    pointlist = []
    for x, y in lst:
        rx, ry = rotate_point(x, y, centerX, centerY, face.angle)
        pointlist.append((rx, ry))
    draw_line(img, pointlist)

def crop_face(img, face:Window, cropsize):
    pass

## that all above PCN.h
## following is PCN.cpp
def loadModel():
    pcn1 = torch.load('pth/pcn1.pth')
    pcn2 = torch.load('pth/pcn2.pth')
    pcn3 = torch.load('pth/pcn3.pth')
    net_[0] = pcn1
    net_[1] = pcn2
    net_[2] = pcn3
    return net_

def resizeImg(img, scale:float):
    h, w = img.shape[:2]
    h_, w_ = int(h / scale), int(w / scale)
    ret = cv2.resize(img, (w_, h_), interpolation=cv2.INTER_NEAREST)
    return ret

def legal(x, y, img):
    if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
        return True
    else:
        return False

def inside(x, y, rect:Window2):
    if rect.x <= x < rect.x + rect.w and rect.y <= y < rect.y + rect.h:
        return True
    else:
        return False

def smooth_angle(a, b):
    if a > b:
        a, b = b, a
    # a <= b
    diff = (b - a) % 360
    if diff < 180:
        return a + diff // 2
    else:
        return b + (360 - diff) // 2

prelist = []
import copy
def smooth_window(winlist):
    global prelist
    for win in winlist:
        for pwin in prelist:
            if IoU(win, pwin) > 0.9:
                win.conf = (win.conf + pwin.conf) / 2
                win.x = pwin.x
                win.y = pwin.y
                win.w = pwin.w
                win.h = pwin.h
                win.angle = pwin.angle
            elif IoU(win, pwin) > 0.6:
                win.conf = (win.conf + pwin.conf) / 2
                win.x = (win.x + pwin.x) // 2
                win.y = (win.y + pwin.y) // 2
                win.w = (win.w + pwin.w) // 2
                win.h = (win.h + pwin.h) // 2
                win.angle = smooth_angle(win.angle, pwin.angle)
    prelist = copy.deepcopy(winlist)
    return winlist

def IoU(w1:Window2, w2:Window2) -> float:
    xOverlap = max(0, min(w1.x + w1.w - 1, w2.x + w2.w - 1) - max(w1.x, w2.x) + 1)
    yOverlap = max(0, min(w1.y + w1.h - 1, w2.y + w2.h - 1) - max(w1.y, w2.y) + 1)
    intersection = xOverlap * yOverlap
    unio = w1.w * w1.h + w2.w * w2.h - intersection
    return intersection / unio

def NMS(winlist:list_win2, local:bool, threshold:float) -> list_win2:
    length = len(winlist)
    if length == 0:
        return winlist
    winlist.sort(key=lambda x: x.conf, reverse=True)
    flag = [0] * length
    for i in range(length):
        if flag[i]:
            continue
        for j in range(i+1, length):
            if local and abs(winlist[i].scale - winlist[j].scale) > EPS:
                continue
            if IoU(winlist[i], winlist[j]) > threshold:
                flag[j] = 1
    ret = [winlist[i] for i in range(length) if not flag[i]]
    return ret

def deleteFP(winlist:list_win2):
    length = len(winlist)
    if length == 0:
        return winlist
    winlist.sort(key=lambda x: x.conf, reverse=True)
    flag = [0] * length
    for i in range(length):
        if flag[i]:
            continue
        for j in range(i+1, length):
            win = winlist[j]
            if inside(win.x, win.y, winlist[i]) and inside(win.x + win.w - 1, win.y + win.h - 1, winlist[i]):
                flag[j] = 1
    ret = [winlist[i] for i in range(length) if not flag[i]]
    return ret

def preprocess_img(img, dim=None):
    if dim:
        img = cv2.resize(img, (dim, dim))
    return img - np.array([104, 117, 123])

# method overload allow input as vector
def set_input(img):
    if type(img) == list:
        img = np.stack(img, axis=0)
    else:
        img = img[np.newaxis, :, :, :]
    img = img.transpose((0, 3, 1, 2))
    return torch.FloatTensor(img)

def pad_img(img):
    row = min(int(img.shape[0] * 0.2), 100)
    col = min(int(img.shape[1] * 0.2), 100)
    ret = cv2.copyMakeBorder(img, row, row, col, col, cv2.BORDER_CONSTANT)
    return ret

def trans_window(img, img_pad, winlist: list_win2):
    row = (img_pad.shape[0] - img.shape[0]) // 2
    col = (img_pad.shape[1] - img.shape[1]) // 2
    ret = list()
    for win in winlist:
        if win.w > 0 and win.h > 0:
            ret.append(Window(win.x-col, win.y-row, win.w, win.angle, win.conf))
    return ret

def stage1(img, img_pad, net, thres):
    row = (img_pad.shape[0] - img.shape[0]) // 2
    col = (img_pad.shape[1] - img.shape[1]) // 2
    print("row={}, col={}".format(row, col))
    winlist = []
    netSize = 24
    curScale = minFace_ / netSize
    img_resized = resizeImg(img, curScale)
    print("thres={}".format(thres))
    print("resizeIMG: rows={}, cols={}".format(img_resized.shape[0], img_resized.shape[1]))
    print("before while: curScale={}, minFace_={}".format(curScale, minFace_))
    print("here go in while\n")
    while min(img_resized.shape[:2]) >= netSize:
        img_resized = preprocess_img(img_resized)
        net_input = set_input(img_resized)
        net.eval()
        # reg -> bbox, prob -> cls_prob
        cls_prob, rotate, bbox = net(net_input)
        w = netSize * curScale
        print('\nw = {:.3f}'.format(w))
        print("prob shape: = ", cls_prob.shape)
        print("prob->height = ", cls_prob.shape[2])
        print("prob->width = ", cls_prob.shape[3])
        for i in range(cls_prob.size()[2]): # cls_prob[2]->height        
            for j in range(cls_prob.size()[3]): # cls_prob[3]->width
                if cls_prob[0, 1, i, j].item() > thres:
                    sn = bbox[0, 0, i, j].item()
                    xn = bbox[0, 1, i, j].item()
                    yn = bbox[0, 2, i, j].item()
                    rx = int(j * curScale * stride_ - 0.5 * sn * w + sn * xn * w + 0.5 * w) + col
                    ry = int(i * curScale * stride_ - 0.5 * sn * w + sn * yn * w + 0.5 * w) + row
                    rw = int(w * sn)
                    if legal(rx, ry, img_pad) and legal(rx + rw - 1, ry + rw -1, img_pad):
                        if (rotate[0, 1, i, j].item() > 0.5):
                            winlist.append(Window2(rx, ry, rw, rw, 0, curScale, cls_prob[0, 1, i, j].item()))
                        else:
                            winlist.append(Window2(rx, ry, rw, rw, 180, curScale, cls_prob[0, 1, i, j].item()))
        img_resized = resizeImg(img_resized, scale_)                    
        curScale = img.shape[0] / img_resized.shape[0]
        print('resize stage:')
        print("resizeimg: \nrows={}\n cols={}".format(img_resized.shape[0], img_resized.shape[1]))
        print("curScale = {:.3f}".format(curScale))
        print("winlist count: ", len(winlist))
        
    return winlist                
    


def stage2(img, img180, net, thres, dim, winlist):
    length = len(winlist)
    if length == 0:
        return winlist
    datalist = []
    height = img.shape[0]
    for win in winlist:
        if abs(win.angle) < EPS:
            datalist.append(preprocess_img(img[win.y:win.y+win.h, win.x:win.x+win.w,:], dim))
        else:
            y2 = win.y + win.h -1
            y = height - 1 - y2
            datalist.append(preprocess_img(img[y:y+win.h, win.x:win.x+win.w, :], dim))
    net_input = set_input(datalist)
    net.eval()
    cls_prob, rotate, bbox = net(net_input)
    ret = []
    for i in range(length):
        if cls_prob[i, 1].item() > thres:
            sn = bbox[i, 0].item()
            xn = bbox[i, 1].item()
            yn = bbox[i, 2].item()
            cropX = winlist[i].x
            cropY = winlist[i].y 
            cropW = winlist[i].w
            if abs(winlist[i].angle) > EPS:
                cropY = height - 1 - (cropY + cropW - 1)
            w = int(sn * cropW)
            x = int(cropX - 0.5 * sn * cropW + cropW * sn * xn + 0.5 * cropW)
            y = int(cropY - 0.5 * sn * cropW + cropW * sn * yn + 0.5 * cropW)
            maxRotateScore = 0
            maxRotateIndex = 0
            for j in range(3):
                if rotate[i, j].item() > maxRotateScore:
                    maxRotateScore = rotate[i, j].item()
                    maxRotateIndex = j
            if legal(x, y, img) and legal(x+w-1, y+w-1, img):
                angle = 0
                if abs(winlist[i].angle) < EPS:
                    if maxRotateIndex == 0:
                        angle = 90
                    elif maxRotateIndex == 1:
                        angle = 0
                    else:
                        angle = -90
                    ret.append(Window2(x, y, w, w, angle, winlist[i].scale, cls_prob[i, 1].item()))
                else:
                    if maxRotateIndex == 0:
                        angle = 90
                    elif maxRotateIndex == 1:
                        angle = 180
                    else:
                        angle = -90
                    ret.append(Window2(x, height-1-(y+w-1), w, w, angle, winlist[i].scale, cls_prob[i, 1].item()))
    return ret

def stage3(img, img180, img90, imgNeg90, net, thres, dim, winlist):
    length = len(winlist)
    if length == 0:
        return winlist
    
    datalist = []
    height, width = img.shape[:2]

    for win in winlist:
        if abs(win.angle) < EPS:
            datalist.append(preprocess_img(img[win.y:win.y+win.h, win.x:win.x+win.w, :], dim))
        elif abs(win.angle - 90) < EPS:
            datalist.append(preprocess_img(img90[win.x:win.x+win.w, win.y:win.y+win.h, :], dim))
        elif abs(win.angle + 90) < EPS:
            x = win.y
            y = width - 1 - (win.x + win.w -1)
            datalist.append(preprocess_img(imgNeg90[y:y+win.h, x:x+win.w, :], dim))
        else:
            y2 = win.y + win.h - 1
            y = height - 1 - y2 
            datalist.append(preprocess_img(img90[win.x:win.x+win.w, win.y:win.y+win.h, :], dim))
    net_input = set_input(datalist)
    net.eval()
    cls_prob, rotate, bbox = net(net_input)
    ret = []

    for i in range(length):
        if True or cls_prob[i, 1].item() > thres:
            sn = bbox[i, 0].item()
            xn = bbox[i, 1].item()
            yn = bbox[i, 2].item()
            cropX = winlist[i].x
            cropY = winlist[i].y
            cropW = winlist[i].w
            img_tmp = img
            if abs(winlist[i].angle - 180) < EPS:
                cropY = height - 1 - (cropY + cropW -1)
                img_tmp = img180
            elif abs(winlist[i].angle - 90) < EPS:
                cropX, cropY = cropY, cropX
                img_tmp = img90
            elif abs(winlist[i].angle + 90) < EPS:
                cropX = winlist[i].y
                cropY = width -1 - (winlist[i].x + winlist[i].w - 1)
                img_tmp = imgNeg90
    
            w = int(sn * cropW)
            x = int(cropX - 0.5 * sn * cropW + cropW * sn * xn + 0.5 * cropW)
            y = int(cropY - 0.5 * sn * cropW + cropW * sn * yn + 0.5 * cropW)
            angle = angleRange_ * rotate[i, 0].item()
            if legal(x, y, img_tmp) and legal(x+w-1, y+w-1, img_tmp):
                if abs(winlist[i].angle) < EPS:
                    ret.append(Window2(x, y, w, w, angle, winlist[i].scale, cls_prob[i, 1].item()))
                elif abs(winlist[i].angle - 180) < EPS:
                    ret.append(Window2(x, height-1-(y+w-1), w, w, 180-angle, winlist[i].scale, cls_prob[i, 1].item()))
                elif abs(winlist[i].angle - 90) < EPS:
                    ret.append(Window2(y, x, w, w, 90-angle, winlist[i].scale, cls_prob[i, 1].item()))
                else:
                    ret.append(Window2(width-y-w, x, w, w, -90+angle, winlist[i].scale, cls_prob[i, 1].item()))
    return ret

def detect(img, img_pad):
    img180 = cv2.flip(img, 0)
    img90 = cv2.transpose(img_pad)
    imgNeg90 = cv2.flip(img90, 0)
    
    winlist = stage1(img, img_pad, net_[0], classThreshold_[0])
    print("\nstage1: winlist", len(winlist))
    winlist = NMS(winlist, True, nmsThreshold_[0])
    print("\nstage1 NMS: winlist", len(winlist))

    winlist = stage2(img_pad, img180, net_[1], classThreshold_[1], 24, winlist)
    print("\nstage2: winlist", len(winlist))
    winlist = NMS(winlist, True, nmsThreshold_[1])
    print("\nstage2 NMS: winlist", len(winlist))

    winlist = stage3(img_pad, img180, img90, imgNeg90, net_[2], classThreshold_[2], 48, winlist)
    print("\nstage3: winlist", len(winlist))
    winlist = NMS(winlist, False, nmsThreshold_[2])
    print("\nstage3 NMS: winlist", len(winlist))
    winlist = deleteFP(winlist)
    print("\ndeleteFP: winlist", len(winlist))
    return winlist

def track(img, net, thres, dim, winlist):
    pass

def pcn_detect(img):
    img_pad = pad_img(img)
    winlist = detect(img, img_pad)
    if stable_:
        winlist = smooth_window(winlist)
    return trans_window(img, img_pad, winlist)

if __name__ == '__main__':
    loadModel()
    img = cv2.imread('0.jpg') 
    faces = pcn_detect(img)
    for face in faces:
        draw_face(img, face)
    cv2.imshow("PCN", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()