import java.util.*;
import java.awt.*;
import java.awt.geom.*;


public class Intersection {


	static class PointDist {

		public Point point;
		public double distance;
		public Polygon polygon;
		public int line;

		public PointDist() {
			point=new Point(0,0);
			distance=0;
		}

		public PointDist(Point p, double distance, Polygon polygon, int line) {
			point=p;
			this.distance=distance;
			this.polygon=polygon;
			this.line=line;
		}

		public String toString() {
			return new String(polygon+" "+line+" "+point+" "+distance);
		}

	}

	public static PointDist intersect(Polygon poly, Point p1, Point p2) {

		Vector<PointDist> stack=new Vector<PointDist>(1,0);

		for (int pp=0;pp<poly.npoints;pp++) {
			Point start=new Point(poly.xpoints[pp],poly.ypoints[pp]);
			Point end=new Point(poly.xpoints[(pp+1)%poly.npoints],poly.ypoints[(pp+1)%poly.npoints]);
			Point i=intersect(start,end,p1,p2);
			if (i!=null) {
			double di1=Math.sqrt(((double)i.x-p1.x)*((double)i.x-p1.x)+((double)i.y-p1.y)*((double)i.y-p1.y));
					
				if (stack.size()>0) {
					Point top=stack.get(0).point;
					double dt1=Math.sqrt(((double)top.x-p1.x)*((double)top.x-p1.x)+((double)top.y-p1.y)*((double)top.y-p1.y));
					if (dt1>di1) stack.add(0,new PointDist(i,di1,poly,pp)); else stack.add(new PointDist(i,di1,poly,pp));
				} else {
					
					stack.add(new PointDist(i,di1,poly,pp));
				}
			}
		}

		if (stack.size()>0) return stack.get(0); else return null;
		

	}


	public static Point intersect(Point p1,Point p2, Point p3,Point p4) {

		double xD1,yD1,xD2,yD2,xD3,yD3;  
		double dot,deg,len1,len2;  
		double segmentLen1,segmentLen2;  
		double ua,ub,div;  
	 
		// calculate differences  
		xD1=p2.x-p1.x;  
		xD2=p4.x-p3.x;  
		yD1=p2.y-p1.y;  
		yD2=p4.y-p3.y;  
		xD3=p1.x-p3.x;  
		yD3=p1.y-p3.y;    
		
		// calculate the lengths of the two lines  
		len1=Math.sqrt(xD1*xD1+yD1*yD1);  
		len2=Math.sqrt(xD2*xD2+yD2*yD2);  
		
		// calculate angle between the two lines.  
		dot=(xD1*xD2+yD1*yD2); // dot product  
		deg=dot/(0.00000000001+len1*len2);  
		
		// if abs(angle)==1 then the lines are parallell,  
		// so no intersection is possible  
		if(Math.abs(deg)==1) return null;  
		
		// find intersection Pt between two lines  
		Point pt=new Point(0,0);  
		div=yD2*xD1-xD2*yD1;  
		ua=(xD2*yD3-yD2*xD3)/div;  
		ub=(xD1*yD3-yD1*xD3)/div;  
		pt.x=(int)(ua*xD1+p1.x);  
		pt.y=(int)(ua*yD1+p1.y);  
		
		// calculate the combined length of the two segments  
		// between Pt-p1 and Pt-p2  
		xD1=pt.x-p1.x;  
		xD2=pt.x-p2.x;  
		yD1=pt.y-p1.y;  
		yD2=pt.y-p2.y;  
		segmentLen1=Math.sqrt(xD1*xD1+yD1*yD1)+Math.sqrt(xD2*xD2+yD2*yD2);  
		
		// calculate the combined length of the two segments  
		// between Pt-p3 and Pt-p4  
		xD1=pt.x-p3.x;  
		xD2=pt.x-p4.x;  
		yD1=pt.y-p3.y;  
		yD2=pt.y-p4.y;  
		segmentLen2=Math.sqrt(xD1*xD1+yD1*yD1)+Math.sqrt(xD2*xD2+yD2*yD2);  
		
		// if the lengths of both sets of segments are the same as  
		// the lenghts of the two lines the point is actually  
		// on the line segment.  
		
		// if the point isn’t on the line, return null  
		if(Math.abs(len1-segmentLen1)>0.1 || Math.abs(len2-segmentLen2)>0.1)  
		return null;  
		
		// return the valid intersection  
		return pt;  
	}

}