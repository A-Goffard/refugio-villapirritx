import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

// Un 403 puede ser sesión caducada o un fallo de CSRF (configuración del servidor):
// solo lo primero debe mandar a la pantalla de login
export const esSesionCaducada = (error) =>
  error.response?.status === 403 && !error.response.data?.detail?.startsWith('CSRF')

export const useAuthStore = defineStore('auth', () => {
  const usuario = ref(null)
  const comprobado = ref(false)

  // Pregunta al backend si hay sesión abierta (y de paso recibe la cookie CSRF)
  async function comprobarSesion() {
    if (comprobado.value) return usuario.value
    try {
      const { data } = await axios.get('/api/auth/sesion/')
      usuario.value = data.usuario
    } catch {
      usuario.value = null
    }
    comprobado.value = true
    return usuario.value
  }

  async function iniciarSesion(nombre, contrasena) {
    await comprobarSesion()
    const { data } = await axios.post('/api/auth/login/', { usuario: nombre, contrasena })
    usuario.value = data.usuario
  }

  async function cerrarSesion() {
    try {
      await axios.post('/api/auth/logout/')
    } finally {
      usuario.value = null
    }
  }

  // Si el backend responde 403 es que la sesión ha caducado
  function sesionCaducada() {
    usuario.value = null
  }

  return { usuario, comprobarSesion, iniciarSesion, cerrarSesion, sesionCaducada }
})
