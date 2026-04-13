import { showNotification } from "./main.js";

async function contact(form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const name = form["name"].value.trim();
    const email = form["email"].value.trim();
    const message = form["message"].value.trim();

    if (name.length === 0 || email.length === 0 || message.length === 0) {
      showNotification("Rellena todos los campos para que podamos contactar contigo.");
      return;
    }

    const contactMessage = { name: name, email: email, message: message };
    try {
      const response = await fetch("http://192.168.0.100:5000/api/contacto", {
        method: "POST",
        headers: { Accept: "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(contactMessage),
      });

      const result = await response.json();
      if (response.ok) {
        showNotification("Mensaje enviado, te contactaremos lo antes posible.", "success");
        form.reset();
      } else {
        showNotification(result.error || "Error inesperado", "error");
      }
    } catch (error) {
      console.log(error);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  contact(form);

  const cancelButton = document.getElementById("cancelButton");
  cancelButton.addEventListener("click", () => {
    window.history.back();
  });
});
