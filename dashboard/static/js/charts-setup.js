function setupCharts(vulnerabilityData, hostData, softwareData) {
    // Setup Vulnerability Chart
    var ctxVulnerabilityChart = document.getElementById('vulnerabilityChart').getContext('2d');
    new Chart(ctxVulnerabilityChart, {
        type: 'pie',
        data: {
            labels: ['None', 'Low', 'Medium', 'High', 'Critical'],
            datasets: [{
                data: vulnerabilityData,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        }
    });

    // Setup Host Chart
    var ctxHostChart = document.getElementById('hostChart').getContext('2d');
    new Chart(ctxHostChart, {
        type: 'pie',
        data: {
            labels: hostData.labels,
            datasets: [{
                data: hostData.data,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        }
    });

    // Setup Software Chart
    var ctxSoftwareChart = document.getElementById('softwareChart').getContext('2d');
    new Chart(ctxSoftwareChart, {
        type: 'pie',
        data: {
            labels: softwareData.labels,
            datasets: [{
                data: softwareData.data,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        }
    });
}
