#include <stdio.h>
#include <stdlib.h>
struct Node {
    int val;
    struct Node* next;
};
struct Node* head = NULL;
struct Node *top=NULL;

void push(int x)
{
   // struct Node* tr = NULL;
  //  printf("Enter valur:");//int x;
   
       // scanf("%d",&x);
        struct Node* new = (struct Node*)malloc(sizeof(struct Node));
        new->val=x;
        new->next=NULL;
        if (head==NULL)
        {
            head=new;
            top=new;
        }
        else{
            top->next=new;
            top=new;

        }

    }
void pop()
{
    struct Node* prev;
    prev = head; struct Node*p;
    while(prev->next->next != NULL){
        prev=prev->next;
    }
    prev->next=NULL;
   // printf("%d",prev->val);
    p=top;
   top = prev;
   free(p);


   
}



void display( ){
	struct Node* tr=head;
	while(tr != NULL)
	{
		printf("%d\n",tr->val);
		tr=tr->next;

		


	}	




}




int main()
{
    push(5);
     push(4); push(3); push(2);
     pop();
   display();
    
    return 0;
}