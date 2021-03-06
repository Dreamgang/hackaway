/** The heap data structure -- heap is a nearly complete binary tree
Give array A, A[0] is the root, then

In a MAX-HEAP, the max-heap property is that for every node i other than the root.
A[parent(i)] >= A[i]

In a MIN-HEAP, the min-heap property is that for every node i other than the root.
A[parent(i)] <= A[i]

Very Important Procedures:
Max-Heapify, which runs in O(lg n)time, is the key to maintaining the max-heap property.
Build-Max-Heap, which runs in linear time, produces a max-heap from an unordered input array.
Heapsort procedure, which runs in O(n lg n) time, sorts an array in place.
Max-Heap-Insert, Heap-Extract-Max, Heap-Increase-Key, and Heap-Maximum procedures, which
run in O(lg n) time, allow the heap data structure to implement a priority queue.

*/
#include <stdio.h>
#include <limits.h>

/* data is the space to store elements
 * length is the number of elements, no matter it is heap or not
 * heap_size is the size of a heap, when data is not a heap, 
 * heap_size is 0.
 */
typedef struct heap {
    int data[100];
    int length;
    int heap_size;
} Heap;

int parent(int i){
    return (i-1)/2;
}

int left(int i){
    return 2*i+1;
}

int right(int i){
    return 2*(i+1);
}

void swap(Heap *A, int i, int j){
    A->data[i] = A->data[i] + A->data[j];
    A->data[j] = A->data[i] - A->data[j];
    A->data[i] = A->data[i] - A->data[j];
}

/* sort the i element, although recursive but lg n time.
 * think about a triangle consist of i, i-left, i-right nodes
 * find out the index of largest value of three
 * if the index is i itself, it means done
 * else swap the i and the index, focus on the largest index
 * and run again.
 * it results the larger value goes up and smaller value down
 * because every tine it chooses one branch to go down, so
 * the time is O(lg n)
 */
void max_heapify(Heap *A, int i){
    int l = left(i);
    int r = right(i);
    int largest;
    if ((l < A->heap_size) && (A->data[l] > A->data[i])){
        largest = l;
    } else {
        largest = i;
    }
    if ((r < A->heap_size) && (A->data[r] > A->data[largest])){
        largest = r;
    }
    if (largest != i){
        swap(A, i, largest);
        max_heapify(A, largest);
    }
}

// Note: for a nearly complete tree, start from 0, tree->length/2 is the 
// first leave node. So, if we want to build a heap, we should start 
// from the last node that is not a leaf node, and go up to the root
// step by step
// time: n / 2 * lg n => n(lg n)
void build_max_heap(Heap *A){
    A->heap_size = A->length;
    for (int i = A->length/2-1 ; i >= 0; i--){       // n / 2
        max_heapify(A, i);                           // lg n
    }
}


/* firstly, build a max heap
 * iterate from the last one to the second one
 * swap the first one and the iterate one
 * and shrink the swap size to exclude the last one
 * cause the maximum be placed the last position
 * now, it is not a heap anymore, so heap_size set 
 * to 0 is proper.
 */
void heapsort(Heap *A){
    build_max_heap(A);                      // n(lg n)
    for (int i=A->heap_size-1; i>0; i--){   // n - 1 
        swap(A, 0, i);
        A->heap_size--;                     // modify heap_size
        max_heapify(A, 0);                  // lg n
    }
}


void println(Heap *A){
    printf("Heap size: %d\n", A->heap_size);
    for (int i = 0; i < A->heap_size; i++){
        printf("%d ", A->data[i]);
    }
    putchar('\n');
}

int heap_maximum(Heap *A){
    if (A->heap_size <= 0){
        puts("Error: heap is empty!");
        return -1;
    }
    return A->data[0];
}

/* judgement
 * get the first one, swap the first and 
 * the last one and shrink the heap size
 * finally heapify on the new first value
 * causes length and heap size inequal
 */
int heap_extract_max(Heap *A){
    int max;

    if (A->heap_size <= 0){
        puts("Error: heap is empty!");
        return -1;
    }
    max = A->data[0];
    A->data[0] = A->data[A->heap_size-1];
    A->heap_size--;
    max_heapify(A, 0);
    return max;
}


// go up with the chain of parents
void heap_increase_key(Heap *A, int i, int key){
    if (key < A->data[i]){
        puts("Error! New key is smaller than current key");
        return;
    }
    A->data[i] = key;
    while ((i > 0) && (A->data[parent(i)] < A->data[i])){
        swap(A, i, parent(i));
        i = parent(i);
    }
}


void max_heap_insert(Heap *A, int key){
    A->heap_size = A->heap_size + 1;
    A->data[A->heap_size-1] = INT_MIN;
    heap_increase_key(A, A->heap_size-1, key);
}


void main(){
    Heap A = {.data={4, 1, 3, 2, 16, 9, 10, 14, 8, 7}, 
              .length=10,
              .heap_size=0};
    build_max_heap(&A);
    println(&A);

    int max = heap_extract_max(&A);
    printf("Maximum is: %d\n", max);
    printf("After extract maximum: ");
    println(&A);

    heapsort(&A);
    puts("after sort");
    for (int i = 0; i < A.length; i++)
        printf("%d ", A.data[i]);
    putchar('\n');

    // after heapsort, the heap is broken
    // so need to rebuild it
    build_max_heap(&A);

    printf("After insert 25: ");
    max_heap_insert(&A, 25);
    println(&A);

}
