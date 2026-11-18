<script setup>
import { ULTIMA_ACTUALIZACION } from '@/datosLegales'

// Estructura común del aviso legal, la privacidad y las cookies
defineProps({
    titulo: { type: String, required: true },
})
</script>

<template>
<div class="body">
    <div class="capaBlanca pagina-legal">
        <article>
            <h1>{{ titulo }}</h1>
            <p class="actualizacion">Última actualización: {{ ULTIMA_ACTUALIZACION }}</p>
            <slot />
        </article>
    </div>
</div>
</template>

<style>
/* Sin scoped: tiene que llegar al contenido de cada página (el slot) */
.pagina-legal {
    justify-content: center;
}

.pagina-legal article {
    max-width: 800px;
    width: 100%;
    line-height: 1.6;
    color: #333;
}

.pagina-legal h1 { margin-bottom: 0.3rem; }
.pagina-legal .actualizacion { color: #777; font-size: 0.9rem; margin: 0 0 2rem; }

.pagina-legal h2 {
    color: var(--darkPurple);
    font-size: 1.25rem;
    margin: 2rem 0 0.6rem;
}

.pagina-legal p { margin: 0 0 0.8rem; }

.pagina-legal ul {
    margin: 0 0 1rem 1.2rem;
    padding: 0;
}

.pagina-legal li {
    list-style: disc;
    margin-bottom: 0.4rem;
}

.pagina-legal a { color: var(--pink); text-decoration: underline; }

.pagina-legal table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.5rem 0 1rem;
    font-size: 0.95rem;
}

.pagina-legal th, .pagina-legal td {
    border: 1px solid #ddd;
    padding: 0.5rem;
    text-align: left;
    vertical-align: top;
}

.pagina-legal th { background: var(--lightPurple); color: var(--darkPurple); }

/* En el móvil las tablas pueden ser más anchas que la pantalla */
.pagina-legal .tabla { overflow-x: auto; }
</style>
