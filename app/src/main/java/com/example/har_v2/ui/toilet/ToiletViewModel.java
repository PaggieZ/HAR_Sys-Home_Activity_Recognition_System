package com.example.har_v2.ui.toilet;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class ToiletViewModel extends ViewModel{

    private final MutableLiveData<String> mText;

    public ToiletViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("Toilet Usage Trends");
    }

    public LiveData<String> getText() {
        return mText;
    }
}
