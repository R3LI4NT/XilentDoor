using System;
using System.Security.Cryptography;
using System.Text;

namespace XilentDoor.Utils
{
    public static class Encryption
    {
        public static string Encrypt(string plainText, string key = "MyStrongKey12345")
        {
            using (Aes aes = Aes.Create())
            {
                aes.Key = Encoding.UTF8.GetBytes(key.PadRight(16));
                aes.IV = new byte[16];

                var encryptor = aes.CreateEncryptor();
                byte[] inputBuffer = Encoding.UTF8.GetBytes(plainText);
                byte[] output = encryptor.TransformFinalBlock(inputBuffer, 0, inputBuffer.Length);
                return Convert.ToBase64String(output);
            }
        }

        public static string Decrypt(string encryptedText, string key = "MyStrongKey12345")
        {
            using (Aes aes = Aes.Create())
            {
                aes.Key = Encoding.UTF8.GetBytes(key.PadRight(16));
                aes.IV = new byte[16];

                var decryptor = aes.CreateDecryptor();
                byte[] inputBuffer = Convert.FromBase64String(encryptedText);
                byte[] output = decryptor.TransformFinalBlock(inputBuffer, 0, inputBuffer.Length);
                return Encoding.UTF8.GetString(output);
            }
        }
    }
}