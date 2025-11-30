<script setup>
// No necesitamos lógica específica aquí por ahora
</script>

<template>
    <div class="body">

        <div class="capaBlanca">

            <div class="centre">
                <img class="logo" src="/logos/logo.png" alt="logo Villa Pirritx">
                <h2>VILLA PIRRITX</h2>
            </div>

            <div class="centre capaBlanca">
                <div>
                    <p class="textCentre">
                        Gracias a nuestra labor desinteresada y a vuestra ayuda hemos conseguido salvar a un gran número
                        de animales desde que en 2016 se creara Villa Pirritx.
                    </p>
                </div>


                <div class="miniRosa">
                    <p class="numero-grande">1050</p>
                    <p>animales ayudados</p>
                </div>

                <div class="stats-container">
                    <div class="horizontal">
                        <img class="logoPeq" src="/iconos/perro.png" alt="Perros">
                        <div>
                            <p>Perros</p>
                            <p class="numero-grande">500</p>
                        </div>

                    </div>
                    <div class="horizontal">
                        <img class="logoPeq" src="/iconos/gato.png" alt="Gatos">
                        <div>
                            <p>Gatos</p>
                            <p class="numero-grande">195</p>
                        </div>
                    </div>
                    <div class="horizontal">
                        <img class="logoPeq" src="/iconos/ave.png" alt="Otros animales">
                        <div>
                            <p>Aves</p>
                        <p class="numero-grande">35</p>
                        </div>
                    </div>
                    <div class="horizontal">
                        <img class="logoPeq" src="/iconos/conejo.png" alt="Otros animales">
                        <div>
                            <p>Otros</p>
                            <p class="numero-grande">20</p>
                        </div>
                    </div>
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


.logo {
    max-width: 15rem;
}

.miniRosa {
    border-radius: 1rem;
    /* Un poco más suave */
    width: 100%;
    margin: 1rem 0;
}

.numero-grande {
    font-size: 2rem;
    font-weight: bold;
    color: var(--darkPurple);
}

.stats-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1rem;
}

.logoPeq {
    width: 5rem;
    /* Tamaño fijo para los iconos de estadísticas */
    height: auto;
}

.animalitos {
    width: 100%;
    max-width: 20rem;
    /* Responsive: nunca más de 20rem, pero se adapta si es menor */
    margin-top: 2rem;
}

.mt-2 {
    margin-top: 2rem;
}

/* RESPONSIVE: MÓVIL */
@media (max-width: 768px) {

    .capaBlanca,
    .capaRosa {
        padding: 2rem 1rem;
        flex-direction: column;
    }

    .stats-container {
        gap: 1rem;
    }
}
</style>