
document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const nombre = document.getElementById("nombre").value;
  const correo = document.getElementById("email").value;
  const rol = document.getElementById("rol").value;

  try {
    const res = await fetch("http://localhost:3000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, correo, rol })
    });

    const data = await res.json();

    if (res.ok) {
      // Guardar datos en localStorage
      localStorage.setItem("usuarioId", data.id);
      localStorage.setItem("rol", data.rol);
      localStorage.setItem("nombre", data.nombre);

      // Redirigir según el rol
      if (data.rol === "profesor") {
        window.location.href = "../views/vista_profesor.html";
      } else {
        window.location.href = "../views/vista_estudiante.html";
      }
    } else {
      alert("❌ Error: " + data.error);
    }
  } catch (err) {
    alert("❌ No se pudo conectar con el servidor.");
    console.error(err);
  }
});
