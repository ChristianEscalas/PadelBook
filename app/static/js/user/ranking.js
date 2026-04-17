import { showNotification } from "../main.js";

async function loadRanking(params = "") {
  try {
    const response = await fetch(`http://192.168.0.100:5000/api/user/ranking${params}`, {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada", "error");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      showNotification("Error al cargar ranking", "error");
      return;
    }

    const data = await response.json();
    const container = document.getElementById("rankingContainer");

    container.innerHTML = "";

    data.forEach((user) => {
      container.innerHTML += `
        <div class="tarjetaJugador">
          <div class="infoJugador">
            <div class="fotoJugador>
              <img src="/static/${user.photo}" data-id="${user.id}" class="clickableUser">
            </div>

            <div class="infoJugador">
              <h3>${user.firstname}</h3>
              <p>${user.points} puntos</p>
            </div>
          </div>
        </div>
      `;
    });
  } catch (error) {
    console.error(error);
  }
}

function handleForm(form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const params = new URLSearchParams(formData);

    let query = "";
    if (params.toString()) {
      query = "?" + params.toString();
    }

    loadRanking(query);
  });
}

document.addEventListener("click", (event) => {
  if (event.target.classList.contains("clickableUser")) {
    const id = event.target.dataset.id;
    window.location.href = `/usuario/${id}`;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("rankingForm");
  handleForm(form);

  loadRanking();
});
