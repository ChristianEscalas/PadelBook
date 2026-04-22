import { showNotification } from "../main.js";

async function load_following() {
  try {
    const response = await fetch(`/api/user/seguidos`, {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      showNotification("Sesión expirada", "error");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      showNotification("Error al cargar los seguidores", "error");
      return;
    }

    const data = await response.json();
    const container = document.getElementById("followersContainer");

    container.innerHTML = "";

    data.forEach((user) => {
      container.innerHTML += `
        <div class="tarjetaJugador">
          <div class="infoJugador">
            <div class="fotoJugador">
              <img src="/static/${user.photo}" data-id="${user.id}" class="clickableUser">
            </div>

            <div class="infoJugador">
              <h3>${user.firstname} ${user.lastname}</h3>
            </div>

            <div class="boton">
              <button class="dejarSeguirBoton" data-id="${user.id}">Dejar de seguir</button>
            </div>
          </div>
        </div>
      `;
    });
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("click", async (event) => {
  if (event.target.classList.contains("clickableUser")) {
    const id = event.target.dataset.id;
    window.location.href = `/usuario/${id}`;
  }

  if (event.target.classList.contains("dejarSeguirBoton")) {
    const id = event.target.dataset.id;
    try {
      const response = await fetch(`/api/user/usuario/dejar_de_seguir/${id}`, {
        method: "DELETE",
        headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
      });

      const result = await response.json();

      if (!response.ok) {
        showNotification(result.error, "error");
        return;
      }

      showNotification(result.message, "success");
      load_following();
    } catch (error) {
      console.error(error);
    }
  }
});

document.addEventListener("DOMContentLoaded", () => {
  load_following();

  const returnButton = document.getElementById("Volver");
  returnButton.addEventListener("click", () => {
    window.location.href = "/perfil";
  });
});
