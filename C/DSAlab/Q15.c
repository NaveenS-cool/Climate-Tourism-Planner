#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#define MAX 100

typedef struct {
    int value;
    int arrIndex; 
    int nextIndex; 
} HeapNode;

void swap(HeapNode *a, HeapNode *b) {
    HeapNode temp = *a;
    *a = *b;
    *b = temp;
}

void heapify(HeapNode heap[], int size, int i) {
    int smallest = i;
    int left = 2*i + 1;
    int right = 2*i + 2;
    if (left < size && heap[left].value < heap[smallest].value)
        smallest = left;
    if (right < size && heap[right].value < heap[smallest].value)
        smallest = right;
    if (smallest != i) {
        swap(&heap[i], &heap[smallest]);
        heapify(heap, size, smallest);
    }
}

void mergeKSortedArrays(int arr[][MAX], int sizes[], int k) {
    HeapNode heap[MAX];
    int i;
    int heapSize = 0;
    for (i = 0; i < k; i++) {
        if (sizes[i] > 0) {
            heap[heapSize].value = arr[i][0];
            heap[heapSize].arrIndex = i;
            heap[heapSize].nextIndex = 1;
            heapSize++;
        }
    }
    for (i = (heapSize - 1) / 2; i >= 0; i--) {
        heapify(heap, heapSize, i);
    }
    printf("\nMerged Sorted List: ");
    while (heapSize > 0) {
        HeapNode root = heap[0];
        printf("%d ", root.value);
        if (root.nextIndex < sizes[root.arrIndex]) {
            heap[0].value = arr[root.arrIndex][root.nextIndex];
            heap[0].arrIndex = root.arrIndex;
            heap[0].nextIndex = root.nextIndex + 1;
        } else {
            heap[0] = heap[heapSize - 1];
            heapSize--;
        }
        heapify(heap, heapSize, 0);
    }
}

int main() {
    int k, i, j;
    int arr[MAX][MAX], sizes[MAX];
    printf("Enter number of sorted lists (k): ");
    scanf("%d", &k);
    for (i = 0; i < k; i++) {
        printf("Enter size of list %d: ", i + 1);
        scanf("%d", &sizes[i]);
        printf("Enter %d sorted elements: ", sizes[i]);
        for (j = 0; j < sizes[i]; j++) {
            scanf("%d", &arr[i][j]);
        }
    }
    mergeKSortedArrays(arr, sizes, k);
    return 0;
}
