package com.robin.myapplication;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.view.ScaleGestureDetector;
import android.view.View;
import android.widget.Toast;

public class PictureView extends View implements ScaleGestureDetector.OnScaleGestureListener {


    private int offsetx = 0;
    private int offsety = 0;

    private int bmpoffsetx = 0;
    private int bmpoffsety = 0;

    private String currentPicture;
    private Bitmap bitmap;

    private int colour = Color.BLACK;
    private float mScaleFactor = 1.0f;

    private int c = 0;
    private int r = 0;


    public PictureView(Context context) {
        super(context);
    }


    public void setBitmap(Bitmap bmp) {
        bitmap = bmp;
    }

    public void setColour(int col) {
        colour = col;
    }

    public void setRowsCols(int rt, int ct) {
        r = rt;
        c = ct;
    }

    public void onDraw(Canvas canvas) {
        //  super.onDraw(canvas);
        try {
            if (bitmap == null) {
                Paint p = new Paint();
                p.setStyle(Paint.Style.FILL);
                p.setColor(Color.RED);
                canvas.drawRect(new Rect(0, 0, getWidth(), getHeight()), p);
                return;
            } else if (!bitmap.isMutable()) {
                Paint p = new Paint();
                p.setStyle(Paint.Style.FILL);
                p.setColor(Color.GRAY);
                canvas.drawRect(new Rect(0, 0, getWidth(), getHeight()), p);
                return;
            }
            Rect src = new Rect(bmpoffsetx, bmpoffsety, bitmap.getWidth(), bitmap.getHeight());
            Rect dst = new Rect(0, 0, getWidth(), getHeight());

            canvas.drawBitmap(bitmap, src, dst, null);

            //Toast.makeText(this, "canvas is " + canvas.toString(), Toast.LENGTH_SHORT).show();

            Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
            paint.setStrokeWidth(1.0f);
            paint.setStyle(Paint.Style.STROKE);
            paint.setColor(colour);

            //Toast.makeText(this, "set paints etc", Toast.LENGTH_SHORT).show();

            int width = getWidth() / c;
            int height = getHeight() / r;
            if (width < height) height = width;
            else width = height;

            //Toast.makeText(this, "" + width + "," + height, Toast.LENGTH_SHORT).show();

            for (int cc = 0; cc < c; cc++) {
                for (int rr = 0; rr < r; rr++) {
                    Rect rect = new Rect(offsetx + cc * width, offsety + rr * height, offsetx + (cc + 1) * width - 1, offsety + (rr + 1) * height - 1);
                    //Toast.makeText(this, "" + rect, Toast.LENGTH_SHORT).show();
                    canvas.drawRect(rect, paint);
                }
            }

        } catch (Exception ex) {

            Toast.makeText(this.getContext(), ex.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public boolean onScale(ScaleGestureDetector detector) {
        return false;
    }

    @Override
    public boolean onScaleBegin(ScaleGestureDetector detector) {
        return false;
    }

    @Override
    public void onScaleEnd(ScaleGestureDetector detector) {

    }
}
