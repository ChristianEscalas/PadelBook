import { showNotification } from "../main.js";

async function login(form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = form["username"].value.trim();
    const password = form["password"].value.trim();
    if (username.length === 0 || password.length === 0) {
      return;
    }

    const user = { username: username, password: password };
    try {
      const response = await fetch("http://192.168.0.100:5000/api/auth/login", {
        method: "POST",
        headers: { Accept: "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(user),
      });

      const result = await response.json();

      if (response.ok) {
        localStorage.setItem("access_token", result.access_token);

        const payload = JSON.parse(atob(result.access_token.split(".")[1]));
        const rol = payload.rol;

        if (rol === "player") {
          window.location.href = "/reservar";
        } else if (rol === "owner") {
          window.location.href = "/mis_clubes";
        } else {
          console.log("Rol desconocido", rol);
        }
      } else {
        showNotification("Nombre de usuario o contraseña incorretos", "error");
      }
    } catch (error) {
      console.log(error);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  login(form);

  const cancelButton = document.getElementById("cancelButton");
  cancelButton.addEventListener("click", () => {
    window.history.back();
  });

  const registerButton = document.getElementById("registerButton");
  registerButton.addEventListener("click", () => {
    window.location.href = "/registrar";
  });
});
