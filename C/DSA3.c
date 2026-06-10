#include<stdio.h>
#define M 100
typedef struct
{
    int row;
    int col;
    int value;
}sparse;
void sparsetomatrix(sparse layer[],int n,int mat[M][M])
{
    for(int i=0;i<n;i++)
    mat[layer[i].row][layer[i].col]=layer[i].value;


}
void addMatrices(int mat1[M][M],int mat2[M][M],int res[M][M],int r,int c)
{
     for(int i=0;i<r;i++)
         for(int j=0;j<c;j++)
            res[i][j]=mat1[i][j]+mat2[i][j];
}
void transpose(int mat[M][M],int trans[M][M],int r,int c)
{
        for(int i=0;i<r;i++)
         for(int j=0;j<c;j++)
            trans[j][i]=mat[i][j];


}
void display(int mat[M][M],int c,int r)
{
    for(int i=0;i<r;i++)
    {
         for(int j=0;j<c;j++)
         {
            printf("%d",mat[i][j]);
            if(j<c-1)
             printf(",");
         }
          printf("\n");
        }
}




int main()
{
    int r,c;
    printf("Enter rows and colums");
    scanf("%d%d",&r,&c);
    sparse layer1[M],layer2[M],layer3[M];
    int c1,c2,c3;
    printf("Enter count:");
    scanf("%d",&c1);
    for(int i=0;i<c1;i++)
    {
        printf("Enter(row,column,value)%d:",i+1);
        scanf("%d%d%d",&layer1[i].row,&layer1[i].col,&layer1[i].value);
    }


    printf("Enter count:");
    scanf("%d",&c2);
    for(int i=0;i<c2;i++)
    {
        printf("Enter(row,column,value):");
        scanf("%d%d%d",&layer2[i].row,&layer2[i].col,&layer2[i].value);
    }


    printf("Enter count:");
    scanf("%d",&c3);
    for(int i=0;i<c3;i++)
    {
        printf("Enter(row,column,value):");
        scanf("%d%d%d",&layer3[i].row,&layer3[i].col,&layer3[i].value);
    }
    int mat1[M][M]={0};
    int mat2[M][M]={0};
    int mat3[M][M]={0};
    int temp[M][M]={0};
    int comb[M][M]={0};
    int trans[M][M]={0};
    sparsetomatrix(layer1,c1,mat1);
    sparsetomatrix(layer2,c2,mat2);
    sparsetomatrix(layer3,c3,mat3);
    addMatrices(mat1,mat2,temp,r,c);
    addMatrices(temp,mat3,comb,r,c);
    transpose(comb,trans,r,c);
    display(trans,c,r);
    

    return 0;

}
