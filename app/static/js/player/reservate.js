import { loadCovert, loadMunicipalities, loadSurface, loadType, loadWall } from "./main.js";
import { showNotification } from "../main.js";

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
            <p>${club.club_name}</p>
            <div class="infoClub">

              <div class="fotoclub">
              <img src="${club.photo}" alt="Foto del club">
              </div>

              <div class="info">
                <p><span>Dirección:</span></p>
                <p><span>Horario:</span></p>
                <p><span>Duración de los partidos:</span></p>
              </div>

              <div class="datos">
                <p>${club.address}</p>
                <p>De ${club.open_hour} a ${club.close_hour}</p>
                <p>${club.game_duration}</p>
              </div>

              <div class="boton-reserva">
                <button type="button" class="boton-reservar" data-id="${club.id}">Reservar</button>
              </div>
            </div>
          </div>`;

        const confirmReservationButton = document.querySelector(".boton-reservar");
        confirmReservationButton.addEventListener("click", () => {
          window.location.href = `/confirmar_reserva?club_id=${club.id}`;
        });
      });
    } catch (error) {
      console.error(error);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadCovert();
  loadMunicipalities();
  loadSurface();
  loadType();
  loadWall();

  const form = document.getElementById("reservarForm");
  sendForm(form);
});
