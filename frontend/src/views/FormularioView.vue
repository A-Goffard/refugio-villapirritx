<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

// Datos del formulario
const form = ref({
    tipo: 'OTRO',
    nombre: '',
    email: '',
    telefono: '',
    mensaje: ''
})

const loading = ref(false)
const enviado = ref(false)
const errorMsg = ref('')

// Al cargar, miramos qué botón pulsaron (por la URL ?tipo=...)
onMounted(() => {
    if (route.query.tipo) {
        form.value.tipo = route.query.tipo
    }
})

// Diccionario para títulos bonitos
const titulos = {
    'ACOGIDA': 'Solicitud de Casa de Acogida',
    'VOLUNTARIADO': 'Solicitud de Voluntariado',
    'ADOPCION': 'Solicitud de Adopción',
    'DONACION': 'Donación de Material',
    'VIAJE': 'Viaje Solidario',
    'OTRO': 'Contactar'
}

const enviarFormulario = async () => {
    loading.value = true
    errorMsg.value = ''
    
    try {
        await axios.post('/api/solicitudes/', form.value)
        enviado.value = true
        // Scroll arriba suave
        window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (e) {
        console.error(e)
        errorMsg.value = "Hubo un error al enviar. Por favor, inténtalo de nuevo o escríbenos por redes sociales."
    } finally {
        loading.value = false
    }
}
</script>

<template>
<div class="body">
    <div class="capaBlanca centre">
        
        <div v-if="enviado" class="mensaje-exito">
            <img src="/iconos/patita.png" class="patita-animada" alt="Éxito">
            <h2>¡Mensaje Recibido!</h2>
            <p>Muchas gracias, {{ form.nombre }}.</p>
            <p>El equipo de Villa Pirritx ha recibido tu solicitud de <strong>{{ titulos[form.tipo] }}</strong>.</p>
            <p>Nos pondremos en contacto contigo lo antes posible.</p>
            <router-link to="/">
                <button class="btnRosa">Volver al inicio</button>
            </router-link>
        </div>

        <div v-else class="form-container">
            <h2>{{ titulos[form.tipo] || 'Formulario de Contacto' }}</h2>
            <p>Rellena tus datos y te contactaremos para explicarte los siguientes pasos.</p>

            <form @submit.prevent="enviarFormulario" class="mi-formulario">
                
                <div class="campo">
                    <label>Nombre Completo</label>
                    <input type="text" v-model="form.nombre" required placeholder="Ej: Ane García">
                </div>

                <div class="campo-doble">
                    <div class="campo">
                        <label>Email</label>
                        <input type="email" v-model="form.email" required placeholder="tucorreo@ejemplo.com">
                    </div>
                    <div class="campo">
                        <label>Teléfono</label>
                        <input type="tel" v-model="form.telefono" required placeholder="600 123 456">
                    </div>
                </div>

                <div class="campo">
                    <label>Asunto</label>
                    <select v-model="form.tipo">
                        <option value="ACOGIDA">Casa de Acogida</option>
                        <option value="ADOPCION">Adopción</option>
                        <option value="VOLUNTARIADO">Voluntariado</option>
                        <option value="DONACION">Donación Material</option>
                        <option value="VIAJE">Viaje Solidario</option>
                        <option value="OTRO">Otro tema</option>
                    </select>
                </div>

                <div class="campo">
                    <label>Mensaje / Dudas</label>
                    <textarea v-model="form.mensaje" rows="5" placeholder="Cuéntanos un poco sobre ti..."></textarea>
                </div>

                <div v-if="errorMsg" class="error">{{ errorMsg }}</div>

                <button type="submit" class="btnMorado full-width" :disabled="loading">
                    {{ loading ? 'Enviando...' : 'Enviar Solicitud' }}
                </button>
            </form>
        </div>
    </div>
</div>
</template>

<style scoped>
.form-container {
    max-width: 600px;
    width: 100%;
    margin: 2rem auto;
    padding: 2rem;
    background: var(--lightPurple); /* Fondo suave */
    border-radius: 1rem;
}

.mi-formulario {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-top: 2rem;
    text-align: left;
}

.campo {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.campo-doble {
    display: flex;
    gap: 1rem;
}
@media (max-width: 600px) { .campo-doble { flex-direction: column; } }

label { font-weight: bold; color: var(--darkPurple); font-size: 0.9rem; }

input, select, textarea {
    padding: 0.8rem;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: inherit;
}

input:focus, textarea:focus, select:focus {
    outline: 2px solid var(--pink);
    border-color: transparent;
}

.full-width { width: 100%; margin-top: 1rem; }

.mensaje-exito {
    text-align: center;
    padding: 3rem;
}

.patita-animada { width: 80px; animation: bote 1s infinite alternate; margin-bottom: 1rem; }
@keyframes bote { from { transform: translateY(0); } to { transform: translateY(-10px); } }

.error { color: red; font-weight: bold; text-align: center; }
</style>