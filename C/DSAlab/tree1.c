#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define the structure for a tree node
struct Node {
    char name[50];
    struct Node *left;
    struct Node *right;
};

// Function to create a new node
struct Node* createNode(char name[]) {
    struct Node* newNode = (struct Node*) malloc(sizeof(struct Node));
    strcpy(newNode->name, name);
    newNode->left = newNode->right = NULL;
    return newNode;
}

// Function to insert a node in the binary tree (alphabetically)
struct Node* insert(struct Node* root, char name[]) {
    if (root == NULL)
        return createNode(name);

    if (strcmp(name, root->name) < 0)
        root->left = insert(root->left, name);
    else if (strcmp(name, root->name) > 0)
        root->right = insert(root->right, name);
    else
        printf("Duplicate name '%s' not inserted.\n", name);

    return root;
}

// Inorder traversal (alphabetical order)
void inorder(struct Node* root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%s\n", root->name);
        inorder(root->right);
    }
}

// Free memory
void freeTree(struct Node* root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root);
    }
}

int main() {
    struct Node* root = NULL;
    int n;
    char name[50];

    printf("Enter number of names to insert: ");
    scanf("%d", &n);
    getchar();  // consume newline

    for (int i = 0; i < n; i++) {
        printf("Enter name %d: ", i + 1);
        fgets(name, sizeof(name), stdin);
        name[strcspn(name, "\n")] = '\0';  // remove newline
        root = insert(root, name);
    }

    printf("\nInorder traversal of binary tree (alphabetical order):\n");
    inorder(root);

    freeTree(root);
    return 0;
}
