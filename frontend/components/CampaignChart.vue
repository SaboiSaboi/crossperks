<template>
  <div class="h-fit">
    <BarChart
      v-if="chartData"
      :chart-data="chartData"
      :chart-options="chartOptions"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { BarChart } from "vue-chart-3";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  BarController,
} from "chart.js";

// ✅ Register necessary Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  BarController
);

// ✅ Hardcoded engagement data (MVP)
const chartData = computed(() => ({
  labels: [
    "Day 1",
    "Day 2",
    "Day 3",
    "Day 4",
    "Day 5",
    "Day 6",
    "Day 7",
    "Day 8",
    "Day 9",
    "Day 10",
    "Day 11",
    "Day 12",
    "Day 13",
    "Day 14",
    "Day 15",
    "Day 16",
    "Day 17",
    "Day 18",
    "Day 19",
    "Day 20",
  ],
  datasets: [
    {
      label: "Redemptions",
      data: [3, 5, 8, 4, 6, 3, 5, 8, 4, 6, 20, 10, 2, 4, 15, 2, 1, 18, 12, 15], // Hardcoded engagement numbers
      backgroundColor: "#6366F1",
    },
  ],
}));

// ✅ Chart display options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: { beginAtZero: true },
  },
};
</script>
