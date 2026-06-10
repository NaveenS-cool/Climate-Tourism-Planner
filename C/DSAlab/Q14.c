#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 100

typedef struct {
    int token;
    char name[50];
    int category;
} Customer;

typedef struct {
    Customer arr[MAX];
    int front, rear;
} Queue;

void initQueue(Queue* q) {
    q->front = q->rear = -1;
}

int isEmpty(Queue* q) {
    return q->front == -1;
}

int isFull(Queue* q) {
    return (q->rear + 1) % MAX == q->front;
}

void enqueue(Queue* q, Customer c) {
    if (isFull(q)) {
        printf("Queue full! Cannot add customer.\n");
        return;
    }
    if (isEmpty(q)) {
        q->front = q->rear = 0;
    } else {
        q->rear = (q->rear + 1) % MAX;
    }
    q->arr[q->rear] = c;
}

Customer dequeue(Queue* q) {
    Customer c = q->arr[q->front];
    if (q->front == q->rear) {
        q->front = q->rear = -1;
    } else {
        q->front = (q->front + 1) % MAX;
    }
    return c;
}

int main() {
    int N, choice;
    int tokenCounter = 1;
    Queue disabledQ, seniorQ, defenceQ, normalQ;
    initQueue(&disabledQ);
    initQueue(&seniorQ);
    initQueue(&defenceQ);
    initQueue(&normalQ);

    printf("Enter number of customers: ");
    scanf("%d", &N);

    for (int i = 0; i < N; i++) {
        Customer c;
        c.token = tokenCounter++;

        printf("\nEnter name of customer %d: ", i+1);
        scanf("%s", c.name);

        printf("Enter category (1 = Differently abled, 2 = Senior citizen, 3 = Defence, 4 = Normal): ");
        scanf("%d", &c.category);
        switch (c.category) {
            case 1: enqueue(&disabledQ, c); break;
            case 2: enqueue(&seniorQ, c); break;
            case 3: enqueue(&defenceQ, c); break;
            case 4: enqueue(&normalQ, c); break;
            default: printf("Invalid category! Skipping customer.\n");
        }
    }

    printf("\nServing customers in priority order\n");

    while (!isEmpty(&disabledQ) || !isEmpty(&seniorQ) || !isEmpty(&defenceQ) || !isEmpty(&normalQ)) {
        Customer c;

        if (!isEmpty(&disabledQ)) c = dequeue(&disabledQ);
        else if (!isEmpty(&seniorQ)) c = dequeue(&seniorQ);
        else if (!isEmpty(&defenceQ)) c = dequeue(&defenceQ);
        else c = dequeue(&normalQ);

        printf("Token %d - %s (Category %d) is being served.\n", c.token, c.name, c.category);
    }

    return 0;

}
