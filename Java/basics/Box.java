package basics;

public class Box {
    double l;
    double w;
    double h;

    Box(){
        this.l=-1;
        this.w=-1;
        this.h=-1;
    }
    Box(double j){
        this.l=j;
        this.w=j;
        this.h=j;

    }
    Box(double i,double j,double k){
        this.l=i;
        this.w=j;
        this.h=k;
    }
    public static void Hi(String nam){
        System.out.println("hello"+nam );
    }
}
