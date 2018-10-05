package com.robin.myapplication;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.graphics.Rect;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.view.Display;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.ScaleGestureDetector;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.InputStream;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener, ScaleGestureDetector.OnScaleGestureListener {

    private float mScaleFactor = 1.0f;
    private static final int MY_PERMISSIONS_REQUEST_READ_PICS = 0;
    private final int SELECT_PHOTO = 1;


    private int offsetx = 0;
    private int offsety = 0;


    private String currentPicture;
    private Bitmap bitmap;

    private boolean locked = false;
    ImageView pictureView;


    @Override
    protected void onCreate(Bundle savedInstanceState) {


        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        permissionCheck();

        final FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                locked = !locked;
                if (locked) {
                    Snackbar.make(view, "Locked", Snackbar.LENGTH_LONG)
                            .setAction("Action", null).show();
                    // fab.setBackgroundColor(getResources().getColor(R.color.boo, null));
                } else {
                    //  fab.setBackgroundColor(getResources().getColor(R.color.yay, null));
                }
            }
        });

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        pictureView = (ImageView) findViewById(R.id.pictureView);
        //if (getIntent().hasExtra("Picture")) {
        //    setPicture(getIntent().getStringExtra("Picture"));
       // }
        if (getIntent().hasExtra("Grid")) {
            gridDraw(getIntent().getStringExtra("Grid"));
        }

        final ScaleGestureDetector detector = new ScaleGestureDetector(this, this);

        pictureView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                detector.onTouchEvent(event);
                return true;
            }
        });


    }

    public void setPicture() {
        //currentPicture = imgstr;
        //bitmap = BitmapFactory.decodeFile(currentPicture);
        pictureView.setImageBitmap(bitmap);
        Toast.makeText(this, "set to " + bitmap.toString(), Toast.LENGTH_SHORT).show();
    }

    public void resetPicture() {
        pictureView.setImageBitmap(bitmap);
    }

    public void gridDraw() {
        gridDraw(2, 2);
    }

    public void gridDraw(String grid) {
        gridDraw(2, 2);
    }

    public void gridDraw(int c, int r) {
        Toast.makeText(this, "going to draw grid", Toast.LENGTH_SHORT).show();
        if (bitmap == null) {
            Toast.makeText(this, "bmp is null", Toast.LENGTH_SHORT).show();
            return;
        }

        // pictureView.setImageURI(Uri.fromFile(new File(currentPicture)));
        Bitmap griddedBitmap = Bitmap.createBitmap(bitmap);
        Canvas canvas = new Canvas(griddedBitmap);
        Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);

        paint.setColor(Color.BLACK);

        Toast.makeText(this, "set paints etc", Toast.LENGTH_SHORT).show();
        Display display = getWindowManager().getDefaultDisplay();
        Toast.makeText(this, "got display " + display.toString(), Toast.LENGTH_SHORT).show();
        Point size = new Point();
        display.getSize(size);
        int width = size.x / c;
        int height = size.y / r;

        Toast.makeText(this, "" + width + "," + height, Toast.LENGTH_SHORT).show();

        for (int cc = 0; cc < c; cc++) {
            for (int rr = 0; rr < r; rr++) {
                Rect rect = new Rect(offsetx + cc * width, offsety + rr * height, offsetx + (cc + 1) * width - 1, offsety + (rr + 1) * height - 1);

                Toast.makeText(this, "" + rect, Toast.LENGTH_SHORT).show();
                canvas.drawRect(rect, paint);
            }
        }

        pictureView.setImageBitmap(griddedBitmap);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.

        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        if (locked) return true;
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        } else if (id == R.id.action_grid_2x2) {
            gridDraw(2, 2);
            return true;
        } else if (id == R.id.action_grid_3x3) {
            gridDraw(3, 3);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_gallery) {
            Intent selectImageIntent = new Intent(Intent.ACTION_PICK);
            selectImageIntent.setType("image/*");
            Intent chooser = Intent.createChooser(selectImageIntent, "Choose Picture");
            startActivityForResult(chooser, SELECT_PHOTO);
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent imageReturnedIntent) {
        super.onActivityResult(requestCode, resultCode, imageReturnedIntent);

        switch (requestCode) {
            case SELECT_PHOTO:
                if (resultCode == RESULT_OK) {
                    try {
                        final Uri imageUri = imageReturnedIntent.getData();
                        final InputStream imageStream = getContentResolver().openInputStream(imageUri);
                        bitmap = BitmapFactory.decodeStream(imageStream);
                    //    pictureView.setImageBitmap(selectedImage);
                        setPicture();
                    } catch (FileNotFoundException e) {
                        e.printStackTrace();
                    }

                }
        }
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
            Toast.makeText(this, "permission granted", Toast.LENGTH_SHORT).show();
        }

    }

    @Override
    public boolean onScale(ScaleGestureDetector detector) {
        mScaleFactor *= detector.getScaleFactor();
        mScaleFactor = Math.max(0.1f,
                Math.min(mScaleFactor, 10.0f));
        pictureView.setScaleX(mScaleFactor);
        pictureView.setScaleY(mScaleFactor);

        return true;

    }

    @Override
    public boolean onScaleBegin(ScaleGestureDetector detector) {
        return true;
    }

    @Override
    public void onScaleEnd(ScaleGestureDetector detector) {
//return ;
    }

}
