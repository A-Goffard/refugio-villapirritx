<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

// Datos del formulario
const formulario = ref({
  nombre: '',
  email: '',
  telefono: '',
  animal: '', // Aquí guardaremos el nombre del animal automáticamente
  mensaje: ''
})

const enviando = ref(false)
const mensajeExito = ref(false)
const error = ref(null)

// Al cargar, miramos si viene un animal en la URL
onMounted(() => {
  if (route.query.animal) {
    formulario.value.animal = route.query.animal
  }
})

// Función para enviar
const enviarFormulario = async () => {
  enviando.value = true
  error.value = null
  
  try {
    // Enviamos los datos a tu Django
    await axios.post('/api/enviar-adopcion/', formulario.value)
    mensajeExito.value = true
    
    // Opcional: Volver al listado después de 3 segundos
    setTimeout(() => {
      router.push('/adopcion')
    }, 4000)
    
  } catch (e) {
    console.error(e)
    error.value = "Hubo un error al enviar. Por favor, escríbenos directamente por email."
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <div class="body">
    <div class="capaBlanca centre">
      
      <div v-if="mensajeExito" class="exito-box">
        <img src="/iconos/patita.png" alt="Éxito" class="patita-animada">
        <h2>¡Solicitud Recibida!</h2>
        <p>Gracias por querer dar un hogar a <strong>{{ formulario.animal }}</strong>.</p>
        <p>El equipo de Villa Pirritx te contactará pronto.</p>
        <button class="btnRosa" @click="router.push('/adopcion')">Volver a los animales</button>
      </div>

      <div v-else class="form-container">
        <h2>Solicitud de Adopción</h2>
        <p class="subtitulo">Estás preguntando por: <span class="nombre-animal">{{ formulario.animal }}</span></p>

        <form @submit.prevent="enviarFormulario">
          
          <div class="campo">
            <label>Tu Nombre *</label>
            <input type="text" v-model="formulario.nombre" required placeholder="Ej: Aintzane" />
          </div>

          <div class="campo">
            <label>Tu Email *</label>
            <input type="email" v-model="formulario.email" required placeholder="tucorreo@email.com" />
          </div>

          <div class="campo">
            <label>Teléfono *</label>
            <input type="tel" v-model="formulario.telefono" required placeholder="600 000 000" />
          </div>

          <div class="campo">
            <label>Cuéntanos un poco sobre ti *</label>
            <textarea v-model="formulario.mensaje" required rows="4" placeholder="¿Tienes más animales? ¿Vives en piso o casa? ¿Hay niñas o niños en tu casa?"></textarea>
          </div>

          <div v-if="error" class="error-msg">{{ error }}</div>

          <button type="submit" class="btnRosa" :disabled="enviando">
            {{ enviando ? 'Enviando...' : 'Enviar Solicitud' }}
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<style scoped>
.form-container { max-width: 600px; margin: 0 auto; text-align: left; }
.subtitulo { text-align: center; margin-bottom: 2rem; color: #666; }
.nombre-animal { color: var(--darkPurple); font-weight: bold; font-size: 1.2rem; }

.campo { margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--darkPurple); }
input, textarea {
    width: 100%;
    padding: 10px;
    border: 2px solid #eee;
    border-radius: 8px;
    font-size: 1rem;
}
input:focus, textarea:focus { border-color: var(--lightPurple); outline: none; }

.btnRosa { width: 100%; margin-top: 1rem; }
.btnRosa:disabled { background-color: #ccc; cursor: not-allowed; }

.exito-box { text-align: center; padding: 3rem; }
.patita-animada { width: 60px; margin-bottom: 1rem; animation: bote 1s infinite; }
.error-msg { color: red; margin-bottom: 1rem; text-align: center; }

@keyframes bote { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
</style>