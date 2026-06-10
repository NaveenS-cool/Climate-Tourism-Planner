#include <stdio.h>
#include <stdlib.h>
struct Node{
    char val;
   struct Node* left;struct Node* right;
};

struct Node* create()
{
        char v;
       // printf("Enter value:");
       scanf("%c",&v);
        if (v == 'x') return NULL;
        struct Node* root=  (struct Node*)malloc(sizeof(struct Node));
        root->val = v;
        root->left = create();
        root->right = create();



}





int main()
{
    struct Node* root=NULL;
    root = create();
    return 0;
}