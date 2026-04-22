import { showNotification } from "../main.js";

const userId = window.location.pathname.split("/")[2];

let isFollowing = false;

async function loadUserProfile() {
  try {
    const response = await fetch(`/api/user/usuario/${userId}`, {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      showNotification("Error al cargar el perfil", "error");
      return;
    }

    const data = await response.json();

    document.getElementById("username").innerText = data.username;
    document.getElementById("mobile").innerText = data.mobile;
    document.getElementById("category").innerText = data.category;
    document.getElementById("firstname").innerText = data.firstname;
    document.getElementById("lastname").innerText = data.lastname;
    document.getElementById("points").innerText = data.points;

    const photo = document.getElementById("photo");
    photo.src = `/static/${data.photo}`;
    photo.setAttribute("alt", "Foto de perfil");
  } catch (error) {
    console.error(error);
  }
}

async function checkFollowStatus() {
  try {
    const response = await fetch(`/api/user/usuario/es_seguido/${userId}`, {
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    const data = await response.json();
    isFollowing = data.following;

    updateFollowButton();
  } catch (error) {
    console.error(error);
  }
}

function updateFollowButton() {
  const followButton = document.getElementById("seguirBoton");

  if (isFollowing) {
    followButton.innerText = "Dejar de seguir";
  } else {
    followButton.innerText = "Seguir";
  }
}

async function toggleFollow() {
  try {
    const url = isFollowing ? `/api/user/usuario/dejar_de_seguir/${userId}` : `/api/user/usuario/seguir/${userId}`;

    const method = isFollowing ? "DELETE" : "POST";

    const response = await fetch(url, {
      method,
      headers: { Accept: "application/json", Authorization: "Bearer " + localStorage.getItem("access_token") },
    });

    const result = await response.json();

    if (!response.ok) {
      showNotification(result.error, "error");
      return;
    }

    isFollowing = !isFollowing;
    updateFollowButton();

    showNotification(result.message, "success");
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadUserProfile();
  checkFollowStatus();

  document.getElementById("seguirBoton").addEventListener("click", toggleFollow);

  document.getElementById("volverBoton").addEventListener("click", () => {
    window.history.back();
  });
});
