<script setup>
import { RouterLink } from 'vue-router'
import PaginaLegal from '@/components/shared/PaginaLegal.vue'
import { ASOCIACION } from '@/datosLegales'
</script>

<template>
<PaginaLegal titulo="Aviso legal">
    <h2>1. Datos de la asociación</h2>
    <p>En cumplimiento del artículo 10 de la Ley 34/2002, de servicios de la sociedad de la información y de comercio
        electrónico (LSSI), te informamos de que esta web pertenece a:</p>
    <ul>
        <li><strong>Titular:</strong> {{ ASOCIACION.nombre }}</li>
        <li><strong>CIF:</strong> {{ ASOCIACION.cif }}</li>
        <li><strong>Domicilio:</strong> {{ ASOCIACION.domicilio }}</li>
        <li><strong>Inscripción:</strong> {{ ASOCIACION.registro }}</li>
        <li><strong>Email:</strong> <a :href="`mailto:${ASOCIACION.email}`">{{ ASOCIACION.email }}</a></li>
        <li><strong>Web:</strong> {{ ASOCIACION.web }}</li>
    </ul>

    <h2>2. Para qué sirve esta web</h2>
    <p>Esta web informa sobre las actividades de la asociación, los animales que buscan hogar y las formas de
        colaborar con nosotros, y te permite contactar con nosotros y solicitar una adopción.</p>

    <h2>3. Uso de la web</h2>
    <p>Al navegar por esta web te comprometes a usarla de buena fe y a no dar datos falsos en los formularios. La
        asociación puede cambiar el contenido y el diseño de la web en cualquier momento.</p>

    <h2>4. Sobre los animales en adopción</h2>
    <p>Intentamos tener siempre al día la información de cada animal, pero su situación puede cambiar rápido. Que un
        animal aparezca en la web no garantiza que siga disponible. Enviar el cuestionario pre-adopción no supone que la
        adopción esté concedida: la asociación valora cada solicitud y decide qué hogar es el más adecuado para cada
        animal.</p>

    <h2>5. Propiedad intelectual</h2>
    <p>Los textos, fotografías de los animales, logotipos e imágenes de esta web pertenecen a la asociación o a sus
        autores, y no pueden usarse con fines comerciales sin permiso. ¡Pero sí puedes compartir las fichas de los
        animales y nuestras publicaciones para ayudarles a encontrar familia! Te pedimos que indiques que son de
        Villa Pirritx.</p>
    <p>Los logotipos y marcas de otras entidades que aparecen en la web (por ejemplo, Yako Happy) pertenecen a sus
        propietarios.</p>

    <h2>6. Donativos y enlaces a otras webs</h2>
    <p>La web incluye enlaces a redes sociales y a plataformas de donación o venta (Teaming, Coral, Yako Happy). Esas
        páginas son de otras empresas, con sus propias condiciones, y la asociación no responde de su contenido ni de
        su funcionamiento. Las condiciones de la donación de Yako Happy por cada compra las fija esa empresa.</p>

    <h2>7. Responsabilidad</h2>
    <p>Hacemos lo posible para que la web funcione bien y sea segura, pero no podemos garantizar que no haya
        interrupciones o errores. La asociación no se hace responsable de los daños que puedan derivarse de ellos ni
        del mal uso que se haga de la web.</p>

    <h2>8. Datos personales y cookies</h2>
    <p>Cómo tratamos tus datos se explica en la <RouterLink to="/privacidad">política de privacidad</RouterLink>, y las
        cookies en la <RouterLink to="/cookies">política de cookies</RouterLink>.</p>

    <h2>9. Legislación aplicable</h2>
    <p>Este aviso legal se rige por la legislación española.</p>
</PaginaLegal>
</template>
