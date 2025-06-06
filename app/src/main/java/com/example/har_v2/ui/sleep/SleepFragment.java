package com.example.har_v2.ui.sleep;

import android.graphics.Color;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.har_v2.databinding.FragmentSleepBinding;
import com.example.har_v2.ui.sharedviewmodel.SharedViewModel;
import com.github.mikephil.charting.charts.LineChart;

import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter;
import com.github.mikephil.charting.formatter.ValueFormatter;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;


public class SleepFragment extends Fragment {

    private FragmentSleepBinding binding;

    private LineChart lineChart ;
    private SharedViewModel sharedViewModel;

    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        sharedViewModel = new ViewModelProvider(requireActivity()).get(SharedViewModel.class);

        binding = FragmentSleepBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        lineChart = binding.sleepLineChart;
        lineChart.setScaleEnabled(true);
        lineChart.setPinchZoom(true);
        lineChart.setDragDecelerationEnabled(true);
        lineChart.setDoubleTapToZoomEnabled(true);
        lineChart.getDescription().setEnabled(false);
        lineChart.getAxisRight().setDrawLabels(false);
        lineChart.setExtraLeftOffset(20f);
        lineChart.setExtraRightOffset(30f);
        XAxis xAxis = lineChart.getXAxis();
        xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
        xAxis.setLabelRotationAngle(45f);
        xAxis.setGranularity(1f);

        YAxis yAxis = lineChart.getAxisLeft();
        yAxis.setAxisMinimum(0f);
        yAxis.setAxisMaximum(15f);
        yAxis.setAxisLineWidth(2f);
        yAxis.setAxisLineColor(Color.BLACK);
        yAxis.setLabelCount(10);

        // Create a custom ValueFormatter to show custom labels (yValues) instead of float values
        ValueFormatter customValueFormatter = new ValueFormatter() {
            @Override
            public String getFormattedValue(float value) {
                // Map the index to the custom yLabel
                int hours = (int) value;
                int minutes = Math.round((value - hours) * 60);

                return String.format(Locale.US, "%02d:%02d", hours, minutes);
            }
        };

//        String[] days_test = {"01/23/2018", "01/24/2018", "01/25/2018", "01/26/2018"};
//        String[] data_test = {"10:18", "8:19", "4:12", "7:35"};

        List<String> xValues = new ArrayList<>();
        List<Entry> entries = new ArrayList<>();
        List<Integer> colors = new ArrayList<>();

        sharedViewModel.get_sleep_days().observe(getViewLifecycleOwner(), data -> {
            if (data != null && binding != null) {
                xValues.clear();
                xValues.addAll(Arrays.asList(data));
                xAxis.setValueFormatter(new IndexAxisValueFormatter(xValues));
                xAxis.setLabelCount(xValues.size(), true);

            }
        });

        sharedViewModel.get_sleep_values().observe(getViewLifecycleOwner(), data -> {
            if (data != null && binding != null) {
                colors.clear();
                entries.clear();
                for (int i = 0; i < data.length; i++){
                    float sleepInHours = timeStringToHours(data[i]);
                    if (sleepInHours >= 0) {
                        entries.add(new Entry(i, sleepInHours));
                        colors.add(getColor(sleepInHours));
                    }
                }
                LineDataSet dataSet = new LineDataSet(entries, "Sleep Trends (HH:MM)");
                dataSet.setColor(Color.BLUE);
                dataSet.setValueTextSize(16f);
                dataSet.setValueTextColor(Color.BLACK);
                dataSet.setCircleColors(colors);
                dataSet.setCircleRadius(10f);
                dataSet.setDrawCircleHole(false);
                dataSet.setDrawCircles(true);

                dataSet.setValueFormatter(customValueFormatter);
                LineData lineData = new LineData(dataSet);
                lineChart.setData(lineData);
                lineChart.fitScreen();
                lineChart.invalidate();
            }
        });

        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }


    public Float timeStringToHours(String timeString) {

        if (timeString == null || !timeString.contains(":")){
            return 0f;
        }

        String[] timeParts = timeString.split(":");
        if (timeParts.length < 2){
            return 0f;
        }

        try {
            // Parse the hours and minutes as integers
            int hours = Integer.parseInt(timeParts[0]);
            int minutes = Integer.parseInt(timeParts[1]);
            // Convert to total minutes
            return hours + minutes/60f;
        } catch (NumberFormatException e) {
            return 0f;
        }

    }

    public Integer getColor(Float sleep_time){
        if (sleep_time >= 8){
            return 0xFF99DD44;
        }
        else {
            return Color.RED;
        }
    }

}
