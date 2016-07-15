package com.robin.stopmotion;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

/**
 * Created by potterr on 20/01/2016.
 */
public class RobinView extends SurfaceView {
    private Bitmap bmp;
    private SurfaceHolder surfaceHolder;

    public void setBitmap(Bitmap bmp) {
        this.bmp=bmp;
    }

    public RobinView(Context c) {
        super(c);

        surfaceHolder=getHolder();

        surfaceHolder.addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                Canvas canvas=surfaceHolder.lockCanvas(null);
                onDraw(canvas);
                surfaceHolder.unlockCanvasAndPost(canvas);
            }

            @Override
            public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

            }

            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {

            }
        });
    }
    @Override
    protected void onDraw(Canvas canvas) {
        canvas.drawColor(Color.BLACK);
        canvas.drawBitmap(bmp, 10, 10, null);
    }
}
