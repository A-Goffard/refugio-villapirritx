// Lado máximo en píxeles (el backend usa el mismo límite)
const LADO_MAXIMO = 1600

// Reduce la foto en el propio móvil antes de subirla: pasa de varios MB a unos cientos de KB.
// Si el navegador no puede leerla (p. ej. HEIC en un ordenador), se sube tal cual.
export async function reducirImagen(archivo) {
    const url = URL.createObjectURL(archivo)
    try {
        const imagen = new Image()
        imagen.src = url
        await imagen.decode()

        const escala = Math.min(1, LADO_MAXIMO / Math.max(imagen.naturalWidth, imagen.naturalHeight))
        const canvas = document.createElement('canvas')
        canvas.width = Math.round(imagen.naturalWidth * escala)
        canvas.height = Math.round(imagen.naturalHeight * escala)
        canvas.getContext('2d').drawImage(imagen, 0, 0, canvas.width, canvas.height)

        const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', 0.85))
        if (!blob) return archivo
        const nombre = archivo.name.replace(/\.[^.]+$/, '') + '.jpg'
        return new File([blob], nombre, { type: 'image/jpeg' })
    } catch {
        return archivo
    } finally {
        URL.revokeObjectURL(url)
    }
}
