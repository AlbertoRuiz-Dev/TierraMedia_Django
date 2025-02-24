let characters = [];

fetch('/api/datos/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al obtener los datos');
        }
        return response.json();
    })
    .then(data => {
        characters = data;
        pelea();
    })
    .catch(error => console.error('Error:', error));

// Función que se ejecuta al pulsar el botón "Batalla!"
function pelea() {
    event.preventDefault();

    // Se obtienen los id de ambos personajes
    let id1 = document.querySelector("[name='character']").value;
    let id2 = document.querySelector("[name='character2']").value;

    // Se obtienen los personajes
    let personaje1 = characters.find(c => c.id == id1);
    let personaje2 = characters.find(c => c.id == id2);

    // Si alguno de los dos personajes no se encuentra mostramos un error
    if (!personaje1 || !personaje2) {
        console.log("Error: No se encontraron los personajes.");
        return;
    }

    // Obtenemos los datos de los personajes y si no tienen valores les ponemos uno
    let vida1 = 100;
    let vida2 = 100;

    let personaje1Stats = {
        nombre: personaje1.name,
        danio: personaje1.equipped_weapon ? personaje1.equipped_weapon.damage : 10,
        critico: personaje1.equipped_weapon ? personaje1.equipped_weapon.critic : 5,
        defensa: personaje1.equipped_armor ? personaje1.equipped_armor.defense : 0
    };

    let personaje2Stats = {
        nombre: personaje2.name,
        danio: personaje2.equipped_weapon ? personaje2.equipped_weapon.damage : 10,
        critico: personaje2.equipped_weapon ? personaje2.equipped_weapon.critic : 5,
        defensa: personaje2.equipped_armor ? personaje2.equipped_armor.defense : 0
    };

    // Asignamos el turno
    let turno = 1;

    // Mostrar la interfaz de la batalla
    document.getElementById("battle_arena").style.display = "block";
    document.getElementById("char1_name").textContent = personaje1Stats.nombre;
    document.getElementById("char2_name").textContent = personaje2Stats.nombre;

    document.getElementById("char1_hp").textContent = vida1;
    document.getElementById("char2_hp").textContent = vida2;

    // Función para atacar
    function atacar(jugador, tipo) {
        if ((jugador === 1 && turno !== 1) || (jugador === 2 && turno !== 2)) {
            console.log("No es tu turno!");
            return;
        }

        let atacante = jugador === 1 ? personaje1Stats : personaje2Stats;
        let defensor = jugador === 1 ? personaje2Stats : personaje1Stats;
        let hp_defensor = jugador === 1 ? vida2 : vida1;

        let base_danio = atacante.danio;
        let critico = atacante.critico;

        // Modificamos el danio según el tipo de ataque
        if (tipo === "debil") {
            base_danio = Math.floor(base_danio * 0.7);  // 30% menos danio
            critico *= 2;  // Doble de probabilidad de crítico
        }

        let es_critico = Math.random() * 100 < critico;
        let danio_total = es_critico ? base_danio * 2 : base_danio;

        // Restar defensa
        danio_total = Math.max(danio_total - defensor.defensa, 0);  // Evita danio negativo
        hp_defensor -= danio_total;

        // Actualizar HP en pantalla
        if (jugador === 1) {
            vida2 = hp_defensor;
            document.getElementById("char2_hp").textContent = vida2;
        } else {
            vida1 = hp_defensor;
            document.getElementById("char1_hp").textContent = vida1;
        }

        document.getElementById("status").textContent = `${atacante.nombre} atacó a ${defensor.nombre} con un ${tipo} causando ${danio_total} de danio ${es_critico ? "🔥 (CRÍTICO!)" : ""}`;

        // Verificar si el defensor perdió
        if (hp_defensor <= 0) {
            document.getElementById("status").textContent = `🏆 ${atacante.nombre} ha ganado la batalla!`;
            desactivarBotones();
            return;
        }

        // Cambiar turno y actualizar la UI
        turno = turno === 1 ? 2 : 1;
        actualizarTurno();
    }

    function actualizarTurno() {
        let botones1 = document.querySelectorAll("#char1_controls button");
        let botones2 = document.querySelectorAll("#char2_controls button");

        if (turno === 1) {
            botones1.forEach(btn => btn.disabled = false);
            botones2.forEach(btn => btn.disabled = true);
        } else {
            botones1.forEach(btn => btn.disabled = true);
            botones2.forEach(btn => btn.disabled = false);
        }
    }

    function desactivarBotones() {
        document.querySelectorAll("button").forEach(btn => btn.disabled = true);
    }

    // Asignar eventos a los botones de ataque
    document.getElementById("char1_fuerte").onclick = () => atacar(1, "fuerte");
    document.getElementById("char1_debil").onclick = () => atacar(1, "debil");
    document.getElementById("char2_fuerte").onclick = () => atacar(2, "fuerte");
    document.getElementById("char2_debil").onclick = () => atacar(2, "debil");

    actualizarTurno(); // Inicia la batalla con el primer turno
}