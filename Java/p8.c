#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char word[50];
    struct Node *next;
} Node;

Node* addWord(Node *head, char *word) {
    Node newNode = (Node)malloc(sizeof(Node));
    strcpy(newNode->word, word);
    newNode->next = NULL;

    if (head == NULL)
        return newNode;

    Node *temp = head;
    while (temp->next != NULL)
        temp = temp->next;
   
    temp->next = newNode;
    return head;
}

void printDocument(Node *head) {
    Node *temp = head;
    while (temp != NULL) {
        printf("%s ", temp->word);
        temp = temp->next;
    }
    printf("\n");
}

int findAndReplace(Node *head, char *term, char *replacement) {
    int count = 0;
    Node *temp = head;
    while (temp != NULL) {
        if (strcmp(temp->word, term) == 0) {
            strcpy(temp->word, replacement);
            count++;
        }
        temp = temp->next;
    }
    return count;
}

int main() {
    Node *document = NULL;
    int n, i;
    char word[50], term[50], replacement[50];

    printf("Enter number of words in document: ");
    scanf("%d", &n);

    printf("Enter words:\n");
    for(i = 0; i < n; i++) {
        scanf("%s", word);
        document = addWord(document, word);
    }

    printf("Enter the word to find: ");
    scanf("%s", term);

    printf("Enter the replacement word: ");
    scanf("%s", replacement);

    int replacements = findAndReplace(document, term, replacement);

    printf("Number of replacements made: %d\n", replacements);
    printf("Updated document: ");
    printDocument(document);

    return 0;
}