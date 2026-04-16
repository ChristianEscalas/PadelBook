import { showNotification } from "../main.js";

const isEditMode = window.location.pathname === "/editar_perfil";

async function handleForm(form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    if (!isEditMode) {
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
    }

    let url = "http://192.168.0.100:5000/api/auth/registrar";
    let method = "POST";

    if (isEditMode) {
      url = "http://192.168.0.100:5000/api/user/perfil";
      method = "PUT";
    }

    try {
      const response = await fetch(url, {
        method,
        body: formData,
        ...(isEditMode && {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
        }),
      });

      const result = await response.json();

      if (response.ok) {
        showNotification(isEditMode ? "Perfil actualizado correctamente" : "Usuario creado correctamente", "success");

        setTimeout(() => {
          window.location.href = isEditMode ? "/perfil" : "/login";
        }, 1000);
      } else if (response.status === 409) {
        showNotification(result.error || "Conflicto de datos", "error");
      } else if (response.status === 400) {
        showNotification(result.error || "Datos inválidos", "error");
      } else {
        showNotification(result.error || "Error inesperado", "error");
      }
    } catch (error) {
      console.log("Error: ", error);
    }
  });
}

async function loadProfileIfEdit() {
  if (!isEditMode) return;

  try {
    const response = await fetch("http://192.168.0.100:5000/api/user/perfil", {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    const data = await response.json();

    document.getElementById("username").value = data.username;
    document.getElementById("email").value = data.email;
    document.getElementById("firstname").value = data.firstname;
    document.getElementById("lastname").value = data.lastname;
    document.getElementById("mobile").value = data.mobile;
    document.getElementById("age").value = data.age;
    document.getElementById("address").value = data.address;
    document.getElementById("category").value = data.category;

    document.getElementById("rol").value = data.rol;

    if (document.getElementById("rol_hidden")) {
      document.getElementById("rol_hidden").value = data.rol;
    }
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  handleForm(form);

  loadProfileIfEdit();

  const cancelBtn = document.getElementById("cancelBtn") || document.getElementById("cancelButton");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      window.location.href = isEditMode ? "/perfil" : "/";
    });
  }
});
