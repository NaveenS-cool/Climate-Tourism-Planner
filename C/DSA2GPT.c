#include <stdio.h>

typedef struct {
    int coeff;
    int exp;
} P;

int main() {
    P m[7];
    P k[7];
    P c[7];

    printf("Enter polynomial m (coeff and exp):\n");
    for (int i = 0; i < 7; i++) {
        scanf("%d %d", &m[i].coeff, &m[i].exp);
    }

    printf("Enter polynomial k (coeff and exp):\n");
    for (int i = 0; i < 7; i++) {
        scanf("%d %d", &k[i].coeff, &k[i].exp);
    }

    for (int i = 0; i < 7; i++) {
        c[i].coeff = (m[i].coeff + k[i].coeff) % 3;
        c[i].exp = m[i].exp;  // assuming same exponents
    }

    printf("Output (coeff exp):\n");
    for (int i = 0; i < 7; i++) {
        printf("%d %d", c[i].coeff, c[i].exp);
        if (i < 6) printf(", ");
    }
    printf("\n");

    return 0;
}
