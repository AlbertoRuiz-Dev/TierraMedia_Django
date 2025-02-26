document.addEventListener('DOMContentLoaded', function () {
    // Asegúrate de que los botones estén deshabilitados correctamente en función del turno
    toggleTurnButtons();

    // Función para realizar el ataque
    function realizarAtaque(ataque, attackerId) {
        // Realizar la solicitud AJAX al servidor
        fetch('/battle/attack/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // Si tienes CSRF activado
            },
            body: JSON.stringify({
                ataque: ataque,
                attacker: attackerId
            })
        })
        .then(response => response.json())  // Esperar respuesta en formato JSON
        .then(data => {
            console.log('Respuesta de la batalla:', data);
            // Si hay un error, lo mostramos en la consola
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                // Si la respuesta es exitosa, actualizamos la UI
                // Actualizar los puntos de vida de los personajes y la frase
                document.getElementById('char1_hp').textContent = data.char1_hp;
                document.getElementById('char2_hp').textContent = data.char2_hp;
                document.getElementById('comentario').innerText = data.frase;

                // Actualizar el turno del jugador
                if (data.turn_player === data.char1_id) {
                    // Si es el turno del jugador 1, habilitar sus botones de ataque
                    document.getElementById('char1_fuerte').disabled = false;
                    document.getElementById('char1_debil').disabled = false;
                    document.getElementById('char2_fuerte').disabled = true;
                    document.getElementById('char2_debil').disabled = true;
                } else {
                    // Si es el turno del jugador 2, habilitar sus botones de ataque
                    document.getElementById('char2_fuerte').disabled = false;
                    document.getElementById('char2_debil').disabled = false;
                    document.getElementById('char1_fuerte').disabled = true;
                    document.getElementById('char1_debil').disabled = true;
                }

                // Si se acabó el juego o algún personaje tiene 0 HP, mostrar mensaje de fin de juego
                if (data.char1_hp <= 0 || data.char2_hp <= 0) {
                    document.getElementById('comentario').innerText = data.winner;
                }
            }
        })
        .catch(error => console.error('Error al realizar el ataque:', error));
    }

    // Función para habilitar o deshabilitar los botones de acuerdo al turno
    function toggleTurnButtons() {
        const turnPlayer = document.getElementById('turn_player').value;

        // Deshabilitar los botones del jugador que no tiene el turno
        if (turnPlayer === document.getElementById('char1_id').value) {
            document.getElementById('char1_fuerte').disabled = false;
            document.getElementById('char1_debil').disabled = false;
            document.getElementById('char2_fuerte').disabled = true;
            document.getElementById('char2_debil').disabled = true;
        } else {
            document.getElementById('char2_fuerte').disabled = false;
            document.getElementById('char2_debil').disabled = false;
            document.getElementById('char1_fuerte').disabled = true;
            document.getElementById('char1_debil').disabled = true;
        }
    }

    // Asignar el evento para los botones de ataque
    document.getElementById('char1_fuerte').addEventListener('click', function () {
        realizarAtaque('fuerte', document.getElementById('char1_id').value);
    });
    document.getElementById('char1_debil').addEventListener('click', function () {
        realizarAtaque('debil', document.getElementById('char1_id').value);
    });

    document.getElementById('char2_fuerte').addEventListener('click', function () {
        realizarAtaque('fuerte', document.getElementById('char2_id').value);
    });
    document.getElementById('char2_debil').addEventListener('click', function () {
        realizarAtaque('debil', document.getElementById('char2_id').value);
    });
});