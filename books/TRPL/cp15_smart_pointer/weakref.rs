use std::rc::{Rc, Weak};
use std::cell::RefCell;

#[derive(Debug)]
struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak::new()),                              // nothing 
        children: RefCell::new(vec![]),                                 // empty vector
    });

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());     // None

    let branch = Rc::new(Node {
        value: 5,
        parent: RefCell::new(Weak::new()),                              // None
        children: RefCell::new(vec![leaf.clone()]),                     // leaf as children
    });

    *leaf.parent.borrow_mut() = Rc::downgrade(&branch);                 // link branch to leaf as weak reference
    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
}