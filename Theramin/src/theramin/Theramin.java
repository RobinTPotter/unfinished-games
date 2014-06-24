package theramin;

import java.awt.*;
import java.io.*;
import java.awt.event.*;
import java.util.*;
import javax.swing.*;
import javax.sound.sampled.*;

class HarmonicControl extends Panel {
		
	Scrollbar scroll;
	TextField val;
	Button kill;
	float value;
	HarmonicControlPanel hcp;

	public HarmonicControl(HarmonicControlPanel hcp) {


		super();

		this.hcp=hcp;
		scroll=new Scrollbar(Scrollbar.VERTICAL,50,1,0,100);
		val=new TextField(1);	
		value=1;
		val.setText("1");



		val.addMouseListener(new MouseAdapter() {
			public void mouseEntered(MouseEvent m) {
				val.requestFocus();
				val.selectAll();
			}
		});


		val.addTextListener(new TextListener() {
			public void textValueChanged(TextEvent t) {
				float stored=value;
				try {
					value=Float.parseFloat(val.getText());
					val.setBackground(Color.white);
				} catch(Exception ex) {
					value=stored;
					val.setBackground(Color.red);
				}
			}
		});

		setFont(new Font("SansSerif", Font.PLAIN, 7));

		kill=new Button("x");
		kill.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent a) {
				HarmonicControl.this.hcp.remove(HarmonicControl.this);
			}
		});

		//kill.setMaximumSize(new Dimension(10,10));
		//scroll.setMinimumSize(new Dimension(12,160));


		setBackground(Color.gray);
		setMaximumSize(new Dimension(18,200));
		setMinimumSize(new Dimension(18,200));

		if (false) {

			setLayout(new GridBagLayout());
			GridBagConstraints c = new GridBagConstraints();
		
			c.fill=GridBagConstraints.VERTICAL;
			c.gridx=0;
			c.gridy=0; 
			c.gridheight = 9; 
			add(scroll,c);
			c.anchor=GridBagConstraints.CENTER;

			c.gridx=0;
			c.gridy=10;
			c.gridheight = 1; 
			add(kill,c);


			c.gridx=0;
			c.gridy=11;
			c.gridheight = 1; 
			add(val,c);

		} else {

			setLayout(null);
			add(scroll);
			add(kill);
			add(val);




		}

		validate();

	}

	public float getAmplitude() {
		return (float)scroll.getValue()/100;
	}
	
	public float getHarmonic() { return value; }	

	public void paint(Graphics g) {
		super.paint(g);

		scroll.setBounds(0,0,18,162);
		kill.setBounds(0,163,18,18);
		val.setBounds(0,181,18,18);




		g.setColor((Color.gray).darker());
		g.drawLine(0,0,0,getHeight());
	}

}


class HarmonicControlPanel extends Panel {


	public HarmonicControlPanel() {

		super();


		BoxLayout b=new BoxLayout(this,BoxLayout.X_AXIS);
		setLayout(b);

		setMaximumSize(new Dimension(1000000,200));
		setMinimumSize(new Dimension(200,200));
		setPreferredSize(new Dimension(200,200));

		addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent m) {
				if (m.getClickCount()==2) {
					HarmonicControlPanel.this.add(new HarmonicControl(HarmonicControlPanel.this));

				}
			}
		});


	}

	public HarmonicControl add(HarmonicControl h) {
		super.add(h);
		validate();
		repaint();
		return h;
	}

	public void remove(HarmonicControl h) {
		super.remove(h);
		doLayout();
		h=null;
	}


	public void paint(Graphics g) {
		g.drawRect(0,0,getWidth()-1,getHeight()-1);
	}

	public int getNumberHarmonics() { return getComponents().length; }
	
	public HarmonicControl getHarmonicControl(int hh) {
		if (hh>getComponents().length-1) hh=getComponents().length-1;
		else if (hh<0) hh=0;
		return (HarmonicControl)(getComponents()[hh]);
	}

	public float getHarmonic(int hh) {
		if (hh>getComponents().length-1) hh=getComponents().length-1;
		else if (hh<0) hh=0;
		return ((HarmonicControl)(getComponents()[hh])).getHarmonic();
	}

	public float getAmplitude(int hh) {
		if (hh>getComponents().length-1) hh=getComponents().length-1;
		else if (hh<0) hh=0;
		return ((HarmonicControl)(getComponents()[hh])).getAmplitude();
	}

}

class MainControlPanel extends Panel  {

	Scrollbar gain;
	Scrollbar buffer;
	Scrollbar mouseDiffFactorVal;
	Scrollbar fine;
	TextField basepitch;
	Checkbox record;
	TextField recordfilename;
	Label[] l;
	Generator gen;
	FileOutputStream fos;
	final int WIDTH=150;

	public MainControlPanel() {
		super();

		setBackground((Color.gray));
		setMaximumSize(new Dimension(WIDTH,200));
		setMinimumSize(new Dimension(WIDTH,200));
		setPreferredSize(new Dimension(WIDTH,200));

		gain=new Scrollbar(Scrollbar.HORIZONTAL,50,1,0,100);
		buffer=new Scrollbar(Scrollbar.HORIZONTAL,1024,16,512,4096);
		mouseDiffFactorVal=new Scrollbar(Scrollbar.HORIZONTAL,2,1,1,20);
		fine=new Scrollbar(Scrollbar.HORIZONTAL,50,1,0,200);
		record=new Checkbox("Recording");
		recordfilename=new TextField(10);
		recordfilename.setText((new File(System.getProperty("java.class.path"))).getParent()+File.separator+"temp");
		recordfilename.addMouseListener(new MouseAdapter() {
			public void mouseEntered(MouseEvent m) {
				MainControlPanel.this.recordfilename.requestFocus();
				MainControlPanel.this.recordfilename.selectAll();
			}
		});


		record.addItemListener(new ItemListener() {
			public void itemStateChanged(ItemEvent e) {

				if (record.getState()) recordfilename.setEnabled(false);
				else recordfilename.setEnabled(true);

				if (record.getState()) {
					try {
						if (fos!=null) fos.close();
						fos=new FileOutputStream(recordfilename.getText()+".dat",true);
					} catch(Exception ex) { ex.printStackTrace(); }
				}
			}
		});

		basepitch=new TextField(10);
		basepitch.addMouseListener(new MouseAdapter() {
			public void mouseEntered(MouseEvent m) {
				MainControlPanel.this.basepitch.requestFocus();
				MainControlPanel.this.basepitch.selectAll();
			}
		});
		basepitch.setText("440");
		basepitch.addTextListener(new TextListener() {
			public void textValueChanged(TextEvent t) {
				float gp=gen.pitch;
				try {
					gen.pitch=Float.parseFloat(basepitch.getText());
					basepitch.setBackground(Color.white);
				} catch(Exception ex) {
					gen.pitch=gp;
					basepitch.setBackground(Color.red);
				}
			}
		});

		add(gain);
		add(buffer);
		add(mouseDiffFactorVal);
		add(fine);
		
		fine.addAdjustmentListener(new AdjustmentListener() { public void adjustmentValueChanged(AdjustmentEvent a) { gen.repaint(); }});
		mouseDiffFactorVal.addAdjustmentListener(new AdjustmentListener() { public void adjustmentValueChanged(AdjustmentEvent a) { gen.repaint(); }});
		
		add(record);
		add(recordfilename);
		add(basepitch);



		l=new Label[6];
		l[0]=new Label(); add(l[0]); l[0].setText("G"); //Gain over all
		l[1]=new Label(); add(l[1]); l[1].setText("B"); //buffer size
		l[2]=new Label(); add(l[2]); l[2].setText("M"); //something to do with the mouse control
		l[3]=new Label(); add(l[3]); l[3].setText("T"); //tuning?
		l[4]=new Label(); add(l[4]); l[4].setText("F"); //file name to output raw data to
		l[5]=new Label(); add(l[5]); l[5].setText("P"); //base pitch 440Hz = A

		buffer.addAdjustmentListener(new AdjustmentListener() {
			public void adjustmentValueChanged(AdjustmentEvent a) {
				if (gen!=null)  {
					synchronized(gen) {
						gen.stop();
						gen.commence();
					}
				}
			}
		}) ;

	}
	
	public float getMainAmplitude() {
		return (float)(gain.getValue())/100;
	}

	public int getMainBuffer() {
		return buffer.getValue();
	}

	public float getMainMouseDiffFactor() {
		return (float)(mouseDiffFactorVal.getValue());
	}

	public float getMainFine() {
		return (float)(fine.getValue()-100);
	}

	public void setGenerator(Generator g) {
		gen=g;		
		gen.repaint(200);
	}

	public void doLayout() {
		int yy=0; int hh=20;
		int llwid=10;
		int mmwid=WIDTH-llwid;

		l[0].setBounds(0,yy,llwid,20);
		gain.setBounds(11,yy,mmwid,hh); yy+=hh+1;
		l[1].setBounds(0,yy,llwid,20);
		buffer.setBounds(11,yy,mmwid,hh); yy+=hh+1;
		l[2].setBounds(0,yy,llwid,20);
		mouseDiffFactorVal.setBounds(11,yy,mmwid,hh); yy+=hh+1;
		l[3].setBounds(0,yy,llwid,20);
		fine.setBounds(11,yy,mmwid,hh); yy+=hh+1;
		record.setBounds(0,yy,WIDTH,hh); yy+=hh+1;
		l[4].setBounds(0,yy,llwid,20);
		recordfilename.setBounds(10,yy,mmwid,hh); yy+=hh+1;
		basepitch.setBounds(10,yy,mmwid,hh);
		l[5].setBounds(0,yy,llwid,20);

	}	

	public void paint(Graphics g) {
		doLayout();

	}

}

class Generator extends JPanel implements Runnable {

	private int sampleRate = 22050;

	Point m=new Point(0,0);
	String label;
	AudioFormat audioFormat;

	public volatile float pitch;
	private volatile float amplitude;
	private volatile float playingpitch;
	private float angle;
	float mousediffpitch=0;
	float mousedifffactor=0.5f;

	private byte[] buffer;
	private SourceDataLine line;
	int mx=-1;

	Thread thread;
	int written=0;

	HarmonicControlPanel hcp;
	MainControlPanel mcp;

	public Generator(HarmonicControlPanel p, MainControlPanel mp) {
		setBackground((Color.gray).darker());

		hcp=p;
		mcp=mp;

		pitch=440;
		angle=0;

		setLayout(null);

		addMouseMotionListener(new MouseMotionAdapter() {
			public void mouseMoved(MouseEvent m) {
				mousediffpitch=(int)m.getX();
				Generator.this.m=m.getPoint();

				amplitude=(float)m.getY()/getHeight();

				Generator.this.repaint();
			}
		});

		addMouseListener(new MouseAdapter() {
			public void mouseEntered(MouseEvent m) {
				Generator.this.requestFocus();

			}
		});

		addKeyListener(new KeyAdapter() {
			public void keyPressed(KeyEvent k) {
				try{
					if (k.getKeyCode()>=65 && k.getKeyCode()<=91) pitch=-10+30*(k.getKeyCode()-64);
					System.out.println("pitch set "+pitch);
					mcp.basepitch.setText(String.valueOf(pitch));
					Generator.this.repaint();
				} catch(Exception ex) { ex.printStackTrace(); }
			}
			public void keyReleased(KeyEvent k) {
				try{
				
				} catch(Exception ex) { ex.printStackTrace(); }

			}

		});

		commence();

	}

	public void commence() {

		thread = new Thread(this);
		thread.start();

		System.out.println("!commenced!");

	}


	public void stop() {
		if (line!=null) line.stop();
		line=null;
		thread=null;
		System.out.println("!stopped!");
	}

	public void run() {
		audioFormat = new AudioFormat(sampleRate, 16, 1,  true, false);

		int bufferSize;
 
		try {
			bufferSize =mcp.getMainBuffer(); //sampleRate  / 64;
			System.out.println("setting buffer size  " + bufferSize);
			line = AudioSystem.getSourceDataLine(audioFormat);
			//System.out.println("request buffer size is " + bufferSize);
			line.open(audioFormat, bufferSize);
			bufferSize = line.getBufferSize();
			System.out.println(line+"\n"+audioFormat);
			System.out.println("effective buffer size is " + bufferSize);
		} catch (Exception e) {
			System.out.println(e);
			System.out.println("no line allocated");
			return;
		}
 
		line.start();
		buffer = new byte[bufferSize];
 	
		try {

			while (thread!=null) {
				int available = line.available();
				//System.out.println(available+" "+bufferSize);
		
				if (available > 0) {
					if (available<=bufferSize) play(available); else play(bufferSize);
				} else {
					try {
						// be sure to not sleep for too long
						Thread.sleep(1);
					} catch (InterruptedException e) {
					}
				}
			}
		} catch(Exception ex) { ex.printStackTrace(); }
	}
 
	public void paint(Graphics g) {
		super.paint(g);
		if (m!=null) {

			label=String.valueOf((float)Math.round(100*playingpitch)/100);
			g.setColor(Color.white);
			FontMetrics fm=g.getFontMetrics();
			int width = fm.stringWidth(label);
			g.drawString(label,m.x-width/2,m.y);
			
			int pp=(int)pitch;
			int xx=0;
			int n=0;
			while (xx<getWidth()) {
				float freq=(float)(pp*Math.pow((Math.pow(2,1f/12)),n));

		xx=(int)((mcp.getMainMouseDiffFactor())*(freq-mcp.getMainFine()-pitch));


				//xx=(int)(mousedifffactor*(freq-pitch))-;
				n+=1;
				g.drawLine(xx,0,xx,getHeight());
			}

		}
	}

	private void play(int frames) throws Exception {

		playingpitch=(float)pitch+(mousediffpitch)/mcp.getMainMouseDiffFactor()+mcp.getMainFine();
		float mainamp=mcp.getMainAmplitude();

		for (int i = 0; i < frames-1; i+=2) {


			float value=0;
			

			angle += Math.PI * 2.0 * (playingpitch) / (float)sampleRate;
			for (int hh=0;hh<hcp.getNumberHarmonics();hh++) {
				value+=mainamp*amplitude*hcp.getAmplitude(hh)*Math.sin(hcp.getHarmonic(hh)*angle);
			}			


			if (angle > Math.PI * 2.0) angle -= Math.PI * 2.0;

			short sample=(short)(value * 32767.0f);
			
			buffer[i+1]=(byte) ((sample >> 8) & 0xFF);
			buffer[i]=(byte) (sample & 0xFF);

		}
		
		//System.arraycopy(buffer,0,buffer2,0,buffer.length);
		line.write(buffer, 0, frames);
		
		if (mcp.record.getState()) {
			if (mcp.fos!=null) {
				mcp.fos.write(buffer,0,frames);
				written+=frames;
			}
		}
		//pitch+=1;
	}  


	public void close() {

		try {
			thread=null;
			if (mcp.fos!=null) {
				mcp.fos.flush();
				Thread.sleep(100);
				mcp.fos.close();
			}
			if (mcp.record.getState()) {
				AudioInputStream fis=new AudioInputStream(new FileInputStream(new File(mcp.recordfilename.getText()+".dat")),audioFormat,written/(16/8));
				AudioSystem.write(fis,AudioFileFormat.Type.WAVE, new File(mcp.recordfilename.getText()+".wav"));
				System.out.println(written+" frames");
				written=0;
			}
		} catch(Exception ex) { ex.printStackTrace(); }
	}

}

public class Theramin extends Panel {

	final Generator gen;

	public Theramin() {

		final HarmonicControlPanel hcp=new HarmonicControlPanel();
		final MainControlPanel mcp=new MainControlPanel();
		gen=new Generator(hcp,mcp);
		mcp.setGenerator(gen);
		final Panel f=this;
		final Panel cp=new Panel();



		BoxLayout b=new BoxLayout(cp,BoxLayout.X_AXIS);

		cp.setLayout(b);

		cp.setMaximumSize(new Dimension(1000000,200));
		cp.setMinimumSize(new Dimension(200,200));
		cp.setPreferredSize(new Dimension(200,200));









		f.setLayout(new BoxLayout(f,BoxLayout.Y_AXIS));
	


		Panel sep=new Panel();
		sep.setBackground(Color.gray);
		sep.setMaximumSize(new Dimension(10000000,5));
		sep.addMouseListener(new MouseAdapter(){
			public void mousePressed(MouseEvent m) {
				if (cp.isVisible()) {
					f.remove(hcp);
					cp.setVisible(false);
					f.doLayout();
				} else {
					f.add(cp,0);
					cp.setVisible(true);
					f.doLayout();
				}
			}
			public void mouseEntered(MouseEvent m) {
				if (!cp.isVisible()) {
					f.add(cp,0);
					cp.setVisible(true);
					f.doLayout();
				}
			}
		});


		cp.add(mcp);
		cp.add(hcp);
		f.add(cp);
		f.add(sep);
		f.add(gen);
		hcp.add(new HarmonicControl(hcp));

	}

	public static void main(String[] arg) {
		final Frame f=new Frame();
		final Theramin t=new Theramin();
		f.setSize(300,400);
		f.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent w) {
				t.gen.close();
				System.exit(0);
			}
		});

		f.add(t);
		
		f.setMinimumSize(new Dimension(200,227));
		f.setVisible(true);
		f.doLayout();
		
	}


}
