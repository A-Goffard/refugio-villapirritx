<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { esSesionCaducada } from '@/stores/auth'
import SolicitudDetalle from './SolicitudDetalle.vue'

const emit = defineEmits(['sesion-caducada'])

// --- DATOS ---
const solicitudes = ref([])
const cargando = ref(true)
const errorMsg = ref('')
const filtro = ref('pendientes')

const pendientes = computed(() => solicitudes.value.filter((s) => !s.gestionada))
const solicitudesFiltradas = computed(() => {
    if (filtro.value === 'pendientes') return pendientes.value
    if (filtro.value === 'gestionadas') return solicitudes.value.filter((s) => s.gestionada)
    return solicitudes.value
})

onMounted(async () => {
    try {
        const { data } = await axios.get('/api/solicitudes-adopcion/')
        solicitudes.value = data
    } catch (e) {
        console.error(e)
        if (esSesionCaducada(e)) return emit('sesion-caducada')
        errorMsg.value = 'No se han podido cargar las solicitudes.'
    } finally {
        cargando.value = false
    }
})

// La fecha llega con hora (no es una fecha 'AAAA-MM-DD' como la de los eventos)
const fechaCorta = (fecha) => new Date(fecha).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })

// --- ACCIONES ---
const abierta = ref(null)

const cambiarGestionada = async (solicitud, gestionada) => {
    solicitud.gestionada = gestionada
    try {
        await axios.patch(`/api/solicitudes-adopcion/${solicitud.id}/`, { gestionada })
    } catch (e) {
        solicitud.gestionada = !gestionada
        if (esSesionCaducada(e)) return emit('sesion-caducada')
        alert('No se ha podido guardar el cambio. Inténtalo de nuevo.')
    }
}

const borrar = async (solicitud) => {
    if (!confirm(`¿Borrar la solicitud de ${solicitud.nombre} para siempre?\n\nSi solo está resuelta, mejor márcala como gestionada.`)) return
    try {
        await axios.delete(`/api/solicitudes-adopcion/${solicitud.id}/`)
        solicitudes.value = solicitudes.value.filter((s) => s.id !== solicitud.id)
    } catch (e) {
        if (esSesionCaducada(e)) return emit('sesion-caducada')
        alert('No se ha podido borrar. Inténtalo de nuevo.')
    }
}
</script>

<template>
<div>
    <p class="resumen">Cuestionarios de adopción enviados desde la web. También os llegan por email con el PDF.</p>

    <div class="filtros">
        <button :class="{ activo: filtro === 'pendientes' }" @click="filtro = 'pendientes'">Pendientes ({{ pendientes.length }})</button>
        <button :class="{ activo: filtro === 'gestionadas' }" @click="filtro = 'gestionadas'">Gestionadas</button>
        <button :class="{ activo: filtro === 'todas' }" @click="filtro = 'todas'">Todas</button>
    </div>

    <p v-if="cargando" class="aviso">Cargando solicitudes...</p>
    <p v-else-if="errorMsg" class="aviso error">{{ errorMsg }}</p>
    <p v-else-if="solicitudesFiltradas.length === 0" class="aviso">No hay solicitudes en esta lista.</p>

    <ul v-else class="lista">
        <li v-for="solicitud in solicitudesFiltradas" :key="solicitud.id" :class="['fila', { hecha: solicitud.gestionada }]">
            <span class="miniatura icono">{{ solicitud.especie === 'GATO' ? '🐱' : '🐶' }}</span>

            <div class="datos">
                <strong>{{ solicitud.nombre }}</strong>
                <span class="detalle">Para {{ solicitud.nombre_animal }} · {{ fechaCorta(solicitud.fecha) }}</span>
            </div>

            <div class="acciones">
                <button class="btnRosa" @click="abierta = solicitud">Ver</button>
                <button class="btn-borrar" @click="borrar(solicitud)" :aria-label="`Borrar la solicitud de ${solicitud.nombre}`">🗑</button>
            </div>
        </li>
    </ul>

    <SolicitudDetalle v-if="abierta" :solicitud="abierta"
        @cambiar-gestionada="cambiarGestionada" @cerrar="abierta = null" />
</div>
</template>

<style scoped>
/* Los estilos de la lista están en assets/gestion.css */
.resumen { color: #666; margin-top: 1rem; }

.icono {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    background: var(--lightPurple);
}

.hecha { opacity: 0.6; }

.detalle {
    color: #666;
    font-size: 0.85rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
