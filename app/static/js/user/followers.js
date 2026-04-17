import { showNotification } from "../main.js";

async function load_followers() {
  try {
    const response = await fetch(`http://192.168.0.100:5000/api/user/seguidores`, {
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
      const buttonText = user.is_following ? "Dejar de seguir" : "Seguir";
      const buttonClass = user.is_following ? "dejarSeguirBoton" : "seguirBoton";

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
              <button class="${buttonClass}" data-id="${user.id}">
                ${buttonText}
              </button>
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

  if (event.target.classList.contains("seguirBoton") || event.target.classList.contains("dejarSeguirBoton")) {
    const button = event.target;
    const id = button.dataset.id;

    const isFollowing = button.classList.contains("dejarSeguirBoton");

    const url = isFollowing ? `/api/user/usuario/dejar_de_seguir/${id}` : `/api/user/usuario/seguir/${id}`;

    const method = isFollowing ? "DELETE" : "POST";

    try {
      const response = await fetch(url, {
        method,
        headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
      });

      const result = await response.json();

      if (!response.ok) {
        showNotification(result.error, "error");
        return;
      }

      if (isFollowing) {
        button.innerText = "Seguir";
        button.classList.remove("dejarSeguirBoton");
        button.classList.add("seguirBoton");
      } else {
        button.innerText = "Dejar de seguir";
        button.classList.remove("seguirBoton");
        button.classList.add("dejarSeguirBoton");
      }

      showNotification(result.message, "success");
    } catch (error) {
      console.error(error);
    }
  }
});

document.addEventListener("DOMContentLoaded", () => {
  load_followers();

  const returnButton = document.getElementById("Volver");
  returnButton.addEventListener("click", () => {
    window.location.href = "/perfil";
  });
});
