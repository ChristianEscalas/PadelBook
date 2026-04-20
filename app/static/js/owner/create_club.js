import { showNotification } from "../main.js";

const pathParts = window.location.pathname.split("/");
const isEditMode = window.location.pathname.includes("/editar_club");
const clubId = isEditMode ? pathParts[pathParts.length - 1] : null;

const API = "http://192.168.0.100:5000/api/owner";
const token = localStorage.getItem("access_token");

async function handleForm(form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    if (!isEditMode) {
      const required = ["nombre", "direccion", "horaApertura", "horaCierre", "duracion", "municipio", "activo"];

      for (const field of required) {
        if (!formData.get(field)) {
          showNotification(`El campo ${field} es obligatorio`, "error");
          return;
        }
      }

      const photo = formData.get("photo");
      if (!photo || photo.size === 0) {
        showNotification("Debes subir una foto del club", "error");
        return;
      }
    }

    let url = `${API}/crear_club`;
    let method = "POST";

    if (isEditMode) {
      url = `${API}/editar_club/${clubId}`;
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
        showNotification(isEditMode ? "Club actualizado correctamente" : "Club creado correctamente", "success");

        setTimeout(() => {
          window.location.href = "/mis_clubes";
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

async function loadClubIfEdit() {
  if (!isEditMode) return;

  try {
    const response = await fetch(`${API}/club/${clubId}`, {
      headers: { Accept: "application/json", Authorization: "Bearer " + token },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
      return;
    }

    const data = await response.json();

    document.getElementById("nombre").value = data.club_name;
    document.getElementById("direccion").value = data.address;
    document.getElementById("horaApertura").value = data.open_hour;
    document.getElementById("horaCierre").value = data.close_hour;
    document.getElementById("duracion").value = data.game_duration;
    document.getElementById("municipio").value = data.municipality;

    document.getElementById("activo").value = data.active ? "true" : "false";
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  handleForm(form);
  loadClubIfEdit();

  const cancelBtn = document.getElementById("cancelButton");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      window.location.href = "/mis_clubes";
    });
  }
});
