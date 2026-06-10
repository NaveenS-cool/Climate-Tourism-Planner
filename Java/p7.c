#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char url[100];
    struct Node *prev;
    struct Node *next;
} Node;

Node *current = NULL;

Node* createNode(char *url) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    strcpy(newNode->url, url);
    newNode->prev = NULL;
    newNode->next = NULL;
    return newNode;
}

void visitPage(char *url) {
    Node* newNode = createNode(url);

    if (current != NULL) {
        Node* temp = current->next;
        while (temp != NULL) {
            Node* del = temp;
            temp = temp->next;
            free(del);
        }
        current->next = newNode;
        newNode->prev = current;
    }
    current = newNode;
    printf("Visited: %s\n", current->url);
}

void goBack() {
    if (current == NULL || current->prev == NULL) {
        printf("No previous page to go back.\n");
        return;
    }
    current = current->prev;
    printf("Back to: %s\n", current->url);
}

void goForward() {
    if (current == NULL || current->next == NULL) {
        printf("No forward page available.\n");
        return;
    }
    current = current->next;
    printf("Forward to: %s\n", current->url);
}

void showCurrentPage() {
    if (current == NULL) {
        printf("No page currently open.\n");
    } else {
        printf("Current page: %s\n", current->url);
    }
}

int main() {
    int choice;
    char url[100];

    do {
        printf("\n=== Browser Navigation Menu ===\n");
        printf("1. Visit new page\n");
        printf("2. Go Back\n");
        printf("3. Go Forward\n");
        printf("4. Show Current Page\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        getchar();

        switch (choice) {
            case 1:
                printf("Enter URL: ");
                fgets(url, sizeof(url), stdin);
                url[strcspn(url, "\n")] = '\0';
                visitPage(url);
                break;
            case 2:
                goBack();
                break;
            case 3:
                goForward();
                break;
            case 4:
                showCurrentPage();
                break;
            case 5:
                printf("Exiting browser...\n");
                break;
            default:
                printf("Invalid choice! Try again.\n");
        }
    } while (choice != 5);

    return 0;
}