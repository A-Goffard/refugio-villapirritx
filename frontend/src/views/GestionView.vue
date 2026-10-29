<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ListaAnimales from '@/components/gestion/ListaAnimales.vue'
import ListaEventos from '@/components/gestion/ListaEventos.vue'
import ListaSolicitudes from '@/components/gestion/ListaSolicitudes.vue'
import '@/assets/gestion.css'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

// La pestaña va en la URL (?seccion=eventos) para que al recargar no se pierda
const SECCIONES = ['animales', 'solicitudes', 'eventos']
const seccion = computed(() => (SECCIONES.includes(route.query.seccion) ? route.query.seccion : 'animales'))
const irA = (nueva) => router.replace({ query: nueva === 'animales' ? {} : { seccion: nueva } })

const salir = async () => {
    await auth.cerrarSesion()
    router.push('/')
}

const sesionCaducada = () => {
    auth.sesionCaducada()
    router.push({ name: 'acceso', query: { siguiente: route.fullPath } })
}
</script>

<template>
<div class="body">
    <div class="capaBlanca vista-gestion panel-gestion">

        <div class="cabecera">
            <div>
                <h2>Panel del refugio</h2>
                <p class="saludo">Hola, {{ auth.usuario }}</p>
            </div>
            <button class="btnBlanco btn-salir" @click="salir">Salir</button>
        </div>

        <nav class="pestanas">
            <button :class="{ activa: seccion === 'animales' }" @click="irA('animales')">🐾 Animales</button>
            <button :class="{ activa: seccion === 'solicitudes' }" @click="irA('solicitudes')">📨 Solicitudes</button>
            <button :class="{ activa: seccion === 'eventos' }" @click="irA('eventos')">📅 Eventos</button>
        </nav>

        <ListaAnimales v-if="seccion === 'animales'" @sesion-caducada="sesionCaducada" />
        <ListaSolicitudes v-else-if="seccion === 'solicitudes'" @sesion-caducada="sesionCaducada" />
        <ListaEventos v-else @sesion-caducada="sesionCaducada" />
    </div>
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

.pestanas {
    display: flex;
    margin-top: 1.5rem;
    border-bottom: 2px solid var(--lightPurple);
}

.pestanas button {
    flex: 1;
    margin: 0 0 -2px;
    padding: 0.8rem;
    border: none;
    border-bottom: 3px solid transparent;
    border-radius: 0;
    background: none;
    box-shadow: none;
    font-size: 1rem;
    font-weight: bold;
    color: #888;
}

.pestanas button:hover { transform: none; box-shadow: none; }

.pestanas button.activa {
    color: var(--darkPurple);
    border-bottom-color: var(--pink);
}
</style>
