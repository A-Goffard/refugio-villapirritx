<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="body">
    
    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/logos/logo.png" alt="logo">
            <h2>VILLA PIRRITIX</h2>
        </div>

        <div class="centre card2">
            <p class="textCentre"><b>¡Sin vuestra ayuda nada es posible!</b></p>
            <p class="textCentre">Cada año, miles de animales son abandonados o viven en situaciones de verdadera decadencia, esperando a que alguien les ayude. Por todo esto, y para que sea posible, Villa Pirritx necesita de vuestra ayuda. Sin vosotros/as, esto no sería posible.</p>
            <p class="textCentre">Todos y todas podemos aportar nuestro granito de arena, porque solo unidos conseguiremos que cada uno de los animales que pasen y pasarán por Villa Pirritx tenga un hogar digno para vivir. Existen muchas formas de ayudarnos y ser parte de este gran proyecto.</p>
        </div>
    </div>

    <div class="capaRosa">
        <div class="centre card2">
            <p class="textCentre"><b>¿Te gustaría ser casa de acogida?</b></p>
            <p class="textCentre">En muchas situaciones, salvar un animal puede ser una odisea. Ya lo hemos rescatado, ¿pero ahora qué? Muchas veces, mientras esperamos a esa familia, necesita un hogar temporal donde le den los cuidados y el amor necesario para que se vaya recuperando, no solo físicamente, sino también emocionalmente, de sus heridas.</p>
            
            <RouterLink :to="{ path: '/contacta', query: { asunto: 'Casa de Acogida' }}">
    <button class="btnMorado">Pregúntanos</button>
</RouterLink>
        </div>

        <div class="centre cardLogo">
            <img class="logo" src="/mix/acogida1.jpeg" alt="casa de acogida">
        </div>
    </div>

    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/mix/apadrina1.jpeg" alt="apadrina">
        </div>

        <div class="centre card2">
            <p class="textCentre"><b>Apadrina un ser vivo</b></p>
            <p class="textCentre">Cada perro tiene una historia única de abandono o maltrato. Con tu ayuda, podemos darles una segunda oportunidad, proporcionándoles los cuidados necesarios para que se recuperen. Muchas veces, por nuestra situación personal, no podemos adoptar, pero sí podemos aportar una pequeña cantidad económica que le ayude a sanar.</p>
            
            <RouterLink :to="{ path: '/contacta', query: { asunto: 'Voluntariado' }}">
    <button class="btnRosa">Pregúntanos</button>
</RouterLink>
        </div>
    </div>

    <div class="capaRosa">
        <div class="centre card2">
            <p class="textCentre"><b>Dona cosas que tengas en casa</b></p>
            <p class="textCentre">Ayuda a nuestra protectora donando objetos para nuestros mercadillos solidarios. Tus donaciones se convertirán en recursos para cubrir los cuidados y tratamientos. Puedes donar ropa, libros, juguetes o artículos de decoración.</p>
            
            <RouterLink :to="{ path: '/contacta', query: { asunto: 'Casa de Acogida' }}">
    <button class="btnMorado">Pregúntanos</button>
</RouterLink>
        </div>

        <div class="centre cardLogo">
            <img class="logo" src="/mix/acogida1.jpeg" alt="donaciones">
        </div>
    </div>

    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/mix/voluntarios.jpeg" alt="voluntariado">
        </div>

        <div class="centre card2">
            <p class="textCentre"><b>Voluntariado</b></p>
            <p class="textCentre">Ser voluntario en la protectora es una oportunidad para marcar la diferencia. Con tu tiempo y dedicación, ayudas en su cuidado y les das el cariño que tanto necesitan.</p>
            
            <RouterLink :to="{ path: '/contacta', query: { asunto: 'Voluntariado' }}">
                <button class="btnRosa">Pregúntanos</button>
            </RouterLink>
        </div>
    </div>

    <div class="capaRosa">
        <div class="centre card2">
            <p class="textCentre"><b>Viajes solidarios</b></p>
            <p class="textCentre">Los viajes solidarios son clave. Transportar perros y gatos a otras ciudades o países donde serán adoptados es una misión llena de esperanza. Al participar, ayudas a que los animales lleguen seguros a su nuevo hogar.</p>
            
            <RouterLink :to="{ path: '/contacta', query: { asunto: 'Casa de Acogida' }}">
    <button class="btnMorado">Pregúntanos</button>
</RouterLink>
        </div>

        <div class="centre cardLogo">
            <img class="logo" src="/mix/acogida1.jpeg" alt="viajes">
        </div>
    </div>

    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/mix/voluntarios.jpeg" alt="difunde">
        </div>

        <div class="centre card2">
            <p class="textCentre"><b>Difunde</b></p>
            <p class="textCentre">Difundir en redes o de manera verbal es una de las formas más poderosas de ayudar. Compartiendo publicaciones puedes conectar a nuestros peludos con personas dispuestas a adoptar.</p>
            
<RouterLink :to="{ path: '/contacta', query: { asunto: 'Voluntariado' }}">
    <button class="btnRosa">Pregúntanos</button>
</RouterLink>
        </div>
    </div>

  </div>
</template>

<style scoped>
/* Estilos específicos para esta vista */

.cardLogo {
    /* Ajuste para que las imágenes no sean gigantes */
    width: 100%;
    padding: 1rem;
}

.logo {
    border-radius: 1rem; /* Bordes redondeados para todas las fotos */
    object-fit: cover;
    max-height: 300px;
}

.card2 {
    /* Ajuste para los textos */
    width: 100%;
    max-width: 40rem;
    padding: 1rem;
}

/* RESPONSIVE: MÓVIL */
@media (max-width: 768px) {
    /* Hacemos que las capas se pongan en columna en vez de fila */
    .capaBlanca, .capaRosa {
        flex-direction: column;
        padding: 2rem 1rem;
        text-align: center;
    }

    /* Pequeño truco para el orden en móvil:
       Si quieres que la foto salga siempre arriba o abajo, se puede usar 'order',
       pero por defecto se apilarán según el HTML.
    */
    
    .cardLogo {
        margin-bottom: 1rem;
    }
}
</style>