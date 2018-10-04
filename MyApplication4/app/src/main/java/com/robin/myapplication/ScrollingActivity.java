package com.robin.myapplication;

import android.Manifest;
import android.content.pm.PackageManager;
import android.database.DataSetObserver;
import android.os.Bundle;
import android.app.Activity;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.widget.NestedScrollView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.GridView;
import android.widget.ListAdapter;
import android.widget.Toast;

import java.io.File;

public class ScrollingActivity extends Activity {

    private static final int MY_PERMISSIONS_REQUEST_READ_PICS = 0;
    GridView gridview;
    File[] files;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_scrolling);
        gridview = (GridView) findViewById(R.id.grid_view);

        permissionCheck();

        ImageAdapter imad = new ImageAdapter(this);
        File cam = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_DCIM)
                , "Camera");

        files = cam.listFiles();
        imad.setFiles(files);

        Toast.makeText(ScrollingActivity.this, imad.toString(), Toast.LENGTH_SHORT).show();

        gridview.setAdapter(imad);
        //resizeGridView(files.length, 3);

        Toast.makeText(ScrollingActivity.this, "" + String.valueOf(gridview.getWidth())+" "+ String.valueOf(gridview.getHeight()), Toast.LENGTH_SHORT).show();

        gridview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View v,
                                    int position, long id) {
                Toast.makeText(ScrollingActivity.this, "" + files[position].getPath(),
                        Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void resizeGridView(int items, int columns) {
        ViewGroup.LayoutParams params = gridview.getLayoutParams();
        int oneRowHeight = gridview.getHeight();
        int rows = (int) (items / columns);
        params.height = oneRowHeight * rows;
        gridview.setLayoutParams(params);
        gridview.invalidate();
    }


    public void permissionCheck() {

        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.READ_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {

            // Permission is not granted
            // Should we show an explanation?
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.READ_CONTACTS)) {
                // Show an explanation to the user *asynchronously* -- don't block
                // this thread waiting for the user's response! After the user
                // sees the explanation, try again to request the permission.
            } else {
                // No explanation needed; request the permission
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, MY_PERMISSIONS_REQUEST_READ_PICS
                );

                // MY_PERMISSIONS_REQUEST_READ_CONTACTS is an
                // app-defined int constant. The callback method gets the
                // result of the request.
            }
        } else {
            Toast.makeText(ScrollingActivity.this, "permission granted", Toast.LENGTH_SHORT).show();
        }

    }
}
