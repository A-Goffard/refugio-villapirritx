<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const usuario = ref('')
const contrasena = ref('')
const cargando = ref(false)
const errorMsg = ref('')

const destino = () => route.query.siguiente || '/gestion'

// Si ya tiene la sesión abierta, directa al panel
onMounted(async () => {
    if (await auth.comprobarSesion()) router.replace(destino())
})

const entrar = async () => {
    cargando.value = true
    errorMsg.value = ''
    try {
        await auth.iniciarSesion(usuario.value, contrasena.value)
        router.replace(destino())
    } catch (e) {
        errorMsg.value = e.response?.status === 400
            ? 'Usuario o contraseña incorrectos.'
            : 'No se ha podido conectar. Inténtalo de nuevo.'
    } finally {
        cargando.value = false
    }
}
</script>

<template>
<div class="body">
    <div class="capaBlanca centre">
        <div class="login-container">
            <img src="/iconos/patita.png" class="patita" alt="Patita">
            <h2>Acceso del refugio</h2>
            <p>Entra para gestionar los animales de la web.</p>

            <form @submit.prevent="entrar" class="mi-formulario">
                <div class="campo">
                    <label for="usuario">Usuario</label>
                    <input id="usuario" v-model="usuario" required autocomplete="username" autocapitalize="none">
                </div>
                <div class="campo">
                    <label for="contrasena">Contraseña</label>
                    <input id="contrasena" type="password" v-model="contrasena" required autocomplete="current-password">
                </div>

                <div v-if="errorMsg" class="error">{{ errorMsg }}</div>

                <button type="submit" class="btnMorado full-width" :disabled="cargando">
                    {{ cargando ? 'Entrando...' : 'Entrar' }}
                </button>
            </form>
        </div>
    </div>
</div>
</template>

<style scoped>
.login-container {
    max-width: 400px;
    width: 100%;
    margin: 2rem auto;
    padding: 2rem;
    background: var(--lightPurple);
    border-radius: 1rem;
    text-align: center;
}

.patita { width: 60px; margin-bottom: 0.5rem; }

.mi-formulario {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    margin-top: 1.5rem;
    text-align: left;
}

.campo { display: flex; flex-direction: column; gap: 0.5rem; }

label { font-weight: bold; color: var(--darkPurple); font-size: 0.9rem; }

input {
    padding: 0.8rem;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: inherit;
}

input:focus {
    outline: 2px solid var(--pink);
    border-color: transparent;
}

.full-width { width: 100%; padding: 0.9rem; font-size: 1rem; }

.error { color: red; font-weight: bold; text-align: center; }
</style>
