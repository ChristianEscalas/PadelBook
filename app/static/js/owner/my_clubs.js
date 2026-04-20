import { showNotification } from "../main.js";

async function loadClubs() {
  try {
    const response = await fetch("http://192.168.0.100:5000/api/owner/mis_clubes", {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada, vuelve a iniciar sesión.", "error");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      showNotification("Error al cargar los clubes", "error");
      return;
    }

    const data = await response.json();
    const divclubes = document.getElementById("tarjetas-clubes");

    divclubes.innerHTML = "";
    data.forEach((club) => {
      divclubes.innerHTML += `
      <div class="tarjetaClub">
        <h3>${club.club_name}</h3>
        <div class="infoClub">
        
          <div class="fotoclub">
            <img src="/static/${club.photo}" alt="Foto del club">
          </div>
          
          <div class="info">
            <p><strong>Dirección:</strong></p>
            <p><strong>Horario:</strong></p>
            <p><strong>Duración de los partidos:</strong></p>
            <p><strong>Municipio:</strong></p>
            <p><strong>Activo:</strong></p>
          </div>

          <div class="datos">
            <p>${club.address}</p>
            <p>${club.open_hour} - ${club.close_hour}</p>
            <p>${club.game_duration} minutos</p>
            <p>${club.municipality}</p>
            <p>${club.active}</p>
          </div>

          <div class="botones">
            <button type="button" class="pistasBoton" data-id="${club.id}">Pistas</button>
            <button type="button" class="editarclubBoton" data-id="${club.id}">Editar club</button>
            <button type="button" class="reservasBoton" data-id="${club.id}">Reservas</button>
          </div>
        </div>
      </div>`;
    });
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("click", async (event) => {
  if (event.target.classList.contains("pistasBoton")) {
    const clubId = event.target.dataset.id;
    window.location.href = `/pistas/club/${clubId}`;
  }

  if (event.target.classList.contains("editarclubBoton")) {
    const clubId = event.target.dataset.id;
    window.location.href = `/editar_club/${clubId}`;
  }

  if (event.target.classList.contains("reservasBoton")) {
    const clubId = event.target.dataset.id;
    window.location.href = `/reservas/club/${clubId}`;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  loadClubs();

  document.getElementById("crearClub").addEventListener("click", () => {
    window.location.href = "/crear_club";
  });
});
