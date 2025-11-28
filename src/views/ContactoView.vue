<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
    <div class="body">

        <div class="capaBlanca">
            <div>
                <h1>CONTACTA</h1>
                <div class="centre cardLogo">
                    <img class="logo" src="/logos/logo.png" alt="logo Villa Pirritx">
                </div>
            </div>

            <div class="centre card2">
                <p class="textCentre">
                    Estamos aquí para resolver tus dudas.
                    Escríbenos y te responderemos lo antes posible.
                </p>
            </div>
        </div>

        <div class="capaRosa">
            <div class="centre">
                <h2>Información de contacto</h2>
                <div class="horizontalSpaceAround">

                    <div class="card centre bg-white">
                        <img class="icono-contacto" src="/iconos/patita.png" alt="Email">
                        <h3>Email</h3>
                        <a class="btn-contacto" href="mailto:villapirritxanimaliak@gmail.com">
                            villapirritxanimaliak@gmail.com
                        </a>
                    </div>

                    <div class="card centre bg-white">
                        <img class="icono-contacto" src="/iconos/patita.png" alt="Redes">
                        <h3>Redes Sociales</h3>
                        <p>Síguenos en Instagram</p>
                        <p>y Facebook para ver</p>
                        <p>el día a día del refugio.</p>
                    </div>

                    <div class="card centre bg-white">
                        <img class="icono-contacto" src="/iconos/patita.png" alt="Ubicación">
                        <h3>Ubicación</h3>
                        <p>Sondika, Bizkaia</p>
                        <p>(Cita previa)</p>
                    </div>

                </div>
            </div>
        </div>

        <div class="capaBlanca">
            <div class="centre card2">
                <h2>¿Dónde estamos?</h2>
                <p>Nos encontramos en el entorno de Sondika.</p>
            </div>

            <div class="map-container">
                <iframe
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d23225.59267156321!2d-2.946377767858886!3d43.29748687913508!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd4e50507d77ce09%3A0x6d9575452d242699!2sSondika%2C%20Biscay!5e0!3m2!1sen!2ses!4v1700000000000!5m2!1sen!2ses"
                    width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"
                    referrerpolicy="no-referrer-when-downgrade">
                </iframe>
            </div>
        </div>

    </div>
</template>

<style scoped>
/* Estilos específicos */

.cardLogo {
    margin-bottom: 1rem;
}

.logo {
    max-width: 12rem;
}

/* CORREGIDO: Ahora aplicamos el estilo a la clase .btn-contacto en vez de a 'button' */
.btn-contacto {
    color: var(--pink);
    text-decoration: none;
    border: solid 1px var(--pink);
    padding: 0.5rem;
    border-radius: 6px;
    background-color: var(--white);
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.15);
    cursor: pointer;
    display: inline-block; /* Importante para que respete el padding */
    transition: transform 0.2s;
    word-break: break-all; /* Por si el email es muy largo en móvil */
}

.btn-contacto:hover {
    transform: scale(1.05);
}

/* Tarjetas de contacto con fondo blanco para resaltar sobre el rosa */
.bg-white {
    background-color: var(--white);
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.icono-contacto {
    width: 3rem;
    margin-bottom: 1rem;
}

/* Contenedor del mapa */
.map-container {
    width: 100%;
    max-width: 1000px;
    margin: 2rem auto;
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
    .capaBlanca,
    .capaRosa {
        padding: 2rem 1rem;
    }

    .horizontalSpaceAround {
        gap: 1rem;
    }
}
</style>