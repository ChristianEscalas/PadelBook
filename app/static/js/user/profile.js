import { showNotification } from "../main.js";

async function loadProfile() {
  try {
    const response = await fetch("http://192.168.0.100:5000/api/user/perfil", {
      headers: { Accpet: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (!response.ok) {
      showNotification("Error al cargar perfil", "error");
      return;
    }

    const data = await response.json();

    document.getElementById("username").innerText = data.username;
    document.getElementById("email").innerText = data.email;
    document.getElementById("mobile").innerText = data.mobile;
    document.getElementById("address").innerText = data.address;
    document.getElementById("age").innerText = data.age;
    document.getElementById("firstname").innerText = data.firstname;
    document.getElementById("lastname").innerText = data.lastname;
    document.getElementById("category").innerText = data.category;
    document.getElementById("points").innerText = data.points;
    document.getElementById("rol").innerText = data.rol;

    const photo = document.getElementById("photo");
    photo.setAttribute("src", data.photo);
    photo.setAttribute("alt", "Foto de perfil");

    document.getElementById("photo").src = `/static/${data.photo}`;
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadProfile();

  document.getElementById("editarBtn").addEventListener("click", () => {
    window.location.href = "/editar_perfil";
  });
});
