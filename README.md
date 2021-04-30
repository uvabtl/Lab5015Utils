# Utils
Set of utils to drive the lab equipment remotely. The main use cases are

### PiLas laser
Class `PiLas` in `Lab5015_utils.py`
Allows to turn the laser ON and OFF and change basic parameters such as the tune and the frequency. A script for a quick edit of the settings is also available:
```
python3 drivePiLas.py --power=1 --tune=50  --freq=50000
```

### SMC chiller
Class `SMChiller` in `Lab5015_utils.py`
Allows to turn the chiller ON and OFF and check and change the temperature. A script for a quick edit of the settings is also available:
```
python3 driveChiller.py --power=1 --temp=19.2
```

The following script uses a PD approach to reach and maintain the desired temperature:
```
python3 setBoxTemp_PID.py --target 22
```


### Bind an instrument to a device name
Check instrument characteristics
```
dmesg | grep ttyUSB
udevadm info --name=/dev/ttyUSBx --attribute-walk
```
Create a file `/etc/udev/rules.d/99-usb-serial.rules` with something like this line in it:
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", SYMLINK+="your_device_name"
```
test the change:
```
sudo udevadm trigger
udevadm test -a -p  $(udevadm info -q path -n /dev/your_device_name)

