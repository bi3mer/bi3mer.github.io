(function() {
  new Chart(document.getElementById('lc21chart-ns'), {
    type: 'bar',
    data: {
      labels: ['10', '100', '1000', '10000'],
      datasets: [
        { label: 'Solution 1: Manual head', data: [113.7, 1034.6, 10274.6, 101712.8], backgroundColor: 'rgba(75, 192, 192, 0.7)' },
        { label: 'Solution 2: Dummy node',  data: [111.6, 1037.6, 10508.8, 101812.2], backgroundColor: 'rgba(255, 99, 132, 0.7)' },
      ],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: {
        x: { title: { display: true, text: 'List size (nodes per list)' } },
        y: { title: { display: true, text: 'ns/op' } },
      },
    },
  });
})();
