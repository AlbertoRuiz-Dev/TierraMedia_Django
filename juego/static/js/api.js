// Realiza una petición a la API para obtener el número de miembros por facción
fetch('/api/faction_member_count/')
    // Convierte la respuesta a formato JSON
    .then(response => response.json())
    .then(data => {
        // Extrae las etiquetas (nombres de facciones) y los conteos de miembros del JSON recibido
        const labels = data.map(faction => faction.name); // Array con los nombres de las facciones
        const memberCounts = data.map(faction => faction.member_count); // Array con el número de miembros por facción

        // Obtiene el contexto del canvas donde se renderizará el gráfico
        const ctx = document.getElementById('factionsChart').getContext('2d');

        // Crea una instancia de un gráfico de barras utilizando Chart.js
        const factionsChart = new Chart(ctx, {
            type: 'bar', // Tipo de gráfico: barra
            data: {
                labels: labels, // Etiquetas para el eje X (nombres de las facciones)
                datasets: [{
                    label: 'Miembros de cada Facción', // Etiqueta del conjunto de datos (aparece en la leyenda)
                    data: memberCounts, // Datos del eje Y (número de miembros por facción)

                    // Estilos de las barras
                    backgroundColor: 'rgba(255, 99, 132, 0.6)', // Color de fondo de las barras (rojo)
                    borderColor: 'rgba(255, 99, 132, 1)', // Color del borde de las barras (rojo)
                    borderWidth: 2, // Ancho del borde
                    borderRadius: 12, // Radio de las esquinas de las barras (bordes redondeados)
                    hoverBackgroundColor: 'rgba(255, 54, 54, 0.8)', // Color de fondo al pasar el mouse (rojo más oscuro)
                    barPercentage: 0.6, // Porcentaje de ancho de cada barra con respecto al espacio disponible
                    datalabels: {
                        color: 'rgba(255, 255, 255, 1)', // Color del texto de los datos
                        textStrokeColor: 'rgba(0, 0, 0, 1)', // Color del contorno (sombra) del texto
                        textStrokeWidth: 2 // Ancho del contorno del texto
                    }
                }]
            },
            options: {
                responsive: true, // Permite que el gráfico sea adaptable a diferentes tamaños de pantalla
                scales: {
                    y: {
                        beginAtZero: true, // El eje Y comienza desde cero
                        grid: {
                            color: 'rgba(255, 255, 255, 0.5)' // Color de las líneas de la cuadrícula del eje Y (blanco)
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 1)', // Color de las etiquetas del eje Y (blanco)
                            textStrokeColor: 'rgba(0, 0, 0, 1)', // Color del contorno (sombra) de las etiquetas del eje Y
                            textStrokeWidth: 2 // Ancho del contorno de las etiquetas del eje Y
                        }
                    },
                    x: {
                        grid: {
                            display: false // Oculta las líneas de la cuadrícula del eje X
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 1)', // Color de las etiquetas del eje X (blanco)
                            textStrokeColor: 'rgba(0, 0, 0, 1)', // Color del contorno (sombra) de las etiquetas del eje X
                            textStrokeWidth: 2 // Ancho del contorno de las etiquetas del eje X
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(255, 255, 255, 1)', // Color del texto de la leyenda (blanco)
                            font: {
                                size: 14 // Tamaño de fuente de la leyenda
                            },
                            textStrokeColor: 'rgba(0, 0, 0, 1)', // Color del contorno (sombra) del texto de la leyenda
                            textStrokeWidth: 2, // Ancho del contorno del texto de la leyenda
                            textShadowColor: 'rgba(0, 0, 0, 0.5)', // Color de la sombra del texto de la leyenda
                            textShadowBlur: 4 // Desenfoque de la sombra del texto de la leyenda
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)', // Color de fondo del tooltip (información emergente)
                        titleColor: 'rgba(255, 0, 0, 1)', // Color del título del tooltip (rojo)
                        bodyColor: 'rgba(255, 0, 0, 1)', // Color del cuerpo del tooltip (rojo)
                        borderColor: 'rgba(255, 0, 0, 1)', // Color del borde del tooltip (rojo)
                        borderWidth: 1 // Ancho del borde del tooltip
                    }
                },
                animation: {
                    duration: 800, // Duración de la animación en milisegundos
                    easing: 'easeOutBounce' // Función de aceleración de la animación (rebote al finalizar)
                }
            }
        });
    })
    // Captura y muestra en consola cualquier error que ocurra durante la petición o el proceso
    .catch(error => console.error('Error al obtener los datos:', error));
