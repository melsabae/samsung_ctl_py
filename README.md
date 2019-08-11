# samsung_ctl_py
Python implementation of a Windows-based Samsung BIOS control package

When windows (inevitably) crapped the bed on a Samsung laptop, I was left without certain control over hardware features that the laptop contained. Some of these features are mapped to the fn-keys on the laptop. I have since owned a later iteration of that same laptop, and once again windows crapped the bed. To fix this, I had some bash scripts that echoed directly into files under /sys and the scripts ran as root. This is an updated client/server version, written in python, where the server needs to be able to write into these files (the server will be ran as root out of laziness and not wanting to screw up permissions on kernel-mapped files). The client will simply need write permissions on a socket, and to send a valid command.

A control is a hardware 'control'. Currently the software knows of the wifi rfkill, bluetooth rfkill, performance level, and the usb-charge controls. These controls are known respectively as wifi, bt, cpu, and usb. Some of the other features of the Samsung motherboard have been adopted into GUI platforms, and are not solved for here.

The architecture of the server will be such that: anyone can change a hardware control, but nobody can bypass the command set to do something naughty.

The command set is simple: {get, set, cyc} control [parameter]. Parameter is unused for get and for cyc. Get simply hands back the current value of the control, cyc will rotate through the valid values for the control in a pre-defined order (using the current value as the, you guessed it, current value), and set resolves a control to a fixed value.

The paths file in this directory points a 'control' (currently: cpu, wifi, usb, or bt) to a file that the kernel uses to control that hardware.

actions.py is where the command set is generated from the intersection of: the controls in actions.py and the controls mapped in the paths file.

The test_{read,write} files are scripts to validate that the logic is working.

