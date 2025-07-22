<p align="center">
  <img src="https://github.com/user-attachments/assets/ac3541ca-952e-4511-a259-764834982f8d" alt="XilentDoor" Logo" />
</p>

<p align="center">
   <a href="https://dotnet.microsoft.com/">
    <img src="https://img.shields.io/badge/C%23-Backdoor-blue.svg">
  </a>
    <img src="https://img.shields.io/badge/Release-1.0-blue.svg">
  </a>
    <img src="https://img.shields.io/badge/Public-%F0%9F%97%9D%EF%B8%8F-green.svg">
  </a>
</p>

<h1 align="center"></h1>

### Acerca de XilentDoor

XilentDoor es un backdoor escrito en C# orientado a sistemas Windows. Un backdoor es un tipo de malware diseñado para abrir una puerta trasera permanente en el equipo comprometido, permitiendo al atacante acceder y controlar el sistema de forma sigilosa. 

Es parte de la familia <a href="https://github.com/R3LI4NT/XilentLocker">XilentLocker</a> y <a href="https://github.com/R3LI4NT/XilentRAT">XilentRAT</a>.

<h1 align="center"></h1>

### Características de XilentDoor `1.0`:

- [x] **Persistencia:** El Backdoor se auto-copia en la ruta `AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`, lo que permite que se ejecute automáticamente cada vez que el sistema se reinicie.
      <img width="906" height="127" alt="1" src="https://github.com/user-attachments/assets/899fbcd5-a4bc-4e7e-a38d-12f2a8615b60" />

- [x] **Fingerprinting:** Recopila información básica del sistema donde se ejecuta el backdoor. Esta funcionalidad se suele usar para identificar la máquina víctima o confirmar la infección exitosa antes de enviar datos al atacante.
      <img width="603" height="221" alt="2" src="https://github.com/user-attachments/assets/e15ade45-30cc-46a5-ba86-ac91e0acf4a3" />

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

Correo de contacto:

<img src="https://img.shields.io/badge/r3li4nt.contact@keemail.me-D14836?style=for-the-badge&logo=gmail&logoColor=white" />

<h1 align="center"></h1>

> [!CAUTION]
> Cualquier uso indebido de este software será de exclusiva responsabilidad del usuario final, y no del autor. Este proyecto tiene como objetivo inicial demostrar las capacidades de C# como lenguaje para el desarrollo de malware en entornos controlados. 

<h1 align="center"></h1>

#### Developer: ~R3LI4NT~
