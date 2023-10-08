document.addEventListener('DOMContentLoaded', function () {
     const ctx = document.getElementById('myChart');

    const timeStamps = window.myData.map(d => d.time_stamp.split(" ")[0]);

    const temperatureDataset = {
            label: 'Temperature',
            data: window.myData.map(d => d.temperature),
            fill: false,
            borderColor: 'red',
            tension: 0.1
            };

    const humidityDataset = {
            label: 'Humidity',
            data: window.myData.map(d => d.humidity),
            fill: false,
            borderColor: 'blue',
            tension: 0.1
            };

    const data = {
        labels: timeStamps,
        datasets: [temperatureDataset, humidityDataset],
    };

  const chart = new Chart(ctx, {
      type: 'line',
      data : data,
  });
});
