package robin.hello.finger;

import android.app.Activity;
import android.os.Bundle;
import android.os.Environment;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;

public class TheFinger extends Activity  implements View.OnTouchListener, GestureDetector.OnGestureListener {
    /**
     * Called when the activity is first created.
     *
     */
GestureDetector gd;
    Process process;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        process = launchLogcat();
        setContentView(R.layout.main);

        Plate plate=(Plate)findViewById(R.id.viewingPlate);

        plate.setOnTouchListener(this);

        gd=new GestureDetector(this,this);

    }

    @Override
    public boolean onDown(MotionEvent e) {
        Toast.makeText(this,"Down",Toast.LENGTH_SHORT).show();
        return true;
    }

    @Override
    public void onShowPress(MotionEvent e) {
        Toast.makeText(this,"ShowPress",Toast.LENGTH_SHORT).show();


    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        Toast.makeText(this,"SingleTapUp",Toast.LENGTH_SHORT).show();
        return true;
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {

        Toast.makeText(this,"Scroll " +distanceX+","+distanceY,Toast.LENGTH_SHORT).show();
        return true;
    }

    @Override
    public void onLongPress(MotionEvent e) {

        Toast.makeText(this,"LongPress",Toast.LENGTH_SHORT).show();
    }

    @Override
    public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {
        Toast.makeText(this,"Fling "+velocityX+","+velocityY,Toast.LENGTH_SHORT).show();
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
        Toast.makeText(this,"OnTouch",Toast.LENGTH_SHORT).show();
        return true;
    }
}
