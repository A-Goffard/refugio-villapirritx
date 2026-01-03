<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// --- DATOS ---
const animales = ref([])
const cargando = ref(true)
const error = ref(null)

// --- MODAL ---
const animalSeleccionado = ref(null)

const abrirModal = (animal) => {
  animalSeleccionado.value = animal
  document.body.style.overflow = 'hidden'
}

const cerrarModal = () => {
  animalSeleccionado.value = null
  document.body.style.overflow = 'auto'
}

// --- CARGA ---
onMounted(async () => {
  try {
    const response = await axios.get('/api/animales/')
    animales.value = response.data.filter(a => a.estado === 'ADOPCION' || a.estado === 'URGENTE')
  } catch (e) {
    console.error(e)
    error.value = "Hubo un problema cargando los peludos."
  } finally {
    cargando.value = false
  }
})
</script>

<template>
  <div class="body">
    
    <div class="capaBlanca vista-adopcion">
       
       <div class="encabezado">
          <img src="/iconos/patita.png" class="patita-titulo" alt="huella">
          <h2>Animales en Adopción</h2>
          <p>Haz clic en su foto para conocer su historia.</p>
       </div>

       <div v-if="cargando" class="loading-container">
          <img src="/iconos/patita.png" class="patita-animada" alt="...">
          <p>Llamando a los animales...</p>
       </div>
       <div v-else-if="error" class="error-msg"><p>{{ error }}</p></div>
       <div v-else-if="animales.length === 0"><p>No hay animales ahora mismo.</p></div>

       <div v-else class="cards-container">
          <div v-for="animal in animales" :key="animal.id" class="animal-card" @click="abrirModal(animal)">
              
              <div class="img-container">
                  <img v-if="animal.foto" :src="animal.foto" :alt="animal.nombre" />
                  <img v-else src="/logos/logo.png" class="placeholder" />
                  <span v-if="animal.estado === 'URGENTE'" class="etiqueta-urgente">¡URGENTE!</span>
              </div>

              <div class="info-card">
                  <h3>{{ animal.nombre }}</h3>
                  <p class="desc-corta">{{ animal.descripcion }}</p>
                  <button class="btnMorado">Ver detalles +</button>
              </div>
          </div>
       </div>
    </div>

    <div v-if="animalSeleccionado" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal-content">
        <button class="btn-cerrar" @click="cerrarModal">×</button>
        <div class="modal-grid">
           <div class="modal-img">
              <img v-if="animalSeleccionado.foto" :src="animalSeleccionado.foto">
              <img v-else src="/logos/logo.png" class="placeholder">
           </div>
           <div class="modal-info">
              <h2>{{ animalSeleccionado.nombre }}</h2>
              <span class="etiqueta-estado" v-if="animalSeleccionado.estado === 'URGENTE'">URGENTE</span>
              <p class="modal-fecha" v-if="animalSeleccionado.fecha_nacimiento">
                 <strong>Nacimiento:</strong> {{ animalSeleccionado.fecha_nacimiento }}
              </p>
              <div class="modal-desc"><p>{{ animalSeleccionado.descripcion }}</p></div>
              <div class="modal-acciones">
                <router-link :to="{ path: '/solicitud', query: { animal: animalSeleccionado.nombre }}">
                   <button class="btnRosa btn-grande">Adoptar a {{ animalSeleccionado.nombre }}</button>
                </router-link>
              </div>
           </div>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
/* --- 1. LAYOUT VERTICAL (Sobrescribe capaBlanca solo aquí) --- */
.vista-adopcion {
    display: flex !important;      /* Forzamos flex */
    flex-direction: column !important; /* Dirección columna (Arriba a abajo) */
    align-items: center;
    width: 100%;
}

.encabezado {
    text-align: center;
    margin-bottom: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.patita-titulo { width: 60px; margin-bottom: 0.5rem; }

/* --- 2. CONTENEDOR FLEX (Sustituye al Grid) --- */
.cards-container {
    display: flex;
    flex-wrap: wrap;       /* Si no caben, bajan a la siguiente línea */
    justify-content: center; /* Centrados en la pantalla */
    gap: 2rem;             /* Separación entre tarjetas */
    width: 100%;
    max-width: 1200px;
}

/* --- 3. TARJETA (Estilo Geobizi) --- */
.animal-card {
    width: 300px;  /* Ancho fijo base, igual que tu referencia */
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    border: 1px solid #eee;
    display: flex;
    flex-direction: column;
}

.animal-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

/* Imagen de la tarjeta */
.img-container {
    height: 220px;
    width: 100%;
    background-color: #f8f8f8;
    position: relative;
}
.img-container img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* Recorta para llenar */
    object-position: center top; 
}

.info-card {
    padding: 1.2rem;
    text-align: center;
    flex: 1; /* Para que todos los botones queden alineados abajo si quieres */
}
.info-card h3 { color: var(--darkPurple); margin-bottom: 0.5rem; }

.desc-corta {
    color: #666;
    font-size: 0.9rem;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* Cortar a 2 líneas */
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 1rem;
}

/* --- MODAL (POPUP) --- */
.modal-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.6); z-index: 1000;
    display: flex; justify-content: center; align-items: center;
    backdrop-filter: blur(5px);
    padding: 1rem;
}
.modal-content {
    background: white; width: 100%; max-width: 900px; max-height: 90vh;
    border-radius: 20px; position: relative; overflow-y: auto;
    box-shadow: 0 20px 50px rgba(0,0,0,0.3); animation: aparecer 0.3s ease-out;
}
.modal-grid { display: flex; flex-direction: row; }
.modal-img { flex: 1; min-height: 300px; background: #f0f0f0; }
.modal-img img { width: 100%; height: 100%; object-fit: cover; }
.modal-info { flex: 1; padding: 2rem; display: flex; flex-direction: column; }
.btn-cerrar {
    position: absolute; top: 15px; right: 20px; background: rgba(255,255,255,0.9);
    border: none; font-size: 2rem; cursor: pointer; border-radius: 50%;
    width: 40px; height: 40px; line-height: 1; z-index: 10;
}
.btn-grande { width: 100%; padding: 1rem; font-size: 1.1rem; }
.etiqueta-estado { background: #ff4757; color: white; padding: 0.3rem 0.8rem; border-radius: 5px; width: fit-content; margin-bottom: 1rem; font-weight: bold; font-size: 0.8rem;}
.etiqueta-urgente { position: absolute; top: 10px; right: 10px; background: #ff4757; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: bold; font-size: 0.8rem; }

/* --- RESPONSIVE (MÓVIL) --- */
@media (max-width: 768px) {
    /* En móvil, la tarjeta ocupa todo el ancho disponible */
    .animal-card { width: 100%; max-width: 400px; }
    
    /* Ajustes del modal en móvil */
    .modal-grid { flex-direction: column; }
    .modal-img { height: 250px; }
    .modal-content { width: 95%; margin: 10px; }
}

/* Animaciones y utilidades */
@keyframes aparecer { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.patita-animada { width: 60px; animation: bote 0.8s infinite alternate; margin: 0 auto; display: block;}
@keyframes bote { from { transform: translateY(0); } to { transform: translateY(-10px); } }
.loading-container { text-align: center; width: 100%; margin: 2rem 0; }
.placeholder { opacity: 0.5; padding: 2rem; object-fit: contain !important; }
</style>