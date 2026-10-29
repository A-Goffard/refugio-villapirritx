<script setup>
import { ref, computed, onUnmounted } from 'vue'
import axios from 'axios'
import { esSesionCaducada } from '@/stores/auth'
import { hacerUrlSegura } from '@/utils/urls'
import { reducirImagen } from '@/utils/imagenes'
import ModalGestion from './ModalGestion.vue'

const MAX_DESCRIPCION = 600 // el mismo límite que el modelo Evento

// Si recibe un evento, lo edita; si no, crea uno nuevo
const props = defineProps({
    evento: { type: Object, default: null },
})
const emit = defineEmits(['guardado', 'cerrar', 'sesion-caducada'])

const form = ref({
    titulo: props.evento?.titulo ?? '',
    fecha: props.evento?.fecha ?? '',
    horario: props.evento?.horario ?? '',
    lugar: props.evento?.lugar ?? '',
    descripcion: props.evento?.descripcion ?? '',
})

// La imagen es opcional y no se recorta: suelen ser carteles y se muestran enteros
const imagenNueva = ref(null)
const quitarImagen = ref(false)
const previsualizacion = ref(null)
const preparandoImagen = ref(false)
const guardando = ref(false)
const errorMsg = ref('')

const imagenVisible = computed(() => {
    if (previsualizacion.value) return previsualizacion.value
    if (quitarImagen.value) return null
    return hacerUrlSegura(props.evento?.imagen)
})

const elegirImagen = async (evento) => {
    const archivo = evento.target.files[0]
    evento.target.value = ''
    if (!archivo) return
    preparandoImagen.value = true
    imagenNueva.value = await reducirImagen(archivo)
    if (previsualizacion.value) URL.revokeObjectURL(previsualizacion.value)
    previsualizacion.value = URL.createObjectURL(imagenNueva.value)
    quitarImagen.value = false
    preparandoImagen.value = false
}

const quitar = () => {
    imagenNueva.value = null
    if (previsualizacion.value) URL.revokeObjectURL(previsualizacion.value)
    previsualizacion.value = null
    quitarImagen.value = true
}

onUnmounted(() => {
    if (previsualizacion.value) URL.revokeObjectURL(previsualizacion.value)
})

const guardar = async () => {
    guardando.value = true
    errorMsg.value = ''

    const datos = new FormData()
    Object.entries(form.value).forEach(([campo, valor]) => datos.append(campo, valor ?? ''))
    if (imagenNueva.value) datos.append('imagen', imagenNueva.value)
    else if (quitarImagen.value) datos.append('imagen', '') // vacío = borrar la imagen

    try {
        const { data } = props.evento
            ? await axios.patch(`/api/eventos/${props.evento.id}/`, datos)
            : await axios.post('/api/eventos/', datos)
        emit('guardado', data)
    } catch (e) {
        console.error(e)
        if (esSesionCaducada(e)) {
            emit('sesion-caducada')
        } else if (e.response?.status === 413) {
            errorMsg.value = 'La imagen es demasiado grande. Prueba con otra.'
        } else if (e.response?.data?.imagen) {
            errorMsg.value = 'No se ha podido leer la imagen. Prueba con otra (JPG o PNG).'
        } else {
            errorMsg.value = 'No se ha podido guardar. Revisa la conexión e inténtalo de nuevo.'
        }
    } finally {
        guardando.value = false
    }
}
</script>

<template>
<ModalGestion :titulo="evento ? 'Editar evento' : 'Nuevo evento'" @cerrar="emit('cerrar')">
    <form @submit.prevent="guardar" class="mi-formulario">
        <div class="campo">
            <label for="titulo">Título</label>
            <input id="titulo" v-model="form.titulo" required maxlength="100" placeholder="Ej: Mercadillo solidario">
        </div>

        <div class="campo-doble">
            <div class="campo">
                <label for="fecha">Fecha</label>
                <input id="fecha" type="date" v-model="form.fecha" required>
            </div>
            <div class="campo">
                <label for="horario">Horario</label>
                <input id="horario" v-model="form.horario" required maxlength="100" placeholder="De 11:00 a 14:00">
            </div>
        </div>

        <div class="campo">
            <label for="lugar">Lugar</label>
            <input id="lugar" v-model="form.lugar" required maxlength="150" placeholder="Ej: Plaza de Sondika">
        </div>

        <div class="campo">
            <label for="descripcion">Descripción breve</label>
            <textarea id="descripcion" v-model="form.descripcion" rows="4" required :maxlength="MAX_DESCRIPCION"
                placeholder="Qué habrá, a qué se destina lo recaudado..."></textarea>
            <small>{{ form.descripcion.length }} / {{ MAX_DESCRIPCION }}</small>
        </div>

        <div class="campo">
            <span class="etiqueta">Imagen o cartel <span class="opcional">(opcional)</span></span>
            <label class="selector-foto">
                <img v-if="imagenVisible" :src="imagenVisible" alt="Imagen del evento">
                <span v-else class="sin-foto">🖼️</span>
                <span class="texto-foto">
                    {{ preparandoImagen ? 'Preparando imagen...' : (imagenVisible ? 'Cambiar imagen' : 'Añadir imagen') }}
                </span>
                <input type="file" accept="image/*" @change="elegirImagen" hidden>
            </label>
            <button v-if="imagenVisible" type="button" class="btn-enlace" @click="quitar">Quitar imagen</button>
        </div>

        <div v-if="errorMsg" class="error">{{ errorMsg }}</div>

        <button type="submit" class="btnMorado full-width" :disabled="guardando || preparandoImagen">
            {{ guardando ? 'Guardando...' : 'Guardar' }}
        </button>
    </form>
</ModalGestion>
</template>

<style scoped>
/* Los estilos comunes del formulario están en assets/gestion.css */
.campo-doble { display: flex; gap: 1rem; }
.campo-doble .campo { flex: 1; min-width: 0; }
@media (max-width: 480px) { .campo-doble { flex-direction: column; } }

.etiqueta { font-weight: bold; color: var(--darkPurple); font-size: 0.9rem; }

/* La imagen se ve entera (los carteles suelen ser verticales) */
.selector-foto img {
    width: 100%;
    max-height: 320px;
    object-fit: contain;
    border-radius: 0.6rem;
}
</style>
