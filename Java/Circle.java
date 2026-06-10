public class Circle 
{
    private double radius;
    void setradius(double radius)
    {
        this.radius=radius;
    }
    public  Circle(double radius){
            this.radius=radius;
    }
    void getradius(){
        System.out.println("Radius:"+radius);;
    }
     double  area()
    {
        return Math.PI*radius*radius;
    }
    double perimeter()
    {
        return 2*radius*Math.PI;
    }
    
}
