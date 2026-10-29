<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { hacerUrlSegura } from '@/utils/urls'
import AnimalFormulario from '@/components/gestion/AnimalFormulario.vue'
import { ESTADOS } from '@/components/gestion/estados'

const auth = useAuthStore()
const router = useRouter()

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

const cargar = async () => {
    try {
        const { data } = await axios.get('/api/animales/')
        animales.value = data
    } catch (e) {
        console.error(e)
        errorMsg.value = 'No se han podido cargar los animales.'
    } finally {
        cargando.value = false
    }
}
onMounted(cargar)

// --- SESIÓN ---
const salir = async () => {
    await auth.cerrarSesion()
    router.push('/')
}

const sesionCaducada = () => {
    auth.sesionCaducada()
    router.push({ name: 'acceso', query: { siguiente: '/gestion' } })
}

// --- FORMULARIO (MODAL) ---
// undefined = cerrado, null = animal nuevo, objeto = editar ese animal
const editando = ref(undefined)

const abrirFormulario = (animal = null) => {
    editando.value = animal
    document.body.style.overflow = 'hidden'
}

const cerrarFormulario = () => {
    editando.value = undefined
    document.body.style.overflow = 'auto'
}

onUnmounted(() => {
    document.body.style.overflow = 'auto'
})

const alGuardar = (guardado) => {
    const indice = animales.value.findIndex((a) => a.id === guardado.id)
    if (indice === -1) animales.value.unshift(guardado)
    else animales.value[indice] = guardado
    cerrarFormulario()
}

// --- ACCIONES RÁPIDAS ---
const cambiarEstado = async (animal, estado) => {
    const anterior = animal.estado
    animal.estado = estado
    try {
        await axios.patch(`/api/animales/${animal.id}/`, { estado })
    } catch (e) {
        animal.estado = anterior
        if (e.response?.status === 403) return sesionCaducada()
        alert('No se ha podido cambiar el estado. Inténtalo de nuevo.')
    }
}

const borrar = async (animal) => {
    if (!confirm(`¿Borrar a ${animal.nombre} para siempre?\n\nSi ha sido adoptado, mejor cambia su estado a "Adoptado".`)) return
    try {
        await axios.delete(`/api/animales/${animal.id}/`)
        animales.value = animales.value.filter((a) => a.id !== animal.id)
    } catch (e) {
        if (e.response?.status === 403) return sesionCaducada()
        alert('No se ha podido borrar. Inténtalo de nuevo.')
    }
}
</script>

<template>
<div class="body">
    <div class="capaBlanca vista-gestion">

        <div class="cabecera">
            <div>
                <h2>Panel del refugio</h2>
                <p class="saludo">Hola, {{ auth.usuario }} · {{ totalEnWeb }} animales en la web</p>
            </div>
            <button class="btnBlanco btn-salir" @click="salir">Salir</button>
        </div>

        <button class="btnMorado btn-nuevo" @click="abrirFormulario()">＋ Añadir animal</button>

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
                    <button class="btnRosa" @click="abrirFormulario(animal)">Editar</button>
                    <button class="btn-borrar" @click="borrar(animal)" :aria-label="`Borrar a ${animal.nombre}`">🗑</button>
                </div>
            </li>
        </ul>
    </div>

    <AnimalFormulario v-if="editando !== undefined" :animal="editando"
        @guardado="alGuardar" @cerrar="cerrarFormulario" @sesion-caducada="sesionCaducada" />
</div>
</template>

<style scoped>
.vista-gestion {
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch;
    max-width: 700px;
    width: 100%;
    margin: 0 auto;
    padding: 1.5rem 1rem;
}

.cabecera {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.cabecera h2 { color: var(--darkPurple); margin: 0; }
.saludo { color: #666; margin: 0.3rem 0 0; }
.btn-salir { margin: 0; }

.btn-nuevo {
    width: 100%;
    padding: 1rem;
    font-size: 1.1rem;
    margin-top: 1.5rem;
}

.filtros {
    display: flex;
    gap: 0.5rem;
    margin: 1.5rem 0 1rem;
    overflow-x: auto;
}

.filtros button {
    margin: 0;
    flex-shrink: 0;
    padding: 0.5rem 1rem;
    border: 1px solid var(--darkPurple);
    border-radius: 2rem;
    background: white;
    color: var(--darkPurple);
    box-shadow: none;
}

.filtros button.activo {
    background: var(--darkPurple);
    color: white;
}

.aviso { text-align: center; color: #666; margin: 2rem 0; }
.error { color: red; font-weight: bold; }

.lista { display: flex; flex-direction: column; gap: 0.8rem; }

.fila {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.7rem;
    background: white;
    border: 1px solid #eee;
    border-radius: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.miniatura {
    width: 64px;
    height: 64px;
    flex-shrink: 0;
    object-fit: cover;
    border-radius: 0.7rem;
    background: #f8f8f8;
}

.miniatura.placeholder { object-fit: contain; opacity: 0.5; padding: 0.4rem; }

.datos {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}

.datos strong {
    color: var(--darkPurple);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

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

.acciones { display: flex; gap: 0.4rem; flex-shrink: 0; }
.acciones button { margin: 0; padding: 0.6rem 0.9rem; }

.btn-borrar {
    background: white;
    border: 1px solid #f3c1c6;
}

@media (max-width: 420px) {
    .fila { flex-wrap: wrap; }
    .acciones { width: 100%; }
    .acciones .btnRosa { flex: 1; }
}
</style>
