package robin.hello.finger;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Environment;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;

public class TheFinger extends Activity  {
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

        plate = (Plate) findViewById(R.id.viewingPlate);

       // plate.setOnTouchListener(this);


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
/*
    @Override
    public boolean onTouch(View v, MotionEvent event) {
        plate.setM((int) (event.getX()), (int)(event.getY()));
        plate.setCol(Color.CYAN);
        plate.invalidate();
        return true;
    }*/
}
