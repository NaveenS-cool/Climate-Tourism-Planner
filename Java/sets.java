public class sets {
    public static void main(String[] args) {
        
       int[] B = {4,5,3,6};
       int[] A = {1,2,3,6};
       boolean s = false;
       int[] U = {1,3,2,0,0,0};
       int[] I={0,0};
       int n,k;
       k=0;
       n=2;
       for(int i=0;i<4 ; i++){
             for(int j=0;j<4 ; j++){
                if (B[i]==A[j]){
                    s=true;
                    break;
                }

       }
       if (!s){
        U[++n]=B[i];
       }
       else{
        I[k++] = B[i];
       }

       }

        
        for(int i=0;i<5 ; i++){
            System.out.println(U[i]);
            System.out.println("k");

       }
       System.out.println(I[0]);
         System.out.println(I[1]);
    }
    
}
