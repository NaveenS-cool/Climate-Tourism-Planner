#include <stdio.h>

int isPossible(int pages[], int n, int s, int maxPages) {
    int students = 1, sum = 0;
    for (int i = 0; i < n; i++) {
        if (pages[i] > maxPages)
            return 0;
        if (sum + pages[i] > maxPages) {
            students++;
            sum = pages[i];
        } else {
            sum += pages[i];
        }
    }
    return students <= s;
}

int findMinPages(int pages[], int n, int s) {
    if (s > n) return -1; // More students than books

    int low = pages[0], high = 0;
    for (int i = 0; i < n; i++) {
        if (pages[i] > low) low = pages[i];
        high += pages[i];
    }

    int result = high;

    while (low <= high) {
        int mid = (low + high) / 2;
        if (isPossible(pages, n, s, mid)) {
            result = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }

    return result;
}

/*void printAllocation(int pages[], int n, int s, int maxPages) {
    int sum = 0, student = 1;
    printf("Student %d: [", student);
    for (int i = 0; i < n; i++) {
        if (sum + pages[i] > maxPages) {
            printf("\b\b] → %d pages\n", sum); // backspace to remove comma
            student++;
            sum = pages[i];
            printf("Student %d: [%d, ", student, pages[i]);
        } else {
            printf("%d, ", pages[i]);
            sum += pages[i];
        }
    }
    printf("\b\b] → %d pages\n", sum);
}*/
void printAllocation(int *pages,int n,int s,int min){
    int student=1;
    int sum=0;
    int k=-1;
    int j=0;
    int i=0;
    while(k<=n){
        if (sum<=min){
            sum+=pages[i++];
              printf("%d,i=%d,",sum,i);
            k++;
            printf("%d\n",k);
        }
        else{
            printf("student %d:[",student++);
            //int r=k-j;
            while(j<k){
                printf("%d ",pages[j]);
                j++;
                //for(int l=0;l<r-2;l++)
                  //  printf(",");
                    

            }
            printf("]\n");
            sum=20;
            
        }

    }



}

int main() {
    int pages[] = {10, 20, 30, 40, 50, 60};
    int n = sizeof(pages) / sizeof(pages[0]);
    int s = 4;

    int minPages = findMinPages(pages, n, s);
    printf("Minimum of the maximum pages: %d\n", minPages);
    printAllocation(pages, n, s, minPages);

        return 0;
}