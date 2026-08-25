# Manual de Implementación — Proyecto Violeta

Sistema de seguridad personal basado en dron autónomo 3DR Solo con ROS 2 Jazzy y companion computer Raspberry Pi 4.

---

## Índice

1. [Hardware requerido](#hardware-requerido)
2. [Instalación de Open Solo 4](#instalación-de-open-solo-4)
3. [Desmontaje del dron y reemplazo de SD](#desmontaje-del-dron-y-reemplazo-de-sd)
4. [Configuración de la Raspberry Pi 4](#configuración-de-la-raspberry-pi-4)
5. [Instalación de ROS 2 Jazzy y MAVROS](#instalación-de-ros-2-jazzy-y-mavros)
6. [Instalación de dependencias Python](#instalación-de-dependencias-python)
7. [Estructura del proyecto](#estructura-del-proyecto)
8. [Configuración de red](#configuración-de-red)
9. [Arranque del sistema](#arranque-del-sistema)
10. [Uso de la interfaz web](#uso-de-la-interfaz-web)
11. [Procedimiento de vuelo](#procedimiento-de-vuelo)
12. [Resolución de problemas comunes](#resolución-de-problemas-comunes)

---

## 1. Hardware requerido

- 3DR Solo (copter + controller)
- Raspberry Pi 4 (con Ubuntu 24.04 preinstalado)
- MicroSD de repuesto (mínimo 8GB, clase 10)
- Fuente de alimentación para la Pi (powerbank o fuente fija)
- Cable ethernet (para configuración inicial)
- Laptop con Windows y acceso SSH
- Batería LiPo 4S completamente cargada para el Solo

---

## 2. Instalación de Open Solo 4

Open Solo 4 es el firmware de código abierto que reemplaza al firmware original del 3DR Solo. Se instala tanto en el copter como en el controller.

### Referencia oficial

Seguir exactamente los pasos descritos en:
`https://github.com/OpenSolo/OpenSolo/wiki/Install-Open-Solo#user-content-OPEN_SOLO_4`

### Resumen del proceso

1. Descargar los archivos de Open Solo 4 desde el repositorio oficial de GitHub.
2. Conectar la laptop a la red WiFi del Solo (`SoloLink_XXXXXX`).
3. Acceder al copter via SSH: `ssh root@10.1.1.10`
4. Acceder al controller via SSH: `ssh root@10.1.1.1`
5. Transferir los archivos de actualización a cada dispositivo via `scp`.
6. Ejecutar el script de instalación en cada uno y esperar a que reinicien.

**IMPORTANTE:** Asegurarse de que la batería del Solo esté completamente cargada antes de iniciar la instalación. Si la batería se agota durante el proceso, los archivos del sistema pueden corromperse, lo que requiere reemplazar la tarjeta SD manualmente (ver sección 3).

---

## 3. Desmontaje del dron y reemplazo de SD

Este procedimiento fue necesario porque la batería del Solo se agotó durante la instalación inicial de Open Solo 4, corrompiendo los archivos del sistema en la tarjeta SD interna.

### Herramientas necesarias

- Destornillador
- Tarjeta MicroSD con imagen de Open Solo 4 ya grabada

### Pasos

1. Apagar el Solo completamente y retirar la batería.
2. Identificar los motores 2 y 4 (motores delanteros: frontal derecho y trasero izquierdo según la numeración ArduCopter).
3. Retirar las hélices de los motores 2 y 4 girándolas en sentido contrario a su rosca.
4. Desatornillar los motores 2 y 4 del chasis (4 tornillos por motor).
5. Levantar con cuidado la placa superior del chasis — los motores 2 y 4 desmontados permiten que la placa tenga suficiente holgura para levantarse sin forzar los cables.
6. Localizar la tarjeta MicroSD en la placa principal del copter.
7. Retirar la SD corrupta e insertar la de repuesto con la imagen de Open Solo 4 ya grabada.
8. Volver a colocar la placa, atornillar los motores 2 y 4, y reinstalar las hélices.
9. Conectar la batería y encender el Solo — debe arrancar con Open Solo 4 correctamente.

### Cómo grabar la imagen en la SD de repuesto

En la laptop, usar **Balena Etcher** o el comando `dd`:

```bash
# En Linux/Mac
sudo dd if=opensorowiki-image.img of=/dev/sdX bs=4M status=progress

# En Windows: usar Balena Etcher (interfaz gráfica)
```

La imagen de Open Solo 4 se descarga desde el repositorio oficial de OpenSolo en GitHub.

---

## 4. Configuración de la Raspberry Pi 4

### Sistema operativo

Ubuntu 24.04 LTS (ARM64) para Raspberry Pi.

### Conectar a la Pi por primera vez (ethernet)

```bash
ssh ubuntu@<IP-ethernet-de-la-Pi>
# Contraseña por defecto: ubuntu
```

La IP se obtiene revisando el router o con `nmap -sn 192.168.X.0/24` desde la laptop.

### Cambiar contraseña

```bash
passwd
# Nueva contraseña del proyecto: violeta
```

### Conectar la Pi al WiFi del Solo

El Solo controller crea una red WiFi. Conectar la Pi a esa red para que funcione como companion computer sin cables:

```bash
sudo nmcli dev wifi connect "SoloLink_3A1989" password "sololink"
sudo nmcli connection modify "SoloLink_3A1989" connection.autoconnect yes
sudo nmcli connection modify "SoloLink_3A1989" connection.autoconnect-priority 10
```

Deshabilitar el ethernet para que no compita con el WiFi al arrancar:

```bash
sudo nmcli connection modify "Wired connection 1" connection.autoconnect no
sudo reboot
```

Después del reinicio, la Pi se conecta automáticamente al WiFi del Solo. Verificar conectividad:

```bash
ping 10.1.1.1
```

### IPs de la red del Solo

| Dispositivo      | IP          |
|------------------|-------------|
| Solo gateway     | 10.1.1.1    |
| Solo copter      | 10.1.1.10   |
| Raspberry Pi 4   | 10.1.1.144  |
| Laptop           | 10.1.1.176  |

### Configurar DNS para instalar paquetes

La red del Solo no tiene salida a internet. Para instalar paquetes, conectar el ethernet temporalmente y agregar DNS:

```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

---

## 5. Instalación de ROS 2 Jazzy y MAVROS

### ROS 2 Jazzy

Se asume que ROS 2 Jazzy ya está instalado en Ubuntu 24.04. Si no está instalado, seguir la guía oficial:
`https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debians.html`

### MAVROS

MAVROS es el paquete que actúa como bridge entre ROS 2 y el protocolo MAVLink del Solo.

```bash
sudo apt install ros-jazzy-mavros ros-jazzy-mavros-extras -y
sudo /opt/ros/jazzy/lib/mavros/install_geographiclib_datasets.sh
```

### Crear workspace de ROS 2

```bash
mkdir -p ~/solo_ws/src
cd ~/solo_ws/src
ros2 pkg create --build-type ament_python solo_guard
cd ~/solo_ws
colcon build
source install/setup.bash
```

---

## 6. Instalación de dependencias Python

Con el ethernet conectado para tener internet:

```bash
sudo apt install python3-pip -y
pip3 install flask flask-socketio eventlet --break-system-packages
pip3 install dronekit --break-system-packages
pip3 install future --break-system-packages
pip3 install websocket-client --break-system-packages
```

### Parche de compatibilidad de DroneKit con Python 3.12

DroneKit no es nativamente compatible con Python 3.12. Aplicar el siguiente parche:

```bash
sed -i 's/collections.MutableMapping/collections.abc.MutableMapping/g' \
    ~/.local/lib/python3.12/site-packages/dronekit/__init__.py

sed -i 's/collections.Callable/collections.abc.Callable/g' \
    ~/.local/lib/python3.12/site-packages/dronekit/__init__.py
```

---

## 7. Estructura del proyecto

Todo el proyecto vive en un único archivo Python que contiene la lógica de vuelo, el servidor web y la interfaz de usuario:

```
~/solo_ws/webapp/
├── solo_guard_dk.py          # Archivo principal del proyecto
└── solo_guard_dk_backup.py   # Backup de versión estable
```

### Componentes dentro de solo_guard_dk.py

**Conexión DroneKit**
Se conecta al Solo via MAVLink sobre UDP:
```python
vehicle = connect('udp:0.0.0.0:14550', wait_ready=True, heartbeat_timeout=30)
```

**Loop de telemetría** (hilo separado, ejecuta cada 1 segundo)
Lee posición GPS, voltaje de batería, modo de vuelo y estado de armado. Emite los datos via Socket.IO a todos los clientes conectados.

**Loop de seguimiento** (hilo separado, ejecuta cada 2 segundos)
Cuando el modo seguimiento está activo, calcula la distancia entre el dron y el objetivo. Si la distancia es mayor a 5 metros, envía un comando `simple_goto` al Solo.

**Servidor Flask + Socket.IO**
Sirve la interfaz web en el puerto 5000 y maneja los siguientes eventos:

| Evento       | Acción en el dron                          |
|--------------|--------------------------------------------|
| `arm`        | Cambia a modo GUIDED, arma y despega a 2m  |
| `follow`     | Guarda coordenadas objetivo y activa seguimiento |
| `panic`      | Activa/desactiva sirena en el browser      |
| `stop`       | Detiene el seguimiento, cambia a modo LOITER |
| `emergency_land` | Cambia a modo LAND inmediatamente      |

**Interfaz HTML/CSS/JS**
Embebida dentro del mismo archivo Python como string. Incluye animación de introducción, panel de telemetría, campos para ingresar coordenadas, y botones de control.

---

## 8. Configuración de red

Para acceder a la web app, tanto la laptop como el celular deben estar conectados al WiFi del Solo:

- **SSID:** `SoloLink_3A1989`
- **Contraseña:** `sololink`

La Raspberry Pi se conecta automáticamente a esta red al arrancar (configurado en la sección 4).

Para SSH a la Pi desde la laptop dentro de la red del Solo:

```bash
ssh ubuntu@10.1.1.144
# Contraseña: violeta
```

---

## 9. Arranque del sistema

### Paso 1 — Encender hardware

1. Encender el controller del Solo (mantener botón hasta que vibre).
2. Encender el copter del Solo (mismo procedimiento).
3. Conectar alimentación a la Raspberry Pi.
4. Conectar laptop y/o celular al WiFi `SoloLink_3A1989`.

### Paso 2 — Conectar a la Pi por SSH

```bash
ssh ubuntu@10.1.1.144
```

### Paso 3 — Abrir tmux para múltiples terminales

```bash
tmux
```

Comandos útiles de tmux:

| Acción               | Comando          |
|----------------------|------------------|
| Nueva ventana        | `Ctrl+B` luego `c` |
| Cambiar a ventana N  | `Ctrl+B` luego `N` |
| Salir sin cerrar     | `Ctrl+B` luego `d` |
| Volver a sesión      | `tmux attach`    |
| Cerrar todo          | `tmux kill-server` |

### Paso 4 — Lanzar MAVROS (Terminal 1)

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch mavros apm.launch fcu_url:="udp://:14550@10.1.1.1:14550"
```

Esperar a ver mensajes de conexión. Es normal ver algunos warnings de parámetros al inicio.

### Paso 5 — Lanzar la web app (Terminal 2)

```bash
source /opt/ros/jazzy/setup.bash
python3 ~/solo_ws/webapp/solo_guard_dk.py
```

Cuando aparezca `Conectado` y la URL del servidor, el sistema está listo.

### Paso 6 — Abrir la interfaz web

En cualquier dispositivo conectado al WiFi del Solo, abrir en el browser:

```
http://10.1.1.144:5000
```

---

## 10. Uso de la interfaz web

La interfaz muestra una animación de introducción al cargarse. Después aparece el panel de control con las siguientes secciones:

### Panel de telemetría
- **Batería:** Porcentaje estimado basado en voltaje (rango 15.2V–16.8V).
- **Estado:** Indica si el dron está armado o en reposo.
- **Modo:** Modo de vuelo actual (LOITER, GUIDED, LAND, etc.).

### Palabra clave de emergencia
Muestra una palabra aleatoria generada al cargar la página. En futuras versiones, el sistema detectará esta palabra via micrófono del dispositivo para activar el protocolo de pánico automáticamente.

### Coordenadas de destino
Ingresar latitud y longitud del punto al que debe navegar el dron. Usar el formato decimal con 6 decimales:

- **Latitud:** `19.054512`
- **Longitud:** `-98.283622`

Las coordenadas se obtienen manteniendo presionado cualquier punto en Google Maps.

### Botones de control

| Botón                     | Función                                              |
|---------------------------|------------------------------------------------------|
| Armar y Despegar          | Arma el dron y despega a 2 metros de altura          |
| Enviar destino            | Envía las coordenadas ingresadas al dron             |
| Pánico                    | Activa/desactiva sirena sonora en el browser         |
| Detener                   | Detiene el seguimiento y pone el dron en modo LOITER |
| Aterrizaje de Emergencia  | Aterriza inmediatamente en la posición actual        |

---

## 11. Procedimiento de vuelo

1. Llevar el dron a un área abierta, sin obstáculos y con cielo despejado.
2. Encender sistema y esperar GPS fix (los mensajes `PreArm: GPS` desaparecen de la terminal cuando el fix es suficiente — mínimo 6 satélites y error horizontal menor a 5m).
3. Ingresar las coordenadas del destino en la app.
4. Presionar **Armar y Despegar** — el dron armará, esperará 3 segundos y subirá a 2 metros.
5. Presionar **Enviar destino** — el dron navegará autónomamente hacia las coordenadas.
6. La distancia mínima recomendada entre el dron y el destino es de **15 metros**. Con distancias menores el vector de dirección es demasiado pequeño y el GPS puede causar errores de navegación.
7. Cuando el dron llegue a menos de 5 metros del destino, se detendrá en hover automáticamente.
8. Para aterrizar, usar el controller del Solo bajando la palanca izquierda, o presionar **Aterrizaje de Emergencia** desde la app.

---

## 12. Resolución de problemas comunes

### La Pi no se conecta al WiFi del Solo al arrancar

Verificar que la conexión esté configurada para autoconectar:

```bash
nmcli connection show "SoloLink_3A1989" | grep autoconnect
```

Si no está activa, ejecutar nuevamente:

```bash
sudo nmcli connection modify "SoloLink_3A1989" connection.autoconnect yes
```

### No hay heartbeat de MAVLink

Verificar que el Solo esté encendido y en la misma red. Comprobar conectividad:

```bash
ping 10.1.1.1
```

Si hay respuesta pero no hay heartbeat, reiniciar MAVROS.

### El dron no cambia a modo GUIDED

El controller del Solo tiene prioridad sobre los comandos de software. DroneKit puede forzar el cambio a GUIDED incluso con el RC activo, lo que es el comportamiento esperado en este proyecto.

### GPS glitching o error horizontal alto

Ocurre principalmente en interiores o bajo techo. Llevar el dron a un área abierta y esperar 2-3 minutos para que el GPS se estabilice.

### El dron vuela en dirección incorrecta

Indica un problema de calibración de compás. Antes de volar, verificar con:

```bash
python3 -c "
from dronekit import connect
vehicle = connect('udp:0.0.0.0:14550', wait_ready=True)
print('Heading:', vehicle.heading)
print('EKF ok:', vehicle.ekf_ok)
vehicle.close()
"
```

Si `ekf_ok` es `False`, realizar la calibración de compás desde la app oficial del Solo o Mission Planner antes de volar.

### Batería baja — el dron no arma

El Solo tiene un failsafe de batería baja que impide el armado. Cargar la batería completamente antes de intentar volar. El porcentaje se muestra en la web app; se recomienda no volar con menos del 30%.

### La web app no carga en el celular

Verificar que el celular esté conectado al WiFi `SoloLink_3A1989` y no a otra red. La app solo es accesible dentro de la red local del Solo.

---

## Credenciales y datos de acceso

| Servicio           | Dato                          |
|--------------------|-------------------------------|
| WiFi Solo          | SoloLink_3A1989 / sololink    |
| SSH Raspberry Pi   | ubuntu@10.1.1.144 / violeta   |
| Web App            | http://10.1.1.144:5000        |
| SSH Solo copter    | root@10.1.1.10                |
| SSH Solo controller| root@10.1.1.1                 |

---

*Proyecto Violeta — Sistema de seguridad personal con dron autónomo*
*Desarrollado con ROS 2 Jazzy, MAVROS, DroneKit y Flask*
