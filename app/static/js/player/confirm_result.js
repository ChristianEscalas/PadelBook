import { showNotification } from "../main.js";

const reservationId = window.location.pathname.split("/").pop();
const token = localStorage.getItem("access_token");

async function loadResult() {
  try {
    const response = await fetch(`http://192.168.0.100:5000/api/player/reservas/resultado/${reservationId}`, {
      headers: { Accpet: "application/json", Authorization: "Bearer " + token },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada", "error");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) return;

    const data = await response.json();

    if (data.sets_a && data.sets_b) {
      document.getElementById("a1").value = data.sets_a[0];
      document.getElementById("a2").value = data.sets_a[1];
      document.getElementById("a3").value = data.sets_a[2];

      document.getElementById("b1").value = data.sets_b[0];
      document.getElementById("b2").value = data.sets_b[1];
      document.getElementById("b3").value = data.sets_b[2];

      document.getElementById("estadoTexto").textContent = "Resultado ya introducido. Pendiente de confirmación del rival.";
    } else {
      document.getElementById("estadoTexto").textContent = "Introduce el resultado del partido.";
    }
  } catch (error) {
    console.error(error);
  }
}

async function submitResult(event) {
  event.preventDefault();

  const sets_a = [parseInt(document.getElementById("a1").value) || 0, parseInt(document.getElementById("a2").value) || 0, parseInt(document.getElementById("a3").value) || 0];

  const sets_b = [parseInt(document.getElementById("b1").value) || 0, parseInt(document.getElementById("b2").value) || 0, parseInt(document.getElementById("b3").value) || 0];

  try {
    const response = await fetch(`http://192.168.0.100:5000/api/player/reservas/confirmar_resultado/${reservationId}`, {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json", Authorization: "Bearer " + token },
      body: JSON.stringify({ sets_a, sets_b }),
    });

    const result = await response.json();

    if (!response.ok) {
      showNotification(result.error || "Error al guardar resultado", "error");
      return;
    }

    if (result.finalized) {
      showNotification("Resultado confirmado por ambos jugadores", "success");
      window.location.href = `/reserva/${reservationId}`;
    } else {
      showNotification("Resultado guardado. Falta confirmación del rival", "success");
      loadResult();
    }
  } catch (error) {
    console.error(error);
  }
}

function cancel() {
  window.history.back();
}

document.addEventListener("DOMContentLoaded", () => {
  loadResult();

  document.getElementById("formResultado").addEventListener("submit", submitResult);
  document.getElementById("cancelBtn").addEventListener("click", cancel);
});
