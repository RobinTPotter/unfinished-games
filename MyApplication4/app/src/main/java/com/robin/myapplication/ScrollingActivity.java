package com.robin.myapplication;

import android.database.DataSetObserver;
import android.os.Bundle;
import android.app.Activity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.GridView;
import android.widget.ListAdapter;
import android.widget.Toast;

public class ScrollingActivity extends Activity {
GridView gridView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scrolling);
        GridView gridview = (GridView) findViewById(R.id.grid_view);
        Toast.makeText(ScrollingActivity.this, gridview.toString() , Toast.LENGTH_SHORT).show();
        ImageAdapter imad = new ImageAdapter(this);

        Toast.makeText(ScrollingActivity.this, imad.toString() ,          Toast.LENGTH_SHORT).show();
        gridview.setAdapter(imad);
        gridview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View v,
                                    int position, long id) {
                Toast.makeText(ScrollingActivity.this, "" + position,
                        Toast.LENGTH_SHORT).show();
            }
        });
    }
}
