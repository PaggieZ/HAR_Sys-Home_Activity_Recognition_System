package com.example.har_v2.ui.sharedviewmodel;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class SharedViewModel extends ViewModel {

    private final MutableLiveData<String> home_date = new MutableLiveData<>();
    private final MutableLiveData<String> home_sleep_status = new MutableLiveData<>();
    private final MutableLiveData<String> home_toilet_status = new MutableLiveData<>();
    private final MutableLiveData<String> home_uti_prediction = new MutableLiveData<>();
    private final MutableLiveData<String> home_battery_status = new MutableLiveData<>();

    private final MutableLiveData<String[]> sleep_days = new MutableLiveData<>();
    private final MutableLiveData<String[]> sleep_values = new MutableLiveData<>();

    private final MutableLiveData<String[]> toilet_days = new MutableLiveData<>();
    private final MutableLiveData<String[]> toilet_values = new MutableLiveData<>();

    private final MutableLiveData<String[]> batteries_percentages = new MutableLiveData<>();
    private final MutableLiveData<String[]> batteries_names = new MutableLiveData<>();




    // Getters

    public LiveData<String> get_home_date() {
        return home_date;
    }
    public LiveData<String> get_home_sleep_status() {
        return home_sleep_status;
    }
    public LiveData<String> get_home_toilet_status() {
        return home_toilet_status;
    }
    public LiveData<String> get_home_uti_prediction() {
        return home_uti_prediction;
    }
    public LiveData<String> get_home_battery_status() {
        return home_battery_status;
    }


    public LiveData<String[]> get_sleep_days() {
        return sleep_days;
    }
    public LiveData<String[]> get_sleep_values() {
        return sleep_values;
    }
    public LiveData<String[]> get_toilet_days() {
        return toilet_days;
    }
    public LiveData<String[]> get_toilet_values() {return toilet_values; }
    public LiveData<String[]> get_batteries_names() {
        return batteries_names;
    }
    public LiveData<String[]> get_batteries_percentages() {
        return batteries_percentages;
    }



    // Setters

    public void set_home_date(String data) { home_date.postValue(data);}
    public void set_home_sleep_status(String data) {
        home_sleep_status.postValue(data);
    }
    public void set_home_toilet_status(String data) {
        home_toilet_status.postValue(data);
    }
    public void set_home_uti_prediction(String data) {
        home_uti_prediction.postValue(data);
    }
    public void set_home_battery_status(String data) { home_battery_status.postValue(data); }

    public void set_sleep_days(String[] data) {
        sleep_days.postValue(data);
    }
    public void set_sleep_values(String[] data) {
        sleep_values.postValue(data);
    }
    public void set_toilet_days(String[] data) { toilet_days.postValue(data); }
    public void set_toilet_values(String[] data) {toilet_values.postValue(data); }
    public void set_batteries_names(String[] data) {
        batteries_names.postValue(data);
    }
    public void set_batteries_percentages(String[] data) {
        batteries_percentages.postValue(data);
    }


}