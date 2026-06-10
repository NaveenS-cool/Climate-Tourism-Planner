import java.awt.*;
import java.awt.event.*;
        
class MyFrame extends Frame implements ActionListener
{
    Label l;
    int count=1;
    Button b;
    public MyFrame()
    {
        super("counter");
        l = new Label("  "+count);
        b = new Button("Click me");
        setLayout(new FlowLayout());
        b.addActionListener(this);
        add(b);
        add(l);
        
        
    }

    @Override
    public void actionPerformed(ActionEvent e) {
       count*=2;
       l.setText(" "+count);
    }

}

public class swing2 {
    public static void main(String[] args){
    
        MyFrame f = new MyFrame();
        f.setSize(1000, 1000);
        f.setVisible(true);
    }
    
    
}