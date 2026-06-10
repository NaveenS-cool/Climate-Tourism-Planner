#include <stdio.h>
#include <string.h>
struct string
{
    char s[20];

};
struct string S[20];
void Sarray(char* s,int w)
{

      strcpy(s,S[w].s);
}



int main()
{
    char c[40];
    char temp[10];
    //char n[] = "";
    char find[10] ;
     char r[10];

    fgets(c,sizeof(c),stdin);
    fgets(find,sizeof(find),stdin);
     fgets(r,sizeof(r),stdin);
    int i =0;int j=0;int w =0;int k;
   while (c[i] != '\0' )
   {
            //printf("%c",c[i]);
            if (c[i] == ' ')
            {
                temp[j]='\0';
                //printf("%s",find);
                k = strcmp(temp,find);
                    printf("%s %s ",temp,find);
                  printf("%d\n",k);

                if (k == 0){
                      //   printf("%s",find);
                       // printf("$%s$",temp);
                        strcpy(temp,r);
                       //printf("%s",temp);
                    }
              printf("%s ",temp);
                j=0;
               w++;
               // Sarray(temp,w);


            }
            else{
                temp[j++]=c[i];

            }
            i++;
   }
    return 0;
}