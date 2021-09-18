MPMDv2SerialConnect

Related to my my Raspberry Pi 3B+'s Octopi's pyserial not reading/writing from/to my Monoprice Mini Delta v2 (MPMDv2).

This repo contains 3 [mostly non-MPMDv2] working simple/basic serial reading apps (C#, C++, and Python) [plus a comment on how to use pyserial's serial.tools.miniterm].

All 3 of these apps, plus pyserial's miniterm, on Windows can read from a known good working serial non-MPMDv2 device.

As soon as I point the apps to a MPMDv2, the only apps that can read from the MPMDv2 are the C# and the C++ (non-overlapped IO).

On MacOS, the Python app and pyserial miniterm opens the MPMDv2 serial port fine!

So, something seems wrong w/ pyserial talking to the MPMDv2 only on Windows or Raspberry Pi.

pyserial (again, that Octoprint/Octopi uses) uses Overlapped IO (https://github.com/pyserial/pyserial/blob/master/serial/serialwin32.py), so my next task is to write a simple/basic overlapped IO impl to see if that causes the problem.
If that works and does not repro the problem then I will slowly start to add in trinkets of the extra things that pyserial adds.
If that does not repro the problem then I may be stumped.

Octoprint adds some hacks on top of pyserial that may also have some clues.
Example(s):
https://github.com/OctoPrint/OctoPrint/blob/b6ebe7c8539b86acb217483b853910d23518967f/src/octoprint/util/comm.py#L3669

One alternative that I could consider is creating and installing a virtual serial port proxy on the Octopi.
I would try to write and get a working serial port read/write app of the Pi talking to the MPMDv2.
That app would then create a virtual serial port that can be seen by a device/PC connected over a USB/Serial cable and opened.
Any writes by the device/PC will be proxied through the virtual serial port and forwarded to the MPMDv2.
Any writes by the MPMDv2 will be proxied through the virtual serial port and forwarded to the device/PC.
I may be wrong, but I do not think this would be a trivial task, so I'd rather continue to find out why pyserial cannot open the MPMDv2's serial port.
