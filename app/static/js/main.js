export function showNotification(message, type = "success") {
  const container = document.getElementById("notification-container");

  // Crear el elemento de la notificación
  const toast = document.createElement("div");
  toast.classList.add("custom-alert", `alert-${type}`);
  toast.innerText = message;

  container.appendChild(toast);

  // Eliminarla automáticamente después de 4 segundos
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.5s ease";
    setTimeout(() => toast.remove(), 500);
  }, 4000);
}
