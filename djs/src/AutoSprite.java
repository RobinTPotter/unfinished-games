import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;
import java.net.*;
import java.util.*;

public class AutoSprite extends Sprite implements Runnable {

	Thread thread;
	Graphics2D big;
	public Point[] directionmap=new Point[]{new Point(-1,0),new Point(1,0)};
	double incline=0;
	boolean isFalling;
	double fallSpeed=0;
	DJ main;


	public int currentFloor=-1;
	public Polygon currentPolygon;

	public int nextBarrier=-1;
	public Polygon nextPolygonBarier;

	public AutoSprite(int number, int frames, URL[] names,DJ main) {
		super(number,frames,names);
		this.main=main;

		boolean trapped=true;

		while(trapped) {
			trapped=false;
			position.x=(int)(Math.random()*300+200);
			position.y=(int)(Math.random()*100);
		}
		drawoffsetx=(int)(-width/2);
		drawoffsety=(int)(-height+3);

		number=(int)(Math.random()*2);
		frame=(int)(Math.random()*frames);

		isFalling=true;

		thread=new Thread(this);
		thread.start();
	}

	public void setCurrent() {
		


	}

	public boolean inPolygon(int pp) {
		if (pp>=main.level.size()) return false;
		if (main.level.get(pp).contains(position)) return true; else return false;
	}

	public boolean inPolygon(int dx, int dy) {
		for (int pp=0;pp<main.level.size();pp++) {
			if (main.level.get(pp).contains((double)position.x+(double)dx,(double)position.y+(double)dy)) return true; 
		}
		return false;
	}

	public boolean inPolygon(int pp,int dx, int dy) {
		if (pp>=main.level.size()) return false;
		if (main.level.get(pp).contains(new Point((int)(position.x+dx),(int)(position.y+dy)))) return true; else return false;
	}

	public boolean inPolygon(Polygon pp,int dx, int dy) {
		if (pp==null) return false;
		if (pp.contains(new Point((int)(position.x+dx),(int)(position.y+dy)))) return true; else return false;
	}

	public Object[] getBarriers(int offsetpositionx, int offsetpositiony, int offsetx, int offsety) {

		Vector<Intersection.PointDist> stack=new Vector<Intersection.PointDist>(1,0);
		//put these in a vector like you did the intersection stuff and populate to get closest then genericize 
		Intersection.PointDist[] pd=new Intersection.PointDist[main.level.size()];
		for (int pp=0;pp<main.level.size();pp++) {
			pd[pp]=Intersection.intersect(main.level.get(pp), new Point((int)(position.x+offsetpositionx),(int)(position.y+offsetpositiony)), new Point((int)(position.x+offsetx),(int)(position.y+offsety)));
			if (pd[pp]!=null) {
				if (stack.size()>0 && pd[pp].distance<stack.get(0).distance ) {
					stack.add(0,pd[pp]);
				} else {
					stack.add(pd[pp]);
				}
			}
		}

		if (stack.size()>0) return stack.toArray(); else return null;
	}

	public double getIncline(Polygon polygon, int line) {
	
		Point p1=new Point(polygon.xpoints[line],polygon.ypoints[line]);
		Point p2=new Point(polygon.xpoints[(line+1)%polygon.npoints],polygon.ypoints[(line+1)%polygon.npoints]);

		if (p2.x!=p1.x) return ((double)(p2.y)-p1.y)/((double)p2.x-p1.x);
		else return 1000;

	}

	public void segment() {


		if (currentPolygon==null) return;
		double inc=getIncline(currentPolygon,currentFloor);

		Point p1=new Point((int)position.x,(int)position.y);
		Point p2=new Point(currentPolygon.xpoints[(currentFloor+1)%currentPolygon.npoints],currentPolygon.ypoints[(currentFloor+1)%currentPolygon.npoints]);
		Point p0=new Point(currentPolygon.xpoints[currentFloor],currentPolygon.ypoints[currentFloor]);

		double inc2=((double)(p2.y)-p1.y)/(0.000000000000001+(double)p2.x-p1.x);

		System.out.println("segment "+inc+" "+inc2);

		if   ( (p0.x>p2.x && (position.x>p0.x || position.x<p2.x)) 
				|| (p0.x<=p2.x && (position.x>p2.x || position.x<p0.x))  ) {
			int nn=nextLine();
			incline=getIncline(currentPolygon,nn);
			currentFloor=nn;
			System.out.println("Off line..."+currentFloor+" next line"+nextLine()+" with incline "+inc);
			//fall();
		}


	}

	public int nextLine() {

		Point p1=new Point(currentPolygon.xpoints[(currentFloor+1)%currentPolygon.npoints],currentPolygon.ypoints[(currentFloor+1)%currentPolygon.npoints]);
		Point p0=new Point(currentPolygon.xpoints[currentFloor],currentPolygon.ypoints[currentFloor]);
		Point p2=new Point(currentPolygon.xpoints[(currentFloor+currentPolygon.npoints-1)%currentPolygon.npoints],currentPolygon.ypoints[(currentFloor+currentPolygon.npoints-1)%currentPolygon.npoints]);
		
		//determine direction of polygon
		if (p0.x<p1.x | p0.y<p1.y ) {
			//p0 p1 clock wise
			if (directionmap[number].x>0) {
				//moving +1 clockwise
				return (currentFloor+1)%currentPolygon.npoints;
			} else {
				return (currentFloor+currentPolygon.npoints-1)%currentPolygon.npoints;
			}

		} else {

			//not clock wise
			if (directionmap[number].x>0) {
				//moving +1 clockwise
				return (currentFloor+currentPolygon.npoints-1)%currentPolygon.npoints;
			} else {
				return (currentFloor+1)%currentPolygon.npoints;
			}
		
		}
		
	

	}

	public void setNextBarrier() {

		if (isFalling) {
			System.out.println("called set next bariiers");
			Object[] drops=getBarriers(directionmap[number].x*2,0,directionmap[number].x*2,60);
			if (drops==null) { System.out.println("none found"); }// System.out.println("no barrier below within 6 clicks");
			else {
				Intersection.PointDist drop=(Intersection.PointDist)drops[0];
				System.out.println("\nwill cross "+drop.polygon+" in line "+drop.line+" at "+drop.point+" which is "+drop.distance+" away");
				if (drop.distance<4) {
					isFalling=false;
					System.out.println("\nNot falling");
					position=new Point2D.Double(drop.point.x,drop.point.y);
					incline=getIncline(drop.polygon,drop.line);
					currentPolygon=drop.polygon;
					currentFloor=drop.line;
				}
			}
		} 
/**else {
			Object[] drops=getBarriers(directionmap[number].x*2,0,directionmap[number].x*20,0);
			if (drops==null) {}// System.out.println("no barrier below within 6 clicks");
			else {
				Intersection.PointDist drop=(Intersection.PointDist)drops[0];
				System.out.println("\nwill cross "+drop.polygon+" in line "+drop.line+" at "+drop.point+" which is "+drop.distance+" away");
				if (drop.distance<4) {
					//isFalling=false;
					//System.out.println("\nNot falling");
					
					double inc=getIncline(drop.polygon,drop.line);
					if (Math.abs(inc)>2) {
						System.out.println("direction change "+inc);
						number++;
						if (number>=totalnumber) number=0;

					} else if (inc!=incline) {
						currentPolygon=drop.polygon;
						currentFloor=drop.line;
						position=new Point2D.Double(drop.point.x,drop.point.y);
						incline=inc;
					}
				}
			}
		}
*/

	}

	

	public void fall() {
		fallSpeed=3;
		isFalling=true;
		currentPolygon=null;
		incline=0;
	}

	public void run() {

		try{

			Point[] l=new Point[4];
			while(thread.isAlive()) {

				if (!inPolygon(0,1)) fall();
				//if (inPolygon(currentPolygon,0,-2)) {
				//	System.out.println("Body in polygon");
				//	fall();
				//}

				if (isFalling) {
					
					System.out.print("falling..");
					twitch(0,fallSpeed);
					fallSpeed+=0.1;
					if (fallSpeed>=5) fallSpeed=5;
				} else {
					twitch(directionmap[number].x,directionmap[number].y+incline*directionmap[number].x);

					segment();
				}


				setNextBarrier();

				Thread.sleep(main.walkdelay);
			}	
		
		} catch(Exception ex) {
			ex.printStackTrace();
		}


	}


}