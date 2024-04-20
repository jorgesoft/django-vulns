function setupCharts(vulnerabilityData, hostData, softwareData) {
    // Setup Vulnerability Chart
    var ctxVulnerabilityChart = document.getElementById('vulnerabilityChart').getContext('2d');
    new Chart(ctxVulnerabilityChart, {
        type: 'pie',
        data: {
            labels: ['None', 'Low', 'Medium', 'High', 'Critical'],
            datasets: [{
                data: vulnerabilityData,
                backgroundColor: ['#007bff', '#4bbf73', '#f0ad4e', '#fd7e14', '#d9534f']
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
                backgroundColor: ['#007bff', '#6610f2', '#6f42c1', '#4bbf73', '#20c997']
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
                backgroundColor: ['#007bff', '#6610f2', '#6f42c1', '#4bbf73', '#20c997']
            }]
        }
    });
}
