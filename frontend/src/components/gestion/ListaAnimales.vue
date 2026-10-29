<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { esSesionCaducada } from '@/stores/auth'
import { hacerUrlSegura } from '@/utils/urls'
import AnimalFormulario from './AnimalFormulario.vue'
import { ESTADOS } from './estados'

const emit = defineEmits(['sesion-caducada'])

// --- DATOS ---
const animales = ref([])
const cargando = ref(true)
const errorMsg = ref('')
const filtro = ref('web')

const animalesFiltrados = computed(() => animales.value.filter((a) => {
    if (filtro.value === 'web') return ESTADOS[a.estado]?.enWeb
    if (filtro.value === 'fuera') return !ESTADOS[a.estado]?.enWeb
    return true
}))
const totalEnWeb = computed(() => animales.value.filter((a) => ESTADOS[a.estado]?.enWeb).length)

onMounted(async () => {
    try {
        const { data } = await axios.get('/api/animales/')
        animales.value = data
    } catch (e) {
        console.error(e)
        errorMsg.value = 'No se han podido cargar los animales.'
    } finally {
        cargando.value = false
    }
})

// --- FORMULARIO ---
// undefined = cerrado, null = animal nuevo, objeto = editar ese animal
const editando = ref(undefined)

const alGuardar = (guardado) => {
    const indice = animales.value.findIndex((a) => a.id === guardado.id)
    if (indice === -1) animales.value.unshift(guardado)
    else animales.value[indice] = guardado
    editando.value = undefined
}

// --- ACCIONES RÁPIDAS ---
const cambiarEstado = async (animal, estado) => {
    const anterior = animal.estado
    animal.estado = estado
    try {
        await axios.patch(`/api/animales/${animal.id}/`, { estado })
    } catch (e) {
        animal.estado = anterior
        if (esSesionCaducada(e)) return emit('sesion-caducada')
        alert('No se ha podido cambiar el estado. Inténtalo de nuevo.')
    }
}

const borrar = async (animal) => {
    if (!confirm(`¿Borrar a ${animal.nombre} para siempre?\n\nSi ha sido adoptado, mejor cambia su estado a "Adoptado".`)) return
    try {
        await axios.delete(`/api/animales/${animal.id}/`)
        animales.value = animales.value.filter((a) => a.id !== animal.id)
    } catch (e) {
        if (esSesionCaducada(e)) return emit('sesion-caducada')
        alert('No se ha podido borrar. Inténtalo de nuevo.')
    }
}
</script>

<template>
<div>
    <p class="resumen">{{ totalEnWeb }} animales en la página de adopción</p>

    <button class="btnMorado btn-nuevo" @click="editando = null">＋ Añadir animal</button>

    <div class="filtros">
        <button :class="{ activo: filtro === 'web' }" @click="filtro = 'web'">En la web</button>
        <button :class="{ activo: filtro === 'fuera' }" @click="filtro = 'fuera'">Acogida / adoptados</button>
        <button :class="{ activo: filtro === 'todos' }" @click="filtro = 'todos'">Todos</button>
    </div>

    <p v-if="cargando" class="aviso">Llamando a los animales...</p>
    <p v-else-if="errorMsg" class="aviso error">{{ errorMsg }}</p>
    <p v-else-if="animalesFiltrados.length === 0" class="aviso">No hay animales en esta lista.</p>

    <ul v-else class="lista">
        <li v-for="animal in animalesFiltrados" :key="animal.id" class="fila">
            <img v-if="animal.foto" :src="hacerUrlSegura(animal.foto)" :alt="animal.nombre" class="miniatura">
            <img v-else src="/logos/logo.png" alt="Sin foto" class="miniatura placeholder">

            <div class="datos">
                <strong>{{ animal.nombre }}</strong>
                <select :value="animal.estado" @change="cambiarEstado(animal, $event.target.value)"
                    :class="['estado', animal.estado.toLowerCase()]" :aria-label="`Estado de ${animal.nombre}`">
                    <option v-for="(estado, clave) in ESTADOS" :key="clave" :value="clave">{{ estado.texto }}</option>
                </select>
            </div>

            <div class="acciones">
                <button class="btnRosa" @click="editando = animal">Editar</button>
                <button class="btn-borrar" @click="borrar(animal)" :aria-label="`Borrar a ${animal.nombre}`">🗑</button>
            </div>
        </li>
    </ul>

    <AnimalFormulario v-if="editando !== undefined" :animal="editando"
        @guardado="alGuardar" @cerrar="editando = undefined" @sesion-caducada="emit('sesion-caducada')" />
</div>
</template>

<style scoped>
/* Los estilos de la lista están en assets/gestion.css */
.resumen { color: #666; margin-top: 1rem; }

.estado {
    width: fit-content;
    max-width: 100%;
    padding: 0.3rem 0.5rem;
    border-radius: 0.5rem;
    border: 1px solid #ddd;
    font-size: 0.85rem;
    font-weight: bold;
    background: white;
}

.estado.adopcion { background: #e9f9dc; }
.estado.urgente { background: #ffe0e3; color: #c0392b; }
.estado.acogida { background: #e3f8f9; }
.estado.adoptado { background: #eee; color: #666; }
</style>
