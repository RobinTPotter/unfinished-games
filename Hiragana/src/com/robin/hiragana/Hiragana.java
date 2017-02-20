package com.robin.hiragana;

import android.app.Activity;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.Random;

/**
 * main activity.
 */
public class Hiragana extends Activity {
    /**
     * Called when the activity is first created.
     */
    int score_correct = 0;
    int score_wrong = 0;
    int current_hiragana = 0;
    Button[] buttons;

    String[] hiraganaList = getString(R.string.hiragana).split(",");


    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        final Button buttonReset = (Button) findViewById(R.id.button_reset);
        buttonReset.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                score_correct = 0;
                score_wrong = 0;
                showScore();
            }
        });


        buttons= new Button[hiraganaList.length];
        int hh=0;
        for (Button b : buttons) {
            b.setText(hiraganaList[hh]);
            b.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    if (current_hiragana==hh) score_correct++;
                    else score_wrong++;
                    showScore();
                    nextHiragana();
                }
            });
        }

        nextHiragana();


    }

    /**
     * read the list of characters in the strings resource R.string.hiragana
     * get the imageview object off the layout and update the drawable.
     *
     */
    private void nextHiragana() {


        final ImageView hiraganaImage = (ImageView) findViewById(R.id.imageHiragana);

        int next = 0;
        while (next == current_hiragana) {
            next = (int) Math.floor(Math.random() * hiraganaList.length);
        }

        current_hiragana=next;
        String letter = hiraganaList[current_hiragana];

        Drawable drawable = getResources().getDrawable(getResources()
                .getIdentifier("hiragana_" + letter, "drawable", getPackageName()));

        hiraganaImage.setImageDrawable(drawable);

    }

    private void showScore() {

        final TextView textCorrect = (TextView) findViewById(R.id.textCorrect);
        final TextView textWrong = (TextView) findViewById(R.id.textWrong);
        textCorrect.setText(String.valueOf(score_correct));
        textWrong.setText(String.valueOf(score_wrong));
    }

}
