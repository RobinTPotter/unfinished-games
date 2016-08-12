package robin.hello.finger;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

/**
 * Created by potterr on 11/08/2016.
 */

public class Plate extends SurfaceView implements Runnable {

    long startTime;
    long ticksPerSecond = 15;
    int mx = -1;
    float rad = 10;
    int my = -1;
    int col = -1;
    SurfaceHolder surfaceHolder;
    Thread thread;

    public Plate(Context context) {
        super(context);
        init();
    }

    public Plate(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public Plate(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        init();
    }

    public void init() {

        surfaceHolder = getHolder();

        surfaceHolder.addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                Canvas canvas = surfaceHolder.lockCanvas(null);
                onDraw(canvas);
                surfaceHolder.unlockCanvasAndPost(canvas);
            }

            @Override
            public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

            }

            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {

            }
        });

        thread = new Thread(this);
        thread.start();

    }

    public void run() {
        while (thread != null) {

            Canvas c = null;
            startTime = System.currentTimeMillis();

            try {
                c = getHolder().lockCanvas();
                synchronized (getHolder()) {
                    onDraw(c);
                }
            } catch (Exception e) {
                Log.e("myapp", "Thread.run(ondraw)", e);
            } finally {
                if (c != null) {
                    getHolder().unlockCanvasAndPost(c);
                }
            }


            /*
            sleep
             */

            long sleepTime = ticksPerSecond - (System.currentTimeMillis() - startTime);

            try {
                if (sleepTime > 0) thread.sleep(sleepTime);
                else thread.sleep(10);

            } catch (Exception e) {
                Log.e("myapp", "Thread.run(sleep)", e);
            }
        }

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

    protected void onDraw(Canvas c) {
        super.onDraw(c);

        Paint b=new Paint();
        b.setColor(Color.BLACK);
        c.drawRect(new Rect(0,0,getWidth(),getHeight()),b);

        //if (mx != -1 && my != -1 && col != -1) {

        Paint p = new Paint();
        p.setColor(col);
        c.drawCircle(mx, my, rad, p);
        if (rad > 10) rad -= 0.1;

        Paint i = new Paint();
        i.setColor(Color.WHITE);
        c.drawText("Hi " + rad, 30, 30, i);

        //}

    }
}
