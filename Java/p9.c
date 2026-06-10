#include <stdio.h>
#include <stdlib.h>

typedef struct Term {
    int coeff;
    int exp;
    struct Term *next;
} Term;

Term* createTerm(int coeff, int exp) {
    Term* newTerm = (Term*)malloc(sizeof(Term));
    newTerm->coeff = coeff;
    newTerm->exp = exp;
    newTerm->next = NULL;
    return newTerm;
}

Term* insertTerm(Term* head, int coeff, int exp) {
    if(coeff == 0) return head;

    Term *newTerm = createTerm(coeff, exp);

    if(head == NULL || exp > head->exp) {
        newTerm->next = head;
        return newTerm;
    }

    Term *temp = head;
    Term *prev = NULL;
    while(temp != NULL && temp->exp > exp) {
        prev = temp;
        temp = temp->next;
    }

    if(temp != NULL && temp->exp == exp) {
        temp->coeff += coeff;
        free(newTerm);
        if(temp->coeff == 0) {
            if(prev) prev->next = temp->next;
            else head = temp->next;
            free(temp);
        }
    } else {
        newTerm->next = temp;
        if(prev) prev->next = newTerm;
        else head = newTerm;
    }

    return head;
}

Term* multiplyPolynomials(Term* p1, Term* p2) {
    Term* result = NULL;
    for(Term* t1 = p1; t1 != NULL; t1 = t1->next) {
        for(Term* t2 = p2; t2 != NULL; t2 = t2->next) {
            int coeff = t1->coeff * t2->coeff;
            int exp = t1->exp + t2->exp;
            result = insertTerm(result, coeff, exp);
        }
    }
    return result;
}

void printPolynomial(Term* head) {
    if(!head) {
        printf("0\n");
        return;
    }
    Term* temp = head;
    while(temp != NULL) {
        if(temp->coeff > 0 && temp != head) printf("+");
        if(temp->exp == 0)
            printf("%d", temp->coeff);
        else if(temp->exp == 1)
            printf("%dx", temp->coeff);
        else
            printf("%dx^%d", temp->coeff, temp->exp);
        temp = temp->next;
    }
    printf("\n");
}

int main() {
    int n1, n2;
    Term *poly1 = NULL, *poly2 = NULL;

    printf("Enter number of terms in first polynomial: ");
    scanf("%d", &n1);
    printf("Enter coefficient and exponent for each term:\n");
    for(int i = 0; i < n1; i++) {
        int coeff, exp;
        scanf("%d %d", &coeff, &exp);
        poly1 = insertTerm(poly1, coeff, exp);
    }

    printf("Enter number of terms in second polynomial: ");
    scanf("%d", &n2);
    printf("Enter coefficient and exponent for each term:\n");
    for(int i = 0; i < n2; i++) {
        int coeff, exp;
        scanf("%d %d", &coeff, &exp);
        poly2 = insertTerm(poly2, coeff, exp);
    }

    Term* result = multiplyPolynomials(poly1, poly2);

    printf("Resultant polynomial: ");
    printPolynomial(result);

    return 0;
}
