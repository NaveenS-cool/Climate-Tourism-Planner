#include <stdio.h>
int Q[4];
int Rear = -1;
int Front = -1;


void Enqueue(int x)
{
    if((Rear+1)%4 == Front)
    {
        printf("Overflow");
    }
    else
    {
        if (Rear == -1)
        {
            Front=0;
            Rear=Front;
            Q[Front] = x;
        }
        else
        {
            Rear=(Rear+1)%4;
            Q[Rear] = x;
        }
    }
}


int Dequeue()
{
    if (Front == -1)
    {
        printf("underflow");
    }
    else
    {
        int x = Q[Front];
        if (Front == Rear)
        {
            Front = -1;
            Rear = -1;
        }
        else
        {
            
            Front = (Front+1)%4;
            

        }
        return x;
    }
}
int main()
{
    Enqueue(12);
       Enqueue(23);
          Enqueue(65);
             Enqueue(145);
    for(int i=0;i<4;i++ ){
    printf("%d",Dequeue());
        if (i<3)
        printf(",");
    }
    Dequeue();

    return 0;
}