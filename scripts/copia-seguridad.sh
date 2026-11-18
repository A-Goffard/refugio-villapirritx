#!/usr/bin/env bash
# Copia de seguridad de Villa Pirritx: base de datos + fotos subidas desde el panel.
# Guarda la copia en el servidor y sube otra (cifrada) a Google Drive con rclone.
# Se ejecuta cada noche con cron. Instalación y restauración: scripts/COPIAS.md
set -euo pipefail

# --- Configuración (se puede cambiar con variables de entorno) ---
CARPETA_LOCAL="${CARPETA_LOCAL:-/root/copias-villapirritx}"  # copias dentro del propio servidor
DIAS_LOCAL="${DIAS_LOCAL:-7}"                                 # cuántos días se guardan aquí
DESTINO_DRIVE="${DESTINO_DRIVE:-copias-cifradas:}"            # remoto de rclone configurado en COPIAS.md
DIAS_DRIVE="${DIAS_DRIVE:-30}"                                # cuántos días se guardan en Drive
AVISAR_A="${AVISAR_A:-}"                                      # email para avisos de fallo (vacío = el de la web)

# cron arranca con un PATH mínimo
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Trabajamos desde la carpeta del proyecto (donde está docker-compose.yml)
cd "$(dirname "$0")/.."

TRABAJO=$(mktemp -d)
trap 'rm -rf "$TRABAJO"' EXIT

# Si algo falla, se manda un email usando la configuración de correo de la propia web
avisar_fallo() {
    echo "[$(date '+%F %T')] ERROR: la copia ha fallado en la línea $1"
    docker compose exec -T -e AVISAR_A="$AVISAR_A" backend python manage.py shell -c "
import os
from django.conf import settings
from django.core.mail import send_mail
send_mail('⚠️ Ha fallado la copia de seguridad de la web',
          'La copia de seguridad nocturna de villapirritx.org ha fallado. '
          'El detalle está en /var/log/copia-villapirritx.log, en el servidor.',
          None, [os.environ.get('AVISAR_A') or settings.DEFAULT_FROM_EMAIL])
" || echo "Tampoco se ha podido enviar el email de aviso"
}
trap 'avisar_fallo $LINENO' ERR

FECHA=$(date +%Y-%m-%d_%H%M)
echo "[$(date '+%F %T')] Empezando copia $FECHA"

# 1. Base de datos: copia consistente aunque la web esté funcionando (API de backup de SQLite)
docker compose exec -T backend python -c "
import sqlite3
origen = sqlite3.connect('/app/db.sqlite3')
copia = sqlite3.connect('/tmp/copia.sqlite3')
origen.backup(copia)
copia.close()
origen.close()
"
docker compose cp backend:/tmp/copia.sqlite3 "$TRABAJO/db.sqlite3"
docker compose exec -T backend rm -f /tmp/copia.sqlite3

# 2. Fotos de animales y carteles de eventos
docker compose exec -T backend tar -cf - -C /app media > "$TRABAJO/media.tar"

# 3. Todo junto en un solo archivo, que solo puede leer root
mkdir -p "$CARPETA_LOCAL"
chmod 700 "$CARPETA_LOCAL"
ARCHIVO="$CARPETA_LOCAL/villapirritx-$FECHA.tar.gz"
tar -czf "$ARCHIVO" -C "$TRABAJO" db.sqlite3 media.tar
chmod 600 "$ARCHIVO"
echo "Copia local: $ARCHIVO ($(du -h "$ARCHIVO" | cut -f1))"

# 4. Subir a Google Drive (rclone la cifra al subirla) y borrar allí las antiguas
rclone copy "$ARCHIVO" "$DESTINO_DRIVE"
rclone delete --min-age "${DIAS_DRIVE}d" "$DESTINO_DRIVE"
echo "Subida a Google Drive ($DESTINO_DRIVE)"

# 5. Borrar las copias locales antiguas
find "$CARPETA_LOCAL" -name 'villapirritx-*.tar.gz' -mtime +"$DIAS_LOCAL" -delete

echo "[$(date '+%F %T')] Copia terminada"
