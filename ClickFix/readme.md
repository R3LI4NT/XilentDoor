<p align="center">
  <a href="https://github.com/DenverCoder1/readme-typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=F70000&width=300&lines=Ataque+de+ClickFix"></a>
</p>

<h1 align="center"></h1>

<h3 align="center"><ins>ClickFix - Ingeniería Social</ins></h3>

Últimamente los grupos de malware utilizan la técnica de ClickFix, un método por el cual engañan al usuario para que copie y ejecute manualmente un comando o acción que aparentemente se ve "inofensiva", pero que en realidad instala un malware o da acceso al atacante (reverse shell). Los diseños suelen ser una alerta, captcha falso o un error que no existe. 

En la siguiente captura pueden observar una página de verificación que diseñé con un estilo visual de Cloudflare:

<img width="1365" height="671" alt="ClickFix-1" src="https://github.com/user-attachments/assets/cfd99dfc-fe8c-4ef0-9d0c-14d195f636f3" />

Se le pidé al usuario que copie la ruta `C:\Users\Default\verification.conf` pero al hacerlo también está copiando un código malicioso en PowerShell.

<img width="1141" height="428" alt="ClickFix-2" src="https://github.com/user-attachments/assets/0949045e-cf1d-425f-973f-46b5647a1a8a" />

Sin embargo, al copiarlo también se agregan espacios en blanco por lo que si intenta pegarlo en el Explorador de Archivos (**Paso 3**) solo verá la ruta.

<img width="709" height="82" alt="ClickFix-3" src="https://github.com/user-attachments/assets/a3d734c4-1356-49fd-8fb5-2abe8aec175e" />

Si se retrocede se puede ver el código de powershell que también fue copiado, pero esto solo lo sabe el atacante. La idea es que pase desapercibido en la víctima.

<img width="686" height="43" alt="ClickFix-4" src="https://github.com/user-attachments/assets/767cdf88-10be-4138-960b-f9a2347afaf2" />

Al pegarlo y darle enter, se descarga el Backdoor en la ruta `C:\Users\{Username}\AppData\Local\Temp` y se auto-ejecuta. Recomiendo ofuscar la URL en base64 para evitar detección por parte de los Antivirus. Se adjunta el <a href="https://github.com/R3LI4NT/XilentDoor/blob/main/ClickFix/index.html">index.html</a> para que puedan modificarlo y subir su propio malware.


