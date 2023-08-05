# hrmserve

Bring some service to hrmtools. This is a separate packages because it contain some eavy dependencies (dash)

# install 

```
> pip install hrmserve
```

from sources
```
> git clone git@gricad-gitlab.univ-grenoble-alpes.fr:guieus/hrmserve.git
> cd hrmserve
> python setup.py install 
```


# use

```
> hrmDeviceListServer HRM-00485_HCS_deviceList-3.xlsx
```

And then open the web page http://127.0.0.1:8050/