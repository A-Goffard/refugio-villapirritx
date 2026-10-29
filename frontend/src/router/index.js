import { createRouter, createWebHistory } from "vue-router";

// Importamos las vistas
import HomeView from "@/views/HomeView.vue";
// import AboutView from "@/views/AboutView.vue";
import AdopcionView from "@/views/AdopcionView.vue";
import ColaboraView from "@/views/ColaboraView.vue";
import ProyectoView from "@/views/ProyectoView.vue";
import EventosView from "@/views/EventosView.vue";
import ContactoView from "@/views/ContactoView.vue";
import FormularioView from "@/views/FormularioView.vue";
// import InteresView from "@/views/InteresView.vue";
import SolicitudAdopcion from "../views/SolicitudAdopcion.vue";
import LoginView from "@/views/LoginView.vue";
import GestionView from "@/views/GestionView.vue";
import { useAuthStore } from "@/stores/auth";

// NOTA: No hace falta importar Header y Footer aquí,
// porque ya están puestos fijos en App.vue.
// Pero si quieres dejarlos para probar, usa la ruta correcta:
// import AppHeader from "@/components/shared/AppHeader.vue";
// import AppFooter from "@/components/shared/AppFooter.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  scrollBehavior(to, from, savedPosition) {
    // Si le das al botón "Atrás" del navegador, vuelve donde estabas
    if (savedPosition) {
      return savedPosition;
    } else {
      // Si vas a una página nueva, sube arriba del todo
      return { top: 0 };
    }
  },

  routes: [
    { path: "/", name: "home", component: HomeView },
    // { path: "/about", name: "about", component: AboutView },
    { path: "/colabora", name: "colabora", component: ColaboraView },
    { path: "/adopcion", name: "adopcion", component: AdopcionView },
    { path: "/proyecto", name: "proyecto", component: ProyectoView },
    { path: "/eventos", name: "eventos", component: EventosView },
    { path: "/contacta", name: "contacto", component: ContactoView },
    // { path: "/interes", name: "interes", component: InteresView },
    { path: "/formulario", name: "formulario", component: FormularioView },

    // Rutas del panel del refugio
    { path: "/acceso", name: "acceso", component: LoginView },
    {
      path: "/gestion",
      name: "gestion",
      component: GestionView,
      meta: { requiereLogin: true },
    },
    { path: "/subida", redirect: "/gestion" },
    { path: "/gestion-adopciones", redirect: "/gestion" },
    {
      path: "/solicitud",
      name: "solicitud",
      component: SolicitudAdopcion,
    },

    // Comodín
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});

// Las páginas del panel solo se ven con la sesión iniciada
router.beforeEach(async (to) => {
  if (!to.meta.requiereLogin) return true;
  const auth = useAuthStore();
  if (await auth.comprobarSesion()) return true;
  return { name: "acceso", query: { siguiente: to.fullPath } };
});

export default router;
