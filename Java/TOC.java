public class TOC{
    public static void main(String[] args) {
        int a = 6;
       
        System.out.println(GS(6));
        ;   }



static String GS(int n)
{
    if (n==0)
    return "";
    else    
       return "("+GS(n-1)+")";
}
}