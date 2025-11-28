<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'

// Estado reactivo (equivalente a tus variables de clase en Angular)
const isMenuOpen = ref(false)
const navbarRef = ref(null) // Referencia al elemento del DOM para detectar clics fuera

// Métodos
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

// Lógica para cerrar menú al hacer clic fuera (Reemplazo de @HostListener)
const handleClickOutside = (event) => {
  if (navbarRef.value && !navbarRef.value.contains(event.target)) {
    isMenuOpen.value = false
  }
}

// Ciclo de vida: Activamos el "escucha" cuando el componente nace y lo matamos cuando muere
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <header>
    <div class="eslogan">
      <p>¡Salva una vida, adopta un amigo para toda la vida!</p>
      <p>LAS OPORTUNIDADES SOLO PASAN UNA VEZ EN LA VIDA, VEN Y SALVA UNA VIDA</p>

    </div>
    <nav class="navbar" ref="navbarRef">

      <div class="navbar-brand ">
        <button class="hamburger" @click="toggleMenu">
          <img class="patita" src="/iconos/patita.png" alt="Menú">
        </button>
      </div>

      <ul :class="{ 'active': isMenuOpen }" class="navbar-links">
        <li>
          <RouterLink to="/" @click="closeMenu">Inicio</RouterLink>
        </li>
        <li>
          <RouterLink to="/about" @click="closeMenu">Quienes Somos</RouterLink>
        </li>
        <li>
          <RouterLink to="/colabora" @click="closeMenu">Colabora</RouterLink>
        </li>
        <li>
          <RouterLink to="/adopcion" @click="closeMenu">Adopta</RouterLink>
        </li>
        <li>
          <RouterLink to="/proyecto" @click="closeMenu">Nuestro Proyecto</RouterLink>
        </li>
        <li>
          <RouterLink to="/eventos" @click="closeMenu">Eventos</RouterLink>
        </li>
        <li>
          <RouterLink to="/contacta" @click="closeMenu">Contacta</RouterLink>
        </li>
        <li>
          <RouterLink to="/interes" @click="closeMenu">De interés</RouterLink>
        </li>
      </ul>
    </nav>
  </header>
</template>

<style scoped>
/* --- 1. CONFIGURACIÓN DEL HEADER FIJO --- */
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: var(--white);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* --- 2. ESTILOS GENERALES (Móvil y Escritorio) --- */
.eslogan {
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: var(--lightPink);
  text-align: center;
  font-size: 0.9rem;
}

p {
  margin: 0;
}

.navbar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  background: var(--white);
  position: relative;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.navbar-brand {
  font-size: 1.2rem;
  display: none;
}

.navbar-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  gap: 1rem;
  /* Espacio entre botones */
  transition: transform 0.3s ease-in-out;
}

.navbar-links li {
  /* He quitado el padding de aquí y lo he pasado al enlace 'a' 
     para que el color de fondo ocupe todo el botón */
  padding: 0;
  color: var(--darkPurple);
  cursor: pointer;
  transition: transform 0.2s;
}

/* Estilos de los enlaces */
.navbar-links li a {
  color: inherit;
  text-decoration: none;
  display: block;
  font-weight: 500;
  padding: 0.5rem 1rem;
  /* El padding vive aquí ahora */
  border-radius: 6px;
  transition: background-color 0.3s, color 0.3s;
}

/* Efecto Hover (Ratón por encima) */
.navbar-links li a:hover {
  background-color: var(--lightPink);
  color: var(--darkPurple);
}

/* --- AQUÍ ESTABA EL FALLO --- */
/* Ahora este estilo está fuera del @media, así que aplica siempre */
.navbar-links a.router-link-active {
  background-color: var(--lightPink);
  color: var(--darkPurple);
  font-weight: bold;
  border-radius: 6px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Elementos del menú móvil */
.patita {
  max-width: 2.5rem;
  transition: transform 0.2s;
}

.patita:active {
  transform: scale(0.9);
}

.hamburger {
  display: none;
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
}

/* --- 3. ESTILOS SOLO PARA MÓVIL --- */
@media (max-width: 900px) {
  .navbar {
    justify-content: flex-end;
    padding: 0.5rem 1.5rem;
  }

  .navbar-brand {
    display: block;
  }

  .navbar-links {
    flex-direction: column;
    position: absolute;
    top: 100%;
    right: 0;
    background: var(--white);
    width: 200px;
    height: auto;
    padding: 1rem;
    transform: translateX(100%);
    box-shadow: -4px 4px 10px rgba(0, 0, 0, 0.1);
    border-bottom-left-radius: 15px;
    z-index: 100;
    gap: 0.5rem;
  }

  .navbar-links.active {
    transform: translateX(0);
  }

  .navbar-links li {
    width: 100%;
    text-align: right;
    border-bottom: 1px solid #f0f0f0;
    border-radius: 0;
  }

  .navbar-links li:last-child {
    border-bottom: none;
  }

  .hamburger {
    display: block;
  }

  /* Ajuste específico para móvil del enlace activo */
  .navbar-links a.router-link-active {
    padding-right: 1rem;
    text-align: right;
  }
}
</style>