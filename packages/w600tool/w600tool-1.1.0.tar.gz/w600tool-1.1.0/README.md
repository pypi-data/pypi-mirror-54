# w600tool
A Python-based firmware upload tool for Winner Micro W600 & W601 WiFi Chips.

w600tool.py was started by vshymanskyy (@[vshymanskyy](https://github.com/vshymanskyy/)).

## Features
- Automatically detects bootloader or helps entering `secboot`
- Get/Set MAC address
- Erase secboot and image
- Switch to high-speed mode
- Upload `fls`, `img` files


## Easy Installation

You will need [either Python 2.7 or Python 3.4 or newer](https://www.python.org/downloads/) installed on your system.

The latest stable w600tool.py release can be installed from [pypi](http://pypi.python.org/pypi/w600tool) via pip:

```
$ pip install w600tool
```

With some Python installations this may not work and you'll receive an error, try `python -m pip install w600tool` or `pip2 install w600tool`.

After installing, you will have `w600tool.py` installed into the default Python executables directory and you should be able to run it with the command `w600tool.py`.


## Usage
```log
usage: w600tool.py [-h] [-p PORT] [-b BAUD] [--get-mac] [--set-mac MAC] [-e]
                   [-u FILE]
                   [--upload-baud {115200,460800,921600,1000000,2000000}]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
  -b BAUD, --baud BAUD
  --get-mac
  --set-mac MAC
  -e, --erase
  -u FILE, --upload FILE
  --upload-baud {115200,460800,921600,1000000,2000000}
```

## Example
```log
$ w600tool.py --upload W60X_MicroPython_1.10_B1.1_GZ.fls
Push reset button to enter bootloader...
Switched speed to 2000000
Uploading W60X_MicroPython_1.10_B1.1_GZ.fls
0% [##############################] 100% | ETA: 00:00:00
Total time elapsed: 00:00:09
Reset board to run user code...
```
