import java.awt.*;
public class swing {
    public static void main(String[] args) {

        Frame frame = new Frame();
        
        Button b = new Button("button");
        Label l = new Label("text");
        frame.add(b);
        frame.add(l);
        
        
        frame.setSize(420,420);
        frame.setVisible(true);

        //frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
    }
    
}
