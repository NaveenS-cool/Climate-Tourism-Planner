#include <stdio.h>
#include <stdlib.h>
struct Node
{
	int val;
	struct Node* next;	

	
};

	struct Node* head=NULL;	


struct Node* create()
{
	struct Node* head = NULL;

	struct Node* tr;
		int x;
        printf("Enter value:");
	while(1)
	{
	
	scanf("%d",&x);
	if(x ==-1)break;
		struct Node* newnode = (struct Node*)malloc(sizeof(struct Node));
	newnode->val=x;
	newnode->next=NULL;
	if (head == NULL){
		head = newnode;
		tr=newnode;

	}
	else{
	tr->next=newnode;
	tr=newnode;
	
	}



		

    }
    return head;
}
/*void removenegative(struct Node* head )
    {
    struct Node* tr = head;
	struct Node* p;
	if (tr->val <0) 
	{
		p = tr;
		head = tr->next;
		tr = tr->next;
		free(p);
		

	}
    
	while (tr->next->val <0) 
	{
		p=tr->next;
		tr->next=tr->next->next;
		free(p);
		
	}
    

    }*/

struct Node*  removenode()
{
		struct Node* tr = head;
		struct Node* p=NULL;
		while (tr->val<0){
			p = tr;
		head = tr->next;
		tr = tr->next;
		free(p);}
		while(tr->next->val<0){
			p=tr->next;
			tr=tr->next->next;
			free(p);



		}


		return head;
}



void display( struct Node* head ){
	struct Node* tr=head;
	while(tr != NULL)
	{
		printf("%d\n",tr->val);
		tr=tr->next;

		


	}	




}


int main()
{
	
	head = create();
   // removenegative(head);
    head=removenode();
	display(head);



	return 0;
}