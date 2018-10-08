package com.robin.myapplication;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.widget.ImageView;
import android.widget.Toast;

@SuppressLint("AppCompatCustomView")
public class PictureGridView extends ImageView {



    private int offsetx = 0;
    private int offsety = 0;

    private int r=0;
    private int c=0;

    private Bitmap bitmap;

    private float mScaleFactor = 1.0f;

    Activity parentActivity;

    public PictureGridView(Context c){
        super(c);
    }

    public void setParentActivity(Activity a) {
        parentActivity=a;
    }


    public void setScaleFactor(float sf) {

        mScaleFactor=sf;
    }

    public void onDraw(Canvas canvasx) {

            Toast.makeText(parentActivity, "going to draw grid", Toast.LENGTH_SHORT).show();
            if (bitmap == null) {
                Toast.makeText(parentActivity, "bmp is null", Toast.LENGTH_SHORT).show();
                return;
            } else if (!bitmap.isMutable()) {
                Toast.makeText(parentActivity, "bmp is not mutable", Toast.LENGTH_SHORT).show();
                return;
            }

            // pictureView.setImageURI(Uri.fromFile(new File(currentPicture)));
            // Bitmap griddedBitmap = Bitmap.createBitmap(bitmap);
            Canvas canvas = new Canvas(bitmap);
            canvas.scale(mScaleFactor, mScaleFactor);

            Toast.makeText(parentActivity, "canvas is " + canvas.toString(), Toast.LENGTH_SHORT).show();

            Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
            paint.setStrokeWidth(0.5f);
            paint.setStyle(Paint.Style.STROKE);
            paint.setColor(Color.BLACK);

            Toast.makeText(parentActivity, "set paints etc", Toast.LENGTH_SHORT).show();

            int width = bitmap.getWidth();
            int height = bitmap.getHeight();

            Toast.makeText(parentActivity, "" + width + "," + height, Toast.LENGTH_SHORT).show();

            for (int cc = 0; cc < c; cc++) {
                for (int rr = 0; rr < r; rr++) {
                    Rect rect = new Rect(offsetx + cc * width, offsety + rr * height, offsetx + (cc + 1) * width - 1, offsety + (rr + 1) * height - 1);

                    Toast.makeText(parentActivity, "" + rect, Toast.LENGTH_SHORT).show();
                    canvas.drawRect(rect, paint);
                }
            }

            this.setImageBitmap(bitmap);
        super.onDraw(canvasx);

    }

    public void setRowsColumns(int r, int c) {
        this.r=r;
        this.c=c;
        invalidate();
    }

    public void setImageBitmap(Bitmap bitmap) {
        super.setImageBitmap(bitmap);
        this.bitmap=bitmap;
    }
}
