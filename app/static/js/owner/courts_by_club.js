import { showNotification } from "../main.js";

const id = window.location.pathname.split("/")[3];

async function loadCourts() {
  try {
    const response = await fetch(`http://192.168.0.100:5000/api/owner/pistas/club/${id}`, {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada, vuelve a iniciar sesión.", "error");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      showNotification("Error al cargar las pistas", "error");
      return;
    }

    const data = await response.json();
    const divPistas = document.getElementById("tarjetas-pistas");

    divPistas.innerHTML = "";
    data.forEach((court) => {
      divPistas.innerHTML += `
      <div class="tarjetaPista">
        <h3>Pista nº ${court.number_court}</h3>
        <div class="infoPista">
        
          <div class="info">
            <p><strong>Tipo:</strong></p>
            <p><strong>cubierta:</strong></p>
            <p><strong>Pared:</strong></p>
            <p><strong>Superficie:</strong></p>
            <p><strong>Activa:</strong></p>
          </div>

          <div class="datos">
            <p>${court.court_type}</p>
            <p>${court.covered}</p>
            <p>${court.wall}</p>
            <p>${court.surface}</p>
            <p>${court.active}</p>
          </div>

          <div class="botones">
            <button type="button" class="editarPistaBoton" data-id="${court.id}">Editar pista</button>
          </div>
        </div>
      </div>`;
    });
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("click", async (event) => {
  if (event.target.classList.contains("crearPista")) {
    const courtId = event.target.dataset.id;
    window.location.href = `/club/${id}/crear_pista`;
  }

  if (event.target.classList.contains("editarPistaBoton")) {
    const courtId = event.target.dataset.id;
    window.location.href = `/club/${id}/editar_pista/${courtId}`;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  loadCourts();
  document.getElementById("volverClub").addEventListener("click", () => {
    window.location.href = `/mis_clubes`;
  });
});
