#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
#define M 100

int top=-1;
char stack[M];

void push(char c)
{
	stack[++top]=c;

}
char pop()
{
	if (top == -1)
		return -1;
	return stack[top--];

}
char peek()
{
	return (top == -1)?-1:stack[top];	
}
int precedence(char c)
{
	switch (c)
    {
	case '^':return 3;
	case '/':
	case '*':return 2;
	case '+':
	case '-': return 1;
	default: return -1;
    }

}
int isoperator(char c)
{
	return (c == '^'||c == '-'|| c == '+'|| c == '*'|| c == '/');
}

void infixtopostfix(char* infix,char* postfix)
{
	int i=0;
	int k=0;
	char c;
	while(infix[i] != '\0')
	{
		c = infix[i];
		if (isdigit(c))
			postfix[k++]=c;
		else if (c == '(')
			push(c);
		else if (c == ')')
		{
			while(peek() != ')')
				{postfix[k++] = pop();}
			pop();

		}
        else if(isoperator(c)){
        while(precedence(peek())>=precedence(c))
        {postfix[k++] = pop();}
        push(c);
        }
		i++;
	
	}
	
	while( top != -1)
		postfix[k++] = pop();

postfix[k] = '\0';
}

int intstack[M];
int inttop = -1;
void intpush(int c)
{
  intstack[++inttop]=c;
}
int intpop()
{
	return intstack[inttop--];
}
int evaluate(char* postfix)
{
	int i=0,op1,op2,res;
	while( postfix[i] != '\0' )
	{
		if(isdigit(postfix[i]))
			{intpush(postfix[i] - '0');}
		else
		{ 	
			op1 =intpop();
			op2 = intpop();
			switch(postfix[i])
			{
				case '*': res =op1*op2;break;
				case '+': res=op1+op2;break;
				case '-': res=op1-op2;break;
				case '/': res=op1/op2;break;
				case '^': res = pow(op1,op2);break;





			}
			intpush(res);
			
		
		}
		i++;
    }
    return intpop();

	

}







int main()
{
	char infix[M],postfix[M];
	fgets(infix,M,stdin);
	infix[strcspn(infix,"\n")] = '\0';
	infixtopostfix(infix,postfix);
	printf("Postfix:%s",postfix);
    int res=evaluate(postfix);
    printf("%d",res);
	
	return 0;
}



