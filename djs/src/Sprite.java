import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;
import java.io.*;
import javax.imageio.*;
import java.net.*;

public class Sprite {

	BufferedImage[][] image;
	int frame=0;
	int number=0;
	public boolean cycle=false;
	public Point2D.Double position=new Point2D.Double(30,30);
	public int width=0, height=0;
	public int drawoffsetx=0, drawoffsety=0;
	int frames=0;
	int totalnumber=0;
	

	public Sprite(int number, int frames, URL[] names) {

		totalnumber=number;
		this.frames=frames;
		image=new BufferedImage[number][frames];
		String filesrc=new String();
		int nn=0, ff=0;
		try{
			for (nn=0;nn<number;nn++) {
				for (ff=0;ff<frames;ff++) {
					image[nn][ff] = (BufferedImage)ImageIO.read(names[nn*frames+ff]);
					if (nn==0 & ff==0) {
						width=image[nn][ff].getWidth();
						height=image[nn][ff].getHeight();
					}
					System.out.println("loaded: "+names[nn*frames+ff]+" "+width+","+height);
				}
			}
			
		}catch(Exception ex) { System.out.println("problem loading: "+names[nn*frames+ff]); }
	}

	public void twitch(double dx, double dy) {
		position.x+=dx;
		position.y+=dy;
		frame++;
		if (frame==frames) frame=0;
	}

	public void draw(Graphics g) {
		g.drawImage(image[number][frame],(int)(position.x+drawoffsetx),(int)(position.y+drawoffsety),null);
	}

}