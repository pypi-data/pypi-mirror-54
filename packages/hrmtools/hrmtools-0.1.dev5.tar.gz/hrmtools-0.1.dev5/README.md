# HRM tools 

Collection of tools for HARMONI.

So far only one tool is made to read and handle device list

## Installation 

From pip

```
> pip install hrmtools
```

from sources
```
> git clone git@gricad-gitlab.univ-grenoble-alpes.fr:guieus/hrmtools.git
> cd hrmtools
> python setup.py install 
```

## Exemple

```python 

from hrmtools.devices.cls import Devices

devices = Devices.from_xls('/path/to/HRM-00485_HCS_deviceList-3.xlsx')

print(devices.RWROT.unique_letter)
# same as
print(devices['RWROT']['unique_letter'])
print(repr(devices['RWROT']))
```