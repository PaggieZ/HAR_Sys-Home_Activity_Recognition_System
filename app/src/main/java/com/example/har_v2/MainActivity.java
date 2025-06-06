package com.example.har_v2;

import android.os.Bundle;
import android.widget.Toast;

import com.example.har_v2.ui.sharedviewmodel.SharedViewModel;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.example.har_v2.databinding.ActivityMainBinding;

import java.nio.charset.StandardCharsets;


public class MainActivity extends AppCompatActivity {

    private ActivityMainBinding binding;

    private BluetoothConnectionManager bluetoothConnectionManager;

    private com.example.har_v2.ui.sharedviewmodel.SharedViewModel sharedViewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Inflate the layout and set the content view
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        BottomNavigationView navView = findViewById(R.id.nav_view);

        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_notifications,R.id.navigation_sleep, R.id.navigation_battery, R.id.navigation_toilet, R.id.navigation_bluetooth)
                .build();

        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_activity_main);

        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);

        bluetoothConnectionManager = new BluetoothConnectionManager(this, this::handleMessage);
        sharedViewModel = new ViewModelProvider(this).get(SharedViewModel.class);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (bluetoothConnectionManager != null) {
            bluetoothConnectionManager.close();
        }
    }

    public BluetoothConnectionManager getBluetoothConnectionManager(){
        return bluetoothConnectionManager;
    }


    private boolean handleMessage(android.os.Message message) {
        // handle received message
        if (message.obj != null){
            byte[] receivedData = (byte[]) message.obj;

            if (receivedData.length > 1024) {
                runOnUiThread(() -> Toast.makeText(getApplicationContext(), "Received data is too large", Toast.LENGTH_LONG).show());
                return true;
            }

            String dataString = new String(receivedData, StandardCharsets.UTF_8);
            runOnUiThread(() -> Toast.makeText(getApplicationContext(), dataString, Toast.LENGTH_LONG).show());

            if (dataString.isEmpty()){
                runOnUiThread(() -> Toast.makeText(getApplicationContext(), "Empty string", Toast.LENGTH_SHORT).show());
                return true;
            }

            if (dataString.startsWith("PI_SEND_START") && dataString.endsWith("PI_SEND_END\n")){
                String[] all_data = dataString.split("%");
                if (all_data.length < 2) {
                    runOnUiThread(() -> Toast.makeText(getApplicationContext(), "Invalid data format: Missing main data.", Toast.LENGTH_LONG).show());
                    return true;
                }

                String[] split_data = all_data[1].split("&");
                if (split_data.length < 4) {
                    runOnUiThread(() -> Toast.makeText(getApplicationContext(), "Invalid data format: Expected 4 sections but received" + split_data.length, Toast.LENGTH_LONG).show());
                    return true;
                }

                String[] home_data = split_data[0].split(";");
                if (home_data.length < 5){
                    runOnUiThread(() -> Toast.makeText(getApplicationContext(), "Invalid data format: Expected 5 sections for home_data but received" + split_data.length, Toast.LENGTH_LONG).show());
                    return true;
                }
                String[] sleep_data = split_data[1].split(";");
                String[] toilet_data = split_data[2].split(";");
                String[] battery_data = split_data[3].split(";");

                if (sleep_data.length < 2 || toilet_data.length < 2 || battery_data.length < 2){
                    runOnUiThread(() -> Toast.makeText(getApplicationContext(), "Sleep/Toilet/Battery data missing fields", Toast.LENGTH_LONG).show());
                    return true;
                }

                String home_date = home_data[0];
                String home_sleep_status = home_data[1];
                String home_toilet_status = home_data[2];
                String home_uti_prediction = home_data[3];
                String home_battery_status = home_data[4];

                String[] sleep_days = sleep_data[0].split(",");
                String[] sleep_values = sleep_data[1].split(",");

                String[] toilet_days = toilet_data[0].split(",");
                String[] toilet_values = toilet_data[1].split(",");

                String[] batteries_names = battery_data[0].split(",");
                String[] batteries_percentages = battery_data[1].split(",");

                sharedViewModel.set_home_date(home_date);
                sharedViewModel.set_home_sleep_status(home_sleep_status);
                sharedViewModel.set_home_toilet_status(home_toilet_status);
                sharedViewModel.set_home_uti_prediction(home_uti_prediction);
                sharedViewModel.set_home_battery_status(home_battery_status);

                sharedViewModel.set_sleep_days(sleep_days);
                sharedViewModel.set_sleep_values(sleep_values);
                sharedViewModel.set_toilet_days(toilet_days);
                sharedViewModel.set_toilet_values(toilet_values);

                sharedViewModel.set_batteries_percentages(batteries_percentages);
                sharedViewModel.set_batteries_names(batteries_names);
            }
        }
        return true;
    }

}
