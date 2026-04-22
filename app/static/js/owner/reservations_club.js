import { showNotification } from "../main.js";

const clubId = window.location.pathname.split("/")[3];

async function load_reservations(clubId) {
  const form = document.getElementById("form");
  const formData = new FormData(form);
  const searchParams = new URLSearchParams(formData);

  try {
    const response = await fetch(`/api/owner/reservas/club/${clubId}?${searchParams.toString()}`, {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada, vuelve a iniciar sesión.", "error");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      const errorData = await response.json();
      showNotification(errorData.error, "error");
      return;
    }

    const data = await response.json();
    const reservationsDiv = document.getElementById("tarjetas-reservas");

    reservationsDiv.innerHTML = "";
    data.forEach((reservation) => {
      reservationsDiv.innerHTML += `
          <div class="tarjetareservation">
            <h3>Pista nº ${reservation.number_court}</h3>
            <div class="inforeservation">

              <div class="info">
                <p><strong>Inicio:</strong></p>
                <p><strong>Fin:</strong></p>
                <p><strong>Estado:</strong></p>
              </div>

              <div class="datos">
                <p>${reservation.start_date}</p>
                <p>${reservation.end_date}</p>
                <p>${reservation.status_game}</p>
              </div>

              <div class="botones">
                <button type="button" class="detallesBoton" data-id="${reservation.id}">Detalles</button>
                ${!["Pendiente de resultado", "Finalizada", "Cancelada"].includes(reservation.status_game) ? `<button type="button" class="cancelarBoton" data-id="${reservation.id}">Cancelar</button>` : ""}
              </div>
            </div>
          </div>`;
    });
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  load_reservations(clubId);

  document.getElementById("form").addEventListener("submit", (event) => {
    event.preventDefault();
    load_reservations(clubId);
  });

  document.getElementById("volverBoton").addEventListener("click", () => {
    window.history.back();
  });
});

document.addEventListener("click", (event) => {
  if (event.target.classList.contains("detallesBoton")) {
    window.location.href = `/club/${clubId}/reserva/${event.target.dataset.id}`;
  }

  if (event.target.classList.contains("cancelarBoton")) {
    window.location.href = `/club/${clubId}/reserva/${event.target.dataset.id}/cancelar`;
  }
});
