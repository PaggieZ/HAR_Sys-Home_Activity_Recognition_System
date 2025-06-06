package com.example.har_v2.ui.bluetooth;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class BluetoothViewModel extends ViewModel {


    private final MutableLiveData<String> receivedData = new MutableLiveData<>();


    public MutableLiveData<String> getReceivedData() {
        return receivedData;
    }

    public void setReceivedData(String data) {
        receivedData.postValue(data);
    }


}
