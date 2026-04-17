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

  const result = data.result === null ? "0-0" : data.result;
  let info = `
  <div id="tarjeta-detalle">
    <h3>${data.club}</h3>

    <div id="info-reserva">
      <div id="foto-club">
        <img src="${data.photo}" alt="Foto del club">
      </div>

      <div id="detalle-reserva">
        <div id="datos">
          <p><strong>Fecha: </strong>${data.date}</p>
          <p><strong>Resultado: </strong>${result}</p>
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

  document.getElementById("detalles-reserva").innerHTML += info;

  const confirmButton = document.getElementById("confirmarBoton");

  if (confirmButton) {
    confirmButton.addEventListener("click", () => {
      const id = window.location.pathname.split("/").pop();
      window.location.href = `/reserva/confirmar_resultado/${id}`;
    });
  }

  const token = localStorage.getItem("access_token");
  if (token) {
    const userId = JSON.parse(atob(token.split(".")[1])).sub;
    const isCreator = data.creator_id == userId;
    const isTeamBFirst = teamB.length > 0 && teamB[0].id == userId;

    console.log("RESULT:", data.result);
    console.log("STATUS:", data.status);
    console.log("USER:", userId);
    console.log("CREATOR:", data.creator_id);
    console.log("TEAM B:", teamB);

    if ((isCreator || isTeamBFirst) && data.status === "pending_result") {
      document.getElementById("confirmarBoton").style.display = "block";
    } else {
      document.getElementById("confirmarBoton").style.display = "none";
    }
  }

  const returnButton = document.getElementById("botonVolver");
  returnButton.addEventListener("click", () => {
    window.history.back();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadReservation();
});
