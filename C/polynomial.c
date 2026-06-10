#include <stdio.h>
typedef struct 
{
	int coeff;
	int exp;
}Term;

int add(Term r[],Term p1[],int n1,Term p2[],int n2)
{
	int i=0;int j=0;int k=0;
	while(i<n1 && j<n2)
	{
		if(p1[i].exp > p2[j].exp)
		{ 
			r[k++]=p1[i++];
		}	
		else if(p1[i].exp < p2[j].exp)
		{
			r[k++]=p2[j++];
		}
		else
		{
			r[k].exp=p1[i].exp;
			r[k].coeff=(p1[i].coeff+p2[j].coeff)%3;
			i++;j++;k++;
			
		}

	}
	while(i<n1)
	{
		r[k++]=p1[i++];
	}
	while(j<n2)
	{
		r[k++]=p2[j++];
	}	
	

	return k;
}

void display(Term p[],int n)
{
	for(int i=0;i<n;i++)
	{

		printf("%dx^%d",p[i].coeff,p[i].exp);
		if(i<n-1)
			printf("+");
		
	}
	printf("\n");	


}

/*int input(Term p[])
{
	int n=0;
	char s='n';
	while(s!='y')
	{
		printf("Enter c:");
		scanf("%d",p[n].coeff);
		printf("\nEnter e:");
		scanf("%d",p[n].exp);
 		n++;
		//printf("\nEnter y:");
		//scanf("%c",&s);

		
	}
		return n;
		


}*/
void input(Term p[],int n)
{
	for(int i=0;i<n;i++)
	{
		printf("Enter coefficient:");
		scanf("%d",&p[i].coeff);
		printf("Enter exponent:");
		scanf("%d",&p[i].exp);
	}


}
int main()
{
	Term p1[3];Term p2[3];Term r[6];
	input(p1,3);
	display(p1,3);
	input(p2,3);
	display(p2,3);
	int a=add(r,p1,3,p2,3);
	display(r,a);
	return 0;
	

}

