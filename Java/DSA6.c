#include <stdio.h>
#define M 100
typedef struct
{
	int row;
	int col;
	int value;

}sparse;


int Add(sparse C[],sparse A[],int n1,sparse B[],int n2)
{

	int i=0;int j=0; int k=0;
	while (i<n1 && j<n2)
	if (A[i].row >= B[j].row)
	{
		C[k++]=A[i++];

        }
	else if (B[j].row >= A[i].row)
	{
		C[k++]=B[j++];

        }
	else if (A[i].row == B[j].row)
	{
		C[k].row=A[i].row;
		C[k].value = A[i].value + B[i].value;
	i++;j++;k++;

        }

	while (i<n1)

	{
		C[k++]=A[i++];

        }
	while (j<n2)

	{
		C[k++]=B[j++];

        }
	return k;







}
void display(sparse A[],int n)
{

		for(int i=0;i<n;i++)
		{
			printf("%d,%d,%d\n",A[i].row,A[i].col,A[i].value);
		
		}

}

void transpose(sparse A[],int n,sparse B[])
{
	for(int i=0;i<n;i++)
	{
		
		B[i].row = A[i].col;
		B[i].col=A[i].row;
		B[i].value = A[i].value;
	}
		

}
void sort(sparse A[],int n)
{
	for(int i=0;i<n-1;i++)
	{
		for(int j=0;j<n-i-1;i++)
		{
			if (A[j].row < A[j+1].row)
			{
				int temp = A[j].row;
				A[j].row = A[j+1].row;
				A[j+1].row = temp;
			}
		}
	
	}


}






int main()
{
	int c1,c2,c3;
	sparse layer1[M],layer2[M],layer3[M];
	printf("Enter number of colums:");
	scanf("%d",&c1);
	

	for(int i=0;i<=c1;i++)
	{
		printf("Enter [row,col,value]:");
		scanf("%d%d%d",&layer1[i].row,&layer1[i].col,&layer1[i].value);

	}
 	printf("Enter number of rows:");
	scanf(  "%d",&c2);
	

	for(int i=0;i<=c2;i++)
	{
		printf("Enter [row,col,value]:");
		scanf("%d%d%d",&layer2[i].row,&layer2[i].col,&layer2[i].value);

	}

	printf("Enter number of rows:");
	scanf("%d",&c3);
	

	for(int i=0;i<=c3;i++)
	{
		printf("Enter [row,col,value]:");
		scanf("%d%d%d",&layer3[i].row,&layer3[i].col,&layer3[i].value);

	}
	sparse temp[M];
    sparse comb[M];

	int k = Add(temp,layer1,c1,layer2,c2);
	int n = Add(comb,temp,k,layer3,c3);
	sparse trans[M];
	transpose(comb,n,trans);
	sort(trans,n);
       display(trans,n);




																			

	return 0;
}