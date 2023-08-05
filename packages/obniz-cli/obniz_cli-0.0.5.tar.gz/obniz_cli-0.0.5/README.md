# obniz_cli
`obniz_cli` is cli tool for obnizOS(for ESP32) install.

## Installation
Using pip,
```
pip install obniz_cli
```

## Preparation
Connect the ESP32 device from the serial port to your PC and check if the PC recognizes the device. The following command shows the list of devices.
```
python -m serial.tools.list_ports
```
(You can execute this command after `pip install obniz_cli`.)  
In most cases, port name is `dev/cu.SLAB_USBtoUART` or like `COM3`. If you can't find these port or can find but fail to install, you may need USB-driver for devices from [here](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers).

## Usage
### flashos
```
obniz_cli flashos [-b] [-p]
```
You can install obnizOS to your ESP32 device. If you execute without `-p` option, it is displayed as follows:
```
0: /dev/cu.Bluetooth-Incoming-Port
1: /dev/cu.SLAB_USBtoUART

Select NUMBER from above list(or if you want to cancel, input N key):
```
Select the device you want to install. (A device port can be passed to command with `-p` option like `obniz_cli flashos -p /dev/cu.SLAB_USBtoUART`).  

Then, latest obnizOS is downloaded and installed to device. By default, installation is performed at 115200bps but if installation failed, try to decrease it by `obniz_cli flashos -b 115200`.

After install, cli automatically change serial mode to set obnizOS configuration 

### eraseos
```
obniz_cli eraseos [-p]
```
You can reset your device by this command.