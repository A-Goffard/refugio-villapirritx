<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { cargarImagen, exportarRecorte, PROPORCION_FOTO } from '@/utils/imagenes'

// Muestra la foto dentro de un marco con el formato de la web.
// Se arrastra para encuadrar y se hace zoom con dos dedos o con el deslizador.
const props = defineProps({
    archivo: { type: File, required: true },
})
const emit = defineEmits(['listo', 'cancelar', 'error'])

const ZOOM_MAXIMO = 4

const marco = ref(null)
const imagen = ref(null)
const anchoMarco = ref(0)
const zoom = ref(1)
const posicion = ref({ x: 0, y: 0 }) // esquina superior izquierda de la foto respecto al marco
const exportando = ref(false)

const altoMarco = computed(() => anchoMarco.value / PROPORCION_FOTO)

// Escala con la que la foto cubre justo el marco (zoom 1)
const escalaBase = computed(() => {
    if (!imagen.value) return 1
    return Math.max(anchoMarco.value / imagen.value.naturalWidth, altoMarco.value / imagen.value.naturalHeight)
})
const escala = computed(() => escalaBase.value * zoom.value)

const estiloFoto = computed(() => ({
    width: `${imagen.value.naturalWidth * escala.value}px`,
    height: `${imagen.value.naturalHeight * escala.value}px`,
    transform: `translate(${posicion.value.x}px, ${posicion.value.y}px)`,
}))

// La foto nunca puede dejar huecos dentro del marco
const limitar = ({ x, y }) => {
    const minX = anchoMarco.value - imagen.value.naturalWidth * escala.value
    const minY = altoMarco.value - imagen.value.naturalHeight * escala.value
    return {
        x: Math.min(0, Math.max(minX, x)),
        y: Math.min(0, Math.max(minY, y)),
    }
}

// Cambia el zoom manteniendo fijo el punto central del marco
const cambiarZoom = (nuevoZoom) => {
    const centroX = (anchoMarco.value / 2 - posicion.value.x) / escala.value
    const centroY = (altoMarco.value / 2 - posicion.value.y) / escala.value
    zoom.value = Math.min(ZOOM_MAXIMO, Math.max(1, nuevoZoom))
    posicion.value = limitar({
        x: anchoMarco.value / 2 - centroX * escala.value,
        y: altoMarco.value / 2 - centroY * escala.value,
    })
}

const centrar = () => {
    posicion.value = limitar({
        x: (anchoMarco.value - imagen.value.naturalWidth * escala.value) / 2,
        y: (altoMarco.value - imagen.value.naturalHeight * escala.value) / 2,
    })
}

// Si el marco cambia de ancho (p. ej. al girar el móvil) volvemos a empezar.
// Solo el ancho: en el móvil la barra del navegador también dispara 'resize'.
const medirMarco = () => {
    if (!marco.value || !imagen.value) return
    if (marco.value.clientWidth === anchoMarco.value) return
    anchoMarco.value = marco.value.clientWidth
    zoom.value = 1
    centrar()
}

onMounted(async () => {
    try {
        imagen.value = await cargarImagen(props.archivo)
    } catch {
        // El navegador no sabe leerla (p. ej. HEIC en un ordenador): se sube sin recortar
        emit('error')
        return
    }
    requestAnimationFrame(medirMarco)
    window.addEventListener('resize', medirMarco)
})

onUnmounted(() => {
    window.removeEventListener('resize', medirMarco)
    if (imagen.value) URL.revokeObjectURL(imagen.value.src)
})

// --- ARRASTRAR Y PELLIZCAR ---
const punteros = new Map()
let distanciaInicial = 0
let zoomInicial = 1

const distanciaEntrePunteros = () => {
    const [a, b] = [...punteros.values()]
    return Math.hypot(a.x - b.x, a.y - b.y)
}

const alPulsar = (evento) => {
    marco.value.setPointerCapture(evento.pointerId)
    punteros.set(evento.pointerId, { x: evento.clientX, y: evento.clientY })
    if (punteros.size === 2) {
        distanciaInicial = distanciaEntrePunteros()
        zoomInicial = zoom.value
    }
}

const alMover = (evento) => {
    const anterior = punteros.get(evento.pointerId)
    if (!anterior) return
    const actual = { x: evento.clientX, y: evento.clientY }
    punteros.set(evento.pointerId, actual)

    if (punteros.size === 1) {
        posicion.value = limitar({
            x: posicion.value.x + actual.x - anterior.x,
            y: posicion.value.y + actual.y - anterior.y,
        })
    } else if (punteros.size === 2 && distanciaInicial > 0) {
        cambiarZoom(zoomInicial * distanciaEntrePunteros() / distanciaInicial)
    }
}

const alSoltar = (evento) => {
    punteros.delete(evento.pointerId)
    distanciaInicial = 0
}

const alRueda = (evento) => {
    cambiarZoom(zoom.value * (evento.deltaY < 0 ? 1.1 : 0.9))
}

// --- CONFIRMAR ---
const confirmar = async () => {
    exportando.value = true
    const recorte = {
        x: -posicion.value.x / escala.value,
        y: -posicion.value.y / escala.value,
        ancho: anchoMarco.value / escala.value,
        alto: altoMarco.value / escala.value,
    }
    emit('listo', await exportarRecorte(imagen.value, recorte, props.archivo.name))
}
</script>

<template>
<div class="recortador">
    <p class="instrucciones">Arrastra la foto para encuadrarla. Así es como se verá en la web.</p>

    <div ref="marco" class="marco" @pointerdown="alPulsar" @pointermove="alMover"
        @pointerup="alSoltar" @pointercancel="alSoltar" @wheel.prevent="alRueda">
        <img v-if="imagen && anchoMarco" :src="imagen.src" :style="estiloFoto" alt="" draggable="false">
        <p v-else class="cargando">Cargando foto...</p>
    </div>

    <label class="zoom">
        <span>Zoom</span>
        <input type="range" min="1" :max="ZOOM_MAXIMO" step="0.01" :value="zoom"
            @input="cambiarZoom(Number($event.target.value))" :disabled="!imagen">
    </label>

    <div class="botones">
        <button type="button" class="btnBlanco" @click="emit('cancelar')">Cancelar</button>
        <button type="button" class="btnMorado" @click="confirmar" :disabled="!imagen || exportando">
            {{ exportando ? 'Preparando...' : 'Usar esta foto' }}
        </button>
    </div>
</div>
</template>

<style scoped>
.recortador { display: flex; flex-direction: column; gap: 1rem; }

.instrucciones { color: #666; text-align: center; }

.marco {
    position: relative;
    width: 100%;
    aspect-ratio: 4 / 3;
    overflow: hidden;
    border-radius: 0.6rem;
    background: #222;
    cursor: grab;
    touch-action: none; /* que el navegador no haga scroll mientras se arrastra la foto */
    user-select: none;
}

.marco:active { cursor: grabbing; }

.marco img {
    position: absolute;
    top: 0;
    left: 0;
    max-width: none;
    pointer-events: none;
}

.cargando { color: white; text-align: center; margin-top: 30%; }

.zoom { display: flex; align-items: center; gap: 0.8rem; font-weight: bold; color: var(--darkPurple); }
.zoom input { flex: 1; accent-color: var(--darkPurple); }

.botones { display: flex; gap: 0.8rem; }
.botones button { flex: 1; margin: 0; padding: 0.9rem; font-size: 1rem; }
</style>
