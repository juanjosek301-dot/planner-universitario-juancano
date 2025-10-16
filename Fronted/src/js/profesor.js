document.addEventListener("DOMContentLoaded", () => {
  const nombreProfesor = "Gustavo Ríos"; // Puedes obtenerlo dinámicamente si usas localStorage
  document.getElementById("bienvenida").textContent = `Bienvenido, ${nombreProfesor}`;

  const selectorCurso = document.getElementById("selector-curso");
  const listaEstudiantes = document.getElementById("lista-estudiantes");
  const inputRecomendacion = document.getElementById("input-recomendacion");
  const btnAgregarRecomendacion = document.getElementById("btn-agregar-recomendacion");
  const panelRecomendaciones = document.getElementById("panel-recomendaciones");
  const btnCerrarSesion = document.getElementById("cerrar-sesion");

  // 🔹 Cursos simulados con progreso
  const cursos = {
    "Matemáticas I": [
      { nombre: "Laura Martínez", progreso: 85 },
      { nombre: "Carlos Gómez", progreso: 60 },
      { nombre: "Valentina Ruiz", progreso: 40 }
    ],
    "Historia Universal": [
      { nombre: "Andrés Torres", progreso: 90 },
      { nombre: "María López", progreso: 72 },
      { nombre: "Sofía Ramírez", progreso: 50 }
    ]
  };

  // 🔸 Cargar cursos en el selector
  Object.keys(cursos).forEach(nombreCurso => {
    const option = document.createElement("option");
    option.value = nombreCurso;
    option.textContent = nombreCurso;
    selectorCurso.appendChild(option);
  });

  // 🔸 Mostrar estudiantes al seleccionar curso
  selectorCurso.addEventListener("change", () => {
    const cursoSeleccionado = selectorCurso.value;
    listaEstudiantes.innerHTML = "";

    if (cursoSeleccionado && cursos[cursoSeleccionado]) {
      cursos[cursoSeleccionado].forEach(est => {
        const li = document.createElement("li");
        li.innerHTML = `
          <strong>${est.nombre}</strong><br>
          <div class="progreso-bar">
            <div class="progreso-bar-fill" style="width: ${est.progreso}%"></div>
          </div>
          <span>${est.progreso}% completado</span>
        `;
        listaEstudiantes.appendChild(li);
      });
    }
  });

  // 🔸 Agregar recomendaciones
  btnAgregarRecomendacion.addEventListener("click", () => {
    const texto = inputRecomendacion.value.trim();
    if (texto) {
      const li = document.createElement("li");
      li.textContent = texto;
      panelRecomendaciones.appendChild(li);
      inputRecomendacion.value = "";
    }
  });

  // 🔸 Cerrar sesión
  btnCerrarSesion.addEventListener("click", () => {
    localStorage.removeItem("usuarioActivo");
    window.location.href = "../index.html";
  });
});