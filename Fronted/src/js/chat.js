document.addEventListener("DOMContentLoaded", () => {
  // 🔹 Datos simulados del usuario
  const usuarioActivo = {
    nombre: "Juan Pérez",
    rol: "estudiante", // Cambia a "profesor" si es necesario
    institucion: "Universidad de Medellín"
  };

  // 🔹 Conversaciones simuladas
  const conversaciones = [
    {
      id: "matematicas",
      nombre: "Docente matemáticas",
      mensajes: [
        { emisor: "profesor", texto: "Buen día, estudiantes👋 He preparado un documento con los lineamientos de la tarea." },
        { emisor: "profesor", texto: "Cualquier inquietud me comentan." },
        { emisor: "estudiante", texto: "Esa tarea profe" },
        { emisor: "profesor", texto: "Listo, pronto podrán enviar el archivo terminado." }
      ]
    },
    {
      id: "programacion",
      nombre: "Docente programación",
      mensajes: []
    }
  ];

  // 🔸 Referencias al DOM
  const nombreUsuario = document.getElementById("nombre-usuario");
  const institucionUsuario = document.getElementById("institucion-usuario");
  const listaConversaciones = document.getElementById("lista-conversaciones");
  const nombreChat = document.getElementById("nombre-chat");
  const chatHistorial = document.getElementById("chat-historial");
  const formChat = document.getElementById("form-chat");
  const inputMensaje = document.getElementById("input-mensaje");

  let conversacionActual = conversaciones[0]; // por defecto

  // 🔸 Mostrar datos del usuario
  nombreUsuario.textContent = usuarioActivo.nombre;
  institucionUsuario.textContent = usuarioActivo.institucion;

  // 🔸 Renderizar lista de conversaciones
  conversaciones.forEach((conv, index) => {
    const li = document.createElement("li");
    li.textContent = conv.nombre;
    if (index === 0) li.classList.add("conversacion-activa");
    li.addEventListener("click", () => {
      conversacionActual = conv;
      actualizarConversacionActiva(index);
      renderizarMensajes();
    });
    listaConversaciones.appendChild(li);
  });

  function actualizarConversacionActiva(activaIndex) {
    [...listaConversaciones.children].forEach((li, i) => {
      li.classList.toggle("conversacion-activa", i === activaIndex);
    });
    nombreChat.textContent = conversacionActual.nombre;
  }

  // 🔸 Renderizar mensajes
  function renderizarMensajes() {
    chatHistorial.innerHTML = "";
    conversacionActual.mensajes.forEach(msg => {
      const div = document.createElement("div");
      div.classList.add("mensaje", msg.emisor === "profesor" ? "docente" : "estudiante");
      div.textContent = msg.texto;
      chatHistorial.appendChild(div);
    });
    chatHistorial.scrollTop = chatHistorial.scrollHeight;
  }

  renderizarMensajes(); // inicial

  // 🔸 Enviar mensaje
  formChat.addEventListener("submit", e => {
    e.preventDefault();
    const texto = inputMensaje.value.trim();
    if (texto === "") return;

    // Simular envío
    conversacionActual.mensajes.push({ emisor: usuarioActivo.rol, texto });
    inputMensaje.value = "";
    renderizarMensajes();

    // 🔜 Aquí puedes integrar Firestore:
    // addDoc(collection(db, "mensajes"), {
    //   conversacionId: conversacionActual.id,
    //   emisor: usuarioActivo.rol,
    //   texto,
    //   timestamp: Date.now()
    // });
  });
});
