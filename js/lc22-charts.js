(function() {
  new Chart(document.getElementById('lc22-inline-vs-external'), {
    type: 'bar',
    data: {
      labels: ['1', '5', '8', '10'],
      datasets: [
        { label: 'Inline closure', data: [37, 4613, 183869, 2936273], backgroundColor: 'rgba(75, 192, 192, 0.7)' },
        { label: 'External function', data: [38, 4827, 154946, 2472586], backgroundColor: 'rgba(255, 99, 132, 0.7)' },
      ],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: {
        x: { title: { display: true, text: 'n (pairs of parentheses)' } },
        y: { type: 'logarithmic', title: { display: true, text: 'ns/op (log scale)' } },
      },
    },
  });
})();
