<script setup>
// 1. Importamos los componentes de Swiper y los estilos necesarios
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, Pagination, Navigation } from 'swiper/modules';

// Importar estilos de Swiper
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';

// 2. Definimos las imágenes del carrusel (Pon aquí las rutas de tus fotos reales)
// Puedes usar las que ya tienes o subir nuevas a /public/mix/
const imagenesCarrusel = [
    '/animales/2.png',
    '/animales/3.png',
    '/animales/4.png',
    '/animales/5.png',
    '/animales/6.png',
    '/animales/7.png',
    '/animales/8.png',
    '/animales/9.png',
    '/animales/10.png',
];

// Configuración de los módulos que vamos a usar
const modules = [Autoplay, Pagination, Navigation];
</script>

<template>
    <div class="body">

        <div class="capaBlanca">

            <div class="centre">
                <img class="logo" src="/logos/logo.png" alt="logo Villa Pirritx">
                <h2>VILLA PIRRITX</h2>
            </div>

            <div class="centre capaBlanca bloque-derecho">
                <div>
                    <p class="textCentre">
                        Gracias a nuestra labor desinteresada y a vuestra ayuda hemos conseguido salvar a un gran número
                        de animales desde que en 2016 se creara Villa Pirritx.
                    </p>
                    <p class="textCentre">
                        Desde perros y gatos hasta aves y pequeños mamíferos, ¡incluso cabras! han pasado por nuestras
                        manos buscando un nuevo hogar.
                    </p>
                </div>


                <div class="miniRosa">
                    <p class="numero-grande">> 100</p>
                    <p>animales ayudados</p>
                </div>

                <div class="carrusel-container">
                    <swiper :spaceBetween="30" :centeredSlides="true" :loop="true" :autoplay="{
                        delay: 3000,
                        disableOnInteraction: false,
                    }" :pagination="{
                            clickable: true,
                        }" :breakpoints="{
                            '640': {
                                slidesPerView: 1,
                                spaceBetween: 20,
                            },
                            '768': {
                                slidesPerView: 2,
                                spaceBetween: 30,
                            },
                            '1024': {
                                slidesPerView: 3,
                                spaceBetween: 40,
                            },
                        }" :modules="modules" class="mySwiper">
                        <swiper-slide v-for="(img, index) in imagenesCarrusel" :key="index">
                            <div class="slide-content">
                                <img :src="img" alt="Foto del refugio" class="img-carrusel" />
                            </div>
                        </swiper-slide>
                    </swiper>
                </div>
            </div>

        </div>

        <div class="capaRosa">
            <div class="centre">
                <h2>Nuestro proyecto</h2>
                <h3>Un pequeño gesto para ti, un gran paso para ellos</h3>
                <p class="textCentre">
                    Nuestro proyecto en la protectora de animales se centra en rescatar, rehabilitar y encontrar hogares
                    amorosos para aquellos que han sufrido abandono o maltrato.
                </p>
                <p class="textCentre">En algunas ocasiones, por circunstancias diferentes, algunos animales necesitan
                    ser reubicados temporalmente en hogares de acogida o realojados.</p>
                <p class="textCentre">
                    Brindamos refugio, atención veterinaria y cariño a perros, gatos y otros animalitos mientras
                    buscamos familias definitivas para ellos.
                </p>
                <p class="textCentre">
                    Además, promovemos la importancia de la esterilización y la tenencia responsable de mascotas.
                </p>
            </div>
        </div>

    </div>
</template>

<style scoped>
/* Estilos específicos de esta vista */

/* Contenedor principal para evitar desbordamientos */
.body {
    overflow-x: hidden;
    width: 100%;
}

.logo {
    max-width: 15rem;
    height: auto;
}

/* El bloque de la derecha (donde está el texto y el carrusel) */
.bloque-derecho {
    /* Truco vital para carruseles dentro de Flexbox: evita que se salga */
    min-width: 0;
    width: 100%;
}

.miniRosa {
    border-radius: 1rem;
    width: 100%;
    margin: 1rem 0;
    text-align: center;
    padding: 1rem;
    background-color: var(--lightPink);
}

.numero-grande {
    font-size: 2rem;
    font-weight: bold;
    color: var(--darkPurple);
    margin: 0;
}

/* --- ESTILOS DEL CARRUSEL --- */
.carrusel-container {
    width: 100%;
    /* Quitamos el max-width fijo para que se adapte al padre */
    padding: 1rem 0;
    margin: 0 auto;
}

.mySwiper {
    width: 100%;
    height: 300px;
    padding-bottom: 3rem;
}

.slide-content {
    width: 100%;
    height: 100%;
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.img-carrusel {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* Personalizar los puntitos */
:deep(.swiper-pagination-bullet-active) {
    background-color: var(--darkPurple);
}

:deep(.swiper-pagination-bullet) {
    background-color: var(--darkPurple);
    opacity: 0.4;
}

/* --- RESPONSIVE MEJORADO --- */
/* Cambiamos 768px por 1024px para evitar ese momento en que se corta */
@media (max-width: 1024px) {

    .capaBlanca,
    .capaRosa {
        padding: 2rem 1rem;
        /* Forzamos columna mucho antes */
        flex-direction: column;
        align-items: center;
    }

    /* Hacemos que los bloques ocupen todo el ancho en modo columna */
    .centre,
    .bloque-derecho {
        width: 100%;
        max-width: 100%;
        text-align: center;
        /* Opcional: centra el texto */
    }

    .logo {
        margin-bottom: 2rem;
        /* Separa el logo del texto */
    }

    .mySwiper {
        height: 280px;
    }
}
</style>