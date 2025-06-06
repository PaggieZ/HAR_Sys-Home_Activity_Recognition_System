package com.example.har_v2.ui.battery;

import android.graphics.drawable.ClipDrawable;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.LayerDrawable;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.core.content.res.ResourcesCompat;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;

import com.example.har_v2.R;
import com.example.har_v2.databinding.FragmentBatteryBinding;
import com.example.har_v2.ui.sharedviewmodel.SharedViewModel;


public class BatteryFragment extends Fragment {

    private FragmentBatteryBinding binding;

    private SharedViewModel sharedViewModel;

    private LinearLayout buttonContainer;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {


        sharedViewModel = new ViewModelProvider(requireActivity()).get(SharedViewModel.class);

        binding = FragmentBatteryBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        buttonContainer = root.findViewById(R.id.button_container);

        sharedViewModel.get_batteries_names().observe(getViewLifecycleOwner(), data -> {
            if (data != null && binding != null) {
                if (data.length > 0){
                    createButtons(data);
                }
            }
        });

        sharedViewModel.get_batteries_percentages().observe(getViewLifecycleOwner(), data -> {
            if (data != null && binding != null) {
                if (data.length > 0) {
                    addPercentages(data);
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

    private void createButtons(String[] sensorNames) {
        buttonContainer.removeAllViews();

        for (int i = 0; i < sensorNames.length; i++) {
            Button newButton = new Button(getContext());
            newButton.setText(sensorNames[i]);
            newButton.setId(i);
            LinearLayout.LayoutParams param = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT)
                    ;
            param.setMargins(0, 10, 0, 10);
            newButton.setLayoutParams(param);
            buttonContainer.addView(newButton);
        }
    }

    private void addPercentages(String[] batteryPercentages) {
        for (int i = 0; i < batteryPercentages.length; i++) {
            Button button = (Button) buttonContainer.getChildAt(i);
            if (button != null){
                button.append(" - " + batteryPercentages[i]);
                updateButtonFill(button, Integer.parseInt(batteryPercentages[i]));
            }
        }
    }

    private void updateButtonFill(Button button, int batteryPercentage){
        Drawable background = ResourcesCompat.getDrawable(getResources(), R.drawable.button_background, null);

        if (background instanceof LayerDrawable){
            LayerDrawable layerDrawable = (LayerDrawable) background;

            ClipDrawable clipDrawable = (ClipDrawable) layerDrawable.getDrawable(1);
            int level = batteryPercentage * 100;
            clipDrawable.setLevel(level);
        }

        button.setBackground(background);

    }
}