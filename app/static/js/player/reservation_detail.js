async function loadReservation() {
  const id = window.location.pathname.split("/").pop();

  const response = await fetch(`http://192.168.0.100:5000/api/player/reservas/${id}`, {
    headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
  });

  const data = await response.json();

  // Filtrar los jugadores por equipo
  const teamA = data.players.filter((p) => p.team === "a");
  const teamB = data.players.filter((p) => p.team === "b");

  const renderPlayers = (list) => {
    return list
      .map(
        (p) => `
      <div class="jugador">
        <img src="${p.photo}">
        <p>${p.name}</p>
      </div>
    `,
      )
      .join("");
  };

  let info = `
  <div id="tarjeta-detalle">
    <h3>"${data.club}"</h3>

    <div id="info-reserva">
      <div id="foto-club">
        <img src="${data.photo}" alt="Foto del club">
      </div>

      <div id="detalles-reserva">
        <div id="datos"> <!-- Corregido div="datos" por id="datos" -->
          <p><strong>Fecha:</strong></p>
          <p><strong>Resultado:</strong></p>
        </div>

        <div id="info">
          <p>${data.date}</p>
          <p>${data.result}</p>
        </div>

        <div id="equipos">
          <p><strong>Equipos:</strong></p>

          <div id="parejas">
            <div class="pareja">
              ${renderPlayers(teamA)}
            </div>

            <div class="pareja">
              ${renderPlayers(teamB)}
            </div>
          </div>
        </div>
      </div>

      <div id="botones">
        <button id="confirmarBoton">Confirmar resultado</button>
        <button id="botonVolver">Volver</button>
      </div>
    </div>
  </div>`;

  document.getElementById("detalles-reserva").innerHTML = info;

  const token = localStorage.getItem("access_token");
  if (token) {
    const userId = JSON.parse(atob(token.split(".")[1])).sub;
    const isCreator = data.creator_id == userId;
    const isTeamBFirst = equipoB.length > 0 && equipoB[0].id == userId;

    if (data.result === null && (isCreator || isTeamBFirst)) {
      document.getElementById("confirmarBoton").style.display = "block";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadReservation();
});
