
import java.util.Arrays;
import java.util.Scanner;

public class aibinary {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input array size
        System.out.print("Enter size: ");
        int size = scanner.nextInt();
        int[] arr = new int[size];

        // Input array elements
        System.out.println("Enter array elements:");
        for (int i = 0; i < size; i++) {
            arr[i] = scanner.nextInt();
        }

        // Sort array (required for binary search)
        Arrays.sort(arr);

        // Input target value
        System.out.print("Enter value to search: ");
        int target = scanner.nextInt();

        // Binary search
        boolean found = false;
        int left = 0, right = size - 1;
        int index = -1;

        while (left <= right) {
            int mid = (left + right) / 2;

            if (arr[mid] == target) {
                found = true;
                index = mid;
                break;
            } else if (target < arr[mid]) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }

        // Output result
        if (found) {
            System.out.println("Found at index: " + index);
        } else {
            System.out.println("Not found");
        }

        scanner.close();
    }
}

