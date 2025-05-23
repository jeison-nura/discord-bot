# discord-bot

# Bot de Discord para Reproducción de Música

Este es un bot de Discord simple que permite reproducir música desde YouTube en canales de voz.

## Características

- 🎵 Reproducción de música desde URLs de YouTube
- ⏯️ Comandos para pausar y reanudar la reproducción
- ⏹️ Detener la reproducción y desconectar el bot
- 🔄 Desconexión automática al finalizar la canción

## Requisitos previos

- Python 3.8 o superior
- FFmpeg instalado en el sistema
- Token de bot de Discord

## Instalación

1. Clona este repositorio:
   bash

Run

Open Folder

1

2

git clone https://github.com/tu-usuario/

discord-bot.git

cd discord-bot

2. Instala las dependencias:
   bash

Run

Open Folder

1

pip install -r requirements.txt

3. Crea un archivo .env en la raíz del proyecto con tu token de Discord:
   plaintext

Open Folder

1

DCTOKEN=tu_token_aqui

4. Asegúrate de tener FFmpeg instalado:
   bash

Run

Open Folder

1

winget install "FFmpeg (Essentials Build)"

## Uso

Para iniciar el bot:

bash

Run

Open Folder

1

python bot.py

### Comandos disponibles

- > play [url] - Reproduce música desde la URL proporcionada
- > stop - Detiene la reproducción y desconecta el bot
- > pause - Pausa la reproducción actual
- > resume - Reanuda la reproducción pausada
- > hello - Saluda al bot

## Configuración

Si FFmpeg está instalado en una ubicación diferente, puedes modificar la ruta en el archivo bot.py :

python

Open Folder

1

2

3

4

5

ffmpeg_options = {

'executable' : 'ruta/a/tu/ffmpeg.exe' ,

'before_options' : '-reconnect 1

-reconnect_streamed 1

-reconnect_delay_max 5 -probesize 10M

-analyzeduration 10M' ,

'options' : '-vn -bufsize 8192k'

}

## Solución de problemas

- Error "ffmpeg was not found" : Asegúrate de que FFmpeg esté instalado correctamente y que la ruta en el código sea correcta.
- Problemas de conexión : Verifica que el bot tenga los permisos necesarios en el servidor de Discord.
- Reproducción interrumpida : Intenta ajustar los parámetros de buffer en las opciones de FFmpeg.

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios que te gustaría hacer.

## Licencia

MIT
