#include<stdio.h>
#include<stdlib.h>
#include<string.h>
typedef struct {
    char name[26];
    char RegNo[10];
    float cgpa;

}student;
void swap(student* a,student* b){
    student temp = *a;
    *a=*b;
    *b=temp;

}
void bubblesort(student* arr,int n){
    for(int i=0;i<n-1;i++){
        for(int j=0;j<n-i-1;j++){
            if(strcmp(arr[j].name,arr[j+1].name)>0)
            swap(&arr[j],&arr[j+1]);


    }
}
}
int binarysearch(student* arr,int n,char* target){
    int low=0;
    int high=n-1;
    while(low<=high){
        int mid= (low+high)/2;
        int cmp= strcmp(arr[mid].name,target);
        if (cmp==0)
        return mid;
        else if (cmp<0)
        low=mid+1;
        else
        high=mid-1;

    }
    return -1;
}
int main(){
    FILE* fp = fopen("student.txt","r");
    student students[10];
    int count=0;
    while(fscanf(fp,"%25s %10s %f",students[count].name,students[count].RegNo,&students[count].cgpa) == 3){
        count++;
    }


fclose(fp);
bubblesort(students,count);
char name[26];
printf("Enter name:");
scanf("%s",name);
int f=binarysearch(students,count,name);
if (f!=1){
    printf("found");
}
return 0;
}