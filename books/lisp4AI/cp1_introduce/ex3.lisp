(defun count-number (lst)
  "count number in a list"
  (if (null lst)
      0
      (if (numberp (car lst))
	  (+ 1 (count-number (cdr lst)))
	  (+ 0 (count-number (cdr lst))))))

(defun count-number-2 (lst)
  (cond ((null lst) 0)
	((numberp (car lst))
	 (+ 1 (count-number (cdr lst))))
	(t (count-number (cdr lst)))))

(defun count-number-3 (lst)
  "decide list and atom in difference branch"
  (cond ((null lst) 0)
	((numberp lst) 1)
	((not (listp lst)) 0)
	(t (+ (count-number-3 (car lst))
	      (count-number-3 (cdr lst))))))

(defun count-atom (lst)
  "count atoms in a list"
  (if (null lst)
      0
      (if (atom (car lst))
	  (+ 1 (count-atom (cdr lst)))
	  (+ 0 (count-atom (cdr lst))))))