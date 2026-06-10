#include<stdio.h>
#include<stdlib.h>
void main(){
    FILE* fp=fopen("number.txt","r");
    if (fp==NULL){
        printf("Error");
        return;
    }
    int i,j;
    int count=0;
    int max=0;
    //while(i=fgetc(fp)!=feof(fp)){
         while((j=fgetc(fp)) != EOF){
            putchar(j);
            

         }



    //}
  

    
    
    fclose(fp);



}
