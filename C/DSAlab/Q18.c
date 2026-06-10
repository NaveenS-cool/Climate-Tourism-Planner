
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int steps;

void bubbleSort(int arr[], int n) {
    steps = 0;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            steps++;
            if (arr[j] < arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

void insertionSort(int arr[], int n) {
    steps = 0;
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] < key) {
            arr[j + 1] = arr[j];
            j--;
            steps++;
        }
        arr[j + 1] = key;
    }
}

int getMax(int arr[], int n) {
    int mx = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > mx)
            mx = arr[i];
    return mx;
}

void countingSort(int arr[], int n, int exp) {
    int output[n];
    int count[10] = {0};
    for (int i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;
    for (int i = 8; i >= 0; i--)
        count[i] += count[i + 1];
    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }
    for (int i = 0; i < n; i++)
        arr[i] = output[i];
}

void radixSort(int arr[], int n) {
    steps = 0;
    int m = getMax(arr, n);
    for (int exp = 1; m / exp > 0; exp *= 10) {
        countingSort(arr, n, exp);
        steps++;
    }
}

void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    int L[n1], R[n2];
    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        steps++;
        if (L[i] >= R[j])
            arr[k++] = L[i++];
        else
            arr[k++] = R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j < high; j++) {
        steps++;
        if (arr[j] >= pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return (i + 1);
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void display(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    FILE *fp;
    int arr[100], n = 0, choice, temp[100];
    fp = fopen("numbers.txt", "r");
    if (fp == NULL) {
        printf("File not found\n");
        return 0;
    }
    while (fscanf(fp, "%d", &arr[n]) != EOF)
        n++;
    fclose(fp);

    do {
        printf("\nMenu\n1. Bubble Sort\n2. Insertion Sort\n3. Radix Sort\n4. Merge Sort\n5. Quick Sort\n6. Exit\nEnter choice: ");
        scanf("%d", &choice);
        for (int i = 0; i < n; i++) temp[i] = arr[i];
        switch (choice) {
            case 1:
                bubbleSort(temp, n);
                printf("Sorted Array: ");
                display(temp, n);
                printf("Steps: %d\n", steps);
                break;
            case 2:
                insertionSort(temp, n);
                printf("Sorted Array: ");
                display(temp, n);
                printf("Steps: %d\n", steps);
                break;
            case 3:
                radixSort(temp, n);
                printf("Sorted Array: ");
                display(temp, n);
                printf("Steps: %d\n", steps);
                break;
            case 4:
                steps = 0;
                mergeSort(temp, 0, n - 1);
                printf("Sorted Array: ");
                display(temp, n);
                printf("Steps: %d\n", steps);
                break;
            case 5:
                steps = 0;
                quickSort(temp, 0, n - 1);
                printf("Sorted Array: ");
                display(temp, n);
                printf("Steps: %d\n", steps);
                break;
            case 6:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice\n");
        }
    } while (choice != 6);

    return 0;
}
