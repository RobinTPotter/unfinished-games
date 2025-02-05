
import javax.imageio.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;
import java.awt.geom.*;
import java.net.*;
import java.util.*;


public class DJ extends Frame implements Runnable {

	BufferedImage bi;
	public Graphics2D big;
	public boolean locked;
	private Vector<AutoSprite> djs;
	public Vector<Polygon> level;
	public int walkdelay=100;
	Polygon pickedup;
	Point mp;

	public DJ() {
		setTitle("DJ");
		setSize(600, 400);
		setVisible(true);

		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});

		addMouseListener(new MouseAdapter() {
			public void mousePressed(MouseEvent m) {
				mp=m.getPoint();
				for (int pp=0;pp<level.size();pp++) {
					if (level.get(pp).contains(m.getPoint().x,m.getPoint().y)) pickedup=level.get(pp);
				}
				walkdelay*=4;
			}
			public void mouseReleased(MouseEvent m) {
				walkdelay/=4;
				pickedup=null;
			}
		});

		addMouseMotionListener(new MouseMotionAdapter() {
			public void mouseDragged(MouseEvent m) {
				if (pickedup==null) return;
				Point cp=m.getPoint();
				int dx=cp.x-mp.x;
				if (!(cp.x<getWidth() && cp.x>=0)) dx=0;
				int dy=cp.y-mp.y;
				if (!(cp.y<getHeight() && cp.y>=0)) dy=0;

				pickedup.translate(dx,dy);

				for (int dd=0;dd<djs.size();dd++) {
					AutoSprite dj=djs.get(dd);
					if (dj.currentPolygon==pickedup) {
						dj.position.x+=dx;
						dj.position.y+=dy;
					}
				}


				mp=cp;
			}
		});

		bi=new BufferedImage(getWidth(),getHeight(),BufferedImage.TYPE_INT_ARGB);
		big=(Graphics2D)(bi.getGraphics());

		URL[] urls=new URL[16];

		int frames=8;
		for (int ff=0;ff<frames;ff++) {
			urls[0*frames+ff]=getClass().getResource("images/DJ_Left_snap00"+ff+".png");
			urls[1*frames+ff]=getClass().getResource("images/DJ_Right_snap00"+ff+".png");
		}

		level=new Vector<Polygon>(1,0);
		Polygon p;

		p=new Polygon();
		p.addPoint(100,300);
		p.addPoint(700,280);
		p.addPoint(230,340);
		p.translate(-100,30);
		level.add(p);

		p=new Polygon();
		p.addPoint(200,200);
		p.addPoint(400,230);
		p.addPoint(230,300);
		p.addPoint(130,300);
		p.addPoint(130,200);
		p.addPoint(135,200);
		p.addPoint(170,230);
		p.addPoint(190,230);
		level.add(p);

		djs=new Vector<AutoSprite>(1,0);
		djs.add(new AutoSprite(2,8,urls,this));

		try{
			Image image = ImageIO.read(getClass().getResource("images/cursor1.png"));
			Cursor transparentCursor = Toolkit.getDefaultToolkit().createCustomCursor(image, new Point(0, 0), "invisiblecursor");
			setCursor(transparentCursor);
		}catch(Exception ex) { ex.printStackTrace(); }
	
		locked=false;
		run();

	}









	public void run() {
		try{
			while(!locked) {

				big.setPaint(new GradientPaint(0,0,Color.yellow,0,getHeight(),Color.white));
				big.fillRect(0,0,getWidth(),getHeight());
				
				big.setPaint(Color.blue);
				
				for (int pp=0;pp<level.size();pp++) {
				
					big.setPaint(new GradientPaint(0,0,Color.red,0,getHeight(),Color.white));
					big.fillPolygon(level.get(pp));
					

				}

				for (int dd=0;dd<djs.size();dd++) {
					AutoSprite dj=djs.get(dd);
					dj.draw(big);
			
					//big.setPaint(Color.blue);
					//big.drawRect((int)(dj.position.x+dj.directionmap[dj.number].x*3-1),(int)(dj.position.y-1-8),3,3);
				}

				getGraphics().drawImage(bi,0,0,null);

				Thread.sleep(40);
			}

		} catch(Exception ex) {
			ex.printStackTrace();
		}
	}

	public static void main(String[] arg) {
		new DJ();
	}
}