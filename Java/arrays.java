import java.util.Scanner;

public class arrays {
    public static void main(String[] args) {
         Scanner k = new Scanner(System.in);
    System.out.print("enter size");
    int rj = k.nextInt();
        int[] arr = new int[rj ];
        boolean flag = false;
        for(int i=0;i<rj;i++){
            Scanner sc = new Scanner(System.in);
            arr[i]= sc.nextInt();

        }
         Scanner rd = new Scanner(System.in);
         System.out.print("enter radius");
         int r = rd.nextInt();
       for(int i=0;i<rj;i++){
        if (r==arr[i]){
            flag=true;
            System.out.println(i);
            break;
        }
       }
       if(flag){
        System.out.println("found");
       }
       else{
        System.out.println("NO");
       }
    }
    
}
