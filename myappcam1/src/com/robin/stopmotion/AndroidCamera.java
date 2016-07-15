package com.robin.stopmotion;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.File;
import java.io.OutputStream;
import java.util.Date;
import java.util.List;
import android.net.*;
import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.graphics.*;
import android.hardware.Camera;
import android.os.Bundle;
import android.os.Environment;
import android.view.*;
import android.widget.*;
import android.view.ViewGroup.LayoutParams;
/// import android.R;

public class AndroidCamera extends Activity implements SurfaceHolder.Callback {

    private static String BUTTON_TOGGLE_STRETCH = "ToggleStretch";
    private static String CHANGE_OPACITY_INC = "Opacity+";
    private static String CHANGE_OPACITY_DEC = "Opacity-";

    Camera camera;
    SurfaceView surfaceView;
    SurfaceHolder surfaceHolder;
    boolean previewing = false;

    Bitmap lastPicture = null;
    Canvas canvas;

    File currentDirectory;

    Camera.Size previewSize = null;
    Camera.Size pictureSize = null;
    OddButton buttonTakePicture;

    boolean stretch = true;

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
        /// surfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);


        String x=(new Date()).toString();
        currentDirectory=getAlbumStorageDir("Stopmotion-"+x);

        controlInflater = LayoutInflater.from(getBaseContext());
        View viewControl = controlInflater.inflate(R.layout.control, null);
        LayoutParams layoutParamsControl
                = new LayoutParams(LayoutParams.MATCH_PARENT,/// FILL_PARENT,
                LayoutParams.MATCH_PARENT);/// FILL_PARENT);
        this.addContentView(viewControl, layoutParamsControl);

        buttonTakePicture = (OddButton) findViewById(R.id.takepicture);
        buttonTakePicture.setOnClickListener(new Button.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                /// TODO Auto-generated method stub

                camera.takePicture(myShutterCallback,
                        myPictureCallback_RAW, myPictureCallback_JPG);
            }
        });

    }

    Camera.ShutterCallback myShutterCallback = new Camera.ShutterCallback() {

        @Override
        public void onShutter() {
            /// TODO Auto-generated method stub
        }
    };

    Camera.PictureCallback myPictureCallback_RAW = new Camera.PictureCallback() {

        @Override
        public void onPictureTaken(byte[] arg0, Camera arg1) {
            /// TODO Auto-generated method stub
            //Toast.makeText(getBaseContext(),"Raw Picture "+arg0.length, Toast.LENGTH_SHORT).show();
        }
    };

    Camera.PictureCallback myPictureCallback_JPG = new Camera.PictureCallback() {

        @Override
        public void onPictureTaken(byte[] arg0, Camera arg1) {

            lastPicture = BitmapFactory.decodeByteArray(arg0, 0, arg0.length);

            Uri uriTarget =  android.net.Uri.fromFile(new File(currentDirectory,String.valueOf((new Date()).getTime())+".jpg"));

            OutputStream imageFileOS;
            try {
                imageFileOS = getContentResolver().openOutputStream(uriTarget);
                imageFileOS.write(arg0);
                imageFileOS.flush();
                imageFileOS.close();
                Toast.makeText(AndroidCamera.this,
                        "Image saved: " + uriTarget.toString(),
                        Toast.LENGTH_SHORT).show();

            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }


            buttonTakePicture.setBmp(lastPicture);
            camera.startPreview();
            previewing = true;
        }
    };



    public File getAlbumStorageDir(String albumName) {
        // Get the directory for the user's public pictures directory.
        File file = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES), albumName);
        if (!file.mkdirs()) {
        }
        return file;
    }



    public boolean onCreateOptionsMenu(Menu menu) {

        if (menu.findItem(12) == null || menu.findItem(23) == null) return createMenu(menu);
        else return true;

    }

    public boolean createMenu(Menu menu) {

        menu.clear();

        List<Camera.Size> previewSizes = camera.getParameters().getSupportedPreviewSizes();
        List<Camera.Size> pictureSizes = camera.getParameters().getSupportedPictureSizes();

        int order = 0;

        menu.add(2, Menu.NONE, order++, BUTTON_TOGGLE_STRETCH);
        menu.add(2, Menu.NONE, order++, CHANGE_OPACITY_DEC);
        menu.add(2, Menu.NONE, order++, CHANGE_OPACITY_INC);

        SubMenu sm1 = menu.addSubMenu(0, 12, order++, "Preview Size");

        for (Camera.Size size : previewSizes) {
            String text = String.valueOf(size.width) + "x" + String.valueOf(size.height);
            MenuItem mi = sm1.add(0, Menu.NONE, order++, text);
        }

        SubMenu sm2 = menu.addSubMenu(1, 23, order++, "Picture Size");
        sm2.setGroupCheckable(1, false, true);
        menu.setGroupCheckable(1, false, true);

        for (Camera.Size size : pictureSizes) {
            String text = String.valueOf(size.width) + "x" + String.valueOf(size.height);
            MenuItem mi = sm2.add(1, Menu.NONE, order++, text);
        }

        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        /// public boolean onGroupItemClick(MenuItem item) {

        if (camera != null) {

            if (previewing) camera.stopPreview();
        }

        boolean success = false;

        /// Handle item selection
        if (item.getGroupId() == 0) {
            /// preview
            List<Camera.Size> previewSizes = camera.getParameters().getSupportedPreviewSizes();

            for (Camera.Size size : previewSizes) {
                String text = String.valueOf(size.width) + "x" + String.valueOf(size.height);
                if (text.equals(item.getTitle())) {
                    Camera.Parameters params = camera.getParameters();
                    params.setPreviewSize(size.width, size.height);
                    camera.setParameters(params);
                    success = true;
                    previewSize = size;
                    setSize(size.width, size.height);
                }
            }

        } else if (item.getGroupId() == 1) {

            /// pict
            List<Camera.Size> pictureSizes = camera.getParameters().getSupportedPictureSizes();

            for (Camera.Size size : pictureSizes) {
                String text = String.valueOf(size.width) + "x" + String.valueOf(size.height);
                if (text.equals(item.getTitle())) {
                    Camera.Parameters params = camera.getParameters();
                    params.setPictureSize(size.width, size.height);
                    pictureSize = size;
                    camera.setParameters(params);
                    success = true;
                }
            }
        } else if (item.getGroupId() == 2) {
            if (item.getTitle().equals(BUTTON_TOGGLE_STRETCH)) {

                stretch = !stretch;
                setSize(previewSize.width, previewSize.height);

            } else if (item.getTitle().equals(CHANGE_OPACITY_DEC)) {

                buttonTakePicture.setOpacity(buttonTakePicture.getOpacity() - 24);
                buttonTakePicture.updateBackgound();

            } else if (item.getTitle().equals(CHANGE_OPACITY_INC)) {

                buttonTakePicture.setOpacity(buttonTakePicture.getOpacity() + 24);
                buttonTakePicture.updateBackgound();

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

        if (stretch || (width > measuredWidth && height > measuredHeight)) {

            if (asp > dev_asp) {
                /// wider, set width to device, change height
                width = measuredWidth;
                height = (int) ((float) measuredHeight / asp);

            } else if (asp < dev_asp) {
                /// narrower, set height to device, change width
                height = measuredHeight;
                width = (int) (asp * measuredHeight);
            } else {
                height = measuredHeight;
                width = measuredWidth;
            }

        } else {
            if (width > measuredWidth) {
                width = measuredWidth;
                height = (int) ((float) measuredHeight / asp);
            } else if (height > measuredHeight) {
                width = (int) (asp * measuredHeight);
                height = measuredHeight;

            }
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
                /// TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {

        camera = Camera.open();

    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {

        camera.stopPreview();
        camera.release();
        camera = null;
        previewing = false;
    }

}
