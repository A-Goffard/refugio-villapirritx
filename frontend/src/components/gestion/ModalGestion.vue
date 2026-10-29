<script setup>
import { onMounted, onUnmounted } from 'vue'

// Ventana del panel: fondo oscuro, botón de cerrar y título. Los estilos están en assets/gestion.css
defineProps({
    titulo: { type: String, required: true },
})
const emit = defineEmits(['cerrar'])

// Mientras está abierta, la página de detrás no hace scroll
onMounted(() => { document.body.style.overflow = 'hidden' })
onUnmounted(() => { document.body.style.overflow = 'auto' })
</script>

<template>
<div class="modal-overlay" @click.self="emit('cerrar')">
    <div class="modal-content">
        <button class="btn-cerrar" type="button" @click="emit('cerrar')" aria-label="Cerrar">×</button>
        <h2>{{ titulo }}</h2>
        <slot />
    </div>
</div>
</template>
