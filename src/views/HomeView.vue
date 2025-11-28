<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="body">
    
    <div class="capaBlanca hero-container">
        <div class="centre cardLogo">
            <img class="logo" src="/logos/logo.png" alt="logo">
            <h2>VILLA PIRRITX</h2>
            <p class="textCentre">Ayudando a diferentes animales a encontrar un hogar y poder tener su segunda oportunidad</p>
            
            <div class="botones-hero">
                <RouterLink to="/adopcion">
                    <button class="btnRosa">¡Quiero Adoptar!</button>
                </RouterLink>
                <RouterLink to="/colabora">
                    <button class="btnMorado">Quiero Ayudar</button>
                </RouterLink>
            </div>
        </div>

        <div class="centre imagen-container">
            <img class="imagen" src="/mix/animalitos.png" alt="animalitos">
            <p class="textCentre">TODOS MERECEMOS UNA SEGUNDA OPORTUNIDAD</p>
        </div>
    </div>

    <div class="capaRosa">
        <div class="centre card2">
            <h2>Nuestra Misión</h2>
            <p class="textCentre">
                Desde 2016 luchamos por el bienestar animal en Sondika. 
                Rescatamos, rehabilitamos y buscamos finales felices.
            </p>
            <RouterLink to="/proyecto">
                <button class="btnBlanco">Ver nuestro impacto</button> 
            </RouterLink>
        </div>
    </div>

    <div class="capaBlanca">
        <div class="centre">
            <h2>¿Qué buscas hoy?</h2>
            <div class="horizontalSpaceAround">
                
                <RouterLink to="/adopcion" class="card-link">
                    <div class="cards centre hover-effect">
                        <img class="logoPeq" src="/iconos/adoptar.png" alt="">
                        <h3>Adoptar</h3>
                    </div>
                </RouterLink>

                <RouterLink to="/eventos" class="card-link">
                    <div class="cards centre hover-effect">
                        <img class="logoPeq" src="/iconos/patita.png" alt="">
                        <h3>Próximos Eventos</h3>
                    </div>
                </RouterLink>

                <RouterLink to="/colabora" class="card-link">
                    <div class="cards centre hover-effect">
                        <img class="logoPeq" src="/iconos/ayudar.png" alt="">
                        <h3>Colaborar</h3>
                    </div>
                </RouterLink>

            </div>
        </div>
    </div>

  </div>
</template>

<style scoped>
/* --- ARREGLO DE LA PORTADA (HERO) --- */
.hero-container {
    padding-top: 2rem;
    display: flex;
    flex-direction: column; /* En móvil, uno debajo del otro */
    align-items: center;
    gap: 2rem;
}

/* En pantallas grandes, ponemos el logo y la foto lado a lado */
@media (min-width: 900px) {
    .hero-container {
        flex-direction: row; /* Lado a lado */
        justify-content: center;
        align-items: center;
        gap: 4rem; /* Espacio entre el texto y la foto */
        padding: 4rem 2rem;
    }
}

.botones-hero {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.cardLogo {
    width: 100%;
    max-width: 25rem;
    margin-bottom: 1rem;
    text-align: center;
}

.logo {
    width: 80%;
    max-width: 17rem;
}

/* --- AQUÍ ESTABA EL PROBLEMA DE LA IMAGEN --- */
.imagen-container {
    width: 100%;
    max-width: 37rem; /* Contenedor limitado */
    padding: 0 1rem; /* Un poco de margen en los lados en móvil */
}

.imagen {
    width: 100%;       /* Ocupa el ancho disponible del padre... */
    max-width: 37rem;  /* ...pero nunca más de 37rem */
    height: auto;      /* Mantén la proporción */
    border-radius: 1rem;
    display: block;
    margin: 0 auto;
}

/* Resto de estilos */


.card-link {
    text-decoration: none;
    color: inherit;
}

.hover-effect {
    transition: transform 0.3s;
    cursor: pointer;
}

.hover-effect:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.logoPeq {
    width: 4rem;
    margin-bottom: 0.5rem;
}
</style>