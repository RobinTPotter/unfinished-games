package com.robin.hiragana;

import android.app.Activity;
import android.content.res.Configuration;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

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

    String[] hiraganaList;

    static String SCORE_WRONG_KEY = "score_wrong";
    static String SCORE_CORRECT_KEY = "score_correct";

    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        hiraganaList = getString(R.string.hiragana).split(",");

        if (savedInstanceState != null) {
            score_wrong = savedInstanceState.getInt(SCORE_WRONG_KEY, 0);
            score_correct = savedInstanceState.getInt(SCORE_CORRECT_KEY, 0);
        }

        final Button buttonReset = (Button) findViewById(R.id.button_reset);
        buttonReset.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                score_correct = 0;
                score_wrong = 0;
                showScore();
            }
        });

        buttons = new Button[hiraganaList.length];

        for (int hh = 0; hh < hiraganaList.length; hh++) {
            String text = hiraganaList[hh];
            Button b = (Button) findViewById(getResources().getIdentifier("button_" + text, "id", getPackageName()));
            b.setText(text);
            final int _hh = hh;
            b.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    if (current_hiragana == _hh) score_correct++;
                    else score_wrong++;
                    showScore();
                    nextHiragana();
                }
            });
        }

        showScore();
        if (savedInstanceState == null) nextHiragana();

    }

    @Override
    public void onRestoreInstanceState(Bundle savedInstanceState) {

        score_correct = savedInstanceState.getInt(SCORE_CORRECT_KEY, 0);
        score_wrong = savedInstanceState.getInt(SCORE_WRONG_KEY, 0);
        showScore();

    }

    @Override
    public void onSaveInstanceState(Bundle outState) {

        outState.putInt(SCORE_CORRECT_KEY, score_correct);
        outState.putInt(SCORE_WRONG_KEY, score_wrong);

        super.onSaveInstanceState(outState);

    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);

    }

    /**
     * read the list of characters in the strings resource R.string.hiragana
     * get the imageview object off the layout and update the drawable.
     */
    private void nextHiragana() {

        final ImageView hiraganaImage = (ImageView) findViewById(R.id.imageHiragana);

        int next = 0;
        while (next == current_hiragana) {
            next = (int) Math.floor(Math.random() * hiraganaList.length);
        }

        current_hiragana = next;
        String letter = hiraganaList[current_hiragana];

        Drawable drawable = getResources().getDrawable(getResources()
                .getIdentifier("hiragana_" + letter, "drawable", getPackageName()));

        hiraganaImage.setImageDrawable(drawable);

    }

    /**
     * updates the score labels based on the internal numbers
     */
    private void showScore() {

        final TextView textCorrect = (TextView) findViewById(R.id.textCorrect);
        final TextView textWrong = (TextView) findViewById(R.id.textWrong);
        final TextView textPercent = (TextView) findViewById(R.id.textPercent);
        textCorrect.setText(String.valueOf(score_correct));
        textWrong.setText(String.valueOf(score_wrong));
        if ((score_wrong+score_correct) >0 )textPercent.setText(String.valueOf(Math.round(100*score_correct/(score_wrong+score_correct))) + " %");
        else textPercent.setText("0 %");

    }

}
