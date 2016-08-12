package robin.hello.finger;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;

/**
 * Created by potterr on 11/08/2016.
 */

public class Plate extends View implements GestureDetector.OnGestureListener {

    int mx = -1;
    GestureDetector gd;
    float rad = 10;
    int my = -1;
    int col = -1;

    public Plate(Context context) {
        super(context);

        gd = new GestureDetector(getContext(), this);
    }

    public Plate(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    public Plate(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }

    @Override
    public boolean onDown(MotionEvent e) {
        setM((int) (e.getX()), (int) (e.getY()));
        setCol(Color.GREEN);
        invalidate();
        return true;
    }

    @Override
    public void onShowPress(MotionEvent e) {
        setM((int) (e.getX()), (int) (e.getY()));
        setCol(Color.BLUE);
        invalidate();

    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        setM((int) (e.getX()), (int) (e.getY()));
        setCol(Color.RED);
        invalidate();
        return true;
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {

        setRad(
                getRad() + 2);
        setM((int) (e2.getX()), (int) (e2.getY()));
        setCol(Color.YELLOW);

        invalidate();
        return true;
    }

    @Override
    public void onLongPress(MotionEvent e) {
        setRad(100);
        setM((int) (e.getX()), (int) (e.getY()));
        setCol(Color.MAGENTA);
        invalidate();
    }

    @Override
    public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {

        setM((int) (e2.getX()), (int) (e2.getY()));
        setCol(Color.CYAN);
        invalidate();
        return true;
    }

    public float getRad() {
        return rad;
    }

    public void setRad(float rad) {
        this.rad = rad;
    }

    public void setM(int mx, int my) {
        this.mx = mx;
        this.my = my;
    }

    public int getMx() {
        return mx;
    }

    public void setMx(int mx) {
        this.mx = mx;
    }

    public int getMy() {
        return my;
    }

    public void setMy(int my) {
        this.my = my;
    }

    public int getCol() {
        return col;
    }

    public void setCol(int col) {

        this.col = col;
    }

    public void onDraw(Canvas c) {
        super.onDraw(c);

        //if (mx != -1 && my != -1 && col != -1) {

        Paint p = new Paint();
        p.setColor(col);
        c.drawCircle(mx, my, rad, p);
        if (rad > 10) rad -= 0.1;

        //}

    }
}
