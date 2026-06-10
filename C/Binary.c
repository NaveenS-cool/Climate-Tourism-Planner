#include <stdio.h>
//char A[4];
//A[3]='\0';

void Binary(int n,char* A)
{
    if(n<1)
    {
        
        printf("%s\n",A);
    }
    else
    {
        A[n-1]=1;
        Binary(n-1,A);
        A[n-1]=0;
        Binary(n-1,A);

  
        }    
    }

void main()
{
    char B[5];
    B[4]='\0';
    Binary(3,B);
}