import { showNotification } from "../main.js";

export async function loadMunicipalities() {
  const response = await fetch("http://192.168.0.100:5000/api/municipios", {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    showNotification("Error cargando municipios", "error");
    return;
  }

  const result = await response.json();
  const select = document.getElementById("municipio");

  result.forEach((municipality) => {
    let option = `<option value=${municipality}>${municipality}</option>`;
    select.innerHTML += option;
  });
}

export async function loadType() {
  const response = await fetch("http://192.168.0.100:5000/api/tipo", {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    showNotification("Error cargando tipos de pista", "error");
    return;
  }

  const result = await response.json();
  const select = document.getElementById("tipo");

  result.forEach((type) => {
    let option = `<option value=${type}>${type}</option>`;
    select.innerHTML += option;
  });
}

export async function loadCovert() {
  const response = await fetch("http://192.168.0.100:5000/api/cubierta", {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    showNotification("Error cargando tipos de cubierta", "error");
    return;
  }

  const result = await response.json();
  const select = document.getElementById("cubierta");

  result.forEach((cover) => {
    let option = `<option value=${cover}>${cover}</option>`;
    select.innerHTML += option;
  });
}

export async function loadWall() {
  const response = await fetch("http://192.168.0.100:5000/api/pared", {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    showNotification("Error cargando tipos de pared", "error");
    return;
  }

  const result = await response.json();
  const select = document.getElementById("pared");

  result.forEach((wall) => {
    let option = `<option value=${wall}>${wall}</option>`;
    select.innerHTML += option;
  });
}

export async function loadSurface() {
  const response = await fetch("http://192.168.0.100:5000/api/superficie", {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    showNotification("Error cargando tipos de superficie", "error");
    return;
  }

  const result = await response.json();
  const select = document.getElementById("superficie");

  result.forEach((surface) => {
    let option = `<option value=${surface}>${surface}</option>`;
    select.innerHTML += option;
  });
}
