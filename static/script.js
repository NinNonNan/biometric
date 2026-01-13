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
        });
}
setInterval(fetchData, 1000);