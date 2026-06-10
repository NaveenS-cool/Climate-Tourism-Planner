package basics;
import java.util.Scanner;

public class pattern {
    public static void main(String[] args) {
       Scanner sc = new Scanner(System.in);
         int r = sc.nextInt();
         Scanner sr = new Scanner(System.in);
         int c = sr.nextInt();
        for(int i=1;i<=r;i++){
            int k=0;
            for(int j=1;j<=r;j++){
                //System.out.print(i+j);
                if (i+j==r && k==0){
                    System.out.print("*****");
                    k++;
                }
                else{
                    System.out.print(" ");
                }
            }
            System.out.println();
            sc.close();
            sr.close();
        }
        

    }
    
}
