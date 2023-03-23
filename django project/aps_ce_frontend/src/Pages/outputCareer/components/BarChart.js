import React from "react";
import { Bar } from "react-chartjs-2";
import Chart from "chart.js/auto";

export const BarChart = ({ chartData }) => {
  const options = {
    responsive: true,
    maintainAspectRation: false,
    legend: {
      labels: {
        font: {
          size: 16,
        },
      },
    },
  };
  return (
    <div className="flex items-center justify-center w-full md:w-[600px] lg:w-[1200px] mx-auto px-4 py-8">
      <Bar data={chartData} options={options} />
    </div>
  );
};


