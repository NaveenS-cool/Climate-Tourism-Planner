import java.util.Scanner;
public class Armstrong {
    public static void main(String[] args) {
        int num, digits;
        Scanner sc = new Scanner(System.in);
        num = sc.nextInt();
        //Armstrong a = new Armstrong();
        digits = (int)Math.log10(num)+1;
        System.out.println(digits);
        int temp = num;int sum=0;
        while(temp >0)
        {
            int rem = temp%10;
            sum+=Math.pow(rem,digits);
            temp = temp/10;
        }
        if (sum == num)
            System.out.println(num+" is an Armstrong number");
        else
            System.out.println(num+" is not an Armstrong number");

    }
     int len(int num)
    { 
        int count = 0;
        while(num>0)
        {
            num = num/10; count++;
        }

        return count;
    }
    
}
