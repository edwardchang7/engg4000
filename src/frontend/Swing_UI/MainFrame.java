import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.filechooser.FileNameExtensionFilter;

public class MainFrame extends JFrame {

	private JPanel contentPane, header, buttonPanel;
	private JButton upload, generate;
	private JFileChooser fileChooser;
	private JFrame self;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MainFrame frame = new MainFrame();
					frame.setLocationRelativeTo(null);
					frame.setVisible(true);

				} catch (Exception e) {
					new MessageDialog("Error", "Unable to open the UI", null);
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public MainFrame() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 340, 175);
		contentPane = new JPanel();
		contentPane.setLayout(null);
		setContentPane(contentPane);
		setUndecorated(true);
		getRootPane().setBorder(WindowBorder.getInstance());
		self = this;

		/*
		 * Header
		 */
		header = new Header(this, "ENGG4000_Automated Musicians", null, true);
		contentPane.add(header);

		/*
		 * Button Panels and buttons
		 */
		buttonPanel = new JPanel();
		buttonPanel.setBounds(10, 115, 320, 49);
		contentPane.add(buttonPanel);

		generate = new CustomButton("Generate");
		generate.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				/*
				 * 1. Run the file that will generate a song.
				 */

				var songBuilderPath = System.getProperty("user.dir") + "/src/backend/demo.py";

				ProcessBuilder process = new ProcessBuilder("python", songBuilderPath).inheritIO();
				Process p = null;

				try {
					p = process.start();
				} catch (IOException e1) {
					new MessageDialog("Error", "Unable to execute Song_Builder Python script", null);
				}
				// a delay until the song generation is completed
				try {
					p.waitFor();
					// open EZABC with the generated abc file? -- STILL THINKING
				} catch (InterruptedException e1) {
					new MessageDialog("Error", "Process of building a song was interupted", null);
				}
			}

		});

		upload = new CustomButton("Upload");
		upload.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				fileChooser = new JFileChooser();
				fileChooser.setMultiSelectionEnabled(true);

				// a filter to only filter mxl extension files
				var filter = new FileNameExtensionFilter("Music XML \".mxl\"", "mxl");
				fileChooser.setFileFilter(filter);

				// set the default search dir to be the desktop
				var dirString = System.getProperty("user.home") + "/Desktop";
				var dir = new File(dirString);
				fileChooser.setCurrentDirectory(dir);

				// show the JFC
				var choice = fileChooser.showOpenDialog(self);
				// will hold all the selected files
				File[] files = null;

				/*
				 * ENTER THE DESTINATION OF WHERE TO PUT THE MXL FILES TO BE CONVERTED
				 * 
				 * ENTER THE PATH OF THE RHYTHIMC PATTERN FILE TO BE EXECUTED
				 */
				var destinationDir = "";
				var extractionScriptPath = "";

				/*
				 * 1. For each file within the list of selected files, move them into the folder
				 * that holds files to be converted
				 * 
				 * 2. Run the extraction script to convert and extract all the information
				 * 
				 * ** IN PYTHON, FOR EACH FILE, CHECK IF THE COLLECITON NAME ALREADY EXIST. IF
				 * YES, DONT CONVERT
				 * 
				 * 3. Add a check to see if there is a new '.abc' file created within the abc
				 * folder of converted files, IF NOT, SHOW ERROR DIALOG
				 */

				if (choice == JFileChooser.APPROVE_OPTION) {
					// files = all the slected "xml" files
					files = fileChooser.getSelectedFiles();

					if (files.length == 0) {
						new MessageDialog("Error", "There were no files selected to be parsed", null);
						return;
					}

					// This loop moves the files to the destinationDir to be conveterd to abc and be
					// extracted
					for (File f : files) {
						f.renameTo(new File(destinationDir + f.getName()));
					}

					// This section executes the python script to convert the mxl file to abc and
					// extract the required information and upload it to MongoDB
					ProcessBuilder process = new ProcessBuilder("python", extractionScriptPath).inheritIO();
					Process p = null;
					try {
						p = process.start();
					} catch (IOException e1) {
						new MessageDialog("Error",
								"Unable to perform extraction / uploading of information", null);
					}
					// a delay until the conversion, extraction and upload is completed
					try {
						p.waitFor();
						new MessageDialog("Success",
								"Succesfully extracted and converted the selected files", null);
					} catch (InterruptedException e1) {
						new MessageDialog("Error",
								"Process of extracting and uploading information was interrupted", null);
					}
				} else if (choice == JFileChooser.CANCEL_OPTION) {
					new MessageDialog("Error", "No files were selected", null);
				}
			}
		});

		buttonPanel.add(generate);
		buttonPanel.add(upload);
	}
}
