import { loadCovert, loadMunicipalities, loadSurface, loadType, loadWall } from "./main.js";
import { showNotification } from "../main.js";

// filtrar clubes disponibles
async function sendForm(form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const searchParams = new URLSearchParams(formData);

    try {
      const response = await fetch(`/api/player/buscar_partidos?${searchParams.toString()}`, {
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
      data.forEach((reservation) => {
        clubsDiv.innerHTML += `
          <div class="tarjetaClub">
            <h3>${reservation.club_name}</h3>
            <div class="infoClub">

              <div class="fotoclub">
              <img src="/static/${reservation.photo}" alt="Foto del club">
              </div>

              <div class="info">
                <p><strong>Dirección:</strong></p>
                <p><strong>Fecha:</strong></p>
                <p><strong>Pista:</strong></p>
              </div>

              <div class="datos">
                <p>${reservation.address}</p>
                <p>De ${reservation.date}</p>
                <p>${reservation.number_court}</p>
              </div>

              <div class="boton-reserva">
                <button type="button" class="boton-reservar" data-id="${reservation.id}">Unirse</button>
              </div>
            </div>
          </div>`;
      });
    } catch (error) {
      console.error(error);
    }
  });
}

document.addEventListener("click", (event) => {
  if (event.target.classList.contains("boton-reservar")) {
    const id = event.target.dataset.id;

    window.location.href = `/unirse_reserva?id=${id}`;
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
