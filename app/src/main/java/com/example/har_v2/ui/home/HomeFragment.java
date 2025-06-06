package com.example.har_v2.ui.home;

import android.app.DatePickerDialog;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.DatePicker;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.har_v2.R;
import com.example.har_v2.databinding.FragmentHomeBinding;
import com.example.har_v2.ui.sharedviewmodel.SharedViewModel;
import com.example.har_v2.R;

import java.util.Calendar;
import java.util.Locale;


public class HomeFragment extends Fragment {

    private FragmentHomeBinding binding;
    //    private BluetoothViewModel bluetoothViewModel;
    private SharedViewModel sharedViewModel;

    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
//        // Initialize the BluetoothViewModel
//        bluetoothViewModel = new ViewModelProvider(requireActivity()).get(BluetoothViewModel.class);

        // Initialize the SharedViewModel
        sharedViewModel = new ViewModelProvider(requireActivity()).get(SharedViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        // Observe the data from SharedViewModel
        // 1. Date Button
        sharedViewModel.get_home_date().observe(getViewLifecycleOwner(), data -> {
            if (data != null & binding != null) {
                binding.dateButton.setText(data);
            }
        });

        // 2. Sleep Button
        sharedViewModel.get_home_sleep_status().observe(getViewLifecycleOwner(), data -> {
            if (data != null && data.contains(":") && binding != null) {
                // TO DO: We receive sleep duration in format of HH:MM
                String[] time_parts = data.split(":");
                if (time_parts.length == 2) {
                    try {
                        int hours_int = Integer.parseInt(time_parts[0]);
                        if (hours_int >= 8) {
                            binding.sleepButton.setText(getString(R.string.home_today_sleep_duration_good, data));
                            binding.sleepButton.setBackgroundColor(0xFF99DD44);
                        } else if (data.equals("10:00")) {
                            binding.sleepButton.setText(R.string.home_unable_exact_sleep);
                        } else {
                            binding.sleepButton.setText(getString(R.string.home_today_sleep_duration_less, data));
                            binding.sleepButton.setBackgroundColor(Color.RED);
                        }
                    } catch (NumberFormatException e) {
                        binding.sleepButton.setText(R.string.home_sleep_format_error);
                    }

                }
            }

        });
        // 3.Toilet Button
        sharedViewModel.get_home_toilet_status().observe(getViewLifecycleOwner(), data -> {
            if (data != null && binding != null) {
                binding.toiletButton.setText(getString(R.string.home_toilet_total_count, data));
            }
        });
        // 4. UTI Prediction
        sharedViewModel.get_home_uti_prediction().observe(getViewLifecycleOwner(), data -> {
            if (data != null && binding != null) {
                binding.utiButton.setText(getString(R.string.home_health_update, data));
                if (data.equals("False")) {
                    binding.utiButton.setBackgroundColor(0xFF99DD44);
                } else if (data.equals("True")) {
                    binding.utiButton.setBackgroundColor(Color.RED);
                }
            }
        });
        // 5. Battery Button
        sharedViewModel.get_home_battery_status().observe(getViewLifecycleOwner(), data -> {
            if (data != null) {
                if (!data.equals("None") && binding != null) {
                    binding.batteryButton.setText(getString(R.string.home_some_batteries_low, data));
                    binding.batteryButton.setBackgroundColor(Color.RED);
                } else if (data.equals("None") && binding != null) {
                    binding.batteryButton.setText(R.string.home_battery_state_good);
                    binding.batteryButton.setBackgroundColor(0xFF99DD44);
                }
            }
        });

        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
