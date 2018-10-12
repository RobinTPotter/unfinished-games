package com.robin.myapplication;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.ScaleGestureDetector;
import android.view.View;
import android.widget.Toast;

import java.util.jar.Attributes;

public class PictureView extends View {


    private int offsetx = 0;
    private int offsety = 0;

    private int bmpoffsetx = 0;
    private int bmpoffsety = 0;
    private int bmpwidth = 0;
    private int bmpheight = 0;

    private String currentPicture;
    private Bitmap bitmap;

    private int colour = Color.BLACK;

    private int c = 0;
    private int r = 0;

    private boolean stateLocked=false;

    public void setStateLocked(boolean l) {
        stateLocked=l;
    }

    private float mLastTouchX;
    private float mLastTouchY;
    private static final int INVALID_POINTER_ID = -1;
    private int mActivePointerId = INVALID_POINTER_ID;

    private float mPosX;
    private float mPosY;

    private ScaleGestureDetector mScaleDetector;
    private float mScaleFactor = 1.0f;
    private float mRotate = 0.0f;


    public PictureView(Context context) {
        super(context);
        mScaleDetector = new ScaleGestureDetector(context, new ScaleListener());


    }

    public PictureView(Context context, AttributeSet attr) {
        super(context, attr);
        mScaleDetector = new ScaleGestureDetector(context, new ScaleListener());


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

            boolean matrixStyle = true;

            if (!matrixStyle) {

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
                    destwidth = (int) (destheight * aspect_src);
                    destx = getWidth() / 2 - destwidth / 2;
                }

                Rect dst = new Rect(destx + (int) mPosX, desty + (int) mPosY, destwidth + destx + (int) mPosX, destheight + desty + (int) mPosY);

                canvas.drawBitmap(bitmap, src, dst, null);

            } else {
                Matrix matrix = new Matrix();
                matrix.reset();
                matrix.setTranslate(mPosX, mPosY);
                matrix.setScale(mScaleFactor, mScaleFactor);
                matrix.setRotate(mRotate);
                canvas.drawBitmap(bitmap, matrix, null);
            }
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

                canvas.drawText(""+mScaleFactor+" "+mRotate+" "+mPosX +","+mPosY,0,getHeight()-20,paint);

            }

        } catch (Exception ex) {

            Toast.makeText(this.getContext(), ex.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }


    @Override
    public boolean onTouchEvent(MotionEvent ev) {

        if (stateLocked) return true;

        // Let the ScaleGestureDetector inspect all events.


        mScaleDetector.onTouchEvent(ev);


        final int action = ev.getAction();
        switch (action & MotionEvent.ACTION_MASK) {
            case MotionEvent.ACTION_DOWN: {
                final float x = ev.getX();
                final float y = ev.getY();

                mLastTouchX = x;
                mLastTouchY = y;
                mActivePointerId = ev.getPointerId(0);
                break;
            }

            case MotionEvent.ACTION_MOVE: {
                final int pointerIndex = ev.findPointerIndex(mActivePointerId);
                final float x = ev.getX(pointerIndex);
                final float y = ev.getY(pointerIndex);

                // Only move if the ScaleGestureDetector isn't processing a gesture.
                if (!mScaleDetector.isInProgress()) {
                    final float dx = x - mLastTouchX;
                    final float dy = y - mLastTouchY;

                    mPosX += dx;
                    mPosY += dy;

                    invalidate();
                }

                mLastTouchX = x;
                mLastTouchY = y;

                break;
            }

            case MotionEvent.ACTION_UP: {
                mActivePointerId = INVALID_POINTER_ID;
                break;
            }

            case MotionEvent.ACTION_CANCEL: {
                mActivePointerId = INVALID_POINTER_ID;
                break;
            }

            case MotionEvent.ACTION_POINTER_UP: {
                final int pointerIndex = (ev.getAction() & MotionEvent.ACTION_POINTER_INDEX_MASK)
                        >> MotionEvent.ACTION_POINTER_INDEX_SHIFT;
                final int pointerId = ev.getPointerId(pointerIndex);
                if (pointerId == mActivePointerId) {
                    // This was our active pointer going up. Choose a new
                    // active pointer and adjust accordingly.
                    final int newPointerIndex = pointerIndex == 0 ? 1 : 0;
                    mLastTouchX = ev.getX(newPointerIndex);
                    mLastTouchY = ev.getY(newPointerIndex);
                    mActivePointerId = ev.getPointerId(newPointerIndex);
                }
                break;
            }
        }

        Toast.makeText(this.getContext(), ""+mPosX+","+mPosY, Toast.LENGTH_SHORT).show();

        return true;
    }


    private class ScaleListener extends ScaleGestureDetector.SimpleOnScaleGestureListener {
        @Override
        public boolean onScale(ScaleGestureDetector detector) {
            mScaleFactor *= detector.getScaleFactor();

            // Don't let the object get too small or too large.
            mScaleFactor = Math.max(0.1f, Math.min(mScaleFactor, 10.0f));
            //   Toast.makeText(PictureView.this.getContext(), "" + detector.getScaleFactor(), Toast.LENGTH_SHORT).show();

            invalidate();
            return true;
        }
    }

}
