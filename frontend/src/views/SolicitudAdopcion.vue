<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

// --- DATOS ---
const animal = ref(null)
const cuestionario = ref(null)   // preguntas de perro o de gato (las define el backend)
const respuestas = ref({})
const aceptaPrivacidad = ref(false)
const cargando = ref(true)
const errorCarga = ref(null)

const enviando = ref(false)
const mensajeExito = ref(false)
const error = ref(null)
const erroresCampo = ref({})

// Al cargar, buscamos el animal de la URL (?animal=id) y su cuestionario
onMounted(async () => {
  try {
    const { data } = await axios.get(`/api/animales/${route.query.animal}/`)
    animal.value = data
    cuestionario.value = (await axios.get(`/api/cuestionario/${data.especie}/`)).data
  } catch (e) {
    console.error(e)
    errorCarga.value = e.response?.status === 404
      ? 'No encontramos a este animal. Puede que ya haya sido adoptado.'
      : 'No se ha podido cargar el formulario. Inténtalo de nuevo en un rato.'
  } finally {
    cargando.value = false
  }
})

// Si el servidor rechaza algún campo, lo marcamos y llevamos la pantalla hasta él
const mostrarErroresCampo = async (errores) => {
  erroresCampo.value = errores
  await nextTick()
  document.querySelector('.campo.con-error')?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

const enviarFormulario = async () => {
  enviando.value = true
  error.value = null
  erroresCampo.value = {}

  try {
    await axios.post('/api/solicitudes-adopcion/', {
      animal: animal.value.id,
      respuestas: respuestas.value,
      acepta_privacidad: aceptaPrivacidad.value,
    })
    mensajeExito.value = true
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (e) {
    console.error(e)
    const errores = e.response?.data?.respuestas
    if (errores && typeof errores === 'object') {
      error.value = 'Revisa los campos marcados en rojo.'
      mostrarErroresCampo(errores)
    } else {
      error.value = 'Hubo un error al enviar. Por favor, escríbenos directamente a villapirritxanimaliak@gmail.com'
    }
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
        <p>Gracias por querer dar un hogar a <strong>{{ animal.nombre }}</strong>.</p>
        <p>El equipo de Villa Pirritx revisará tu cuestionario y te contactará pronto.</p>
        <button class="btnRosa" @click="router.push('/adopcion')">Volver a los animales</button>
      </div>

      <div v-else-if="cargando" class="exito-box">
        <img src="/iconos/patita.png" alt="Cargando" class="patita-animada">
        <p>Preparando el cuestionario...</p>
      </div>

      <div v-else-if="errorCarga" class="exito-box">
        <p>{{ errorCarga }}</p>
        <button class="btnRosa" @click="router.push('/adopcion')">Ver animales en adopción</button>
      </div>

      <div v-else class="form-container">
        <h2>Solicitud de Adopción</h2>
        <p class="subtitulo">Quieres adoptar a: <span class="nombre-animal">{{ animal.nombre }}</span></p>
        <p class="introduccion">{{ cuestionario.introduccion }}</p>
        <p class="nota">Los campos con * son obligatorios.</p>

        <form @submit.prevent="enviarFormulario">

          <fieldset v-for="seccion in cuestionario.secciones" :key="seccion.titulo" class="seccion">
            <legend>{{ seccion.titulo }}</legend>

            <div v-for="pregunta in seccion.preguntas" :key="pregunta.clave"
              :class="['campo', { 'con-error': erroresCampo[pregunta.clave] }]">
              <label :for="pregunta.clave">{{ pregunta.texto }}<span v-if="pregunta.obligatoria"> *</span></label>
              <textarea v-if="pregunta.larga" :id="pregunta.clave" v-model="respuestas[pregunta.clave]"
                :required="pregunta.obligatoria" rows="3" maxlength="3000"></textarea>
              <input v-else :id="pregunta.clave" :type="pregunta.tipo" v-model="respuestas[pregunta.clave]"
                :required="pregunta.obligatoria" maxlength="300" />
              <small v-if="erroresCampo[pregunta.clave]" class="error-campo">{{ erroresCampo[pregunta.clave] }}</small>
            </div>
          </fieldset>

          <label class="privacidad">
            <input type="checkbox" v-model="aceptaPrivacidad" required />
            <span>
              Acepto que el Refugio Villa Pirritx guarde estos datos para gestionar la adopción. No se cederán
              a nadie más y puedo pedir que se borren escribiendo a villapirritxanimaliak@gmail.com. *
            </span>
          </label>

          <p class="despedida">{{ cuestionario.despedida }}</p>

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
.form-container { max-width: 700px; margin: 0 auto; text-align: left; width: 100%; }
.subtitulo { text-align: center; margin-bottom: 1rem; color: #666; }
.nombre-animal { color: var(--darkPurple); font-weight: bold; font-size: 1.2rem; }
.introduccion { color: #555; line-height: 1.5; }
.nota { color: #888; font-size: 0.9rem; margin-bottom: 1.5rem; }

.seccion {
    border: none;
    padding: 0;
    margin: 0 0 2rem;
}
legend {
    width: 100%;
    font-size: 1.15rem;
    font-weight: bold;
    color: var(--darkPurple);
    border-bottom: 2px solid var(--lightPurple);
    padding-bottom: 0.4rem;
    margin-bottom: 1.2rem;
}

.campo { margin-bottom: 1.3rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: bold; color: var(--darkPurple); }
input, textarea {
    width: 100%;
    padding: 10px;
    border: 2px solid #eee;
    border-radius: 8px;
    font-size: 1rem;
    font-family: inherit;
}
input:focus, textarea:focus { border-color: var(--lightPurple); outline: none; }
.con-error input, .con-error textarea { border-color: red; }
.error-campo { color: red; }

.privacidad { display: flex; gap: 0.7rem; align-items: flex-start; font-weight: normal; color: #444; }
.privacidad input { width: auto; margin-top: 0.25rem; flex-shrink: 0; }
.despedida { color: #666; font-style: italic; margin: 1.5rem 0; }

.btnRosa { width: 100%; margin-top: 1rem; }
.btnRosa:disabled { background-color: #ccc; cursor: not-allowed; }

.exito-box { text-align: center; padding: 3rem; }
.patita-animada { width: 60px; margin-bottom: 1rem; animation: bote 1s infinite; }
.error-msg { color: red; margin-bottom: 1rem; text-align: center; }

@keyframes bote { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
</style>
