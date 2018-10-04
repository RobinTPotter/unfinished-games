package com.robin.myapplication;


import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.media.Image;
import android.os.Environment;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;

import java.io.File;

public class ImageAdapter extends BaseAdapter {
    private Context mContext;
    File[] files;
    public ImageAdapter(Context c) {
        mContext = c;

    }
public void setFiles(File[] files) {

   this.files = files;

}
    public int getCount() {
        return files.length;
    }

    public Object getItem(int position) {
        return null;
    }

    public long getItemId(int position) {
        return 0;
    }

    // create a new ImageView for each item referenced by the Adapter
    public View getView(int position, View convertView, ViewGroup parent) {
        ImageView imageView;
        if (convertView == null) {
            // if it's not recycled, initialize some attributes
            imageView = new ImageView(mContext);
            imageView.setLayoutParams(new ViewGroup.LayoutParams(256, 256));
            imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
            imageView.setPadding(8, 8, 8, 8);
        } else {
            imageView = (ImageView) convertView;
        }

        Drawable im = Drawable.createFromPath(files[position].getPath());

        Bitmap b = ((BitmapDrawable)im).getBitmap();
        Bitmap bitmapResized = Bitmap.createScaledBitmap(b, 256, 256, false);

        imageView.setImageDrawable(new BitmapDrawable(mContext.getResources() , bitmapResized));

        return imageView;
    }

        public String toString() {
         //   StringBuilder s=new StringBuilder();
         //   for ( File f : files)
          //      s.append(f.getName());
          //  return s.toString();
            return String.valueOf(files.length);
        }
    // references to our images

}