#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char appName[30];
    int frequency;
    struct Node *next;
} Node;

Node *rear = NULL;  // Rear pointer for circular queue

// Function to create a new node
Node* createNode(char *appName) {
    Node newNode = (Node)malloc(sizeof(Node));
    strcpy(newNode->appName, appName);
    newNode->frequency = 1;
    newNode->next = NULL;
    return newNode;
}

// Enqueue a new app
void enqueue(char *appName) {
    Node *newNode = createNode(appName);
    if (rear == NULL) {
        rear = newNode;
        rear->next = rear;  // Circular link
    } else {
        newNode->next = rear->next;
        rear->next = newNode;
        rear = newNode;
    }
    printf("%s added to App List.\n", appName);
}

// Search and increment frequency if app exists
int accessApp(char *appName) {
    if (rear == NULL) return 0;
    Node *temp = rear->next;
    do {
        if (strcmp(temp->appName, appName) == 0) {
            temp->frequency++;
            printf("%s opened, frequency = %d\n", appName, temp->frequency);
            return 1;
        }
        temp = temp->next;
    } while (temp != rear->next);
    return 0;
}

// Remove least frequently used app
void dequeueLFU() {
    if (rear == NULL) {
        printf("App list is empty!\n");
        return;
    }

    Node *temp = rear->next, *prev = rear, *lfuPrev = rear, *lfuNode = rear->next;
    do {
        if (temp->frequency < lfuNode->frequency) {
            lfuNode = temp;
            lfuPrev = prev;
        }
        prev = temp;
        temp = temp->next;
    } while (temp != rear->next);

    if (lfuNode == rear) rear = lfuPrev;  // Update rear if needed
    if (lfuNode == rear->next) rear->next = lfuNode->next;  // Update front if needed
    else lfuPrev->next = lfuNode->next;

    printf("Removing least used app: %s (freq=%d)\n", lfuNode->appName, lfuNode->frequency);
    free(lfuNode);

    if (rear == NULL || rear->next == rear) rear = NULL;  // If queue empty
}

// Display apps and frequencies
void display() {
    if (rear == NULL) {
        printf("App list is empty!\n");
        return;
    }
    Node *temp = rear->next;
    printf("App List (Name : Frequency):\n");
    do {
        printf("%s : %d\n", temp->appName, temp->frequency);
        temp = temp->next;
    } while (temp != rear->next);
}

int main() {
    // Example usage
    enqueue("WhatsApp");
    enqueue("Instagram");
    enqueue("YouTube");

    accessApp("WhatsApp");
    accessApp("Instagram");
    accessApp("WhatsApp");

    display();

    dequeueLFU();  // Remove least used app
    display();

    return 0;
}