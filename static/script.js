// Configurazione Grafico Chart.js
const ctx = document.getElementById('hrChart').getContext('2d');
const hrChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Array(60).fill(''), // Etichette vuote
        datasets: [{
            data: [],
            borderColor: '#0c0',
            borderWidth: 2,
            tension: 0.4, // Linea curva
            pointRadius: 0, // Niente pallini
            fill: false
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { display: false },
            y: { display: false, min: 40, max: 160 } // Nascondi asse Y per pulizia
        },
        animation: false // Disabilita animazione per effetto real-time
    }
});

function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('hr').innerText = data.hr + ' BPM';

            const stateEl = document.getElementById('state');                    
            stateEl.innerText = data.state;
            if (data.state === 'CRITICAL') {
                stateEl.classList.add('critical');
            } else {
                stateEl.classList.remove('critical');
            }
            
            document.getElementById('avg').innerText = data.hr_avg;
            document.getElementById('delta').innerText = data.delta_hr;
            document.getElementById('stress').innerText = data.stress;
            document.getElementById('ts').innerText = data.ts;
            document.getElementById('subject').innerText = data.subject;

            // Aggiorna il grafico
            if (data.history) {
                hrChart.data.datasets[0].data = data.history;
                hrChart.update();
            }
        });
}
setInterval(fetchData, 1000);