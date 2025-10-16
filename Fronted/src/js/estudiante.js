document.addEventListener("DOMContentLoaded", () => {
  // 🔹 Activar pestañas
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const tab = btn.dataset.tab;
      tabContents.forEach(sec => {
        sec.classList.remove("active");
        if (sec.id === tab) sec.classList.add("active");
      });
    });
  });

  // 🧩 Agregar curso
  const formCurso = document.getElementById("form-agregar-curso");
  const listaCursos = document.getElementById("lista-cursos");

  formCurso.addEventListener("submit", e => {
    e.preventDefault();
    const input = document.getElementById("nuevo-curso");
    const nombre = input.value.trim();
    if (nombre) {
      const li = document.createElement("li");
      li.className = "curso-item";
      li.innerHTML = `
        <span>${nombre}</span>
        <button class="btn-eliminar">Eliminar</button>
      `;
      listaCursos.appendChild(li);
      input.value = "";

      li.querySelector(".btn-eliminar").addEventListener("click", () => {
        li.remove();
      });
    }
  });

  // 📌 Actividades simuladas
  document.getElementById("btn-agregar-actividad").addEventListener("click", () => {
    const lista = document.getElementById("lista-actividades");
    const li = document.createElement("li");
    li.textContent = "Nueva actividad: Entrega de proyecto final";
    lista.appendChild(li);
  });

  // ⚠️ Alertas simuladas
  document.getElementById("btn-ver-alertas").addEventListener("click", () => {
    const contenedor = document.getElementById("alertas-list");
    contenedor.innerHTML = `
      <div class="alerta">⚠️ Tienes una nota baja en Matemáticas</div>
      <div class="alerta">📌 Revisa tu asistencia en Historia</div>
    `;
  });

  // 🤖 Recomendaciones simuladas
  document.getElementById("btn-ver-recomendaciones").addEventListener("click", () => {
    const contenedor = document.getElementById("recomendaciones-list");
    contenedor.innerHTML = `
      <div class="recomendacion">💡 Estudia con resúmenes visuales para mejorar retención</div>
      <div class="recomendacion">📚 Revisa los temas de lógica antes del examen</div>
    `;
  });

  // 📅 Calendario académico
  document.getElementById("btn-ver-calendario").addEventListener("click", () => {
    const calendarioEl = document.getElementById("calendario-widget");
    if (!calendarioEl.innerHTML.trim()) {
      const calendar = new FullCalendar.Calendar(calendarioEl, {
        initialView: "dayGridMonth",
        locale: "es",
        events: [
          { title: "Inicio de clases", start: "2025-10-14" },
          { title: "Entrega proyecto", start: "2025-10-20" },
          { title: "Examen final", start: "2025-10-28" }
        ]
      });
      calendar.render();
    }
  });
});
