package robin.android.drawingstuff;

import android.content.Context;
import android.os.Handler;
import android.view.SurfaceHolder;

public class GameThread extends Thread {

		
		SurfaceHolder mSurfaceHolder;
		Context mContext;
		Handler mHandler;
		boolean mRun;
		private final Object mRunLock = new Object();
		

		int mCanvasWidth = 1;
		int mCanvasHeight = 1;
		
		public GameThread(SurfaceHolder surfaceHolder, Context context, Handler handler) {
			mSurfaceHolder = surfaceHolder;
			mHandler = handler;
			mContext = context;
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

				// don't forget to resize the background image
				// mBackgroundImage =
				// Bitmap.createScaledBitmap(mBackgroundImage, width, height,
				// true);
			}
		}
		
	
}
