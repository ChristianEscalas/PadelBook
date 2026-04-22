import { showNotification } from "../main.js";

let selectedTeam = null;

async function loadReservation() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");

  const response = await fetch(`/api/player/reservas/${id}`, {
    headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
  });

  const data = await response.json();

  document.getElementById("club").innerText = data.club;
  document.getElementById("dia").innerText = data.date;
  document.getElementById("duracion").innerText = data.duration + " minutos";
  const photo = document.getElementById("foto");
  photo.src = `/static/${data.photo}`;

  const type = data.type;
  if (type === "double") {
    document.getElementById("tipo").innerText = "Dobles";
  } else {
    document.getElementById("tipo").innerText = "Individual";
  }

  const cover = data.cover;
  if (cover === true) {
    document.getElementById("cubierta").innerText = "Si";
  } else {
    document.getElementById("cubierta").innerText = "No";
  }

  const wall = data.wall;
  if (wall === "glass") {
    document.getElementById("pared").innerText = "Cristal";
  } else {
    document.getElementById("pared").innerText = "Hormigón";
  }

  const surface = data.surface;
  if (surface === "grass") {
    document.getElementById("superficie").innerText = "Césped";
  } else {
    document.getElementById("superficie").innerText = "Hormigón";
  }

  const teamA = document.getElementById("teamA");
  const teamB = document.getElementById("teamB");

  teamA.innerHTML = "";
  teamB.innerHTML = "";

  const playersA = data.players.filter((p) => p.team === "a");
  const playersB = data.players.filter((p) => p.team === "b");

  renderTeam(teamA, playersA, "a");
  renderTeam(teamB, playersB, "b");

  document.getElementById("teamA").insertAdjacentHTML("beforebegin", `<p>${playersA.length}/2</p>`);
  document.getElementById("teamB").insertAdjacentHTML("beforebegin", `<p>${playersB.length}/2</p>`);
}

function renderTeam(container, players, team) {
  players.forEach((p) => {
    container.innerHTML += `
      <div class="jugador">
        <img src="/static/${p.photo}" alt="${p.name}">
        <p>${p.name}</p>
      </div>
    `;
  });

  for (let i = players.length; i < 2; i++) {
    container.innerHTML += `
      <div class="slot" data-team="${team}">
        +
      </div>
    `;
  }
}

document.addEventListener("click", (e) => {
  if (e.target.classList.contains("slot")) {
    selectedTeam = e.target.dataset.team;

    document.querySelectorAll(".slot").forEach((el) => el.classList.remove("selected"));
    e.target.classList.add("selected");
  }
});

async function joinReservation() {
  if (!selectedTeam) {
    showNotification("Selecciona un equipo", "error");
    return;
  }

  const id = new URLSearchParams(window.location.search).get("id");

  const response = await fetch(`/api/player/reservas/unirse/${id}`, {
    method: "POST",
    headers: { Accept: "application/json", "Content-Type": "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    body: JSON.stringify({ team: selectedTeam }),
  });

  if (!response.ok) {
    const error = await response.json();
    showNotification(error.error, "error");
    return;
  }

  showNotification("Te has unido al partido", "success");

  setTimeout(() => {
    window.location.href = "/mis_reservas";
  }, 1000);
}

document.addEventListener("DOMContentLoaded", () => {
  loadReservation();

  document.getElementById("confirmarBoton").addEventListener("click", joinReservation);
  document.getElementById("cancelarBoton").addEventListener("click", () => {
    window.history.back();
  });
});
