// Obtener los datos de las facciones usando la API
fetch('/api/faction_member_count/')
    .then(response => response.json())
    .then(data => {
        // Configurar los datos del gráfico
        const labels = data.map(faction => faction.name);
        const memberCounts = data.map(faction => faction.member_count);

        const ctx = document.getElementById('factionsChart').getContext('2d');
        const factionsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Miembros de cada Facción',
                    data: memberCounts,
                    backgroundColor: 'rgba(99, 132, 255, 0.6)',
                    borderColor: 'rgba(99, 132, 255, 1)',
                    borderWidth: 2,
                    borderRadius: 12,
                    hoverBackgroundColor: 'rgba(54, 162, 235, 0.8)',
                    barPercentage: 0.6
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#ddd'
                        },
                        ticks: {
                            color: '#fff'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#fff'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff',
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        titleColor: '#333',
                        bodyColor: '#666',
                        borderColor: '#ddd',
                        borderWidth: 1
                    }
                },
                animation: {
                    duration: 800,
                    easing: 'easeOutBounce'
                }
            }
        });
    })
    .catch(error => console.error('Error al obtener los datos:', error));