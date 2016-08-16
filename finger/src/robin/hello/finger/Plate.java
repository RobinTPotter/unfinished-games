package robin.hello.finger;

import android.content.Context;
import android.graphics.*;
import android.util.AttributeSet;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

import java.util.Date;
import java.util.Vector;

/**
 * Created by potterr on 11/08/2016.
 */

public class Plate extends SurfaceView implements Runnable {

    private static float RADIUS_LIMIT = 150;
    private static float RADIUS_LIMIT_MINIMUM = 30;
    private static long TICKS_PER_SECOND = 15;

    long startTime;
    int mx = -(int) RADIUS_LIMIT_MINIMUM;
    int my = -(int) RADIUS_LIMIT_MINIMUM;
    Vector<TimePoint> path = new Vector<>();
    int col = -1;
    float rad = RADIUS_LIMIT_MINIMUM;
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

    public void startPath(int mx, int my) {
        path = new Vector<>();
        path.add(new TimePoint(mx, my, (new Date()).getTime()));
    }

    public void addToPath(int mx, int my) {
        path.add(new TimePoint(mx, my, (new Date()).getTime()));
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
    }

    public void stop() {
        try {
            thread.join();
        } catch (Exception ex) {
        }
        thread = null;
        Log.i("TheFingerInform", "Stopped");
    }

    public void start() {

        init();
        thread = new Thread(this);
        thread.start();
        Log.i("TheFingerInform", "Started");
    }

    public void run() {
        Log.i("TheFingerInform", "EnterRun");
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

            long sleepTime = TICKS_PER_SECOND - (System.currentTimeMillis() - startTime);

            try {
                if (sleepTime > 0) thread.sleep(sleepTime);
                else thread.sleep(10);

            } catch (Exception e) {
                Log.e("myapp", "Thread.run(sleep)", e);
            }
        }

        Log.i("TheFingerInform", "ExitRun");

    }

    public float getRad() {
        return rad;
    }

    public void setRad(float rad) {
        if (rad > RADIUS_LIMIT) rad = RADIUS_LIMIT;
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

        if (c == null) return;

        super.onDraw(c);


        Paint b = new Paint();
        b.setColor(Color.BLACK);
        c.drawRect(new Rect(0, 0, getWidth(), getHeight()), b);

        //if (mx != -1 && my != -1 && col != -1) {

        Paint i = new Paint();
        i.setColor(Color.WHITE);

        Paint p = new Paint();
        p.setColor(col);

        long tm = (new Date()).getTime();
        // int yy = 40;
        try {
            if (path != null) {
                if (path.size() > 0) {
                    int pp = 0;
                    for (Point t : path) {
                        float scale_rad = ((rad) * (float) pp / path.size());
                        // c.drawText(t.x + " " + t.y+" "+scale_rad, 10, yy, i);
                        pp++;
                        // yy += 10;
                        c.drawCircle(t.x, t.y, scale_rad, p);
                    }

                    if (path.elementAt(0).getAge() > 500) path.remove(0);
                }

            }
        } catch (Exception ex) {

        }

        c.drawCircle(mx, my, rad, p);

        if (rad > RADIUS_LIMIT_MINIMUM) rad *= 0.97;
        c.drawText("Hi " + (int) (rad) + " " + path.size(), 30, 30, i);

        //}

    }

    class TimePoint extends Point {
        long timestamp;

        public TimePoint(int mx, int my, long tm) {
            super(mx, my);
            timestamp = tm;

        }

        public long getAge() {
            return (new Date()).getTime() - timestamp;
        }

    }
}
