// Django devuelve las fotos con http:// en el servidor; la web va por https
export const hacerUrlSegura = (url) => {
    if (!url) return null;

    // Excepción local
    if (url.includes('127.0.0.1') || url.includes('localhost')) {
        return url;
    }

    // Corrección HTTPS para la web
    if (url.startsWith('http://')) {
        return url.replace('http://', 'https://');
    }

    return url;
}
