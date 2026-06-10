import java.util.Scanner;

public class binarysearch {
    public static void main(String[] args) {
         Scanner k = new Scanner(System.in);
    System.out.print("enter size");
    int rj = k.nextInt();
        int[] arr = new int[rj];
       // boolean flag = false;
        for(int i=0;i<rj;i++){
            Scanner sc = new Scanner(System.in);
            arr[i]= sc.nextInt();

        }
         Scanner rd = new Scanner(System.in);
         System.out.print("enter radius");
         int r = rd.nextInt();
         boolean f=false;
         int l=0;
         int ri=rj-1;
         int i=0;
         int m=(l+ri)/2;
        while(l<=ri){
            if(r==arr[m]){
                f=true;
                i=m;
                break;
            }
            else if(r<arr[m]){
                ri=m-1;
                m=(l+ri)/2;
            }
            else{
                l=m+1;
                m=(l+ri)/2;
            }
        }
         if (f){
            System.out.println("found at"+i);
         }
         else{
            System.out.println("Not found");
         }
    }

}