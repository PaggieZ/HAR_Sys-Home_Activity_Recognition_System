package com.example.har_v2.ui.bluetooth;

//import android.Manifest;
//import android.bluetooth.BluetoothDevice;
//import android.util.Log;
//import android.os.Bundle;
//import android.view.LayoutInflater;
//import android.view.View;
//import android.view.ViewGroup;
//import android.widget.TextView;
//import android.content.pm.PackageManager;
//import android.os.Build;
//import android.widget.Toast;
//
//import androidx.annotation.NonNull;
//import androidx.fragment.app.Fragment;
//import androidx.lifecycle.ViewModelProvider;
//import androidx.core.app.ActivityCompat;
//import androidx.core.content.ContextCompat;
//
//import com.example.har_v2.R;
//import com.example.har_v2.BluetoothConnectionManager;
//import com.example.har_v2.databinding.FragmentBluetoothBinding;
//import com.example.har_v2.ui.bluetooth.BluetoothViewModel;
//
//import java.nio.charset.StandardCharsets;
//import java.util.Map;
//import java.util.Objects;
//import java.util.Set;
//import java.util.stream.Collectors;
//
//
//public class BluetoothFragment extends Fragment {
//
//    private FragmentBluetoothBinding binding;
//
//    private BluetoothViewModel bluetoothViewModel;
//
//    private BluetoothConnectionManager bluetoothConnectionManager;
//
//    public View onCreateView(@NonNull LayoutInflater inflater,
//                             ViewGroup container, Bundle savedInstanceState) {
//        bluetoothViewModel =
//                new ViewModelProvider(this).get(BluetoothViewModel.class);
//
//        binding = FragmentBluetoothBinding.inflate(inflater, container, false);
//        View root = binding.getRoot();
//
////        final TextView textView = binding.textBluetoothFragment;
////        BluetoothViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);
//
//        bluetoothConnectionManager = new BluetoothConnectionManager(requireActivity(), this::handleMessage);
//
//        // Show Paired Devices button
//        binding.btnShowPaired.setOnClickListener(v -> showPairedDevices());
//
//        // Connect to a specific device
//        binding.btnConnect.setOnClickListener(v -> connectDevice());
//
//        // Send data over Bluetooth
//        binding.btnSend.setOnClickListener(v -> sendData());
//
//        return root;
//    }
//
//    @Override
//    public void onDestroyView() {
//        super.onDestroyView();
//        if (bluetoothConnectionManager != null) {
//            bluetoothConnectionManager.close();
//            bluetoothConnectionManager = null;
//        }
//        binding = null;
//    }
//
//
//    private void showPairedDevices() {
//        Set<BluetoothDevice> devices = bluetoothConnectionManager.getPairedDevices();
//        String pairedDevices = devices.stream().map(BluetoothDevice::getName).collect(Collectors.joining(", "));
//        Log.d("Bluetooth", "Paired Devices: " + pairedDevices);
//        binding.textBluetoothFragment.setText(getString(R.string.bt_paired_devices, pairedDevices));
//
//    }
//
//    private void connectDevice() {
//        // Check if permission is required for Android 12+ (API 31+)
//        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
//            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.BLUETOOTH_CONNECT)
//                    != PackageManager.PERMISSION_GRANTED) {
//
//                // Request BLUETOOTH_CONNECT permission for Android 12+
//                ActivityCompat.requestPermissions(requireActivity(),
//                        new String[]{Manifest.permission.BLUETOOTH_CONNECT}, 1);
//                return;  // Exit until permission is granted
//            }
//            // Check for Bluetooth Scan permission if you're scanning for devices
//            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.BLUETOOTH_SCAN)
//                    != PackageManager.PERMISSION_GRANTED) {
//
//                // Request BLUETOOTH_SCAN permission
//                ActivityCompat.requestPermissions(requireActivity(),
//                        new String[]{Manifest.permission.BLUETOOTH_SCAN}, 2);
//                return;  // Exit until permission is granted
//            }
//            // Check for ACCESS_FINE_LOCATION permission if you're scanning for devices
//            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION)
//                    != PackageManager.PERMISSION_GRANTED) {
//
//                // Request ACCESS_FINE_LOCATION permission
//                ActivityCompat.requestPermissions(requireActivity(),
//                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 3);
//                return;  // Exit until permission is granted
//            }
//        } else {
//            // For older versions, ensure BLUETOOTH permission is granted
//            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.BLUETOOTH)
//                    != PackageManager.PERMISSION_GRANTED) {
//
//                // Request Bluetooth permission for Android < 12
//                ActivityCompat.requestPermissions(requireActivity(),
//                        new String[]{Manifest.permission.BLUETOOTH}, 1);
//                return;
//            }
//        }
//
//        // If permission is granted, proceed with connecting
//        Set<BluetoothDevice> devices = bluetoothConnectionManager.getPairedDevices();
//        for (BluetoothDevice device : devices) {
//            if (Objects.equals(device.getName(), "Raspberry_pi")) {
//                bluetoothConnectionManager.connectToDevice(device);
//                binding.textBluetoothFragment.setText(getString(R.string.bt_connected_to, device.getName()));
//
//                // Request data from the connected device
//                bluetoothConnectionManager.requestDataFromDevice();
//            }
//        }
//    }
//
//    private void sendData() {
//        byte[] data = "Hello\n".getBytes();
//        bluetoothConnectionManager.send(data);
//        binding.textBluetoothFragment.setText(getString(R.string.bt_sent_data, "Hello"));
//    }
//
//    private boolean handleMessage(android.os.Message message) {
//        // handle received message
//        if (message.obj != null){
//            byte[] receivedData = (byte[])message.obj;
//            String dataString = new String(receivedData, StandardCharsets.UTF_8);
//            bluetoothViewModel.setReceivedData(dataString);
//        }
//        return true;
//    }
//
//
//}


import android.Manifest;
import android.app.DatePickerDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.util.Log;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.DatePicker;
import android.widget.TextView;
import android.content.pm.PackageManager;
import android.os.Build;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.example.har_v2.MainActivity;
import com.example.har_v2.R;
import com.example.har_v2.BluetoothConnectionManager;
import com.example.har_v2.databinding.FragmentBluetoothBinding;
import com.example.har_v2.ui.sharedviewmodel.SharedViewModel;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Locale;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;


public class BluetoothFragment extends Fragment {

    private FragmentBluetoothBinding binding;

    private BluetoothViewModel bluetoothViewModel;

    private SharedViewModel sharedViewModel;

    private BluetoothConnectionManager bluetoothConnectionManager;

    private BluetoothAdapter bluetoothAdapter;

    private ArrayAdapter<String> discoveredDevicesAdapter;

    private ArrayList<BluetoothDevice> discoveredDevicesList = new ArrayList<>();

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        bluetoothViewModel =
                new ViewModelProvider(this).get(BluetoothViewModel.class);

        binding = FragmentBluetoothBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        sharedViewModel = new ViewModelProvider(requireActivity()).get(SharedViewModel.class);

        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (bluetoothAdapter == null){
            Log.e("Bluetooth", "Bluetooth not supported on this device");
            Toast.makeText(getContext(), "Device does not support Bluetooth", Toast.LENGTH_LONG).show();
            binding.textBluetoothFragment.setText("Device does not support Bluetooth");
            return root;
        }
        discoveredDevicesAdapter = new ArrayAdapter<>(requireContext(), android.R.layout.simple_list_item_1);

        bluetoothConnectionManager = ((MainActivity) requireActivity()).getBluetoothConnectionManager();

        bluetoothViewModel.getReceivedData().observe(getViewLifecycleOwner(), data -> {
            binding.textBluetoothFragment.setText(data);
        });
        // Show Paired Devices button
        binding.btnShowPaired.setOnClickListener(v -> showPairedDevices());
        // Discover Devices button
//        binding.btnDiscover.setOnClickListener(v -> discoverDevices());
        // Connect to a specific device
        binding.btnConnect.setOnClickListener(v -> connectDevice());
        // Send data over Bluetooth
//        binding.btnSend.setOnClickListener(v -> sendData());
        // Get health data from Raspberrypi over Bluetooth
        binding.btnGetData.setOnClickListener(v -> getHealthData());

        // Set up the DatePicker
        binding.btnSelectDate.setOnClickListener(v -> {
            // Get the current date
            final Calendar calendar = Calendar.getInstance();
            int year = calendar.get(Calendar.YEAR);
            int month = calendar.get(Calendar.MONTH);
            int day = calendar.get(Calendar.DAY_OF_MONTH);

            DatePickerDialog datePickerDialog = new DatePickerDialog(getActivity(),
                    (DatePicker view, int selectedYear, int selectedMonth, int selectedDay) -> {
                        // Format date
//                        String selectedDate = (selectedMonth + 1) + "/" + selectedDay + "/" + selectedYear;
                        String selectedDate = String.format(Locale.US, "%d-%02d-%02d", selectedYear, selectedMonth+1, selectedDay);
                        // Update the button text and shared view model
                        binding.btnSelectDate.setText(selectedDate);
                        sharedViewModel.set_home_date(selectedDate);
                    }, year, month, day);

            Calendar minDate = Calendar.getInstance();
            minDate.set(2017, Calendar.SEPTEMBER, 1); // September 1, 2017
            Calendar maxDate = Calendar.getInstance();
            maxDate.set(2018, Calendar.SEPTEMBER, 1); // September 1, 2018

            datePickerDialog.getDatePicker().setMinDate(minDate.getTimeInMillis());
            datePickerDialog.getDatePicker().setMaxDate(maxDate.getTimeInMillis());

            datePickerDialog.show();
        });

        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();

        try {
            requireActivity().unregisterReceiver(deviceDiscoveryReceiver);
        }
        catch (IllegalArgumentException e) {
            Log.w("BluetoothFragment", "Receiver not registered", e);
        }
        binding = null;

    }

    private void showPairedDevices() {
        Set<BluetoothDevice> devices = bluetoothConnectionManager.getPairedDevices();
        if (devices.isEmpty()){
            binding.textBluetoothFragment.setText(R.string.bt_no_paired_devices);
        } else {
            String pairedDevices = devices.stream().map(BluetoothDevice::getName).collect(Collectors.joining(", "));
            Log.d("Bluetooth", "Paired Devices: " + pairedDevices);
            binding.textBluetoothFragment.setText(getString(R.string.bt_paired_devices, pairedDevices));
        }
    }

    private void connectDevice() {


        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.BLUETOOTH_CONNECT)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(requireActivity(),
                        new String[]{Manifest.permission.BLUETOOTH_CONNECT}, 1);
                return;
            }
        } else {
            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.BLUETOOTH_ADMIN)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(requireActivity(),
                        new String[]{Manifest.permission.BLUETOOTH_ADMIN}, 1);
                return;
            }
        }

        // If permission is granted, proceed with connecting
//        Set<BluetoothDevice> devices = bluetoothConnectionManager.getPairedDevices();
        Set<BluetoothDevice> devices = bluetoothAdapter.getBondedDevices();
        for (BluetoothDevice device : devices) {
            if (Objects.equals(device.getName(), "raspberrypi")) {
                bluetoothConnectionManager.connectToDevice(device);
                binding.textBluetoothFragment.setText(getString(R.string.bt_connected_to, device.getName()));

                // Request data from the connected device
                bluetoothConnectionManager.requestDataFromDevice();
                return;
            }
        }
        binding.textBluetoothFragment.setText("Device not paired. Please discover and pair first.");
    }

    private void sendData() {
        byte[] data = "Hello\n".getBytes();
        bluetoothConnectionManager.send(data);
        binding.textBluetoothFragment.setText(getString(R.string.bt_sent_data, "Hello"));
    }

    private boolean handleMessage(android.os.Message message) {
        // handle received message
        if (message.obj != null){
            byte[] receivedData = (byte[]) message.obj;
            String dataString = new String(receivedData, StandardCharsets.UTF_8);
            binding.textBluetoothFragment.setText(dataString);
            bluetoothViewModel.setReceivedData(dataString);

        }
        return true;
    }

    private void discoverDevices() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.BLUETOOTH_SCAN)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(requireActivity(),
                        new String[]{Manifest.permission.BLUETOOTH_SCAN}, 1);
                return;
            }
        }
        else {
            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(requireActivity(),
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
                return;
            }
        }

        if (bluetoothAdapter == null) {
            Log.e("Bluetooth", "Bluetooth not supported on this device");
            binding.textBluetoothFragment.setText("Bluetooth not supported on this device");
            return;
        }

        if (!bluetoothAdapter.isEnabled()) {
            binding.textBluetoothFragment.setText("Please enable Bluetooth first.");
            Toast.makeText(getContext(), "Please enable Bluetooth first.", Toast.LENGTH_LONG).show();
            return;
        }

        if (bluetoothAdapter.isDiscovering()) {
            bluetoothAdapter.cancelDiscovery();
        }

        binding.textBluetoothFragment.setText("Discovering devices...");
        if (discoveredDevicesAdapter == null) {
            discoveredDevicesAdapter = new ArrayAdapter<>(requireContext(), android.R.layout.simple_list_item_1);
        }
        discoveredDevicesAdapter.clear();
        discoveredDevicesList.clear();

        boolean success = bluetoothAdapter.startDiscovery();
        if (!success) {
            binding.textBluetoothFragment.setText("Failed to start discovery.");
            return;
        }
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        requireActivity().registerReceiver(deviceDiscoveryReceiver, filter);
    }

    private final BroadcastReceiver deviceDiscoveryReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if (device != null) {
                    discoveredDevicesList.add(device);
                    discoveredDevicesAdapter.add(device.getName() + " - " + device.getAddress());
                    discoveredDevicesAdapter.notifyDataSetChanged();
                }
                if ("raspberrypi".equals(device.getName())){

                    bluetoothAdapter.cancelDiscovery();

                    if (device.getBondState() == BluetoothDevice.BOND_NONE) {
                        binding.textBluetoothFragment.setText("Pairing with Raspberry Pi");
                        device.createBond();
                    }
                    else {
                        binding.textBluetoothFragment.setText("Raspberry Pi is already paired. \n Click 'Connect to Device'");
                    }
                }
            }

            else if (BluetoothDevice.ACTION_BOND_STATE_CHANGED.equals(action)) {
                int bondState = intent.getIntExtra(BluetoothDevice.EXTRA_BOND_STATE, BluetoothDevice.BOND_NONE);
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);

                if (device != null && "raspberrypi".equals(device.getName()) && bondState == BluetoothDevice.BOND_BONDED) {
                    binding.textBluetoothFragment.setText("Raspberry Pi paired successfully! Click 'Connect to Device'");
                }
                else if (bondState == BluetoothDevice.BOND_NONE) {
                    binding.textBluetoothFragment.setText("Pairing failed. Try again.");
                }
            }

        }
    };

    @Override
    public void onStart() {
        super.onStart();
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        filter.addAction(BluetoothDevice.ACTION_BOND_STATE_CHANGED);
        requireActivity().registerReceiver(deviceDiscoveryReceiver, filter);
    }

    @Override
    public void onStop() {
        super.onStop();
        try {
            requireActivity().unregisterReceiver(deviceDiscoveryReceiver);
        } catch (IllegalArgumentException e) {
            Log.w("Bluetooth", "Receiver already unregistered.");
        }
    }

    public void getHealthData() {
        if (sharedViewModel == null || sharedViewModel.get_home_date().getValue() == null) {
            binding.textBluetoothFragment.setText("No date selected. Please select a date first.");
            return;
        }

        String selectedDate = sharedViewModel.get_home_date().getValue();
        String dataToSend = "GET_DATA\n";
        byte[] data = dataToSend.getBytes();
        bluetoothConnectionManager.send(data);

        String dateToSend = selectedDate + "\n";
        byte[] byteDate = dateToSend.getBytes();
        bluetoothConnectionManager.send(byteDate);

        binding.textBluetoothFragment.setText(R.string.bt_retrieving_health_data);
        binding.textBluetoothFragment.append("for day: " + selectedDate);
    }

}