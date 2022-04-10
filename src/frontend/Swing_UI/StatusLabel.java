import javax.swing.JLabel;

public class StatusLabel extends JLabel {

	public StatusLabel(String text) {
		super(text);
		setFont(StandardFont.getInstance());
		setHorizontalAlignment(JLabel.CENTER);
	}

}
