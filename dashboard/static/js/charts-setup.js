function setupCharts(vulnerabilityData, hostData, host_vulns_data) {
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
        },
        options: {
            plugins: {
              legend: {
                position: 'top',
                onClick: function(e, legendItem) {
                }
              },
              title: {
                display: true,
                text: 'Severity rating for all found vulnerabilities.'
              }
            }
          },
    });

    // Setup Host Chart
    var ctxHostChart = document.getElementById('hostChart').getContext('2d');
    new Chart(ctxHostChart, {
        type: 'doughnut',
        data: {
            labels: hostData.labels,
            datasets: [{
                data: hostData.data,
                backgroundColor: ['#007bff', '#6610f2', '#6f42c1', '#4bbf73', '#20c997']
            }]
        },
        options: {
            plugins: {
              legend: {
                position: 'right',
                onClick: function(e, legendItem) {
              }
              },
              title: {
                display: true,
                text: 'Count of hosts based on their OS.'
              }
            }
          },
    });

    // Setup Software Chart
    var ctxSoftwareChart = document.getElementById('hostVulnsChart').getContext('2d');
    new Chart(ctxSoftwareChart, {
        type: 'doughnut',
        data: {
            labels: host_vulns_data.labels,
            datasets: [{
                data: host_vulns_data.data,
                backgroundColor: ['#007bff', '#6610f2', '#6f42c1', '#4bbf73', '#20c997']
            }]
        },
        options: {
            plugins: {
              legend: {
                position: 'right',
                onClick: function(e, legendItem) {
                }
              },
              title: {
                display: true,
                text: 'Count of vulnerabilities found by host.'
              }
            }
          },
    });
}
