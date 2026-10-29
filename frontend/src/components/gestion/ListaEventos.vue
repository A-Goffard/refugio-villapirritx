<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { esSesionCaducada } from '@/stores/auth'
import { hacerUrlSegura } from '@/utils/urls'
import { formatearFecha, hoy } from '@/utils/fechas'
import EventoFormulario from './EventoFormulario.vue'

const emit = defineEmits(['sesion-caducada'])

// --- DATOS ---
const eventos = ref([])
const cargando = ref(true)
const errorMsg = ref('')
const filtro = ref('proximos')

// Los próximos, del más cercano al más lejano; los pasados, del más reciente al más antiguo
const proximos = computed(() => eventos.value
    .filter((e) => e.fecha >= hoy())
    .sort((a, b) => a.fecha.localeCompare(b.fecha)))
const pasados = computed(() => eventos.value
    .filter((e) => e.fecha < hoy())
    .sort((a, b) => b.fecha.localeCompare(a.fecha)))
const eventosFiltrados = computed(() => (filtro.value === 'proximos' ? proximos.value : pasados.value))

onMounted(async () => {
    try {
        const { data } = await axios.get('/api/eventos/')
        eventos.value = data
    } catch (e) {
        console.error(e)
        errorMsg.value = 'No se han podido cargar los eventos.'
    } finally {
        cargando.value = false
    }
})

const fechaCorta = (fecha) => formatearFecha(fecha, { weekday: 'short', day: 'numeric', month: 'short' })

// --- FORMULARIO ---
// undefined = cerrado, null = evento nuevo, objeto = editar ese evento
const editando = ref(undefined)

const alGuardar = (guardado) => {
    const indice = eventos.value.findIndex((e) => e.id === guardado.id)
    if (indice === -1) eventos.value.push(guardado)
    else eventos.value[indice] = guardado
    editando.value = undefined
}

const borrar = async (evento) => {
    if (!confirm(`¿Borrar el evento "${evento.titulo}"?`)) return
    try {
        await axios.delete(`/api/eventos/${evento.id}/`)
        eventos.value = eventos.value.filter((e) => e.id !== evento.id)
    } catch (e) {
        if (esSesionCaducada(e)) return emit('sesion-caducada')
        alert('No se ha podido borrar. Inténtalo de nuevo.')
    }
}
</script>

<template>
<div>
    <p class="resumen">Los eventos pasados dejan de verse en la web automáticamente.</p>

    <button class="btnMorado btn-nuevo" @click="editando = null">＋ Añadir evento</button>

    <div class="filtros">
        <button :class="{ activo: filtro === 'proximos' }" @click="filtro = 'proximos'">Próximos ({{ proximos.length }})</button>
        <button :class="{ activo: filtro === 'pasados' }" @click="filtro = 'pasados'">Pasados ({{ pasados.length }})</button>
    </div>

    <p v-if="cargando" class="aviso">Cargando eventos...</p>
    <p v-else-if="errorMsg" class="aviso error">{{ errorMsg }}</p>
    <p v-else-if="eventosFiltrados.length === 0" class="aviso">No hay eventos en esta lista.</p>

    <ul v-else class="lista">
        <li v-for="evento in eventosFiltrados" :key="evento.id" class="fila">
            <img v-if="evento.imagen" :src="hacerUrlSegura(evento.imagen)" :alt="evento.titulo" class="miniatura">
            <span v-else class="miniatura sin-imagen">📅</span>

            <div class="datos">
                <strong>{{ evento.titulo }}</strong>
                <span class="detalle">{{ fechaCorta(evento.fecha) }} · {{ evento.lugar }}</span>
            </div>

            <div class="acciones">
                <button class="btnRosa" @click="editando = evento">Editar</button>
                <button class="btn-borrar" @click="borrar(evento)" :aria-label="`Borrar ${evento.titulo}`">🗑</button>
            </div>
        </li>
    </ul>

    <EventoFormulario v-if="editando !== undefined" :evento="editando"
        @guardado="alGuardar" @cerrar="editando = undefined" @sesion-caducada="emit('sesion-caducada')" />
</div>
</template>

<style scoped>
/* Los estilos de la lista están en assets/gestion.css */
.resumen { color: #666; margin-top: 1rem; }

.sin-imagen {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    background: var(--lightPurple);
}

.detalle {
    color: #666;
    font-size: 0.85rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
