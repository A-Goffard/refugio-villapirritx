<script setup>
import { ref, computed, onUnmounted } from 'vue'
import axios from 'axios'
import { hacerUrlSegura } from '@/utils/urls'
import { reducirImagen } from '@/utils/imagenes'
import { ESTADOS } from './estados'

// Si recibe un animal, lo edita; si no, crea uno nuevo
const props = defineProps({
    animal: { type: Object, default: null },
})
const emit = defineEmits(['guardado', 'cerrar', 'sesion-caducada'])

const form = ref({
    nombre: props.animal?.nombre ?? '',
    estado: props.animal?.estado ?? 'ADOPCION',
    fecha_nacimiento: props.animal?.fecha_nacimiento ?? '',
    descripcion: props.animal?.descripcion ?? '',
})
const fotoNueva = ref(null)
const previsualizacion = ref(null)
const preparandoFoto = ref(false)
const guardando = ref(false)
const errorMsg = ref('')

const fotoVisible = computed(() => previsualizacion.value || hacerUrlSegura(props.animal?.foto))

const elegirFoto = async (evento) => {
    const archivo = evento.target.files[0]
    if (!archivo) return
    preparandoFoto.value = true
    fotoNueva.value = await reducirImagen(archivo)
    if (previsualizacion.value) URL.revokeObjectURL(previsualizacion.value)
    previsualizacion.value = URL.createObjectURL(fotoNueva.value)
    preparandoFoto.value = false
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
        if (e.response?.status === 403) {
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
<div class="modal-overlay" @click.self="emit('cerrar')">
    <div class="modal-content">
        <button class="btn-cerrar" type="button" @click="emit('cerrar')" aria-label="Cerrar">×</button>
        <h2>{{ animal ? `Editar a ${animal.nombre}` : 'Nuevo animal' }}</h2>

        <form @submit.prevent="guardar" class="mi-formulario">
            <label class="selector-foto">
                <img v-if="fotoVisible" :src="fotoVisible" alt="Foto del animal">
                <span v-else class="sin-foto">📷</span>
                <span class="texto-foto">
                    {{ preparandoFoto ? 'Preparando foto...' : (fotoVisible ? 'Cambiar foto' : 'Hacer o elegir foto') }}
                </span>
                <input type="file" accept="image/*" @change="elegirFoto" hidden>
            </label>

            <div class="campo">
                <label for="nombre">Nombre</label>
                <input id="nombre" v-model="form.nombre" required maxlength="50">
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

            <button type="submit" class="btnMorado full-width" :disabled="guardando || preparandoFoto">
                {{ guardando ? 'Guardando...' : 'Guardar' }}
            </button>
        </form>
    </div>
</div>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
}

.modal-content {
    background: white;
    width: 100%;
    max-width: 550px;
    max-height: 92vh;
    overflow-y: auto;
    border-radius: 20px;
    padding: 1.5rem;
    position: relative;
}

h2 { color: var(--darkPurple); margin: 0 3rem 1rem 0; }

.btn-cerrar {
    position: absolute;
    top: 0.8rem;
    right: 0.8rem;
    margin: 0;
    width: 44px;
    height: 44px;
    padding: 0;
    border: none;
    border-radius: 50%;
    background: var(--lightPurple);
    font-size: 1.8rem;
    line-height: 1;
}

.mi-formulario { display: flex; flex-direction: column; gap: 1.2rem; }

.selector-foto {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    border: 2px dashed var(--pink);
    border-radius: 1rem;
    cursor: pointer;
    background: #fdf7ff;
}

.selector-foto img {
    width: 100%;
    max-height: 260px;
    object-fit: cover;
    border-radius: 0.6rem;
}

.sin-foto { font-size: 3rem; }
.texto-foto { font-weight: bold; color: var(--darkPurple); }

.campo { display: flex; flex-direction: column; gap: 0.4rem; }

label { font-weight: bold; color: var(--darkPurple); font-size: 0.9rem; }
.opcional { font-weight: normal; color: #888; }
small { color: #666; }

input, select, textarea {
    padding: 0.8rem;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: inherit;
    background: white;
}

input:focus, textarea:focus, select:focus {
    outline: 2px solid var(--pink);
    border-color: transparent;
}

.full-width { width: 100%; padding: 0.9rem; font-size: 1rem; }

.error { color: red; font-weight: bold; text-align: center; }
</style>
