Compilar proyecto en C#:
dotnet clean
dotnet build -c Release 
dotnet run

Copiar todas las dependencias al .exe en C#: <- Esto permite ejecutar el programa en cualquier directorio sin necesidad de tener las dependencias.
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:IncludeAllContentForSelfExtract=true