import { showNotification } from "../main.js";

async function register(form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const required_fields = ["username", "email", "password", "password2", "firstname", "mobile", "age", "rol", "category"];
    for (const field of required_fields) {
      if (!formData.get(field)) {
        showNotification(`El campo ${field} es obligatorio`, "error");
        return;
      }
    }

    if (formData.get("password") !== formData.get("password2")) {
      showNotification("Las contraseñas deben coincidir", "error");
      return;
    }

    const photo = formData.get("photo");
    if (!photo || photo.size === 0) {
      showNotification("Debes subir una foto de perfil", "error");
      return;
    }

    try {
      const respone = await fetch("http://192.168.0.100:5000/api/auth/registrar", {
        method: "POST",
        body: formData,
      });

      const result = await respone.json();
      if (respone.ok) {
        window.location.href = "/login";
        showNotification("Usuario creado correctamente", "success");
      } else if (respone.status === 409) {
        showNotification("El usuario o email ya está registrado", "error");
      } else if (respone.status === 400) {
        showNotification("Faltan datos obligatorios", "error");
      } else {
        showNotification(result.error || "Error inesperado", "error");
      }
    } catch (error) {
      console.log("Error: ", error);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  register(form);

  const cancelButton = document.getElementById("cancelButton");
  cancelButton.addEventListener("click", () => {
    window.history.back();
  });
});
