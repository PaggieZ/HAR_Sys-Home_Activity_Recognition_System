package com.example.har_v2;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.util.Log;

import java.io.IOException;
import java.util.UUID;

public class ConnectThread extends Thread {
    @FunctionalInterface
    public interface ConnectCallback {
        void manageConnectedSocket(BluetoothSocket socket);
    }

    private static final String TAG = ConnectThread.class.getSimpleName();

    private final BluetoothSocket mmSocket;
    private final BluetoothAdapter bluetoothAdapter;
    private final ConnectCallback connectCallback;

    public ConnectThread(BluetoothAdapter _bluetoothAdapter, BluetoothDevice device, ConnectCallback _connectCallback) throws SecurityException{
        bluetoothAdapter = _bluetoothAdapter;
        connectCallback = _connectCallback;

        // Use a temporary object that is later assigned to mmSocket
        // because mmSocket is final.
        BluetoothSocket tmp = null;
        UUID uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

        try {
            tmp = device.createRfcommSocketToServiceRecord(uuid);
        } catch (IOException e) {
            Log.e(TAG, "Socket's create() method failed", e);
        }
        mmSocket = tmp;
    }

    public void run() throws SecurityException {
        // Cancel discovery because it otherwise slows down the connection.
        bluetoothAdapter.cancelDiscovery();

        try {
            // Connect to the remote device through the socket. This call blocks
            // until it succeeds or throws an exception.
            mmSocket.connect();
        } catch (IOException connectException) {
            Log.e(TAG, connectException.toString());
            // Unable to connect; close the socket and return.
            try {
                mmSocket.close();
            } catch (IOException closeException) {
                Log.e(TAG, "Could not close the client socket", closeException);
            }
            return;
        }

        // The connection attempt succeeded. Perform work associated with
        // the connection in a separate thread.
        connectCallback.manageConnectedSocket(mmSocket);
    }

    // Closes the client socket and causes the thread to finish.
    public void cancel() throws SecurityException {
        try {
            mmSocket.close();
        } catch (IOException e) {
            Log.e(TAG, "Could not close the client socket", e);
        }
    }
}