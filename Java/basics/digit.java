package basics;
import java.util.Scanner;

public class digit {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int r = sc.nextInt();
        if (r%3 != 0 && r%5 == 0){
            System.out.println("it is a number");
        }
        else{
            System.out.println("NO");
        }


    }
    
}
