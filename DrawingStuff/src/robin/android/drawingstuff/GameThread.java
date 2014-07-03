package robin.android.drawingstuff;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Handler;
import android.view.SurfaceHolder;

public class GameThread extends Thread {

	    private final static int    MAX_FPS = 20;   
	    private final static int    MAX_FRAME_SKIPS = 5;    
	    private final static int    FRAME_PERIOD = 1000 / MAX_FPS;

	     

	
		SurfaceHolder mSurfaceHolder;
		Context mContext;
		Handler mHandler;
		boolean mRun;
		private final Object mRunLock = new Object();
		

		int mCanvasWidth = 1;
		int mCanvasHeight = 1;
		
		Paint mLinePaint=new Paint();
		String message="";
		private long beginTime;
		private int framesSkipped;
		private int sleepTime;
		
		long timeLast=0;
		
		public GameThread(SurfaceHolder surfaceHolder, Context context, Handler handler) {
			mSurfaceHolder = surfaceHolder;
			mHandler = handler;
			mContext = context;			
			
			init();
		}	
		
		public void init() {
			mLinePaint.setColor(Color.GREEN);	
			
		}
		
		public void setRunning(boolean b) {
			// Do not allow mRun to be modified while any canvas operations
			// are potentially in-flight. See doDraw().
			synchronized (mRunLock) {
				mRun = b;
			}
		}

		/* Callback invoked when the surface dimensions change. */
		public void setSurfaceSize(int width, int height) {
			// synchronized to make sure these all change atomically
			synchronized (mSurfaceHolder) {
				mCanvasWidth = width;
				mCanvasHeight = height;
			}
		}

		public void run() {
			while (mRun) {
				Canvas c = null;
				try {
					c = mSurfaceHolder.lockCanvas(null);
					synchronized (mSurfaceHolder) {						
						// If mRun has been toggled false, inhibit canvas
						// operations.
						synchronized (mRunLock) {
							
							beginTime = System.currentTimeMillis();
		                    framesSkipped = 0;
		                    long timeDiff = System.currentTimeMillis() - beginTime;
		                    sleepTime = (int)(FRAME_PERIOD - timeDiff);
		                    if (sleepTime > 0) {
		                    	try {
		                    		Thread.sleep(sleepTime);
		                    	} catch (InterruptedException e) {}
		                    }
							
							if (mRun) doDraw(c);
							
							
						}
					}
				} finally {
					// do this in a finally so that if an exception is thrown
					// during the above, we don't leave the Surface in an
					// inconsistent state
					if (c != null) {
						mSurfaceHolder.unlockCanvasAndPost(c);
					}
				}
			}
		}
	

		private void doDraw(Canvas canvas) {			
			
			canvas.drawColor(Color.BLACK);
			message=String.valueOf(sleepTime);
			canvas.drawText(message, 25, 25, mLinePaint);

			// Draw the ship with its current rotation
			//canvas.save();

	
			//canvas.restore();
		}

		/**
		 * Figures the lander state (x, y, fuel, ...) based on the passage of
		 * realtime. Does not invalidate(). Called at the start of draw().
		 * Detects the end-of-game and sets the UI to the next state.
		 */
		private void updatePhysics() {
			long now = System.currentTimeMillis();
			
			
			//long now = System.currentTimeMillis();
			timeLast=now;
		}
		
		
}
