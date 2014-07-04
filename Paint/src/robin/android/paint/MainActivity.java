package robin.android.paint;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.widget.Toast;

public class MainActivity extends Activity {
	// private ArrayList<Path> _graphics = new ArrayList<Path>();
	private Paint mPaint;
	private Bitmap bmp;
	private Context mContext;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		if (savedInstanceState != null) {
			bmp = savedInstanceState.getParcelable("drawing");
		}
		setContentView(new DrawingPanel(this));
		mPaint = new Paint();
		mPaint.setDither(true);
		mPaint.setColor(0xFFFFFF00);
		mPaint.setStyle(Paint.Style.FILL);
		// mPaint.setStrokeJoin(Paint.Join.ROUND);
		// mPaint.setStrokeCap(Paint.Cap.ROUND);
		// mPaint.setStrokeWidth(3);

	}

	public void onSaveInstanceState(android.os.Bundle outState) {
		super.onSaveInstanceState(outState);
		outState.putParcelable("drawing", bmp);
		if (mContext != null) Toast.makeText(mContext, "onsave", Toast.LENGTH_LONG).show();
	}

	public void onRestoreInstanceState(android.os.Bundle savedInstanceState) {
		super.onRestoreInstanceState(savedInstanceState);
		if (mContext != null)
			Toast.makeText(mContext, "onrestore", Toast.LENGTH_LONG).show();
		bmp = savedInstanceState.getParcelable("drawing");
	}

	class DrawingPanel extends SurfaceView implements SurfaceHolder.Callback {
		private DrawingThread _thread;

		/* private Path path; */

		public DrawingPanel(Context context) {
			super(context);
			mContext = context;
			getHolder().addCallback(this);
			Toast.makeText(mContext, "Hello", Toast.LENGTH_LONG).show();
			_thread = new DrawingThread(getHolder(), this);
		}

		public boolean onTouchEvent(MotionEvent event) {
			synchronized (_thread.getSurfaceHolder()) {
				if (event.getAction() == MotionEvent.ACTION_DOWN) {
					// path = new Path();
					// path.moveTo(event.getX(), event.getY());
					// path.lineTo(event.getX(), event.getY());
				} else if (event.getAction() == MotionEvent.ACTION_MOVE) {
					// path.lineTo(event.getX(), event.getY());
					Canvas c = new Canvas(bmp);
					c.drawCircle(event.getX(), event.getY(), 10, mPaint);
				} else if (event.getAction() == MotionEvent.ACTION_UP) {
					// path.lineTo(event.getX(), event.getY());
				}

				// _graphics.add(path);
				return true;
			}
		}

		@Override
		public void onDraw(Canvas canvas) {
			/*
			 * for (Path path : _graphics) { //canvas.drawPoint(graphic.x,
			 * graphic.y, mPaint); canvas.drawPath(path, mPaint); }
			 */
			canvas.drawBitmap(bmp, 0, 0, null);
		}

		public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
			// TODO Auto-generated method stub
			if (bmp == null)	bmp = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);

		}

		public void surfaceCreated(SurfaceHolder holder) {
			// TODO Auto-generated method stub
			_thread.setRunning(true);
			_thread.start();
		}

		public void surfaceDestroyed(SurfaceHolder holder) {
			// TODO Auto-generated method stub
			boolean retry = true;
			_thread.setRunning(false);
			while (retry) {
				try {
					_thread.join();
					retry = false;
				} catch (InterruptedException e) {
					// we will try it again and again...
				}
			}
		}
	}

	class DrawingThread extends Thread {
		private SurfaceHolder _surfaceHolder;
		private DrawingPanel _panel;
		private boolean _run = false;

		public DrawingThread(SurfaceHolder surfaceHolder, DrawingPanel panel) {
			_surfaceHolder = surfaceHolder;
			_panel = panel;
		}

		public void setRunning(boolean run) {
			_run = run;
		}

		public SurfaceHolder getSurfaceHolder() {
			return _surfaceHolder;
		}

		@SuppressLint("WrongCall")
		@Override
		public void run() {
			Canvas c;
			while (_run) {
				c = null;
				try {
					c = _surfaceHolder.lockCanvas(null);
					synchronized (_surfaceHolder) {
						_panel.onDraw(c);
					}
				} finally {
					// do this in a finally so that if an exception is thrown
					// during the above, we don't leave the Surface in an
					// inconsistent state
					if (c != null) {
						_surfaceHolder.unlockCanvasAndPost(c);
					}
				}
			}
		}
	}
}