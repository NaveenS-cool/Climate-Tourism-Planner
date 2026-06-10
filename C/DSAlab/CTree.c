#include <stdio.h>
#include <stdlib.h>

struct Node {
    char val;
    struct Node* left;
    struct Node* right;
};

struct Node* create() {
    char v;
    scanf(" %c", &v);   // space before %c skips whitespace

    if (v == 'x') return NULL;

    struct Node* root = (struct Node*)malloc(sizeof(struct Node));
    root->val = v;
    root->left = create();
    root->right = create();

    return root;
}

void preorder(struct Node* root) {
    if (root == NULL) return;
    printf("%c ", root->val);
    preorder(root->left);
    preorder(root->right);
}

int main() {
    struct Node* root = NULL;
    printf("Enter tree in preorder (x for NULL):\n");
    root = create();

    printf("Preorder traversal:\n");
    preorder(root);
    printf("\n");

    return 0;
}
