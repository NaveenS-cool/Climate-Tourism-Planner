public class Loop {
    public static void main(String[] args) {
        int k=0;
         for(int i=0;i<10;i++){
            System.out.println(i);
            if (i==7){
            i--;
                k++;
                if(k==2)break;
        }
        }
    }
}

