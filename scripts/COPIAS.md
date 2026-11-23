# Copias de seguridad de Villa Pirritx

Cada noche, [`copia-seguridad.sh`](copia-seguridad.sh) guarda la base de datos (animales, eventos, solicitudes) y
las fotos subidas desde el panel:

- **En el servidor de la web**: `/root/copias-villapirritx/`, los últimos 7 días (sin cifrar, solo las lee root).
- **En el VPS de copias** (194.164.166.99, Piensa Solutions, España): los últimos 30 días, **cifradas** antes de
  salir del servidor (contienen DNI y datos de salud del cuestionario de adopción).

El servidor de la web **solo puede añadir** copias al VPS: no puede borrarlas ni renombrarlas, y en menos de una
hora pasan a ser de solo lectura. Así, si alguien entrara en el servidor de la web, no podría destruir las copias.
Los 30 días los borra un cron del propio VPS de copias.

Si la copia falla, llega un email de aviso (al Gmail de la asociación, o a quien se indique en `AVISAR_A`).

> ⚠️ Las dos contraseñas del cifrado (paso 4) son imprescindibles para recuperar las copias.
> Si se pierden, las copias no sirven de nada. Guardadlas en un gestor de contraseñas.

---

## Instalación en el VPS de copias (una sola vez, como root)

Mantén abierta tu sesión SSH mientras lo haces, por si un error en la configuración te dejara fuera.

### 1. Usuario solo para recibir las copias

Sin shell, sin contraseña y encerrado en su carpeta, separado de las webs que haya en ese VPS:

```bash
useradd --system --no-create-home --home-dir /srv/copias-villapirritx \
        --shell /usr/sbin/nologin copias-villapirritx

# La raíz de su "jaula" es de root; solo la subcarpeta villapirritx es suya
mkdir -p /srv/copias-villapirritx/villapirritx
chown root:root /srv/copias-villapirritx && chmod 755 /srv/copias-villapirritx
chown copias-villapirritx:copias-villapirritx /srv/copias-villapirritx/villapirritx
chmod 700 /srv/copias-villapirritx/villapirritx

# Sus claves, fuera de la jaula, donde el usuario no puede tocarlas
mkdir -p /etc/ssh/authorized_keys && chmod 755 /etc/ssh/authorized_keys
```

### 2. Solo SFTP y sin poder borrar

Añadir al **final** de `/etc/ssh/sshd_config`:

```
# --- Copias de Villa Pirritx: solo SFTP, encerrado en su carpeta, sin poder borrar ---
Match User copias-villapirritx
    AuthorizedKeysFile /etc/ssh/authorized_keys/%u
    AuthenticationMethods publickey
    PasswordAuthentication no
    KbdInteractiveAuthentication no
    ChrootDirectory /srv/copias-villapirritx
    ForceCommand internal-sftp -d /villapirritx -P remove,rmdir,rename,posix-rename,symlink,hardlink
    AllowTcpForwarding no
    AllowAgentForwarding no
    X11Forwarding no
    PermitTunnel no
```

Comprobar con `sshd -t` (no debe mostrar nada). Se activa en el paso 3, al recargar SSH.

### 3. Proteger las copias recibidas y borrar las de más de 30 días

SFTP impide borrar y renombrar, pero el usuario podría reescribir un archivo suyo. Por eso, cada hora, las copias
recibidas pasan a ser de root y de solo lectura (el usuario puede seguir leyéndolas para restaurar):

```bash
cat > /etc/cron.d/copias-villapirritx <<'EOF'
# Copias de Villa Pirritx: cada hora, las recibidas pasan a ser de root y de solo lectura
15 * * * * root find /srv/copias-villapirritx/villapirritx -type f -name 'villapirritx-*' ! -user root -exec chown root:root {} + -exec chmod 444 {} +
# Borrar las de más de 30 días
30 6 * * * root find /srv/copias-villapirritx/villapirritx -type f -name 'villapirritx-*' -mtime +30 -delete
EOF
```

---

## Instalación en el servidor de la web (una sola vez, como root)

### 1. Instalar rclone

```bash
curl https://rclone.org/install.sh | sudo bash
```

### 2. Clave SSH solo para las copias

```bash
ssh-keygen -t ed25519 -N "" -C "copias villapirritx" -f /root/.ssh/copias_villapirritx
cat /root/.ssh/copias_villapirritx.pub     # clave pública: se puede copiar sin problema
curl -4 -s ifconfig.me; echo               # IP pública de este servidor
```

La clave privada (`/root/.ssh/copias_villapirritx`) no sale nunca de este servidor ni se sube al repositorio.

En el **VPS de copias**, autorizar esa clave solo desde esa IP (todo en **una sola línea**) y recargar SSH:

```bash
echo 'from="IP_DEL_SERVIDOR_WEB",restrict ssh-ed25519 AAAA...clave pública... copias villapirritx' \
  > /etc/ssh/authorized_keys/copias-villapirritx
chmod 644 /etc/ssh/authorized_keys/copias-villapirritx
sshd -t && systemctl reload ssh
```

De vuelta en el servidor de la web, primera conexión para guardar la huella del VPS. Antes de responder `yes`,
compárala con la que da `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` en el VPS de copias:

```bash
printf 'pwd\nls /\n' | sftp -i /root/.ssh/copias_villapirritx copias-villapirritx@194.164.166.99
```

Debe responder `/villapirritx` y, en `ls /`, mostrar solo `villapirritx`.

### 3. Conexión SFTP en rclone

```bash
rclone config create vps-copias sftp host=194.164.166.99 user=copias-villapirritx \
  key_file=/root/.ssh/copias_villapirritx known_hosts_file=/root/.ssh/known_hosts shell_type=none
rclone lsd vps-copias:/      # debe listar la carpeta villapirritx
```

### 4. Cifrado

```bash
rclone config
```

1. `n` → nombre: `copias-vps`
2. Tipo de almacenamiento: `crypt`
3. `remote`: `vps-copias:/villapirritx`
4. `filename_encryption`: **`off`** (los nombres, con la fecha, se siguen viendo; el contenido no)
5. `directory_name_encryption`: `false`
6. `password`: `y` y la contraseña 1. **Guárdala.**
7. `password2` (salt): `y` y la contraseña 2, distinta. **Guárdala también.**
8. Confirma con `y` y sal con `q`.

Si ya había copias cifradas con otras contraseñas, usa las mismas: así una sola pareja sirve para todas.

### 5. Probar

```bash
cd ~/refugio-animales
./scripts/copia-seguridad.sh
rclone ls copias-vps:
```

Tiene que terminar con "Copia terminada" y listar `villapirritx-FECHA.tar.gz`. En el VPS de copias aparece en
`/srv/copias-villapirritx/villapirritx/` como `villapirritx-FECHA.tar.gz.bin`: es la misma copia, cifrada.

Comprobar también que **no se puede borrar** desde aquí (este comando tiene que fallar con "permission denied"):

```bash
rclone deletefile copias-vps:villapirritx-FECHA.tar.gz
```

### 6. Programarla cada noche

```bash
crontab -e
```

Añade esta línea al final (copia a las 3:30 UTC), con el email que debe recibir los avisos de fallo (si se quita
`AVISAR_A=...`, llegan al Gmail de la asociación):

```
30 3 * * * AVISAR_A=tu@email.com /root/refugio-animales/scripts/copia-seguridad.sh >> /var/log/copia-villapirritx.log 2>&1
```

Para ver cómo han ido las últimas copias: `tail -n 20 /var/log/copia-villapirritx.log`

---

## Comprobar que una copia se puede restaurar (recomendado: una vez al mes)

En una carpeta de prueba, **nunca sobre la web**:

```bash
mkdir -p /root/prueba-restauracion && cd /root/prueba-restauracion
rclone ls copias-vps:                                      # elegir una copia
rclone copy copias-vps:villapirritx-FECHA.tar.gz .         # baja y descifra
tar -xzf villapirritx-FECHA.tar.gz                         # deja db.sqlite3 y media.tar
python3 -c "import sqlite3; c=sqlite3.connect('db.sqlite3'); print(c.execute('PRAGMA integrity_check').fetchone()[0]); print('animales:', c.execute('select count(*) from animales_animal').fetchone()[0]); print('solicitudes de adopción:', c.execute('select count(*) from animales_solicitudadopcion').fetchone()[0])"
tar -tf media.tar | wc -l                                  # número de fotos
cd / && rm -rf /root/prueba-restauracion                   # borrar: contiene DNI
```

Tiene que salir `ok` y unos números que cuadren con el panel. Eso demuestra que la copia se descifra, no está
corrupta y tiene datos.

---

## Restaurar una copia

Sirve también para **migrar la web a otro servidor**: despliega la web en el servidor nuevo, configura rclone
(pasos 1 a 4 del servidor de la web, con las **mismas contraseñas** de cifrado, y autoriza la IP nueva en el VPS
de copias) y restaura la última copia.

> En un servidor nuevo, copia `db.sqlite3` a `backend/db.sqlite3` **antes** del primer `docker compose up`.
> Si no existe, Docker crea una carpeta con ese nombre y la web no arranca (habría que borrarla y repetir).

```bash
cd ~/refugio-animales

# 1. Ver las copias disponibles y bajar la que quieras (se descifra sola)
rclone ls copias-vps:
rclone copy copias-vps:villapirritx-2026-11-23_0330.tar.gz /root/restaurar/
#    (o usar una de /root/copias-villapirritx/ si el servidor sigue vivo)

# 2. Descomprimir
cd /root/restaurar
tar -xzf villapirritx-2026-11-23_0330.tar.gz      # deja db.sqlite3 y media.tar

# 3. Parar la web, poner la base de datos y las fotos, y volver a arrancar
cd ~/refugio-animales
docker compose stop backend
cp /root/restaurar/db.sqlite3 backend/db.sqlite3
docker compose run --rm -T backend tar -xf - -C /app < /root/restaurar/media.tar
docker compose up -d
docker compose exec -T backend python manage.py migrate --noinput
```

Las copias anteriores al cambio de destino están en Google Drive, cifradas con las mismas contraseñas, mientras
no se borren. Para restaurar una de ellas, usar el remoto `copias-cifradas:` en lugar de `copias-vps:`.
