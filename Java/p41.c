#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

#define MAX 100

char stack[MAX];
int top=-1;

void push(char c){
    if(top == MAX-1)
        printf("Stack Overflow\n");
    else
        stack[++top]=c;
}

char pop(){
    if(top == -1) return -1;
    else return stack[top--];
}

char peek(){
    if(top == -1) return -1;
    else return stack[top];
}

int precedence(char op){
    switch(op){
        case '^': return 3;
        case '*': case '/': return 2;
        case '+': case '-': return 1;
        default: return -1;
    }
}

int isRightAssociative(char op){
    return op=='^';
}

int isOperator(char ch){
    return ch=='+'||ch=='-'||ch=='*'||ch=='/'||ch=='^';
}

int infixToPostfix(char infix[],char postfix[]){
    int i=0,j=0;
    char ch;
    while((ch=infix[i++])!='\0'){
        if(isdigit(ch)){
            postfix[j++]=ch;
        }
        else if(ch=='('){
            push(ch);
        }
        else if(ch==')'){
            while(peek()!='(')
                postfix[j++]=pop();
            pop();
        }
        else if(isOperator(ch)){
            while(isOperator(peek() && (precedence(ch)<=precedence(peek())) && !isRightAssociative(ch)){
                postfix[j++]=pop();
            }
            push(ch);
        }
    }
    while(top!=-1)
        postfix[j++]=pop();
    postfix[j]='\0';
}

int valStack[MAX];
int valTop=-1;

void valPush(int num){
    valStack[++valTop]=num;
}

int valPop(){
    if(valTop == -1){
        printf("Value Stack Underflow\n");
        return -1;
    }
    return valStack[valTop--];
}

int evaluatePostfix(char postfix[]){
    int i=0;
    char ch;
    while((ch=postfix[i++])!='\0'){
        if(isdigit(ch)){
            valPush(ch-'0');
        }
        else if(isOperator(ch)){
            int b=valPop();
            int a=valPop();
            switch (ch) {
                case '+': valPush(a + b); break;
                case '-': valPush(a - b); break;
                case '*': valPush(a * b); break;
                case '/': valPush(a / b); break;
                case '%': valPush(a % b); break;
                case '^': valPush(pow(a, b)); break;
            }
        }
    }
    return valPop();
}

void main() {
    int choice;
    char infix[MAX], postfix[MAX];
    printf("\n--- MENU ---\n");
    printf("1. Convert Infix to Postfix\n");
    printf("2. Evaluate Postfix Expression\n");
    printf("3. Exit\n");
    while(1){
        printf("Enter choice: ");
        scanf("%d",&choice);
        getchar();
        switch (choice) {
            case 1:
                top = -1;
                printf("Enter infix expression (digits and operators only): ");
                fgets(infix, MAX, stdin);
                infix[strcspn(infix, "\n")] = 0;
                infixToPostfix(infix, postfix);
                printf("Postfix Expression: %s\n", postfix);
                break;
            case 2:
                valTop = -1;
                printf("Enter postfix expression (digits and operators only): ");
                fgets(postfix, MAX, stdin);
                postfix[strcspn(postfix, "\n")] = 0;
                int result = evaluatePostfix(postfix);
                printf("Result: %d\n", result);
                break;
            case 3:
                exit(0);
            default:
                printf("Invalid choice.\n");
        }
    }
}
