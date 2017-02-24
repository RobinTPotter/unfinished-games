package com.robin.hiragana;

import android.content.Context;
import android.widget.Button;

/**
 * Created by potterr on 24/02/2017.
 */
public class SmallButton extends Button {
    public SmallButton(Context context) {
        super(context);
    }

    @Override
    public int getMaxHeight() {
        return 8;
    }
    @Override
    public int getMaxWidth() {
        return 8;
    }
}
