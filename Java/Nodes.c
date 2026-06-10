#include <stdio.h>
#include <stdlib.h>
struct Node{
    int val;
    struct Node* next; 
};
void Insert(struct Node** head,int x)
{
    struct Node *p=(struct Node*)malloc(sizeof(struct Node));
   // scanf("%d",p->val);
   p->val=x;
    p->next=*head;
    *head=p;

}
void insert(struct Node** head,int x)
{
     struct Node *p=(struct Node*)malloc(sizeof(struct Node));
   // scanf("%d",p->val);
   p->val=x;
   struct Node *n=*head;
   
   while(n->next!=NULL)
   {
    n=n->next;

   }
   n->next=p;
}


void traverse(struct Node* head){
    struct Node* p=head;
    while(p!= NULL)
    {
        printf("%d\n",p->val);
        p=p->next;

    }
}

int main()
{
   struct Node* head = (struct Node*)malloc(sizeof(struct Node));
   head->val=5; 
   head->next=NULL;
   Insert(&head,4);
   /*Insert(head,3);
   Insert(head,2); 
   Insert(head,1);*/
   insert(&head,6);
   traverse(head); 

   //printf("%d",head->val);
   free(head);
   return 0;
}
