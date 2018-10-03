package com.robin.myapplication;


import android.content.Context;
import android.graphics.drawable.Drawable;
import android.os.Environment;
import android.os.storage.StorageManager;
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
         files = new File( Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_DCIM)
                , "Camera").listFiles();

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
            imageView.setLayoutParams(new ViewGroup.LayoutParams(85, 85));
            imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
            imageView.setPadding(8, 8, 8, 8);
        } else {
            imageView = (ImageView) convertView;
        }

        imageView.setImageDrawable(Drawable.createFromPath(files[position].getPath()));

        return imageView;
    }

        public String toString() {
            StringBuilder s=new StringBuilder();
            for ( File f : files)
                s.append(f.getName());
            return s.toString();
        }
    // references to our images

}