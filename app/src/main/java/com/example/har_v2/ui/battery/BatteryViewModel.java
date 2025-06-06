package com.example.har_v2.ui.battery;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;
public class BatteryViewModel extends ViewModel{

    private final MutableLiveData<String> mText;
    // date


    public BatteryViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("Current Battery Percentages");
    }

    public LiveData<String> getText() {
        return mText;
    }
}


