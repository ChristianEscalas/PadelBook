import { loadCovert, loadMunicipalities, loadSurface, loadType, loadWall } from "./main.js";
import { showNotification } from "../main.js";

// filtrar clubes disponibles
async function sendForm(form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const searchParams = new URLSearchParams(formData);

    try {
      const response = await fetch(`/api/player/reservar?${searchParams.toString()}`, {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          Accept: "application/json",
        },
      });

      if (response.status === 401) {
        localStorage.removeItem("access_token");
        showNotification("Sesión expirada, vuelve a iniciar sesión.", "error");
        window.location.href = "/login";
        return;
      }

      if (response.status === 400) {
        const errorData = await response.json();
        showNotification(errorData.error, "error");
        return;
      }

      if (!response.ok) {
        showNotification("Error al buscar reservas", "error");
        return;
      }

      const data = await response.json();
      const clubsDiv = document.getElementById("clubesDisponibles");
      clubsDiv.innerHTML = "";
      data.forEach((club) => {
        clubsDiv.innerHTML += `
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
              </div>

              <div class="datos">
                <p>${club.address}</p>
                <p>De ${club.open_hour} a ${club.close_hour}</p>
                <p>${club.game_duration} minutos</p>
              </div>

              <div class="boton-reserva">
                <button type="button" class="boton-reservar" data-id="${club.id}">Reservar</button>
              </div>
            </div>
          </div>`;
      });
    } catch (error) {
      console.error(error);
    }
  });
}

// crear reserva
async function createReservation(form, clubId) {
  const formData = new FormData(form);
  const data = {
    club_id: clubId,
    dia: formData.get("dia"),
    hora: formData.get("hora"),
    duracion: formData.get("duracion"),
    tipo: formData.get("tipo"),
    cubierta: formData.get("cubierta"),
    pared: formData.get("pared"),
    superficie: formData.get("superficie"),
  };

  try {
    const response = await fetch("/api/player/reservar", {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
      body: JSON.stringify(data),
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada, vuelve a iniciar sesión.", "error");
      window.location.href = "/login";
      return;
    }

    if (response.status === 400) {
      const errorData = await response.json();
      showNotification(errorData.error, "error");
      return;
    }

    if (!response.ok) {
      showNotification("Error al crear reserva", "error");
      return;
    }

    const result = await response.json();
    showNotification("Reserva creada correctamente", "success");
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("click", async (e) => {
  if (e.target.classList.contains("boton-reservar")) {
    const form = document.getElementById("reservarForm");
    const clubId = e.target.dataset.id;
    const formData = new FormData(form);
    const params = new URLSearchParams(formData);

    window.location.href = `/confirmar_reserva?club_id=${clubId}&${params.toString()}`;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  loadCovert();
  loadMunicipalities();
  loadSurface();
  loadType();
  loadWall();

  const form = document.getElementById("reservarForm");
  sendForm(form);
});
