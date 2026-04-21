import { showNotification } from "../main.js";

const clubId = window.location.pathname.split("/")[2];
const id = window.location.pathname.split("/")[4];

async function loadReservation() {
  const response = await fetch(`/api/owner/reserva/${id}`, {
    headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
  });

  const data = await response.json();

  document.getElementById("club").innerText = data.club;
  document.getElementById("fecha").innerText = data.date;
  document.getElementById("pista").innerText = data.court_number;
  document.getElementById("photo").src = "/static/" + data.photo;
}

async function cancelReservation() {
  const response = await fetch(`http://192.168.0.100:5000/api/owner/reserva/cancelar/${id}`, {
    method: "POST",
    headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
  });

  const result = await response.json();

  if (response.status == 401) {
    localStorage.removeItem("access_token");
    showNotification("Sesión expirada, vuelve a iniciar sesión.", "error");
    window.location.href = "/login";
    return;
  }

  if (!response.ok) {
    showNotification(result.error, "error");
    return;
  }

  if (response.ok) {
    showNotification(result.message, "success");

    setTimeout(() => {
      window.location.href = `/reservas/club/${clubId}`;
    }, 1000);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadReservation();

  const cancelButton = document.getElementById("cancelarBoton");
  cancelButton.addEventListener("click", cancelReservation);

  const returnButton = document.getElementById("volverBoton");
  returnButton.addEventListener("click", () => {
    window.history.back();
  });
});
