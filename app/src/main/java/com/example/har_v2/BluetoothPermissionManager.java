package com.example.har_v2;

import android.Manifest;
import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;

import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.ArrayList;
import java.util.List;

public class BluetoothPermissionManager {
    private static final int PERMISSION_REQUEST_CODE = 123;
    private static final int ENABLE_BT_REQUEST_CODE = 124;
    private static final String[] BLUETOOTH_PERMISSIONS;

    static {
        int version = Build.VERSION.SDK_INT;
        if (version >= 31) {
            BLUETOOTH_PERMISSIONS = new String[]{
                    Manifest.permission.BLUETOOTH_CONNECT,
                    Manifest.permission.BLUETOOTH_SCAN
            };
        } else {
            BLUETOOTH_PERMISSIONS = new String[]{};
        }
    }

    public static void requestBluetoothPermissionsIfNeeded(Activity activity) {
        String[] permissionsToRequest = getNotGrantedPermissions(activity);

        if (permissionsToRequest.length > 0) {
            ActivityCompat.requestPermissions(activity, permissionsToRequest, PERMISSION_REQUEST_CODE);
        }
    }

    public static boolean hasBluetoothPermissions(Context context) {
        for (String permission : BLUETOOTH_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    public static void enableBluetoothIfNeeded(Activity activity, @Nullable BluetoothAdapter bluetoothAdapter) {
        int version = Build.VERSION.SDK_INT;
        if (bluetoothAdapter != null && !bluetoothAdapter.isEnabled()) {
            if (version >= 31 && ActivityCompat.checkSelfPermission(activity, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                return;
            }

            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            activity.startActivityForResult(enableBtIntent, ENABLE_BT_REQUEST_CODE);
        }
    }

    private static String[] getNotGrantedPermissions(Context context) {
        List<String> notGrantedPermissions = new ArrayList<>();

        for (String permission : BLUETOOTH_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {
                notGrantedPermissions.add(permission);
            }
        }

        return notGrantedPermissions.toArray(new String[0]);
    }
}