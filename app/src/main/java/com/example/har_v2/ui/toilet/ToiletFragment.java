package com.example.har_v2.ui.toilet;

import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.annotation.NonNull;

import com.example.har_v2.databinding.FragmentToiletBinding;
import com.example.har_v2.ui.sharedviewmodel.SharedViewModel;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ToiletFragment extends Fragment {

    private FragmentToiletBinding binding;
    private SharedViewModel sharedViewModel;

    private LineChart lineChart ;

    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        sharedViewModel = new ViewModelProvider(requireActivity()).get(SharedViewModel.class);

        binding = FragmentToiletBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        lineChart = binding.toiletLineChart;
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
        yAxis.setAxisMaximum(25f);
        yAxis.setAxisLineWidth(2f);
        yAxis.setAxisLineColor(Color.BLACK);
        yAxis.setLabelCount(10);


        List<String> xValues = new ArrayList<>();
        List<Entry> entries = new ArrayList<>();

        sharedViewModel.get_toilet_days().observe(getViewLifecycleOwner(), data -> {
            if (data != null && binding != null) {
                xValues.clear();
                xValues.addAll(Arrays.asList(data));
                xAxis.setValueFormatter(new IndexAxisValueFormatter(xValues));
                xAxis.setLabelCount(xValues.size(), true);

            }
        });

        sharedViewModel.get_toilet_values().observe(getViewLifecycleOwner(), data -> {
            if (data != null && binding != null) {
                entries.clear();
                for (int i = 0; i < data.length; i++){
                    float trip_count = timeStringToFloat(data[i]);
                    if (trip_count >= 0) {
                        entries.add(new Entry(i, trip_count));
                    }
                }
                LineDataSet dataSet = new LineDataSet(entries, "Sleep Trends (HH:MM)");
                dataSet.setColor(Color.BLUE);
                dataSet.setValueTextSize(16f);
                dataSet.setValueTextColor(Color.BLACK);
                dataSet.setCircleRadius(10f);
                dataSet.setColor(Color.BLUE);
                dataSet.setDrawCircleHole(false);
                dataSet.setDrawCircles(true);

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


    public Float timeStringToFloat(String timeString) {

        if (timeString == null){
            return 0f;
        }

        try {
            return Float.parseFloat(timeString.trim());
            // Convert to total minutes
        } catch (NumberFormatException e) {
            return 0f;
        }
    }

}