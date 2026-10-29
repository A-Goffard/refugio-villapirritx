<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ModalGestion from './ModalGestion.vue'

// Muestra el cuestionario de una solicitud con las preguntas en el mismo orden que el PDF
const props = defineProps({
    solicitud: { type: Object, required: true },
})
const emit = defineEmits(['cerrar', 'cambiar-gestionada'])

const cuestionario = ref(null)
const errorMsg = ref('')

onMounted(async () => {
    try {
        const { data } = await axios.get(`/api/cuestionario/${props.solicitud.especie}/`)
        cuestionario.value = data
    } catch (e) {
        console.error(e)
        errorMsg.value = 'No se ha podido cargar el cuestionario. Puedes verlo en el PDF.'
    }
})
</script>

<template>
<ModalGestion :titulo="`${solicitud.nombre} → ${solicitud.nombre_animal}`" @cerrar="emit('cerrar')">
    <div class="contacto">
        <a :href="`tel:${solicitud.telefono}`">📞 {{ solicitud.telefono }}</a>
        <a :href="`mailto:${solicitud.email}`">✉️ {{ solicitud.email }}</a>
    </div>

    <div class="botones">
        <a class="btnMorado boton-pdf" :href="`/api/solicitudes-adopcion/${solicitud.id}/pdf/`" target="_blank">
            📄 Ver / imprimir PDF
        </a>
        <label class="gestionada">
            <input type="checkbox" :checked="solicitud.gestionada"
                @change="emit('cambiar-gestionada', solicitud, $event.target.checked)">
            Ya gestionada
        </label>
    </div>

    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    <p v-else-if="!cuestionario" class="aviso">Cargando respuestas...</p>

    <section v-else v-for="seccion in cuestionario.secciones" :key="seccion.titulo" class="seccion">
        <h3>{{ seccion.titulo }}</h3>
        <dl>
            <template v-for="pregunta in seccion.preguntas" :key="pregunta.clave">
                <dt>{{ pregunta.texto }}</dt>
                <dd :class="{ vacia: !solicitud.respuestas[pregunta.clave] }">
                    {{ solicitud.respuestas[pregunta.clave] || 'Sin respuesta' }}
                </dd>
            </template>
        </dl>
    </section>
</ModalGestion>
</template>

<style scoped>
.contacto { display: flex; flex-wrap: wrap; gap: 0.5rem 1.2rem; margin-bottom: 1rem; }
.contacto a { color: var(--darkPurple); font-weight: bold; word-break: break-all; }

.botones {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.8rem 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--lightPurple);
}
.boton-pdf { margin: 0; padding: 0.7rem 1rem; text-decoration: none; display: inline-block; }
.gestionada { display: flex; align-items: center; gap: 0.4rem; font-weight: bold; color: var(--darkPurple); }
.gestionada input { width: 1.2rem; height: 1.2rem; }

.seccion h3 { color: var(--darkPurple); font-size: 1rem; margin: 1.3rem 0 0.5rem; }
dt { font-weight: bold; font-size: 0.85rem; color: #444; margin-top: 0.7rem; }
dd { margin: 0.2rem 0 0; white-space: pre-line; }
dd.vacia { color: #aaa; font-style: italic; }
</style>
