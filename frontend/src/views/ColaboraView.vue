<script setup>
import { RouterLink } from 'vue-router'

const compartirWeb = async () => {
  const datosCompartir = {
    title: 'Villa Pirritx',
    text: '¡Echa un vistazo a la web de Villa Pirritx y ayuda a los animales!',
    url: window.location.href, // Coge la dirección actual automáticamente
  }

  // 1. Si el navegador soporta compartir nativo (Móviles mayormente)
  if (navigator.share) {
    try {
      await navigator.share(datosCompartir)
    } catch (err) {
      console.log('Error al compartir o cancelado por usuario', err)
    }
  } 
  // 2. Si es un ordenador y no soporta compartir, copiamos al portapapeles
  else {
    try {
      await navigator.clipboard.writeText(window.location.href)
      alert('¡Enlace copiado! Ya puedes pegarlo donde quieras.')
    } catch (err) {
      console.error('No se pudo copiar', err)
    }
  }
}

</script>

<template>
  <div class="body">
    
    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/logos/logo.png" alt="logo">
            <h2>VILLA PIRRITX</h2>
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
            
            <RouterLink :to="{ path: '/formulario', query: { tipo: 'ACOGIDA' }}">
    <button class="btnMorado">¡Me apunto!</button>
</RouterLink>
        </div>

        <div class="centre cardLogo">
            <img class="logo" src="/mix/acogida.png" alt="casa de acogida">
        </div>
    </div>

    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/mix/niña.png" alt="apadrina">
        </div>

        <div class="centre card2">
            <p class="textCentre"><b>Apadrina un ser vivo</b></p>
            <p class="textCentre">Cada perro tiene una historia única de abandono o maltrato. Con tu ayuda, podemos darles una segunda oportunidad, proporcionándoles los cuidados necesarios para que se recuperen. Muchas veces, por nuestra situación personal, no podemos adoptar, pero sí podemos aportar una pequeña cantidad económica que le ayude a sanar.</p>
            
            <RouterLink :to="{ path: '/formulario', query: { tipo: 'APADRINA' }}">
    <button class="btnRosa">¡Me apunto!</button>
</RouterLink>
        </div>
    </div>

    <div class="capaRosa">
        <div class="centre card2">
            <p class="textCentre"><b>Dona cosas que tengas en casa</b></p>
            <p class="textCentre">Ayuda a nuestra protectora donando objetos para nuestros mercadillos solidarios. Tus donaciones se convertirán en recursos para cubrir los cuidados y tratamientos. Puedes donar ropa, libros, juguetes o artículos de decoración.</p>
            
            <RouterLink :to="{ path: '/formulario', query: { tipo: 'DONACION' }}">
    <button class="btnMorado">¡Me apunto!</button>
</RouterLink>
        </div>

        <div class="centre cardLogo">
            <img class="logo" src="/mix/dona.png" alt="donaciones">
        </div>
    </div>

    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/mix/logo_Yako_transparente.png" alt="Yako Happy">
        </div>

        <div class="centre card2">
            <p class="textCentre"><b>Compra para tu perro y ayuda a Villa Pirritx</b></p>
            <p class="textCentre">Por cada compra que hagas en la tienda de Yako Happy desde este enlace, donan 1&nbsp;€ a la protectora. A ti no te cuesta nada más, y a ellos les ayuda muchísimo.</p>

            <!-- El enlace tiene que llevar los utm_ para que Yako Happy cuente la compra para el refugio -->
            <a href="https://yakohappy.store/?utm_source=villapirritx&utm_medium=referral&utm_campaign=protectoras"
                target="_blank" rel="noopener sponsored">
                <button class="btnRosa">Ir a la tienda</button>
            </a>
        </div>
    </div>

    <div class="capaRosa">
        <div class="centre card2">
            <p class="textCentre"><b>Voluntariado</b></p>
            <p class="textCentre">Ser voluntario en la protectora es una oportunidad para marcar la diferencia. Con tu tiempo y dedicación, ayudas en su cuidado y les das el cariño que tanto necesitan.</p>

            <RouterLink :to="{ path: '/formulario', query: { tipo: 'VOLUNTARIADO' }}">
                <button class="btnMorado">¡Me apunto!</button>
            </RouterLink>
        </div>

        <div class="centre cardLogo">
            <img class="logo" src="/mix/voluntarios.png" alt="voluntariado">
        </div>
    </div>

    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/mix/viaje.png" alt="viajes">
        </div>

        <div class="centre card2">
            <p class="textCentre"><b>Viajes solidarios</b></p>
            <p class="textCentre">Los viajes solidarios son clave. Transportar perros y gatos a otras ciudades o países donde serán adoptados es una misión llena de esperanza. Al participar, ayudas a que los animales lleguen seguros a su nuevo hogar.</p>


            <RouterLink :to="{ path: '/formulario', query: { tipo: 'VIAJE' }}">
    <button class="btnRosa">¡Me apunto!</button>
</RouterLink>
        </div>
    </div>

    <div class="capaRosa">
        <div class="centre card2">
            <p class="textCentre"><b>Difunde</b></p>
            <p class="textCentre">Difundir en redes o de manera verbal es una de las formas más poderosas de ayudar. Compartiendo publicaciones puedes conectar a nuestros peludos con personas dispuestas a adoptar.</p>
            <p class="textCentre">Síguenos en redes o comparte nuestra página:</p>
                        <br>
                                    <div class="social-media">

                            <a href="https://www.facebook.com/profile.php?id=100068535188856&locale=es_ES"
                                target="_blank" title="Villapirritx en Facebook">
                                <img src="/iconos/bn/facebook.png" alt="Facebook" class="social-icon" title="Facebook"
                                    loading="lazy" />
                            </a>

                            <a href="https://www.instagram.com/villapirritxanimaliak/" target="_blank"
                                title="Villapirritx en Instagram">
                                <img src="/iconos/bn/instagram.png" alt="Instagram" class="social-icon"
                                    title="Instagram" loading="lazy" />
                            </a>

                            <a @click="compartirWeb" class="btn-share" title="Compartir esta página">
                                <img src="/iconos/bn/compartir.png" alt="Compartir" class="social-icon"
                                    title="Compartir" loading="lazy" />
                            </a>

                        </div>


        </div>

        <div class="centre cardLogo">
            <img class="logo" src="/mix/difunde.png" alt="difunde">
        </div>
    </div>

  </div>
</template>

<style scoped>
/* Estilos específicos para esta vista */

/* Foto y texto juntos en el centro: con space-evenly (main.css) se separaban
   mucho en pantallas grandes */
.capaBlanca, .capaRosa {
    justify-content: center;
    align-items: center;
    gap: 3rem;
}

.cardLogo {
    /* Ajuste para que las imágenes no sean gigantes */
    flex: 0 1 300px;
    padding: 1rem;
}

.logo {
    border-radius: 1rem; /* Bordes redondeados para todas las fotos */
    object-fit: cover;
    max-height: 300px;
}

.card2 {
    /* Ajuste para los textos */
    flex: 0 1 40rem;
    padding: 1rem;
}

/* RESPONSIVE: MÓVIL */
@media (max-width: 768px) {
    /* Hacemos que las capas se pongan en columna en vez de fila */
    .capaBlanca, .capaRosa {
        flex-direction: column;
        padding: 2rem 1rem;
        text-align: center;
        align-items: stretch;
        gap: 0;
    }

    /* En móvil la foto siempre encima del texto, aunque en el HTML vaya detrás */
    .cardLogo {
        order: -1;
        flex-basis: auto;
        margin-bottom: 1rem;
    }

    .card2 { flex-basis: auto; }
}
</style>