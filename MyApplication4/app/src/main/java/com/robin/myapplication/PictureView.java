package com.robin.myapplication;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.view.ScaleGestureDetector;
import android.view.View;
import android.widget.Toast;

import java.util.jar.Attributes;

public class PictureView extends View implements ScaleGestureDetector.OnScaleGestureListener {


    private int offsetx = 0;
    private int offsety = 0;

    private int bmpoffsetx = 0;
    private int bmpoffsety = 0;
    private int bmpwidth = 0;
    private int bmpheight = 0;

    private String currentPicture;
    private Bitmap bitmap;

    private int colour = Color.BLACK;
    private float mScaleFactor = 1.0f;

    private int c = 0;
    private int r = 0;


    public PictureView(Context context) {
        super(context);

    }

    public PictureView(Context context, AttributeSet attr) {
        super(context, attr);

    }

    public void setBitmap(Bitmap bmp) {
        bitmap = bmp;
        bmpoffsetx = 0;
        bmpoffsety = 0;
        bmpwidth = bmp.getWidth();
        bmpheight = bmp.getHeight();
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
            Rect src = new Rect(bmpoffsetx, bmpoffsety, bmpwidth, bmpheight);

            double aspect_src = 1.0 * bmpwidth / bmpheight;
            double aspect_dest = 1.0 * getWidth() / getHeight();

            int destx = 0;
            int desty = 0;
            int destwidth = getWidth();
            int destheight = getHeight();

            if (aspect_src > aspect_dest) {
                //src wider, nudge down, calc height
                destheight = (int) (destwidth / aspect_src);
                desty = getHeight() / 2 - destheight / 2;

            } else {
                //dest wider, nudge across calc width
                destwidth = (int) (destheight / aspect_src);
                destx = getWidth() / 2 - destwidth / 2;
            }

            Rect dst = new Rect(destx, desty, destwidth, destheight);


            //make sure grid goes in the centre

            int smaller = getHeight();
            if (getWidth() < smaller) {
                smaller = getWidth();
                offsety = (getHeight() / 2) - (smaller / 2);
                offsetx = 0;
            } else {
                offsetx = (getWidth() / 2) - (smaller / 2);
                offsety = 0;
            }


            canvas.drawBitmap(bitmap, src, dst, null);

            //Toast.makeText(this, "canvas is " + canvas.toString(), Toast.LENGTH_SHORT).show();

            if (c > 0 & r > 0) {

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
            }

        } catch (Exception ex) {

            Toast.makeText(this.getContext(), ex.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public boolean onScale(ScaleGestureDetector detector) {
        float sf = detector.getScaleFactor();
        Toast.makeText(this.getContext(), "" + detector.getScaleFactor(), Toast.LENGTH_SHORT).show();
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
