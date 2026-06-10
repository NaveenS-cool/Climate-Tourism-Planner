#include<stdio.h>
typedef struct{
    int coeff;
    int exp;

}P;
int main(){
    P m[7];
    P k[7];
    P c[7];
    printf("Enter:");
    for(int i=0;i<7;i++){
        scanf("%d %d",m[i].coeff,m[i].exp);
    }
    printf("k");


    printf("ok:");
    for(int i=0;i<7;i++){
        scanf("%d %d",k[i].coeff,k[i].exp);
    }
    
    for(int i=0;i<7;i++){
        c[i].coeff=m[i].coeff+k[i].coeff;
        c[i].coeff%=3;
    }
    
     printf("Output:");
     for(int i;i<7;i++){
        printf("%d %d,",c[i].coeff,c[i].exp);

     }



    return 0;
}