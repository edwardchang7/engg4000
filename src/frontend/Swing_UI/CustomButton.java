import java.awt.Color;
import java.awt.Dimension;

import javax.swing.JButton;

public class CustomButton extends JButton {

	public CustomButton(String text) {
		super(text);

		this.setFocusPainted(false);
		this.setBorder(null);
		this.setBorder(RoundedBorder.getInstance());
		this.setForeground(Color.BLACK);
		this.setContentAreaFilled(false);
		this.setPreferredSize(new Dimension(100, 40));
	}

}
