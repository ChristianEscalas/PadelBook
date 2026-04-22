import { showNotification } from "../main.js";

async function loadPreview() {
  const params = new URLSearchParams(window.location.search);

  // datos del formulario
  document.getElementById("dia").innerText = params.get("dia");
  document.getElementById("hora").innerText = params.get("hora");
  document.getElementById("duracion").innerText = params.get("duracion") + " min";

  const type = params.get("tipo");
  if (type === "double") {
    document.getElementById("tipo").innerText = "Dobles";
  } else {
    document.getElementById("tipo").innerText = "Individual";
  }

  const cover = params.get("cubierta");
  if (cover === "true") {
    document.getElementById("cubierta").innerText = "Si";
  } else {
    document.getElementById("cubierta").innerText = "No";
  }

  const wall = params.get("pared");
  if (wall === "glass") {
    document.getElementById("pared").innerText = "Cristal";
  } else {
    document.getElementById("pared").innerText = "Hormigón";
  }

  const surface = params.get("superficie");
  if (surface === "grass") {
    document.getElementById("superficie").innerText = "Césped";
  } else {
    document.getElementById("superficie").innerText = "Hormigón";
  }

  // llamada al backend
  const response = await fetch(`/api/player/reservar/preview?${params.toString()}`, {
    headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
  });

  if (!response.ok) {
    const error = await response.json();
    showNotification(error.error, "error");
    return;
  }

  const data = await response.json();

  document.getElementById("club").innerText = data.club;
  document.getElementById("pista").innerText = data.court_number;

  const photo = document.getElementById("fotoCluB");
  photo.src = `/static/${data.photo}`;
}

async function confirmReservation() {
  const params = new URLSearchParams(window.location.search);
  const data = Object.fromEntries(params.entries());

  const response = await fetch("/api/player/reservar", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    showNotification(error.error, "error");
    return;
  }

  showNotification("Reserva creada correctamente", "success");

  setTimeout(() => {
    window.location.href = "/mis_reservas";
  }, 1000);
}

document.addEventListener("DOMContentLoaded", () => {
  loadPreview();
  const confirmButton = document.getElementById("confirmarBoton");
  confirmButton.addEventListener("click", confirmReservation);

  const cancelButton = document.getElementById("cancelarBoton");
  cancelButton.addEventListener("click", () => {
    window.history.back();
  });
});
