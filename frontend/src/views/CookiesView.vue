<script setup>
import { RouterLink } from 'vue-router'
import PaginaLegal from '@/components/shared/PaginaLegal.vue'
</script>

<template>
<PaginaLegal titulo="Política de cookies">
    <h2>¿Qué son las cookies?</h2>
    <p>Son pequeños archivos que una web guarda en tu navegador para recordar información, como que has iniciado
        sesión o tus preferencias.</p>

    <h2>¿Usa cookies esta web?</h2>
    <p>Para visitar la web, <strong>no</strong>. No usamos cookies de analítica, de publicidad ni de redes
        sociales.</p>
    <p>Solo se guardan cookies cuando el equipo de la asociación entra en su panel de gestión interno. Son cookies
        técnicas, necesarias para que el acceso funcione de forma segura, y por eso no necesitan tu consentimiento
        (artículo 22.2 de la Ley 34/2002, LSSI):</p>
    <div class="tabla">
        <table>
            <thead>
                <tr><th>Cookie</th><th>Para qué sirve</th><th>Duración</th></tr>
            </thead>
            <tbody>
                <tr><td>sessionid</td><td>Mantener la sesión abierta en el panel de gestión.</td><td>2 semanas</td></tr>
                <tr><td>csrftoken</td><td>Proteger los formularios del panel frente a envíos falsificados.</td><td>1 año</td></tr>
            </tbody>
        </table>
    </div>

    <h2>El mapa de Google</h2>
    <p>En la página de <RouterLink to="/contacta">contacto</RouterLink> puedes ver dónde estamos en un mapa de Google
        Maps. El mapa <strong>solo se carga si pulsas el botón «Mostrar mapa»</strong>. A partir de ese momento, Google
        puede instalar sus propias cookies, según su
        <a href="https://policies.google.com/technologies/cookies?hl=es" target="_blank" rel="noopener">política de
        cookies</a>.</p>

    <h2>Enlaces a otras webs</h2>
    <p>Cuando sales de esta web a través de un enlace (redes sociales, Teaming, Coral, Yako Happy…), se aplican las
        políticas de cookies de esas páginas.</p>

    <h2>¿Cómo borrar o bloquear las cookies?</h2>
    <p>Puedes borrar las cookies guardadas o impedir que se guarden desde la configuración de tu navegador:</p>
    <ul>
        <li><a href="https://support.google.com/chrome/answer/95647?hl=es" target="_blank" rel="noopener">Chrome</a></li>
        <li><a href="https://support.mozilla.org/es/kb/Borrar%20cookies" target="_blank" rel="noopener">Firefox</a></li>
        <li><a href="https://support.apple.com/es-es/105082" target="_blank" rel="noopener">Safari</a></li>
        <li><a href="https://support.microsoft.com/es-es/microsoft-edge/eliminar-cookies-en-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09"
            target="_blank" rel="noopener">Edge</a></li>
    </ul>

    <p>Para saber cómo tratamos tus datos personales, consulta la
        <RouterLink to="/privacidad">política de privacidad</RouterLink>.</p>
</PaginaLegal>
</template>
