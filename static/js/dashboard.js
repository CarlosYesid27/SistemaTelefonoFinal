// Gráfica de torta por marca
const ctxMarca = document.getElementById('telefonosMarcaPieChart').getContext('2d');
const dataMarca = {
    labels: window.labels,
    datasets: [{
        data: window.data,
        backgroundColor: [
            '#3b82f6', '#06b6d4', '#6366f1', '#f87171', '#22d3ee', '#fbbf24', '#10b981', '#a78bfa'
        ],
        borderWidth: 2
    }]
};
const configMarca = {
    type: 'doughnut',
    data: dataMarca,
    options: {
        plugins: {
            legend: {
                display: true,
                position: 'bottom',
                labels: { font: { size: 16 } }
            }
        },
        cutout: '65%'
    }
};
new Chart(ctxMarca, configMarca);

// Gráfica de barras por mes
const ctxMes = document.getElementById('telefonosMesBarChart').getContext('2d');
const dataMes = {
    labels: window.meses,
    datasets: [{
        label: 'Teléfonos registrados',
        data: window.telefonos_por_mes,
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
        borderColor: '#2563eb',
        borderWidth: 2
    }]
};
const configMes = {
    type: 'bar',
    data: dataMes,
    options: {
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return ` ${context.parsed.y} teléfonos`;
                    }
                }
            },
            datalabels: {
                anchor: 'end',
                align: 'top',
                color: '#222',
                font: { weight: 'bold', size: 14 },
                formatter: function(value) {
                    return value;
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Mes',
                    font: { size: 16 }
                },
                ticks: { font: { size: 14 } }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Cantidad',
                    font: { size: 16 }
                },
                ticks: { stepSize: 1, font: { size: 14 } }
            }
        }
    }
};

function renderBarChart() {
    if (typeof ChartDataLabels !== 'undefined') {
        configMes.plugins = [ChartDataLabels];
    }
    new Chart(ctxMes, configMes);
}

if (typeof ChartDataLabels === 'undefined') {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js';
    script.onload = renderBarChart;
    document.head.appendChild(script);
} else {
    renderBarChart();
}