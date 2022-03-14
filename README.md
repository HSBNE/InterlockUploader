# Interlock Uploader

This script batch uploads firmware to the HSBNE doors and interlocks.

### Requirements
This script needs the PlastformIO Core CLI. PlatformIO will automatically handle the dependencies and uploading.

Link to PlatformIO Core: https://docs.platformio.org/en/latest/core/index.html

### Useage
1. Populate devices.csv (explained later). A copy is kept in the HSBNE Infrastructure 1Password.
2. Run main.py. The directory to the interlock source code must contain `platformio.ini`
```
> python3 main.py "path/to/interlock/source/directory" "wifiSSID" "wifiPassword" "hostAddress (e.g. http://portal.int.hsbne.org)" "hostSecret"
```
### devices.csv
The build flags for each door/interlock are specified in `devices.csv`. Items are delineated by a comma `,`. Surrounding spaces are ignored. Rows are separated by a newline `\n`.

The layout is: CSV layout:
```
DeviceName, DeviceIP, CurrentOTAPasswod, NewOTAPassword, DOOR/INTERLOCK, RF125PS_READER/OLD_READER, RGBW/GRBW, N_LEDS, SKELETON_CARD
```

Example:
```
INT-WS-PantoRouter, 10.0.0.124, oldOTAPaswword, myNewCoolOTAPassword, INTERLOCK, RF125PS_READER, GRBW, 1, 124816
DOOR-Quad, 10.0.0.111, someOTAPassword, aDifferentOTAPassword, DOOR, OLD_READER, RGBW, 16, 124816
```
