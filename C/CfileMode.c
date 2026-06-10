#include <stdio.h>

int main() {
    FILE* fp = fopen("number.txt", "r");
    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }

   
   int i,j;
   int count=0;
   int mode=0;
   int max;
   while((fscanf(fp,"%d",&i)) != EOF){
     while((fscanf(fp,"%d",&j)) != EOF){
        printf("%d %d,",i,j);
        if (i==j){
            count++;
        }


     }
     if (count>mode){
           mode = count;
           max=i;
     }

     }

   
   

    fclose(fp);
    return 0;
}
