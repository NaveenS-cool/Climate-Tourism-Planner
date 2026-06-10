#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_QUEUE 100

typedef struct {
    int tokenNumber;
    int remainingForms;
} Customer;

typedef struct {
    Customer data[MAX_QUEUE];
    int front;
    int rear;
    int count;
} Queue;

void initializeQueue(Queue *q);
void enqueue(Queue *q, Customer c);
Customer dequeue(Queue *q);
int isEmpty(Queue *q);
void displayMenu();
void addCustomer(Queue *q, int *tokenCounter);
void serveCustomer(Queue *q);
void displayCurrentCustomer(Queue *q);
void displayQueueStatus(Queue *q);
void listAllCustomers(Queue *q);

int main() {
    Queue queue;
    initializeQueue(&queue);
    int tokenCounter = 1;
    int choice;

    while (1) {
        displayMenu();
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                addCustomer(&queue, &tokenCounter);
                break;
            case 2:
                serveCustomer(&queue);
                break;
            case 3:
                displayCurrentCustomer(&queue);
                break;
            case 4:
                displayQueueStatus(&queue);
                break;
            case 5:
                listAllCustomers(&queue);
                break;
            case 6:
                printf("Exiting...\n");
                exit(0);
            default:
                printf("Invalid choice. Try again.\n");
        }
    }
    return 0;
}

void initializeQueue(Queue *q) {
    q->front = 0;
    q->rear = -1;
    q->count = 0;
}

int isEmpty(Queue *q) {
    return q->count == 0;
}

void enqueue(Queue *q, Customer c) {
    if (q->count == MAX_QUEUE) {
        printf("Queue is full.\n");
        return;
    }
    q->rear = (q->rear + 1) % MAX_QUEUE;
    q->data[q->rear] = c;
    q->count++;
}

Customer dequeue(Queue *q) {
    Customer c = {0, 0};
    if (isEmpty(q)) {
        printf("Queue is empty.\n");
        return c;
    }
    c = q->data[q->front];
    q->front = (q->front + 1) % MAX_QUEUE;
    q->count--;
    return c;
}

void displayMenu() {
    printf("1. Add customer \n");
    printf("2. Serve next customer (Book 1 ticket)\n");
    printf("3. Display current customer being served\n");
    printf("4. Show waiting count\n");
    printf("5. Show full queue\n");
    printf("6. Exit\n");
}

void addCustomer(Queue *q, int *tokenCounter) {
    int forms;
    printf("Enter number of tickets/forms to be booked: ");
    scanf("%d", &forms);

    if (forms <= 0) {
        printf("Invalid number of forms.\n");
        return;
    }

    Customer c;
    c.tokenNumber = (*tokenCounter)++;
    c.remainingForms = forms;
    enqueue(q, c);

    printf("Customer added with Token #%d (Forms: %d)\n", c.tokenNumber, c.remainingForms);
}

void serveCustomer(Queue *q) {
    if (isEmpty(q)) {
        printf("No customers in queue.\n");
        return;
    }

    Customer c = dequeue(q);
    printf("Serving Token #%d (1 form booked)\n", c.tokenNumber);
    c.remainingForms--;

    if (c.remainingForms > 0) {
        printf("Customer Token #%d has %d forms left. Moving to back of queue.\n", c.tokenNumber, c.remainingForms);
        enqueue(q, c);
    } else {
        printf("All forms for Token #%d are completed.\n", c.tokenNumber);
    }
}


void displayCurrentCustomer(Queue *q) {
    if (isEmpty(q)) {
        printf("No customers in queue.\n");
        return;
    }
    Customer c = q->data[q->front];
    printf("Currently serving Token #%d (Remaining forms: %d)\n", c.tokenNumber, c.remainingForms);
}

void displayQueueStatus(Queue *q) {
    printf("Total customers waiting in queue: %d\n", q->count);
}

void listAllCustomers(Queue *q) {
    if (isEmpty(q)) {
        printf("Queue is empty.\n");
        return;
    }

    printf("Customers in queue:\n");
    int i;
    for (i = 0; i < q->count; i++) {
        int idx = (q->front + i) % MAX_QUEUE;
        printf("Token #%d - Remaining Forms: %d\n", q->data[idx].tokenNumber, q->data[idx].remainingForms);
    }
}