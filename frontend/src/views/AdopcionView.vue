<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Variables de datos
const animales = ref([])
const cargando = ref(true)
const error = ref(null)

// --- NUEVO: Lógica para la Ventana Modal ---
const animalSeleccionado = ref(null) // Guardará el animal que el usuario está mirando

const abrirModal = (animal) => {
  animalSeleccionado.value = animal
  // Evitar que el fondo se mueva al hacer scroll
  document.body.style.overflow = 'hidden'
}

const cerrarModal = () => {
  animalSeleccionado.value = null
  // Devolver el scroll a la normalidad
  document.body.style.overflow = 'auto'
}
// -------------------------------------------

onMounted(async () => {
  try {
    const response = await axios.get('/api/animales/')
    animales.value = response.data.filter(a => a.estado === 'ADOPCION' || a.estado === 'URGENTE')
  } catch (e) {
    console.error(e)
    error.value = "Hubo un problema cargando los peludos. Inténtalo más tarde."
  } finally {
    cargando.value = false
  }
})
</script>

<template>
  <div class="body">
<div class="capaBlanca layout-vertical">
       
       <div class="centre encabezado">
          <img src="/iconos/patita.png" class="patita-titulo" alt="huella">
          <h2>Animales en Adopción</h2>
          <p>Haz clic en su foto para conocer su historia.</p>
       </div>

       <div v-if="cargando" class="centre loading-container">
          <img src="/iconos/patita.png" class="patita-animada" alt="Cargando...">
          <p>Llamando a los animales...</p>
       </div>

       <div v-else-if="error" class="textCentre error-msg">
          <p>{{ error }}</p>
       </div>

       <div v-else-if="animales.length === 0" class="textCentre">
          <p>¡Vaya! Ahora mismo no hay animales publicados en adopción.</p>
       </div>

       <div v-else class="animal-grid">
          <div v-for="animal in animales" :key="animal.id" class="animal-card" @click="abrirModal(animal)">
              
              <div class="img-container">
                  <img v-if="animal.foto" :src="animal.foto" :alt="animal.nombre" />
                  <img v-else src="/logos/logo.png" alt="Sin foto" class="placeholder" />
                  
                  <span v-if="animal.estado === 'URGENTE'" class="etiqueta-urgente">¡URGENTE!</span>
              </div>

              <div class="info-resumida">
                  <h3>{{ animal.nombre }}</h3>
                  <p class="desc-corta">{{ animal.descripcion }}</p>
                  <button class="btnMorado">Ver detalles +</button>
              </div>
          </div>
       </div>
    </div>

    <div v-if="animalSeleccionado" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal-content">
        <button class="btn-cerrar" @click="cerrarModal">x</button>
        
        <div class="modal-grid">
           <div class="modal-img">
              <img v-if="animalSeleccionado.foto" :src="animalSeleccionado.foto" :alt="animalSeleccionado.nombre">
              <img v-else src="/logos/logo.png" class="placeholder">
           </div>

           <div class="modal-info">
              <h2>{{ animalSeleccionado.nombre }}</h2>
              <span class="etiqueta-estado" v-if="animalSeleccionado.estado === 'URGENTE'">Caso Urgente</span>
              
              <p class="modal-fecha" v-if="animalSeleccionado.fecha_nacimiento">
                 <strong>Nacimiento:</strong> {{ animalSeleccionado.fecha_nacimiento }}
              </p>
              
              <div class="modal-desc">
                 <p>{{ animalSeleccionado.descripcion }}</p>
              </div>

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
/* --- GRID PRINCIPAL --- */
.patita-titulo{
    width: 80px;
    margin-bottom: 1rem;
}
.layout-vertical {
    display: flex;
    flex-direction: column; /* Pone los elementos uno debajo de otro */
    align-items: center;    /* Los centra horizontalmente */
    justify-content: flex-start;
    width: 100%;
}

.encabezado {
    margin-bottom: 3rem; /* Un poco de aire antes de las fotos */
    text-align: center;
}
.animal-grid {
    display: grid;
    /* Tarjetas más pequeñas (mínimo 250px) */
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 2rem;
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

.animal-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    cursor: pointer; /* Manita al pasar por encima */
    border: 1px solid #eee;
}

.animal-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

/* Arreglo de IMAGEN ALARGADA */
.img-container {
    height: 200px; /* Altura fija más pequeña */
    width: 100%;
    background-color: #f8f8f8;
    position: relative;
}

.img-container img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* CLAVE: Recorta la imagen para llenar el hueco sin deformar */
    object-position: center top; /* Centra la imagen priorizando la parte de arriba (la cara del animal) */
}

.info-resumida {
    padding: 1rem;
    text-align: center;
}

.info-resumida h3 {
    margin: 0 0 0.5rem 0;
    color: var(--darkPurple);
}

.desc-corta {
    color: #666;
    font-size: 0.9rem;
    /* Cortar texto a 2 líneas */
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 1rem;
}

.btn-ver-mas {
    background: transparent;
    border: 1px solid var(--lightPurple);
    color: var(--lightPurple);
    padding: 0.4rem 1rem;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: 0.2s;
}
.animal-card:hover .btn-ver-mas {
    background: var(--lightPurple);
    color: white;
}

/* --- ESTILOS DEL MODAL (POPUP) --- */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.6); /* Fondo oscuro transparente */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 1rem;
    backdrop-filter: blur(5px); /* Efecto borroso de fondo */
}

.modal-content {
    background: white;
    width: 100%;
    max-width: 900px;
    max-height: 90vh; /* Máximo el 90% de la altura de la pantalla */
    border-radius: 20px;
    position: relative;
    overflow-y: auto; /* Scroll si es muy alto */
    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    animation: aparecer 0.3s ease-out;
}

.modal-grid {
    display: flex;
    flex-direction: row; /* Imagen a la izq, texto a la dcha */
}

/* En móviles, poner uno debajo de otro */
@media (max-width: 768px) {
    .modal-grid { flex-direction: column; }
    .modal-img { height: 250px; }
}

.modal-img {
    flex: 1;
    background: #f0f0f0;
    min-height: 300px;
}
.modal-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.modal-info {
    flex: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
}

.modal-info h2 {
    color: var(--darkPurple);
    margin-top: 0;
    font-size: 2rem;
}

.modal-desc {
    margin: 1.5rem 0;
    line-height: 1.6;
    color: #444;
    font-size: 1.05rem;
    white-space: pre-line; /* Respeta los saltos de línea del texto original */
}

.btn-cerrar {
    position: absolute;
    top: 15px;
    right: 20px;
    background: rgba(255,255,255,0.8);
    border: none;
    font-size: 2rem;
    cursor: pointer;
    line-height: 1;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    z-index: 10;
    padding: 0;
}

.btn-grande {
    width: 100%;
    padding: 1rem;
    font-size: 1.1rem;
}

.etiqueta-estado {
    display: inline-block;
    background: #ff4757;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 5px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-bottom: 1rem;
    width: fit-content;
}

/* Animación simple */
@keyframes aparecer {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* Otros estilos generales */
.placeholder { opacity: 0.5; padding: 2rem; object-fit: contain !important; }
.patita-animada { width: 60px; animation: bote 0.8s infinite alternate ease-in-out; }
.etiqueta-urgente { position: absolute; top: 10px; right: 10px; background-color: #ff4757; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: bold; font-size: 0.8rem; }
.centre { text-align: center; }
.textCentre { text-align: center; }
</style>