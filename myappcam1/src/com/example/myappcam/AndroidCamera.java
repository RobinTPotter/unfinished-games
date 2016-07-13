package com.example.myappcam;

import java.io.IOException;
import java.util.List;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Context;
import android.content.pm.ActivityInfo;
import android.graphics.*;
import android.hardware.Camera;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.*;
import android.widget.*;
import android.view.ViewGroup.LayoutParams;
//import android.R;
import com.example.myappcam.R;
import android.hardware.Camera.Size;

public class AndroidCamera extends Activity implements SurfaceHolder.Callback {

    Camera camera;
    SurfaceView surfaceView;
    SurfaceHolder surfaceHolder;
    boolean previewing = false;

    Bitmap lastPicture = null;
    Canvas canvas;

    Camera.Size previewSize = null;
    Camera.Size pictureSize = null;
    OddButton buttonTakePicture;

    LayoutInflater controlInflater = null;

    String stringPath = "/sdcard/samplevideo.3gp";

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

        getWindow().setFormat(PixelFormat.UNKNOWN);
        surfaceView = (SurfaceView) findViewById(R.id.camerapreview);

        surfaceHolder = surfaceView.getHolder();
        surfaceHolder.addCallback(this);
        // surfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);

        controlInflater = LayoutInflater.from(getBaseContext());
        View viewControl = controlInflater.inflate(R.layout.control, null);
        LayoutParams layoutParamsControl
                = new LayoutParams(LayoutParams.MATCH_PARENT,// FILL_PARENT,
                LayoutParams.MATCH_PARENT);// FILL_PARENT);
        this.addContentView(viewControl, layoutParamsControl);

        buttonTakePicture = (OddButton) findViewById(R.id.takepicture);
        buttonTakePicture.setOnClickListener(new Button.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                // TODO Auto-generated method stub

                camera.takePicture(myShutterCallback,
                        myPictureCallback_RAW, myPictureCallback_JPG);
            }
        });



    }

    Camera.ShutterCallback myShutterCallback = new Camera.ShutterCallback() {

        @Override
        public void onShutter() {
            // TODO Auto-generated method stub

        }
    };

    Camera.PictureCallback myPictureCallback_RAW = new Camera.PictureCallback() {

        @Override
        public void onPictureTaken(byte[] arg0, Camera arg1) {
            // TODO Auto-generated method stub

        }
    };

    Camera.PictureCallback myPictureCallback_JPG = new Camera.PictureCallback() {

        @Override
        public void onPictureTaken(byte[] arg0, Camera arg1) {
            // TODO Auto-generated method stub

            Toast.makeText(getBaseContext(), "took picture bitmap", Toast.LENGTH_SHORT).show();

            Bitmap bmp
                    = BitmapFactory.decodeByteArray(arg0, 0, arg0.length);

            lastPicture = Bitmap.createBitmap(bmp, 0, 0, bmp.getWidth(), bmp.getHeight(), new Matrix(), true);

            buttonTakePicture.setBmp(lastPicture);
            // if (sv!=null  && lastPicture!=null)   sv.setBitmap(lastPicture);
            camera.startPreview();
            previewing = true;
        }
    };



    public boolean onCreateOptionsMenu(Menu menu) {

        if (menu.findItem(12) == null || menu.findItem(23) == null) return createMenu(menu);
        else return true;

    }

    public boolean createMenu(Menu menu) {

        menu.clear();

        List<Camera.Size> previewSizes = camera.getParameters().getSupportedPreviewSizes();
        List<Camera.Size> pictureSizes = camera.getParameters().getSupportedPictureSizes();

        int order = 0;

        SubMenu sm1 = menu.addSubMenu(0, 12, order++, "Preview Size");
       // sm1.setGroupCheckable(0, false, true);
      //  menu.setGroupCheckable(0, false, true);


        for (Camera.Size size : previewSizes) {

            //  Button btn = new Button(this);
            String text = String.valueOf(size.width) + "x" + String.valueOf(size.height);
            // btn.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
            MenuItem mi = sm1.add(0, Menu.NONE, order++, text);
       //     mi.setCheckable(true);

        }

        SubMenu sm2 = menu.addSubMenu(1, 23, order++, "Picture Size");
        sm2.setGroupCheckable(1, false, true);
        menu.setGroupCheckable(1, false, true);

        for (Camera.Size size : pictureSizes) {

            //Button btn = new Button(this);
            String text = String.valueOf(size.width) + "x" + String.valueOf(size.height);
            // btn.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
            MenuItem mi = sm2.add(1, Menu.NONE, order++, text);
       //     mi.setCheckable(true);


        }


        return true;
    }


    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        //public boolean onGroupItemClick(MenuItem item) {


        if (camera != null) {

            if (previewing) camera.stopPreview();
        }

        boolean success = false;

        // Handle item selection
        if (item.getGroupId() == 0) {
            //preview
            List<Camera.Size> previewSizes = camera.getParameters().getSupportedPreviewSizes();

            for (Camera.Size size : previewSizes) {
                String text = String.valueOf(size.width) + "x" + String.valueOf(size.height);
                if (text.equals(item.getTitle())) {
                    Camera.Parameters params = camera.getParameters();
                    params.setPreviewSize(size.width, size.height);
                    //  surfaceView.setLayoutParams(new FrameLayout.LayoutParams(size.width,size.height ));
                    camera.setParameters(params);
                    success = true;
                 //   item.setChecked(true);
                    //buttonTakePicture.setSize(size.width,size.height);
                    setSize(size.width,size.height);
                }


            }

        } else if (item.getGroupId() == 1) {
            //pict
            List<Camera.Size> pictureSizes = camera.getParameters().getSupportedPictureSizes();

            for (Camera.Size size : pictureSizes) {
                String text = String.valueOf(size.width) + "x" + String.valueOf(size.height);
                if (text.equals(item.getTitle())) {
                    Camera.Parameters params = camera.getParameters();
                    params.setPictureSize(size.width, size.height);
                    // surfaceView.setLayoutParams(new FrameLayout.LayoutParams(size.width,size.height ));
                    camera.setParameters(params);
                    success = true;
                 //   item.setChecked(true);
                }


            }


        }

        if (camera != null) {

            if (previewing) camera.startPreview();

        }

        return success;

    }




    public void setSize(int width, int height) {

        float asp = (float) width / height;

        int measuredHeight = surfaceView.getMeasuredHeight();
        int measuredWidth = surfaceView.getMeasuredWidth();

        float dev_asp = (float) measuredWidth / measuredHeight;

        if (height>measuredHeight) {

            width =(int) (asp * measuredHeight);
            height = measuredHeight;

        }else{


        }

        int l = (measuredWidth - width) / 2;
        int t = (measuredHeight - height) / 2;

        surfaceView.layout(l, t, l + width, t + height);
        surfaceView.invalidate();

        buttonTakePicture.layout(l, t, l + width, t + height);
        buttonTakePicture.invalidate();

    }



    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width,
                               int height) {
// TODO Auto-generated method stub
        if (previewing) {
            camera.stopPreview();
            previewing = false;
        }

        if (camera != null) {
            try {
                if (previewSize == null) previewSize = camera.getParameters().getPreviewSize();
                if (pictureSize == null) pictureSize = camera.getParameters().getPictureSize();
                camera.setPreviewDisplay(surfaceHolder);
                camera.startPreview();
                previewing = true;
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }


    @Override
    public void surfaceCreated(SurfaceHolder holder) {
// TODO Auto-generated method stub
        camera = Camera.open();


    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
// TODO Auto-generated method stub
        camera.stopPreview();
        camera.release();
        camera = null;
        previewing = false;
    }


}

