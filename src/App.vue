<script setup>
import { RouterView } from 'vue-router'
import AppHeader from '@/components/shared/AppHeader.vue'
import AppFooter from '@/components/shared/AppFooter.vue'
</script>

<template>
  <div class="estructure">
    <AppHeader />

    <div class="borde content-wrap">
        <RouterView />
    </div>
    
    <AppFooter />
  </div>
</template>

<style>
/* Estilos Globales */
body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  overflow-x: hidden;
}

/* --- SOLUCIÓN DEL FOOTER --- */
.estructure {
    display: flex;
    flex-direction: column;
    
    /* 1. Mínimo toda la altura de la pantalla */
    min-height: 100vh; 
    
    /* 2. Añadimos el espacio aquí dentro */
    padding-top: 7rem; /* Ajusta este número si ves mucho/poco hueco con el menú */
    
    /* 3. ¡LA CLAVE! Esto dice: "El padding está INCLUIDO en el 100vh" */
    box-sizing: border-box; 
}

.content-wrap {
    flex: 1; 
    display: flex;
    flex-direction: column;
}
</style>