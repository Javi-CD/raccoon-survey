/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

/* global Chart */
document.addEventListener('DOMContentLoaded', () => {
  const ctxBar = document.getElementById('barChart')?.getContext('2d');
  const ctxPie = document.getElementById('pieChart')?.getContext('2d');
  if (!ctxBar || !ctxPie || !window.Chart) {
    return;
  }

  const barChart = new Chart(ctxBar, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Respuestas',
          data: [],
          backgroundColor: '#1D4ED8',
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });

  const pieChart = new Chart(ctxPie, {
    type: 'pie',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Encuestas',
          data: [],
          backgroundColor: ['#2563EB', '#9CA3AF', '#F59E0B'],
        },
      ],
    },
    options: { responsive: true, plugins: { legend: { position: 'bottom' } } },
  });

  window.RSCharts = { barChart, pieChart };
});
