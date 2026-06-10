import java.util.Scanner;
public class Binary {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n= sc.nextInt();
        int[] arr= new int[20];
        int i=0;
        while(n!=0){
            int r=n%2;
            arr[i]=r;
            i++;
            n=n/2;
        }

        for(int j=0;j<i;j++){
            System.out.print(arr[i-j-1]);
        }
    }
    
}
