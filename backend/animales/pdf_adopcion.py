"""PDF del cuestionario pre-adopción relleno, con el mismo orden que el papel del refugio."""
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from . import cuestionario

LOGO = Path(__file__).parent / 'recursos' / 'logo.png'
MORADO = colors.HexColor('#4b1248')
GRIS = colors.HexColor('#666666')

ESTILOS = {
    'refugio': ParagraphStyle('refugio', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=MORADO),
    'subrefugio': ParagraphStyle('subrefugio', fontName='Helvetica', fontSize=10, leading=13, textColor=GRIS),
    'titulo': ParagraphStyle('titulo', fontName='Helvetica-Bold', fontSize=15, leading=19, alignment=1,
                             spaceBefore=6, spaceAfter=4),
    'datos': ParagraphStyle('datos', fontName='Helvetica', fontSize=10, leading=13, alignment=1, textColor=GRIS),
    'texto': ParagraphStyle('texto', fontName='Helvetica', fontSize=9.5, leading=13, alignment=4),
    'seccion': ParagraphStyle('seccion', fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=MORADO,
                              spaceBefore=14, spaceAfter=6),
    'pregunta': ParagraphStyle('pregunta', fontName='Helvetica-Bold', fontSize=9.5, leading=12, spaceBefore=6),
    'respuesta': ParagraphStyle('respuesta', fontName='Helvetica', fontSize=10, leading=13, leftIndent=10,
                                spaceBefore=2),
    'vacia': ParagraphStyle('vacia', fontName='Helvetica-Oblique', fontSize=9, leading=12, leftIndent=10,
                            spaceBefore=2, textColor=colors.HexColor('#aaaaaa')),
}


def _texto(valor):
    """Escapa el texto del usuario para que reportlab no lo interprete como etiquetas."""
    return escape(valor).replace('\n', '<br/>')


def _pie(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(GRIS)
    canvas.drawString(2 * cm, 1.2 * cm, 'Refugio Villa Pirritx · Cuestionario pre-adopción · Documento confidencial')
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f'Página {doc.page}')
    canvas.restoreState()


def generar_pdf(solicitud):
    definicion = cuestionario.CUESTIONARIOS[solicitud.especie]
    respuestas = solicitud.respuestas or {}
    fecha = timezone.localtime(solicitud.fecha).strftime('%d/%m/%Y %H:%M')

    cabecera = Table(
        [[[Paragraph('Refugio Villa Pirritx', ESTILOS['refugio']),
           Paragraph('Protectora de Animales', ESTILOS['subrefugio'])],
          Image(str(LOGO), width=2.6 * cm, height=2.6 * cm * 784 / 914)]],
        colWidths=[None, 3 * cm],
    )
    cabecera.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))

    historia = [
        cabecera,
        Paragraph(definicion['titulo'].upper(), ESTILOS['titulo']),
        Paragraph(f'Animal: <b>{_texto(solicitud.nombre_animal)}</b> ({solicitud.get_especie_display()}) · '
                  f'Solicitud recibida el {fecha}', ESTILOS['datos']),
        Spacer(1, 8),
        Paragraph(_texto(definicion['introduccion']), ESTILOS['texto']),
    ]

    for seccion in definicion['secciones']:
        historia.append(Paragraph(_texto(seccion['titulo']), ESTILOS['seccion']))
        for pregunta in seccion['preguntas']:
            respuesta = respuestas.get(pregunta['clave'])
            historia.append(KeepTogether([
                Paragraph(_texto(pregunta['texto']), ESTILOS['pregunta']),
                Paragraph(_texto(respuesta), ESTILOS['respuesta']) if respuesta
                else Paragraph('Sin respuesta', ESTILOS['vacia']),
            ]))

    historia += [Spacer(1, 14), Paragraph(_texto(definicion['despedida']), ESTILOS['texto'])]

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.6 * cm, bottomMargin=2 * cm,
        title=f'Cuestionario pre-adopción - {solicitud.nombre} - {solicitud.nombre_animal}', author='Refugio Villa Pirritx',
    )
    doc.build(historia, onFirstPage=_pie, onLaterPages=_pie)
    return buffer.getvalue()
