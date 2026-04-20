import { showNotification } from "../main.js";
import { loadCovert, loadSurface, loadType, loadWall } from "../player/main.js";

const pathParts = window.location.pathname.split("/");
const isEditMode = window.location.pathname.includes("/editar_pista");
const clubId = pathParts[2];
const courtId = isEditMode ? pathParts[4] : null;

const API = "http://192.168.0.100:5000/api/owner";
const token = localStorage.getItem("access_token");

async function handleForm(form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    if (!isEditMode) {
      const required = ["numero", "tipo", "cubierta", "pared", "superficie", "activa"];

      for (const field of required) {
        if (!formData.get(field)) {
          showNotification(`El campo ${field} es obligatorio`, "error");
          return;
        }
      }
    }

    let url = `${API}/club/${clubId}/crear_pista`;
    let method = "POST";

    if (isEditMode) {
      url = `${API}/club/${clubId}/editar_pista/${courtId}`;
      method = "PUT";
    }

    try {
      const response = await fetch(url, {
        method,
        body: formData,
        headers: { Accept: "application/json", Authorization: "Bearer " + token },
      });

      if (response.status === 401) {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
        return;
      }

      const result = await response.json();

      if (response.ok) {
        showNotification(isEditMode ? "Pista actualizada correctamente" : "Pista creada correctamente", "success");

        setTimeout(() => {
          window.location.href = `/pistas/club/${clubId}`;
        }, 1000);
      } else if (response.status === 409) {
        showNotification(result.error, "error");
      } else if (response.status === 400) {
        showNotification(result.error, "error");
      } else {
        showNotification("Error inesperado", "error");
      }
    } catch (error) {
      console.error(error);
      showNotification("Error de conexión", "error");
    }
  });
}

async function loadCourtIfEdit() {
  if (!isEditMode) return;

  try {
    const response = await fetch(`${API}/club/${clubId}/pista/${courtId}`, {
      headers: { Accept: "application/json", Authorization: "Bearer " + token },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
      return;
    }

    const data = await response.json();
    document.getElementById("numero").value = data.number_court;
    document.getElementById("tipo").value = data.court_type;
    document.getElementById("cubierta").value = data.covered;
    document.getElementById("pared").value = data.wall;
    document.getElementById("superficie").value = data.surface;

    document.getElementById("activo").value = data.active ? "true" : "false";
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadCovert();
  loadSurface();
  loadType();
  loadWall();

  const form = document.getElementById("form");
  handleForm(form);
  loadCourtIfEdit();

  const cancelBtn = document.getElementById("cancelButton");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      window.history.back();
    });
  }
});
