async function loadReservation() {
  const id = window.location.pathname.split("/").pop();

  const response = await fetch(`/api/owner/reserva/${id}`, {
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
        <img src="/static/${p.photo}">
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
        <img src="/static/${data.photo}" alt="Foto del club">
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
              <p><strong>Equipo A:</strong></p>
              ${renderPlayers(teamA)}
            </div>

            <div class="pareja">
              <p><strong>Equipo B:</strong></p>
              ${renderPlayers(teamB)}
            </div>
          </div>
        </div>
      </div>

      <div id="botones">
        <button id="botonVolver">Volver</button>
      </div>
    </div>
  </div>`;

  document.getElementById("detalles-reserva").innerHTML += info;

  const returnButton = document.getElementById("botonVolver");
  returnButton.addEventListener("click", () => {
    window.history.back();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadReservation();
});
