package com.example.myappcam;

import android.app.ActionBar;
import android.content.Context;
import android.graphics.*;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.util.AttributeSet;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.util.Date;

/**
 * Created by potterr on 13/07/2016.
 */
public class OddButton extends View {

    Bitmap bmp;
    String timeupdate = "not set";
    Bitmap bck;

    public void setBmp(Bitmap bmp) {
        this.bmp = bmp;
        Toast.makeText(this.getContext(), "Set bitmap", Toast.LENGTH_SHORT).show();
        this.timeupdate = (new Date()).toString();
        invalidate();
    }

    public OddButton(Context context) {
        this(context, null);
    }

    public OddButton(Context context, AttributeSet attrs) {
        this(context, attrs, android.R.attr.buttonStyle);
    }

    public OddButton(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
    }

    public void draw(Canvas c) {
        super.draw(c);

        Paint p = new Paint();
        p.setColor(Color.BLUE);
        p.setStyle(Paint.Style.STROKE);
        p.setStrokeWidth(1.0f);

        Paint bp = new Paint();
        bp.setARGB(120, 20, 0, 0);


        c.drawRect(0, 0, getWidth() - 1, getHeight() - 1, p);
        c.drawRect(10, 10, getWidth() - 10, getHeight() - 10, p);

        if (bmp != null) {

            c.drawBitmap(bmp, new Rect(0, 0, bmp.getWidth(), bmp.getHeight()), new Rect(0, 0, getWidth(), getHeight()), bp);

            c.drawText("Hello", 10, 10, p);
            c.drawText(String.valueOf(bmp.getWidth()), 10, 30, p);
            c.drawText(String.valueOf(bmp.getHeight()), 10, 50, p);

        }

        c.drawText("Hello", 20, 20, p);
        c.drawText(timeupdate, 20, 40, p);

    }

}