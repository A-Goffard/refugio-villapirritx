<script setup>
import { ref, computed, onUnmounted } from 'vue'
import axios from 'axios'
import { hacerUrlSegura } from '@/utils/urls'
import { ESTADOS } from './estados'
import RecortadorFoto from './RecortadorFoto.vue'
import ModalGestion from './ModalGestion.vue'
import { esSesionCaducada } from '@/stores/auth'

// Si recibe un animal, lo edita; si no, crea uno nuevo
const props = defineProps({
    animal: { type: Object, default: null },
})
const emit = defineEmits(['guardado', 'cerrar', 'sesion-caducada'])

const form = ref({
    nombre: props.animal?.nombre ?? '',
    especie: props.animal?.especie ?? 'PERRO',
    estado: props.animal?.estado ?? 'ADOPCION',
    fecha_nacimiento: props.animal?.fecha_nacimiento ?? '',
    descripcion: props.animal?.descripcion ?? '',
})
const fotoOriginal = ref(null)   // la foto tal cual sale del móvil (para poder reencuadrarla)
const recortando = ref(false)
const fotoNueva = ref(null)      // la foto ya recortada que se subirá
const previsualizacion = ref(null)
const guardando = ref(false)
const errorMsg = ref('')

const fotoVisible = computed(() => previsualizacion.value || hacerUrlSegura(props.animal?.foto))

const elegirFoto = (evento) => {
    const archivo = evento.target.files[0]
    evento.target.value = '' // para poder volver a elegir la misma foto
    if (!archivo) return
    fotoOriginal.value = archivo
    recortando.value = true
}

const usarFoto = (archivo) => {
    fotoNueva.value = archivo
    if (previsualizacion.value) URL.revokeObjectURL(previsualizacion.value)
    previsualizacion.value = URL.createObjectURL(archivo)
    recortando.value = false
}

// Si el navegador no puede abrir la foto para recortarla, se sube entera (el servidor la reduce)
const fotoSinRecortar = () => {
    usarFoto(fotoOriginal.value)
    fotoOriginal.value = null
}

const cancelarRecorte = () => {
    recortando.value = false
    if (!fotoNueva.value) fotoOriginal.value = null
}

onUnmounted(() => {
    if (previsualizacion.value) URL.revokeObjectURL(previsualizacion.value)
})

const guardar = async () => {
    guardando.value = true
    errorMsg.value = ''

    const datos = new FormData()
    Object.entries(form.value).forEach(([campo, valor]) => datos.append(campo, valor ?? ''))
    if (fotoNueva.value) datos.append('foto', fotoNueva.value)

    try {
        const { data } = props.animal
            ? await axios.patch(`/api/animales/${props.animal.id}/`, datos)
            : await axios.post('/api/animales/', datos)
        emit('guardado', data)
    } catch (e) {
        console.error(e)
        if (esSesionCaducada(e)) {
            emit('sesion-caducada')
        } else if (e.response?.status === 413) {
            errorMsg.value = 'La foto es demasiado grande. Prueba con otra.'
        } else if (e.response?.data?.foto) {
            errorMsg.value = 'No se ha podido leer la foto. Prueba con otra (JPG o PNG).'
        } else {
            errorMsg.value = 'No se ha podido guardar. Revisa la conexión e inténtalo de nuevo.'
        }
    } finally {
        guardando.value = false
    }
}
</script>

<template>
<ModalGestion :titulo="animal ? `Editar a ${animal.nombre}` : 'Nuevo animal'" @cerrar="emit('cerrar')">
    <RecortadorFoto v-if="recortando" :archivo="fotoOriginal"
        @listo="usarFoto" @cancelar="cancelarRecorte" @error="fotoSinRecortar" />

    <form v-show="!recortando" @submit.prevent="guardar" class="mi-formulario">
        <div class="foto">
            <label class="selector-foto">
                <img v-if="fotoVisible" :src="fotoVisible" alt="Foto del animal">
                <span v-else class="sin-foto">📷</span>
                <span class="texto-foto">{{ fotoVisible ? 'Cambiar foto' : 'Hacer o elegir foto' }}</span>
                <input type="file" accept="image/*" @change="elegirFoto" hidden>
            </label>
            <button v-if="fotoOriginal" type="button" class="btn-enlace" @click="recortando = true">
                Volver a encuadrar
            </button>
        </div>

        <div class="campo">
            <label for="nombre">Nombre</label>
            <input id="nombre" v-model="form.nombre" required maxlength="50">
        </div>

        <div class="campo">
            <label for="especie">Especie</label>
            <select id="especie" v-model="form.especie">
                <option value="PERRO">Perro</option>
                <option value="GATO">Gato</option>
            </select>
            <small>Decide qué cuestionario de adopción se pide en la web.</small>
        </div>

        <div class="campo">
            <label for="estado">Estado</label>
            <select id="estado" v-model="form.estado">
                <option v-for="(estado, clave) in ESTADOS" :key="clave" :value="clave">{{ estado.texto }}</option>
            </select>
            <small>{{ ESTADOS[form.estado].enWeb ? 'Aparecerá en la página de adopción.' : 'No aparecerá en la página de adopción.' }}</small>
        </div>

        <div class="campo">
            <label for="fecha">Fecha de nacimiento <span class="opcional">(opcional)</span></label>
            <input id="fecha" type="date" v-model="form.fecha_nacimiento">
        </div>

        <div class="campo">
            <label for="descripcion">Descripción e historia</label>
            <textarea id="descripcion" v-model="form.descripcion" rows="6" required
                placeholder="Cómo es, cómo llegó al refugio, con quién se lleva bien..."></textarea>
        </div>

        <div v-if="errorMsg" class="error">{{ errorMsg }}</div>

        <button type="submit" class="btnMorado full-width" :disabled="guardando">
            {{ guardando ? 'Guardando...' : 'Guardar' }}
        </button>
    </form>
</ModalGestion>
</template>

<style scoped>
/* Los estilos comunes del formulario están en assets/gestion.css */

/* Mismo formato que la tarjeta de la web (PROPORCION_FOTO) */
.selector-foto img {
    width: 100%;
    aspect-ratio: 4 / 3;
    object-fit: cover;
    border-radius: 0.6rem;
}

.foto { display: flex; flex-direction: column; align-items: center; }
</style>
