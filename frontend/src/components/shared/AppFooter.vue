<script setup>
import { RouterLink } from 'vue-router'

// Obtenemos el año actual automáticamente para el copyright
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="site-footer">
    <div class="footer-content">
      
      <div class="footer-section brand">
        <h3>VILLA PIRRITX</h3>
        <p>
          Dando segundas oportunidades a quienes más lo necesitan. 
          Adopta, colabora y salva vidas.
        </p>
        <div class="socials">
            <a href="https://www.instagram.com/villapirritxanimaliak/" target="_blank" aria-label="Instagram">Instagram</a>
            <a href="https://www.facebook.com/profile.php?id=100068535188856&locale=es_ES" target="_blank" aria-label="Facebook">Facebook</a>
        </div>
      </div>

      <div class="footer-section links">
        <h4>Explora</h4>
        <ul>
          <li><RouterLink to="/">Inicio</RouterLink></li>
          <li><RouterLink to="/adopcion">Adopta un amigo</RouterLink></li>
          <li><RouterLink to="/colabora">Cómo ayudar</RouterLink></li>
          <li><RouterLink to="/eventos">Eventos solidarios</RouterLink></li>
          <li><RouterLink to="/contacta">Contacto</RouterLink></li>
        </ul>
      </div>

      <div class="footer-section contact">
        <h4>Contacto</h4>
        <p>📍 Sondika, Bizkaia</p>
        
        <p>📧 <a href="mailto:villapirritxanimaliak@gmail.com">villapirritxanimaliak@gmail.com</a></p>
        
        <div class="donativos-info">
            <h4>Donativos</h4>            
            <div class="datos-bancarios">
                <p><strong>Bizum:</strong> 699 80 70 49</p>
                <p><strong>Cuenta:</strong> ES66 0081 7515 6100 0154 8864</p>
            </div>
        </div>
      </div>

    </div>

    <div class="footer-bottom">
      <p>© {{ currentYear }} Asociación Protectora de Animales Villa Pirritx. Todos los derechos reservados.</p>
      <p>By <a class="footer-link-Geobizi" href="https://www.geobizi.com" target="_blank"
            rel="noopener noreferrer">Geobizi&lt;TIK&gt;<img class="logo-geobizi" src="/iconos/Hojitas.png"
              alt="Hojitas"></a></p>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  background-color: var(--darkPurple); 
  color: var(--white);
  padding-top: 3rem;
  margin-top: auto; 
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem 2rem;
  gap: 2rem;
}

.footer-section {
  flex: 1;
  min-width: 250px;
}

/* Estilos Columna 1 */
.brand h3 {
  color: var(--lightPink); 
  margin-bottom: 1rem;
}

.brand p {
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.socials {
  display: flex;
  gap: 1rem;
}

.socials a {
  color: var(--white);
  text-decoration: underline;
  font-size: 0.9rem;
}

/* Estilos Columna 2 */
.links h4, .contact h4 {
  color: var(--lightPink);
  margin-bottom: 1.2rem;
  font-size: 1.1rem;
}

.links ul {
  list-style: none;
  padding: 0;
}

.links li {
  margin-bottom: 0.8rem;
}

.links a {
  color: var(--white);
  text-decoration: none;
  transition: color 0.3s;
}

.links a:hover {
  color: var(--lightPink);
  padding-left: 5px; 
}

/* Estilos Columna 3 */
.contact p {
  margin-bottom: 0.8rem;
}

.contact a {
  color: var(--white);
  text-decoration: none;
}

.donativos-info {
    margin-top: 1rem;
}

.datos-bancarios {
    margin-top: 1rem;
    font-size: 0.9rem;
    background: rgba(255,255,255,0.1); /* Fondo sutil para destacar los números */
    padding: 0.5rem;
    border-radius: 8px;
}

.datos-bancarios p {
    margin: 0.3rem 0;
    word-break: break-all; /* Para que el IBAN no rompa el diseño en móvil */
}

/* Barra inferior */
.footer-bottom {
  background-color: #2e0d3f; 
  text-align: center;
  padding: 1rem;
  font-size: 0.85rem;
  color: #ccc;
}
.footer-link-Geobizi {
  display: inline-flex;
  color: var(--darkgreen);
  text-decoration: none;
  transition: color 0.2s ease, transform 0.2s ease;
}
.logo-geobizi {
  height: 17px;
}
/* Responsive */
@media (max-width: 564px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
  }
  
  .links a:hover {
    padding-left: 0;
  }

  .socials {
    justify-content: center;
  }
}
</style>