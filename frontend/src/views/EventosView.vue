<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { hacerUrlSegura } from '@/utils/urls'
import { formatearFecha, leerFecha, hoy } from '@/utils/fechas'

const eventos = ref([])
const cargando = ref(true)
const error = ref(null)

onMounted(async () => {
    try {
        const response = await axios.get('/api/eventos/')
        // Solo los de hoy en adelante, el más cercano primero
        eventos.value = response.data
            .filter((e) => e.fecha >= hoy())
            .sort((a, b) => a.fecha.localeCompare(b.fecha))
    } catch (e) {
        console.error(e)
        error.value = 'Hubo un problema cargando los eventos.'
    } finally {
        cargando.value = false
    }
})

const dia = (fecha) => leerFecha(fecha).getDate()
const mes = (fecha) => formatearFecha(fecha, { month: 'short' }).replace('.', '')
const enlaceMapa = (lugar) => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(lugar)}`
</script>

<template>
<div class="body">
    <div class="capaBlanca vista-eventos">

        <div class="encabezado">
            <img src="/iconos/patita.png" class="patita-titulo" alt="huella">
            <h2>Eventos Solidarios</h2>
            <p>Ven a vernos: todo lo que se recauda va para los animales del refugio.</p>
        </div>

        <div v-if="cargando" class="aviso">
            <img src="/iconos/patita.png" class="patita-animada" alt="...">
            <p>Buscando eventos...</p>
        </div>
        <p v-else-if="error" class="aviso error">{{ error }}</p>

        <div v-else-if="eventos.length === 0" class="aviso sin-eventos">
            <p>Ahora mismo no hay eventos programados.</p>
            <p>Mientras tanto, hay muchas otras formas de echar una pata.</p>
            <router-link to="/colabora"><button class="btnRosa">Cómo ayudar</button></router-link>
        </div>

        <div v-else class="lista-eventos">
            <article v-for="evento in eventos" :key="evento.id" class="evento">
                <a v-if="evento.imagen" :href="hacerUrlSegura(evento.imagen)" target="_blank" rel="noopener" class="evento-imagen">
                    <img :src="hacerUrlSegura(evento.imagen)" :alt="evento.titulo">
                </a>

                <div class="evento-info">
                    <div class="cabecera-evento">
                        <div class="calendario" :title="formatearFecha(evento.fecha)">
                            <span class="dia">{{ dia(evento.fecha) }}</span>
                            <span class="mes">{{ mes(evento.fecha) }}</span>
                        </div>
                        <div>
                            <h3>{{ evento.titulo }}</h3>
                            <p class="fecha-larga">{{ formatearFecha(evento.fecha) }}</p>
                        </div>
                    </div>

                    <p class="dato">🕒 {{ evento.horario }}</p>
                    <p class="dato">
                        📍 <a :href="enlaceMapa(evento.lugar)" target="_blank" rel="noopener">{{ evento.lugar }}</a>
                    </p>
                    <p class="descripcion">{{ evento.descripcion }}</p>
                </div>
            </article>
        </div>
    </div>
</div>
</template>

<style scoped>
.vista-eventos {
    display: flex !important;
    flex-direction: column !important;
    align-items: center;
    width: 100%;
}

.encabezado {
    text-align: center;
    margin-bottom: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.patita-titulo { width: 60px; margin-bottom: 0.5rem; }

.aviso { text-align: center; margin: 2rem 0; }
.error { color: red; font-weight: bold; }
.sin-eventos p { color: #666; }

.patita-animada {
    width: 60px;
    animation: bote 0.8s infinite alternate;
    margin: 0 auto;
    display: block;
}

@keyframes bote {
    from { transform: translateY(0); }
    to { transform: translateY(-10px); }
}

.lista-eventos {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
    max-width: 900px;
}

.evento {
    display: flex;
    background: white;
    border: 1px solid #eee;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

/* La imagen se ve entera: suelen ser carteles */
.evento-imagen {
    flex: 0 0 40%;
    background: #f8f8f8;
    display: flex;
    align-items: center;
    justify-content: center;
}

.evento-imagen img {
    width: 100%;
    max-height: 450px;
    object-fit: contain;
    display: block;
}

.evento-info {
    flex: 1;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}

.cabecera-evento {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.cabecera-evento h3 { color: var(--darkPurple); font-weight: bold; margin: 0; }

.calendario {
    flex-shrink: 0;
    width: 64px;
    padding: 0.4rem 0;
    border-radius: 0.8rem;
    background: var(--darkPurple);
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    line-height: 1.1;
}

.calendario .dia { font-size: 1.6rem; font-weight: bold; }
.calendario .mes { font-size: 0.8rem; text-transform: uppercase; }

.fecha-larga { color: #666; margin: 0.2rem 0 0; }
.fecha-larga::first-letter { text-transform: uppercase; }

.dato { margin: 0; }
.dato a { color: var(--pink); text-decoration: underline; }

.descripcion {
    margin: 0.5rem 0 0;
    color: #444;
    white-space: pre-line; /* respeta los saltos de línea que escriba en el panel */
}

@media (max-width: 768px) {
    .evento { flex-direction: column; }
    .evento-imagen { flex-basis: auto; }
}
</style>
