import java.util.Scanner;
class Factorial
{
	static int factorial(int n)
	{
	int fact=1;int i=1;
		do
		{
		fact=fact*i;	
		}while(i<=n);
	return fact;
	}
	public static void main(String args[])
	{
		Scanner sc = new Scanner(System.in); 
		int n = sc.nextInt();
		System.out.println("Factorial ="+factorial(n));

	}



}