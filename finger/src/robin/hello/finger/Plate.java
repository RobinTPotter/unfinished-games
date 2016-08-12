package robin.hello.finger;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.View;

/**
 * Created by potterr on 11/08/2016.
 */

public class Plate extends View {


    int mx = -1;

    public float getRad() {
        return rad;
    }

    public void setRad(float rad) {
        this.rad = rad;
    }

    float rad = 10;

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

    int my = -1;
    int col = -1;

    public Plate(Context context) {
        super(context);
    }

    public Plate(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    public Plate(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
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
