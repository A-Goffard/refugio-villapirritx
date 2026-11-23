<script setup>
import { RouterLink } from 'vue-router'
import PaginaLegal from '@/components/shared/PaginaLegal.vue'
import { ASOCIACION } from '@/datosLegales'
</script>

<template>
<PaginaLegal titulo="Política de privacidad">
    <p>
        En {{ ASOCIACION.nombre }} cuidamos los datos de las personas que nos escribís igual que cuidamos de los
        animales. Aquí te explicamos, de forma sencilla, qué datos recogemos en esta web, para qué y qué derechos tienes,
        de acuerdo con el Reglamento General de Protección de Datos (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD).
    </p>

    <h2>1. ¿Quién es el responsable de tus datos?</h2>
    <ul>
        <li><strong>Responsable:</strong> {{ ASOCIACION.nombre }}</li>
        <li><strong>CIF:</strong> {{ ASOCIACION.cif }}</li>
        <li><strong>Domicilio:</strong> {{ ASOCIACION.domicilio }}</li>
        <li><strong>Email:</strong> <a :href="`mailto:${ASOCIACION.email}`">{{ ASOCIACION.email }}</a></li>
    </ul>

    <h2>2. ¿Qué datos tratamos y para qué?</h2>
    <p><strong>Formulario de contacto</strong> (casa de acogida, voluntariado, donación de material, viajes solidarios y
        otras consultas): tu nombre, email, teléfono y el mensaje que nos escribas. Los usamos para responderte y
        organizar la colaboración que nos ofreces.</p>

    <p><strong>Cuestionario pre-adopción:</strong> tus datos identificativos y de contacto (nombre, DNI, domicilio,
        teléfono, email, año de nacimiento, estado civil, profesión) y tus respuestas sobre tu vivienda, las personas
        con las que convives, tus horarios, tu experiencia con animales y tu veterinario/a. Los usamos para valorar si la
        adopción es adecuada para el animal y para tu familia, contactar contigo y, si la adopción sigue adelante,
        preparar el contrato de adopción y hacer el seguimiento posterior.</p>
    <p>El cuestionario pregunta si alguien de tu familia tiene alergias. Es un dato de salud, que solo tratamos porque
        nos das tu <strong>consentimiento explícito</strong> al enviar el cuestionario, y únicamente para comprobar que
        la convivencia con el animal será posible.</p>

    <p><strong>Emails que nos envíes</strong> directamente: tu dirección y lo que nos cuentes, para responderte.</p>

    <p><strong>Visitas a la web:</strong> como casi todas las webs, el servidor guarda un registro técnico de cada visita
        (dirección IP, fecha y hora, página visitada y tipo de navegador). Solo se usa para mantener la web segura y
        resolver errores, y no lo usamos para saber quién eres.</p>

    <p><strong>Donativos por transferencia o Bizum:</strong> los datos que aparezcan en la operación (nombre, cuenta o
        teléfono e importe), para registrar el donativo y cumplir nuestras obligaciones contables.</p>

    <p>No usamos tus datos para enviarte publicidad ni para elaborar perfiles, y no tomamos decisiones automatizadas
        sobre ti.</p>

    <h2>3. ¿Por qué podemos tratarlos? (base legal)</h2>
    <ul>
        <li><strong>Formulario de contacto y emails:</strong> tu consentimiento, que nos das al marcar la casilla del
            formulario o al escribirnos (art. 6.1.a RGPD).</li>
        <li><strong>Cuestionario pre-adopción:</strong> tu solicitud para adoptar, que necesitamos valorar antes de
            firmar el contrato de adopción (art. 6.1.b RGPD), y tu consentimiento explícito para el dato sobre alergias
            (art. 9.2.a RGPD).</li>
        <li><strong>Donativos:</strong> el cumplimiento de obligaciones legales contables y fiscales (art. 6.1.c RGPD).</li>
        <li><strong>Registro de visitas:</strong> nuestro interés legítimo en mantener la web segura y funcionando
            (art. 6.1.f RGPD).</li>
    </ul>
    <p>Puedes retirar tu consentimiento cuando quieras escribiéndonos. Eso no afecta a lo que hayamos hecho antes con
        él.</p>

    <h2>4. ¿Cuánto tiempo los guardamos?</h2>
    <ul>
        <li><strong>Contacto y emails:</strong> el tiempo necesario para atenderte y, como máximo, un año desde nuestra
            última comunicación.</li>
        <li><strong>Solicitudes de adopción que no siguen adelante:</strong> como máximo, un año desde que las
            recibimos.</li>
        <li><strong>Adopciones formalizadas:</strong> mientras dure el seguimiento del animal y, después, durante los
            plazos que exija la ley.</li>
        <li><strong>Donativos:</strong> durante los plazos que exija la normativa contable y fiscal.</li>
        <li><strong>Registro de visitas:</strong> 15 días; después se borra automáticamente.</li>
    </ul>
    <p>Pasados esos plazos, los borramos.</p>

    <h2>5. ¿Con quién los compartimos?</h2>
    <p>No vendemos ni cedemos tus datos a nadie, salvo que una ley nos obligue (por ejemplo, a la Administración
        Pública o a juzgados).</p>
    <p>Para que la web funcione usamos estos proveedores, que solo pueden usar tus datos siguiendo nuestras
        instrucciones:</p>
    <ul>
        <li><strong>{{ ASOCIACION.alojamiento }}</strong>: servidor donde está alojada esta web y donde se guardan los
            formularios.</li>
        <li><strong>{{ ASOCIACION.copias }}</strong>: servidor en España donde guardamos las copias de seguridad
            cifradas de la web.</li>
        <li><strong>Google (Gmail)</strong>: la cuenta de correo de la asociación, donde recibimos los avisos de los
            formularios y tus emails. Google puede tratar datos fuera de la Unión Europea; lo hace con las garantías
            del Marco de Privacidad de Datos UE-EE. UU.</li>
    </ul>
    <p>Si colaboras a través de <strong>Teaming</strong>, <strong>Coral</strong> o <strong>Yako Happy</strong>, son esas
        plataformas quienes recogen y tratan tus datos, con sus propias políticas de privacidad. Nosotros no recibimos
        tus datos de pago.</p>

    <h2>6. ¿Qué derechos tienes?</h2>
    <p>Puedes pedirnos en cualquier momento:</p>
    <ul>
        <li><strong>Acceso:</strong> saber qué datos tuyos tenemos.</li>
        <li><strong>Rectificación:</strong> corregir los que estén mal.</li>
        <li><strong>Supresión:</strong> que los borremos.</li>
        <li><strong>Oposición</strong> y <strong>limitación:</strong> que dejemos de usarlos, o que solo los
            guardemos.</li>
        <li><strong>Portabilidad:</strong> recibirlos en un formato que puedas llevar a otro sitio.</li>
    </ul>
    <p>Escríbenos a <a :href="`mailto:${ASOCIACION.email}`">{{ ASOCIACION.email }}</a> con el asunto
        «Protección de datos», contándonos qué necesitas. Si no podemos saber que eres tú, te pediremos algún dato
        para comprobarlo. Te responderemos en un plazo máximo de un mes.</p>
    <p>Si crees que no hemos tratado bien tus datos, puedes presentar una reclamación ante la
        <a href="https://www.aepd.es" target="_blank" rel="noopener">Agencia Española de Protección de Datos</a>.</p>

    <h2>7. Otras cosas que debes saber</h2>
    <ul>
        <li>Para enviarnos tus datos debes tener al menos 14 años. Para adoptar, tienes que ser mayor de edad.</li>
        <li>Los datos que nos des deben ser ciertos. Si nos das datos de otras personas (por ejemplo, de quienes viven
            contigo o de tu veterinario/a), debes haberles informado antes.</li>
        <li>Solo el equipo de la asociación puede ver los formularios, desde un panel protegido con contraseña, y la
            web funciona con conexión cifrada (HTTPS). Hacemos copias de seguridad diarias, cifradas, que se borran
            a los 30 días.</li>
        <li>Sobre las cookies, consulta nuestra <RouterLink to="/cookies">política de cookies</RouterLink>.</li>
    </ul>

    <h2>8. Cambios en esta política</h2>
    <p>Si cambiamos esta política, lo publicaremos en esta página y actualizaremos la fecha de arriba.</p>
</PaginaLegal>
</template>
