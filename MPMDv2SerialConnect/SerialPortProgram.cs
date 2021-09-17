using System;
using System.IO.Ports;
using System.Windows.Forms;

namespace MPMDv2SerialConnect
{
    class SerialPortProgram
    {
        [STAThread]
        static void Main(string[] args)
        {
            var portName = "COM8";
            var port = new SerialPort(portName, 115200, Parity.None, 8, StopBits.One)
            {
                Handshake = Handshake.None
            };
            port.DataReceived += (sender, e) => {
                Console.Write((sender as SerialPort).ReadExisting());
            };
            Console.WriteLine($"Opening {portName} 115200 N 8 1 to read");
            port.Open();
            Console.WriteLine("Reading...");
            Application.Run();
        }
    }
}
