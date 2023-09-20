package com.example.talktales_groovy;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.ContextWrapper;
import android.content.pm.PackageManager;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.File;

public class MainActivity extends AppCompatActivity {

    private static int MICROPHONE_PERMISSION_CODE = 200;
    MediaRecorder mediaRecorder;
    ImageButton button;
    TextView textview;
    ScrollView scroll;
    boolean check = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (isMicrophonePresent())
            getMicrophonePermission();

        button = (ImageButton)findViewById(R.id.imagebuttonID);
        textview = (TextView)findViewById(R.id.textviewID);
        scroll = (ScrollView)findViewById((R.id.scrollID));

        if(!Python.isStarted())
            Python.start(new AndroidPlatform(this));
        Python py = Python.getInstance();
        final PyObject pyObj = py.getModule("script");

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if(!check) {
                    PyObject obj = pyObj.callAttr("main");
                    button.setImageResource(R.drawable.round_mic_off_24);
                    check = true;
                    try{
                        mediaRecorder = new MediaRecorder();
                        mediaRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                        mediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
                        mediaRecorder.setOutputFile(getRecordingFilePath());
                        mediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
                        mediaRecorder.prepare();
                        mediaRecorder.start();

                        Toast.makeText(getApplicationContext(), "Recording is started", Toast.LENGTH_SHORT).show();
                    }
                    catch (Exception e){
                        e.printStackTrace();
                    }
                    textview.setText(textview.getText() + obj.toString());
                }
                else{
                    button.setImageResource(R.drawable.round_mic_24);
                    check = false;
                    mediaRecorder.stop();
                    mediaRecorder.release();
                    mediaRecorder = null;
                    Toast.makeText(getApplicationContext(), "Recording is stopped", Toast.LENGTH_SHORT).show();
                    // textview.setText("");
                }
            }
        });

    }

    private boolean isMicrophonePresent(){
        return this.getPackageManager().hasSystemFeature(PackageManager.FEATURE_MICROPHONE);
    }

    private void getMicrophonePermission(){
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                == PackageManager.PERMISSION_DENIED) {
            ActivityCompat.requestPermissions(this, new String[]
                    {Manifest.permission.RECORD_AUDIO}, MICROPHONE_PERMISSION_CODE);
        }
    }

    @NonNull
    private String getRecordingFilePath(){
        ContextWrapper contextWrapper = new ContextWrapper(getApplicationContext());
        File musicDirectory = contextWrapper.getExternalFilesDir(Environment.DIRECTORY_MUSIC);
        File file = new File(musicDirectory, "testRecordingFile"+".mp3");
        return file.getPath();
    }


}