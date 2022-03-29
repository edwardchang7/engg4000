import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

public class MessageDialog extends JDialog {

	private final JPanel contentPanel = new JPanel();

	private JPanel header, buttonPanel;
	private JButton ok;
	private JLabel contextLabel;

	private static final String HEADER = "<html><center>";
	private static final String FOOTER = "</center></html>";

	/**
	 * Create the dialog.
	 */
	public MessageDialog(String title, String context, ImageIcon icon) {
		setModal(true);
		setModalityType(ModalityType.APPLICATION_MODAL);
		setBounds(100, 100, 450, 193);
		getContentPane().setLayout(new BorderLayout());
		contentPanel.setLayout(null);
		getContentPane().add(contentPanel, BorderLayout.CENTER);
		setUndecorated(true);
		getRootPane().setBorder(WindowBorder.getInstance());

		/*
		 * Header
		 */
		header = new Header(this, title, icon, false);
		contentPanel.add(header);

		/*
		 * ButtonPanel and buttons
		 */
		buttonPanel = new JPanel();
		buttonPanel.setBounds(10, 132, 430, 50);

		contentPanel.add(buttonPanel);

		contextLabel = new JLabel(HEADER + context + FOOTER);
		contextLabel.setFont(StandardFont.getInstance());
		contextLabel.setHorizontalAlignment(SwingConstants.CENTER);
		contextLabel.setBounds(10, 46, 430, 75);
		contentPanel.add(contextLabel);

		ok = new CustomButton("Ok");
		ok.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				dispose();
			}

		});

		buttonPanel.add(ok);

		setLocationRelativeTo(null);
		setVisible(true);
	}
}
