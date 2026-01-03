<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// Variables para guardar los datos
const animales = ref([]);
const cargando = ref(true);
const error = ref(null);

// Cuando la página se carga, pedimos los datos
onMounted(async () => {
  try {
    // Petición a tu Django local
    const response = await axios.get("/api/animales/");

    // Filtramos solo los que están en ADOPCION o URGENTE
    animales.value = response.data.filter(
      (a) => a.estado === "ADOPCION" || a.estado === "URGENTE"
    );
  } catch (e) {
    console.error(e);
    error.value = "Hubo un problema cargando los peludos. Inténtalo más tarde.";
  } finally {
    cargando.value = false;
  }
});
</script>

<template>
  <div class="body">
    <div class="capaBlanca">
      <div class="centre encabezado">
        <img src="/iconos/patita.png" class="patita-titulo" alt="huella" />
        <h2>Animales en Adopción</h2>
        <p>
          Estos pequeños buscan una segunda oportunidad. ¿Eres tú su familia?
        </p>
      </div>

      <div v-if="cargando" class="centre loading-container">
        <img
          src="/iconos/patita.png"
          class="patita-animada"
          alt="Cargando..."
        />
        <p>Llamando a los animales...</p>
      </div>

      <div v-else-if="error" class="textCentre error-msg">
        <p>{{ error }}</p>
      </div>

      <div v-else-if="animales.length === 0" class="textCentre">
        <p>¡Vaya! Ahora mismo no hay animales publicados en adopción.</p>
      </div>

      <div v-else class="animal-grid">
        <div v-for="animal in animales" :key="animal.id" class="animal-card">
          <div class="img-container">
            <img v-if="animal.foto" :src="animal.foto" :alt="animal.nombre" />
            <img
              v-else
              src="/logos/logo.png"
              alt="Sin foto"
              class="placeholder"
            />

            <span v-if="animal.estado === 'URGENTE'" class="etiqueta-urgente"
              >¡URGENTE!</span
            >
          </div>

          <div class="info">
            <div class="info-header">
              <h3>{{ animal.nombre }}</h3>
              <span class="fecha-nac" v-if="animal.fecha_nacimiento">
                Nac: {{ animal.fecha_nacimiento }}
              </span>
            </div>

            <p class="desc">{{ animal.descripcion }}</p>

            <div class="acciones">
              <router-link
                :to="{ path: '/solicitud', query: { animal: animal.nombre } }"
              >
                <button class="btnRosa">Preguntar por mí</button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos para que quede bonito y responsive */
.encabezado {
  margin-bottom: 2rem;
  text-align: center;
}
.patita-titulo {
  width: 3rem;
  margin-bottom: 0.5rem;
}

.animal-grid {
  display: grid;
  /* Esto hace que sea responsive automático: columnas de mínimo 300px */
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.animal-card {
  background: var(--white);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Sombra suave */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid #f0f0f0;
}

.animal-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.img-container {
  height: 250px;
  width: 100%;
  overflow: hidden;
  position: relative;
  background-color: var(--lightPurple);
}

.img-container img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Recorta la imagen para llenar el hueco sin deformar */
}

.placeholder {
  object-fit: contain !important;
  padding: 2rem;
  opacity: 0.5;
}

.etiqueta-urgente {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ff4757;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.8rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.info {
  padding: 1.5rem;
  flex: 1; /* Ocupa el espacio restante */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.info h3 {
  margin: 0;
  color: var(--darkPurple);
  font-size: 1.5rem;
}

.fecha-nac {
  font-size: 0.85rem;
  color: #888;
}

.desc {
  color: #555;
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 1.5rem;

  /* Cortar texto si es muy largo con '...' */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.acciones {
  text-align: center;
}

/* Animación de carga */
.loading-container {
  margin: 3rem 0;
}
.patita-animada {
  width: 60px;
  animation: bote 0.8s infinite alternate ease-in-out;
}
@keyframes bote {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-15px);
  }
}

.error-msg {
  color: #e74c3c;
  font-weight: bold;
  margin: 2rem;
}
</style>
