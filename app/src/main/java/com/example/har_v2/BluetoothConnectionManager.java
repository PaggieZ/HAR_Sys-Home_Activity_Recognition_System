package com.example.har_v2;


import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.os.Build;
import android.os.Handler;
import android.os.Message;

import androidx.annotation.Nullable;

import java.lang.ref.WeakReference;
import java.util.HashSet;
import java.util.Set;

public class BluetoothConnectionManager {
    private final WeakReference<Activity> activityWeakReference;
    private final Handler.Callback callback;

    @Nullable
    private final BluetoothAdapter bluetoothAdapter;
    @Nullable
    private ConnectThread connectThread;
    @Nullable
    private ConnectedThread connectedThread;

    public BluetoothConnectionManager(Activity activity, Handler.Callback _callback) {
        activityWeakReference = new WeakReference<>(activity);
        callback = _callback;

        bluetoothAdapter = getBluetoothAdapter(activity);
        BluetoothPermissionManager.requestBluetoothPermissionsIfNeeded(activity);
        BluetoothPermissionManager.enableBluetoothIfNeeded(activity, bluetoothAdapter);
    }

    public boolean isActivityAlive() {
        return activityWeakReference.get() != null;
    }

    public boolean isEnabled() {
        return isActivityAlive() && bluetoothAdapter != null && bluetoothAdapter.isEnabled();
    }

    public Set<BluetoothDevice> getPairedDevices() {
        Activity activity = activityWeakReference.get();

        if (activity == null || bluetoothAdapter == null) {
            return new HashSet<>();
        }

        if (!BluetoothPermissionManager.hasBluetoothPermissions(activity)) {
            BluetoothPermissionManager.requestBluetoothPermissionsIfNeeded(activity);
            return new HashSet<>();
        }

        BluetoothPermissionManager.enableBluetoothIfNeeded(activity, bluetoothAdapter);
        @SuppressWarnings("MissingPermission")
        Set<BluetoothDevice> pairedDevices = bluetoothAdapter.getBondedDevices();

        return pairedDevices;
    }

    public void connectToDevice(BluetoothDevice bluetoothDevice) {
        if (connectedThread != null && connectedThread.isAlive()) {
            connectedThread.cancel();
            connectedThread = null;
        }

        if (bluetoothAdapter == null) {
            return;
        }
        connectThread = new ConnectThread(bluetoothAdapter, bluetoothDevice, this::manageConnectedSocket);
        connectThread.start();
    }

    public void send(byte[] data) {
        if (connectedThread != null) {
            connectedThread.write(data);
        }
    }

    public void close() {
        if (connectThread != null) {
            connectThread.cancel();
            connectThread = null;
        }
        if (connectedThread != null) {
            connectedThread.cancel();
            connectedThread = null;
        }
    }

    private static BluetoothAdapter getBluetoothAdapter(Context context) {
        int version = Build.VERSION.SDK_INT;

        if (version >= 23) {
            BluetoothManager bluetoothManager = context.getSystemService(BluetoothManager.class);
            return bluetoothManager.getAdapter();
        } else if (version >= 18) {
            BluetoothManager bluetoothManager = (BluetoothManager) context.getSystemService(Context.BLUETOOTH_SERVICE);
            return bluetoothManager.getAdapter();
        }
        return BluetoothAdapter.getDefaultAdapter();
    }

    private void manageConnectedSocket(BluetoothSocket socket) {
        if (connectedThread != null && connectedThread.isAlive()) {
            connectedThread.cancel();
            connectedThread = null;
        }

        Activity activity = activityWeakReference.get();
        if (activity == null) {
            return;
        }
        Handler handler = new Handler(activity.getMainLooper(), callback);

        connectedThread = new ConnectedThread(socket, handler);
        connectedThread.start();
    }

    public void requestDataFromDevice(){
        if (connectedThread != null) {
            byte[] requestData = "GET_DATA".getBytes();
            connectedThread.write(requestData);
        }
    }
}
