<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="body">
    
    <div class="capaBlanca">
        <div class="centre cardLogo">
            <img class="logo" src="/logos/logo.png" alt="logo">
            <h2>VILLA PIRRITIX</h2>
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

        <div class="centre">
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
                <button class="btnBlanco">Ver nuestro impacto</button> </RouterLink>
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
.hero-section {
    padding-top: 2rem;
}

.botones-hero {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    justify-content: center;
}

.cardLogo {
    max-width: 25rem;
    margin-bottom: 2rem;
}

.logo {
    max-width: 17rem;
}

.imagen {
    max-width: 37rem;
    border-radius: 1rem;
}

.btnBlanco {
    background-color: var(--white);
    color: var(--darkPurple);
    border: 1px solid var(--darkPurple);
    padding: 0.5rem 1.5rem;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;
}

.card-link {
    text-decoration: none;
    color: inherit;
}

.hover-effect {
    transition: transform 0.3s;
    cursor: pointer;
}

.hover-effect:hover {
    transform: translateY(-5px); /* Efecto de levantar la tarjeta */
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.logoPeq {
    width: 4rem;
    margin-bottom: 0.5rem;
}
</style>