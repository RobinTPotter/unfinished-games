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

    int opacity = 128;

    public int getOpacity() {
        return opacity;
    }

    public void setOpacity(int opacity) {
        if (opacity > 255) opacity = 255;
        if (opacity < 0) opacity = 0;
        this.opacity = opacity;
    }

    public void setBmp(Bitmap bmp) {
        this.bmp = bmp;
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


    public void updateBackgound() {

        setAlpha((float)(opacity)/255);
        //getBackground().setAlpha(opacity);  // 50% transparent
        Toast.makeText(getContext(),"Opacity "+opacity,Toast.LENGTH_SHORT).show();

    }
    public void draw(Canvas c) {


        super.draw(c);

        Paint p = new Paint();
        p.setColor(Color.BLUE);
        p.setStyle(Paint.Style.STROKE);
        p.setStrokeWidth(1.0f);

        Paint bp = new Paint();
        bp.setARGB(128, 255, 0, 0);

        if (bmp != null) {

            c.drawBitmap(bmp, new Rect(0, 0, bmp.getWidth(), bmp.getHeight()), new Rect(0, 0, getWidth(), getHeight()), null);

            c.drawText("Hello", 10, 10, p);
            c.drawText(String.valueOf(bmp.getWidth()) + "x" + String.valueOf(bmp.getHeight()), 10, 30, p);
            c.drawText(timeupdate, 10, 50, p);

        }

    }

}
