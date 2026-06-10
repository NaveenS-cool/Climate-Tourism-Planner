import java.util.Scanner;

public class Switch2{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        String op = sc.next();
        switch(op)
        {
            case "+": System.out.println(a+b);break;
             case "*": System.out.println(a*b);break;
              case "-": System.out.println(a-b);break;
               case "/": System.out.println(a/b);break;
                case "^": System.out.println(Math.pow(a,b));break;
                default: System.out.println("Wrong choice");

        }



    }



}
