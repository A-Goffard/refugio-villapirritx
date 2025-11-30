<template>
  <div class="construccion-container">
    <div class="contenido">
      <img src="/iconos/patita.png" alt="Patita" class="patita-animada">
      <h1>¡Ups! Estamos trabajando en ello</h1>
      <p>Esta sección de <strong>Villa Pirritx</strong> está en construcción.</p>
      <p>Nuestros voluntarios informáticos están tecleando tan rápido como pueden (y acariciando gatos entre medias).</p>
      
      <router-link to="/" class="btn-volver">Volver al Inicio</router-link>
    </div>
  </div>
</template>

<style scoped>
.construccion-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh; /* Que ocupe bastante pantalla */
  text-align: center;
  padding: 2rem;
}

.contenido {
  background-color: var(--white);
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  max-width: 600px;
}

h1 {
  color: var(--darkPurple);
  margin: 1rem 0;
}

.patita-animada {
  width: 80px;
  animation: bote 2s infinite ease-in-out;
}

.btn-volver {
  display: inline-block;
  margin-top: 2rem;
  padding: 0.8rem 1.5rem;
  background-color: var(--lightPink);
  color: var(--darkPurple);
  text-decoration: none;
  border-radius: 20px;
  font-weight: bold;
  transition: transform 0.2s;
}

.btn-volver:hover {
  transform: scale(1.05);
}

@keyframes bote {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px) rotate(10deg); }
}
</style>