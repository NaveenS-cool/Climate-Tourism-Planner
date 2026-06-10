package basics;
import java.util.Scanner;
public class Prime {
    public static void main(String[] args) {
         Scanner sc = new Scanner(System.in);
         int r = sc.nextInt();
         boolean flag = true;
         for(int i=2;i<r/2;i++){
            if(r%i==0){
                flag = false;
                break;
            } 
         }
         if(flag){
            System.out.println("Prime");
         }
         else{
            System.out.println("Not prime");
         }
    }
    
}
