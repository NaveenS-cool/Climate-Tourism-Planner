#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    char word[50];
    char meaning[200];
    struct TreeNode *left, *right;
} TreeNode;

TreeNode* createNode(char* word, char* meaning) {
    TreeNode* newNode = (TreeNode*)malloc(sizeof(TreeNode));
    strcpy(newNode->word, word);
    strcpy(newNode->meaning, meaning);
    newNode->left = newNode->right = NULL;
    return newNode;
}

TreeNode* insert(TreeNode* root, char* word, char* meaning) {
    if (root == NULL) return createNode(word, meaning);

    int cmp = strcmp(word, root->word);
    if (cmp < 0) root->left = insert(root->left, word, meaning);
    else if (cmp > 0) root->right = insert(root->right, word, meaning);
    else {
        printf("Word already exists. Updating meaning...\n");
        strcpy(root->meaning, meaning);
    }
    return root;
}

TreeNode* search(TreeNode* root, char* word) {
    if (root == NULL) return NULL;

    int cmp = strcmp(word, root->word);
    if (cmp == 0) return root;
    else if (cmp < 0) return search(root->left, word);
    else return search(root->right, word);
}

TreeNode* findMin(TreeNode* root) {
    while (root->left != NULL) root = root->left;
    return root;
}

TreeNode* deleteNode(TreeNode* root, char* word) {
    if (root == NULL) return NULL;

    int cmp = strcmp(word, root->word);

    if (cmp < 0) root->left = deleteNode(root->left, word);
    else if (cmp > 0) root->right = deleteNode(root->right, word);
    else {
        if (root->left == NULL && root->right == NULL) {
            free(root);
            return NULL;
        }
        else if (root->left == NULL) {
            TreeNode* temp = root->right;
            free(root);
            return temp;
        }
        else if (root->right == NULL) {
            TreeNode* temp = root->left;
            free(root);
            return temp;
        }
        else {
            TreeNode* temp = findMin(root->right);
            strcpy(root->word, temp->word);
            strcpy(root->meaning, temp->meaning);
            root->right = deleteNode(root->right, temp->word);
        }
    }

    return root;
}

void inorder(TreeNode* root) {
    if (root == NULL) return;
    inorder(root->left);
    printf("%s : %s\n", root->word, root->meaning);
    inorder(root->right);
}

int main() {
    TreeNode* root = NULL;
    int choice;
    char word[50], meaning[200];

    while (1) {
        printf("\nDictionary Menu\n");
        printf("1. Insert <word, meaning>\n");
        printf("2. Find meaning of a word\n");
        printf("3. Remove a word\n");
        printf("4. Display dictionary (inorder)\n");
        printf("5. Exit\n");
        printf("Enter choice: ");
        scanf("%d", &choice);
        getchar();

        switch (choice) {
            case 1:
                printf("Enter word: ");
                scanf("%s", word);
                getchar();
                printf("Enter meaning: ");
                fgets(meaning, sizeof(meaning), stdin);

               meaning[strcspn(meaning, "\n")] = 0;
                root = insert(root, word, meaning);
                break;
            case 2:
                printf("Enter word to search: ");
                scanf("%s", word);
                {
                    TreeNode* result = search(root, word);
                    if (result) printf("Meaning of %s: %s\n", result->word, result->meaning);
                    else printf("Word not found in dictionary.\n");
                }
                break;
            case 3:
                printf("Enter word to remove: ");
                scanf("%s", word);
                root = deleteNode(root, word);
                break;
            case 4:
                printf("\nDictionary Contents\n");
                inorder(root);
                break;
            case 5:
                exit(0);
            default:
                printf("Invalid choice.\n");

        }
    }
    return 0;
}
