import { showNotification } from "../main.js";

async function loadReservations() {
  try {
    const response = await fetch("http://192.168.0.100:5000/api/player/mis_reservas", {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada, vuelve a iniciar sesión.", "error");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      showNotification("Error al cargar las reservas", "error");
      return;
    }

    const data = await response.json();
    const divTarjetas = document.getElementById("tarjetas-reserva");

    divTarjetas.innerHTML = "";
    data.forEach((reservation) => {
      divTarjetas.innerHTML += `
      <div class="tarjetaClub">
        <h3>${reservation.club_name}</h3>
        <div class="infoClub">
        
          <div class="fotoclub">
            <img src="${reservation.photo}" alt="Foto del club">
          </div>
          
          <div class="info">
            <p><strong>Fecha:</strong></p>
            <p><strong>Pista nº:</strong></p>
            <p><strong>Duración:</strong></p>
            <p><strong>Tipo:</strong></p>
          </div>

          <div class="datos">
            <p>${reservation.date}</p>
            <p>${reservation.number_court}</p>
            <p>${reservation.duration} minutos</p>
            <p>${reservation.type}</p>
          </div>

          <div class="info">
            <p><strong>Cubierta:</strong></p>
            <p><strong>Pared:</strong></p>
            <p><strong>Superficie:</strong></p>
            <p><strong>Estado:</strong></p>
          </div>

          <div class="datos">
            <p>${reservation.cover}</p>
            <p>${reservation.wall}</p>
            <p>${reservation.surface}</p>
            <p>${reservation.status}</p>
          </div>

          <div class="boton-reserva">
            <button type="button" class="detallesBoton" data-id="${reservation.id}">
              Detalles
            </button>

            ${
              !["Pendiente de resultado", "Finalizada"].includes(reservation.status)
                ? reservation.is_creator
                  ? `<button type="button" class="cancelarBoton" data-id="${reservation.id}">Cancelar</button>`
                  : `<button type="button" class="salirBoton" data-id="${reservation.id}">Desapuntarse</button>`
                : ""
            }

          </div>
        </div>
      </div>`;
    });
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("click", async (event) => {
  if (event.target.classList.contains("detallesBoton")) {
    const reservationId = event.target.dataset.id;
    window.location.href = `/reserva/${reservationId}`;
  }

  if (event.target.classList.contains("cancelarBoton")) {
    const cancelId = event.target.dataset.id;
    window.location.href = `/reserva/cancelar/${cancelId}`;
  }

  if (event.target.classList.contains("salirBoton")) {
    const id = event.target.dataset.id;

    const response = await fetch(`/api/player/reservas/salirse/${id}`, {
      method: "POST",
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada", "error");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      const error = await response.json();
      showNotification(error.error, "error");
      return;
    }

    showNotification("Te has salido del partido", "success");

    loadReservations();
  }
});

document.addEventListener("DOMContentLoaded", () => {
  loadReservations();
});
