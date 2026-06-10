#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 1000  // Max number of integers in the file

int main() {
    FILE* fp = fopen("number.txt", "r");
    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    int numbers[MAX_SIZE];
    int count = 0;

    // Read numbers into the array
    while (fscanf(fp, "%d", &numbers[count]) != EOF && count < MAX_SIZE) {
        count++;
    }

    fclose(fp);

    int mode = numbers[0];
    int maxCount = 0;

    // Linear search to find the mode
    for (int i = 0; i < count; i++) {
        int current = numbers[i];
        int currentCount = 0;

        for (int j = 0; j < count; j++) {
            if (numbers[j] == current) {
                currentCount++;
            }
        }

        if (currentCount > maxCount) {
            maxCount = currentCount;
            mode = current;
        }
    }

    printf("Mode: %d (occurred %d times)\n", mode, maxCount);

    return 0;
}
