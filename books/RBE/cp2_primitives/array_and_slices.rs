use std::mem;

fn analyze_slice(slice: &[i32]) {
    println!("First element of the slice: {}", slice[0]);
    println!("The slice has {} elements", slice.len());
}

fn main() {
    let xs: [i32; 5] = [1, 2, 3, 4, 5];

    // init
    let ys: [i32; 500] = [0; 500];

    println!("First element of the array: {}", xs[0]);
    println!("Array size is {}", xs.len());

    // memory bytes
    println!("array occupies {} bytes", mem::size_of_val(&xs));
    // automatically borrowed as slices
    analyze_slice(&xs);

    // slices can point to a section of an array
    analyze_slice(&ys[1 .. 4]);
}
