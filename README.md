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
