
#include <stdio.h>
#include <stdlib.h>

#define RAM 4000

typedef struct Block {
    int pid;
    int size;
    struct Block *next;
} Block;

Block *head = NULL;

void initMemory() {
    head = (Block*)malloc(sizeof(Block));
    head->pid = 0;
    head->size = RAM;
    head->next = NULL;
}

void displayMemory() {
    Block *curr = head;
    printf("\nMemory Map\n");
    int i = 0;
    while (curr) {
        if (curr->pid == 0)
            printf("Block %d: FREE (%d KB)\n", i, curr->size);
        else
            printf("Block %d: P%d (%d KB)\n", i, curr->pid, curr->size);
        curr = curr->next;
        i++;
    }
    printf("----------------------\n");
}

void mergeFreeBlocks() {
    Block *curr = head;
    while (curr && curr->next) {
        if (curr->pid == 0 && curr->next->pid == 0) {
            curr->size += curr->next->size;
            Block *temp = curr->next;
            curr->next = curr->next->next;
            free(temp);
        } else {
            curr = curr->next;
        }
    }
}

int allocateFirstFit(int pid, int size) {
    Block *curr = head;
    while (curr) {
        if (curr->pid == 0 && curr->size >= size) {
            if (curr->size > size) {
                Block *newBlock = (Block*)malloc(sizeof(Block));
                newBlock->pid = 0;
                newBlock->size = curr->size - size;
                newBlock->next = curr->next;

                curr->next = newBlock;
                curr->size = size;
            }
            curr->pid = pid;
            return 1;
        }
        curr = curr->next;
    }
    return 0;
}

int allocateBestFit(int pid, int size) {
    Block *curr = head, *best = NULL;
    while (curr) {
        if (curr->pid == 0 && curr->size >= size) {
            if (!best || curr->size < best->size)
                best = curr;
        }
        curr = curr->next;
    }
    if (!best) return 0;

    if (best->size > size) {
        Block *newBlock = (Block*)malloc(sizeof(Block));
        newBlock->pid = 0;
        newBlock->size = best->size - size;
        newBlock->next = best->next;

        best->next = newBlock;
        best->size = size;
    }
    best->pid = pid;
    return 1;
}

int allocateWorstFit(int pid, int size) {
    Block *curr = head, *worst = NULL;
    while (curr) {
        if (curr->pid == 0 && curr->size >= size) {
            if (!worst || curr->size > worst->size)
                worst = curr;
        }
        curr = curr->next;
    }
    if (!worst) return 0;

    if (worst->size > size) {
        Block *newBlock = (Block*)malloc(sizeof(Block));
        newBlock->pid = 0;
        newBlock->size = worst->size - size;
        newBlock->next = worst->next;

        worst->next = newBlock;
        worst->size = size;
    }
    worst->pid = pid;
    return 1;
}

void freeProcess(int pid) {
    Block *curr = head;
    int found = 0;
    while (curr) {
        if (curr->pid == pid) {
            curr->pid = 0;
            found = 1;
        }
        curr = curr->next;
    }
    if (!found) printf("Process P%d not found!\n", pid);
    mergeFreeBlocks();
}

int main() {
    int choice, option, pid, size;
    printf("Memory Allocation Simulation (4MB = 4000KB)\n");
    printf("Choose strategy:\n1. First Fit\n2. Best Fit\n3. Worst Fit\nEnter choice: ");
    scanf("%d", &choice);

    initMemory();

    while (1) {
        printf("\n1. Request Memory\n2. Release Memory\n3. Show Memory Map\n4. Exit\nEnter option: ");
        scanf("%d", &option);

        if (option == 1) {
            printf("Enter Process ID: ");
            scanf("%d", &pid);
            printf("Enter size (KB): ");
            scanf("%d", &size);

            int success = 0;
            if (choice == 1) success = allocateFirstFit(pid, size);
            else if (choice == 2) success = allocateBestFit(pid, size);
            else if (choice == 3) success = allocateWorstFit(pid, size);

            if (success)
                printf("Allocated P%d (%d KB)\n", pid, size);
            else
                printf("Allocation failed for P%d (%d KB)\n", pid, size);
        }
        else if (option == 2) {
            printf("Enter Process ID to release: ");
            scanf("%d", &pid);
            freeProcess(pid);
            printf("Released P%d\n", pid);
        }
        else if (option == 3) {
            displayMemory();
        }
        else if (option == 4) {
            break;
        }
        else {
            printf("Invalid option!\n");
        }
    }
    return 0;
}

