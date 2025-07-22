using System.IO;
using System.Reflection;

namespace XilentDoor.Utils
{
    public static class Helpers
    {
        public static string GetExecutablePath()
        {
            return Assembly.GetExecutingAssembly().Location;
        }

        public static string GetAppDataPath()
        {
            return Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Microsoft", "Windows");
        }
    }
}