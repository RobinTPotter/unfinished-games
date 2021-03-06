package robin.hello.finger;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;

public class TheFinger extends Activity implements View.OnTouchListener, GestureDetector.OnGestureListener {
    /**
     * Called when the activity is first created.
     */
    GestureDetector gd;
    Process process;
    Plate plate;

    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        process = launchLogcat();
        setContentView(R.layout.main);


    }

    @Override
    public void onResume() {
        super.onResume();

        plate = (Plate) findViewById(R.id.viewingPlate);
        plate.setOnTouchListener(this);
        gd = new GestureDetector(this, this);


        plate.start();

        Log.i("TheFingerInform","Resumed");
    }

    public void onPause() {
        super.onPause();
        plate.stop();
        Log.i("TheFingerInform","Paused");
    }

    @Override
    public boolean onDown(MotionEvent e) {
        plate.setM((int) (e.getX()), (int) (e.getY()));
        plate.setCol(Color.GREEN);
        plate.startPath((int) (e.getX()), (int) (e.getY()));
        // plate.invalidate();
        return true;
    }

    @Override
    public void onShowPress(MotionEvent e) {
        plate.setM((int) (e.getX()), (int) (e.getY()));
        plate.setCol(Color.BLUE);
        // plate.invalidate();

    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        plate.setM((int) (e.getX()), (int) (e.getY()));
        plate.setCol(Color.RED);
        // plate.invalidate();
        return true;
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {

        plate.setRad(plate.getRad() * 1.1f);
        plate.setM((int) (e2.getX()), (int) (e2.getY()));
        plate.addToPath((int) (e2.getX()), (int) (e2.getY()));

        if (Math.abs(distanceX) > Math.abs(distanceY)) plate.setCol(Color.YELLOW);
        else plate.setCol(Color.GRAY);

        return true;
    }

    @Override
    public void onLongPress(MotionEvent e) {
        plate.setRad(100);
        plate.setM((int) (e.getX()), (int) (e.getY()));
        plate.setCol(Color.MAGENTA);
        // plate.invalidate();
    }

    @Override
    public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {

        plate.setM((int) (e2.getX()), (int) (e2.getY()));
        plate.setCol(Color.CYAN);
        // plate.invalidate();
        return true;
    }

    private Process launchLogcat() {

        try {
            File filename = new File(Environment.getExternalStorageDirectory() + "/thefinger-logfile.log");
            filename.createNewFile();
            String cmd = "logcat -d -f " + filename.getAbsolutePath();
            return Runtime.getRuntime().exec(cmd);
        } catch (IOException e) {
            Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
            e.printStackTrace();
            return null;
        }
    }

    @Override
    public boolean onTouch(View v, MotionEvent event) {

        return gd.onTouchEvent(event);
    }
}
