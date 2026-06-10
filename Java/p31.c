#include <stdio.h>

#define MAX 100

// Function to convert normal matrix to sparse tuple
void convertToSparse(int mat[MAX][MAX], int rows, int cols, int sparse[MAX][3]) {
    int k = 1; // index for sparse tuple
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (mat[i][j] != 0) {
                sparse[k][0] = i;
                sparse[k][1] = j;
                sparse[k][2] = mat[i][j];
                k++;
            }
        }
    }
    sparse[0][0] = rows;
    sparse[0][1] = cols;
    sparse[0][2] = k - 1; // count of non-zero elements
}

// Function to add two sparse matrices
void addSparse(int s1[MAX][3], int s2[MAX][3], int sum[MAX][3]) {
    int i = 1, j = 1, k = 1;
    if (s1[0][0] != s2[0][0] || s1[0][1] != s2[0][1]) {
        printf("Matrices cannot be added!\n");
        return;
    }

    sum[0][0] = s1[0][0];
    sum[0][1] = s1[0][1];

    while (i <= s1[0][2] && j <= s2[0][2]) {
        if (s1[i][0] < s2[j][0] || (s1[i][0] == s2[j][0] && s1[i][1] < s2[j][1])) {
            sum[k][0] = s1[i][0];
            sum[k][1] = s1[i][1];
            sum[k][2] = s1[i][2];
            i++; k++;
        }
        else if (s2[j][0] < s1[i][0] || (s1[i][0] == s2[j][0] && s2[j][1] < s1[i][1])) {
            sum[k][0] = s2[j][0];
            sum[k][1] = s2[j][1];
            sum[k][2] = s2[j][2];
            j++; k++;
        }
        else {
            sum[k][0] = s1[i][0];
            sum[k][1] = s1[i][1];
            sum[k][2] = s1[i][2] + s2[j][2];
            i++; j++; k++;
        }
    }

    while (i <= s1[0][2]) {
        sum[k][0] = s1[i][0];
        sum[k][1] = s1[i][1];
        sum[k][2] = s1[i][2];
        i++; k++;
    }

    while (j <= s2[0][2]) {
        sum[k][0] = s2[j][0];
        sum[k][1] = s2[j][1];
        sum[k][2] = s2[j][2];
        j++; k++;
    }

    sum[0][2] = k - 1;
}

// Function to transpose sparse matrix
void transposeSparse(int s[MAX][3], int t[MAX][3]) {
    int rows = s[0][0], cols = s[0][1], terms = s[0][2];
    t[0][0] = cols;
    t[0][1] = rows;
    t[0][2] = terms;

    int k = 1;
    for (int col = 0; col < cols; col++) {
        for (int i = 1; i <= terms; i++) {
            if (s[i][1] == col) {
                t[k][0] = s[i][1];
                t[k][1] = s[i][0];
                t[k][2] = s[i][2];
                k++;
            }
        }
    }
}

// Function to display sparse tuple
void displaySparse(int s[MAX][3]) {
    int terms = s[0][2];
    printf("Row Col Val\n");
    for (int i = 0; i <= terms; i++) {
        printf("%d   %d   %d\n", s[i][0], s[i][1], s[i][2]);
    }
    printf("\n");
}

int main() {
    int rows, cols;

    printf("Enter number of rows and cols of the scene: ");
    scanf("%d %d", &rows, &cols);

    int layer1[MAX][MAX] = {0}, layer2[MAX][MAX] = {0}, layer3[MAX][MAX] = {0};
    int s1[MAX][3], s2[MAX][3], s3[MAX][3], sum12[MAX][3], finalSum[MAX][3], trans[MAX][3];

    printf("Enter Layer 1 (Static buildings) matrix:\n");
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            scanf("%d", &layer1[i][j]);

    printf("Enter Layer 2 (Moving vehicles) matrix:\n");
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            scanf("%d", &layer2[i][j]);

    printf("Enter Layer 3 (Animated characters) matrix:\n");
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            scanf("%d", &layer3[i][j]);

    // Convert to sparse
    convertToSparse(layer1, rows, cols, s1);
    convertToSparse(layer2, rows, cols, s2);
    convertToSparse(layer3, rows, cols, s3);

    printf("\nSparse representation of Layer 1:\n");
    displaySparse(s1);
    printf("Sparse representation of Layer 2:\n");
    displaySparse(s2);
    printf("Sparse representation of Layer 3:\n");
    displaySparse(s3);

    // Add layer1 and layer2
    addSparse(s1, s2, sum12);

    // Add result with layer3
    addSparse(sum12, s3, finalSum);

    printf("Final transformation sparse matrix:\n");
    displaySparse(finalSum);

    // Transpose before sending to GPU
    transposeSparse(finalSum, trans);

    printf("Transposed sparse matrix (sent to GPU):\n");
    displaySparse(trans);

    return 0;
}