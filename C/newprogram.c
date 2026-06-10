#include<stdio.h>
int main(){

    int n;
    printf("Enter number;");
    scanf("%d",&n);
    int i=0;
    int f=0,s=1,t;
    printf("%d\n",f);
 printf("%d\n",s);
    while(i<n){
       t=s+f;
        printf("%d\n",t);
        f=s;
        s=t;
        i++;


   }
    return 0;
}