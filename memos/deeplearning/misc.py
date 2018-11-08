"""
convolution network
"""
import numpy as np

def valid(width, kernel, pad, slide):
    res = (width - kernel + 2 * pad)/slide + 1
    return res == int(res)

def bn(x, e=1e-7):
    """before we pass x to next conv, we apply
    batch normalization"""
    mu = np.mean(x)
    sigma2 = np.var(x)
    x_ = (x - mu) / np.sqrt(sigma2 + e)
    return x_

if __name__ == "__main__":
    width = 224
    kernel = 11
    pad = 0
    slide = 4
    print(valid(width, kernel, pad, slide))
    width = 227
    print(valid(width, kernel, pad, slide))

    # 
    x = np.array([1, 2, 3, 4, 5])
    x_ = bn(x)
    print(x_)