# About
Dns server with round-robin and health-check support.  
Running periodic async service health-checks to answer only alive service addresses.

Async checks worker using python's `threading` module.

# How to use
## Clone repository
```bash
$ git clone git@github.com:a1fred/route666.git
```

# Dependencies
* Linux-like OS
* python2.7, maybe earlier

No additional python libraries needed.

## Configure
Configuration stored in `./pool.json`.
Example configuration:
```json
{
    "example.org.": {
        "method": "http_200_response",
        "NODES": [
            {
                "addr": "213.180.193.3",
                "url": "http://213.180.193.3/"
            },
            {
                "addr": "93.158.134.3",
                "url": "http://93.158.134.3/"
            },
            {
                "addr": "213.180.204.3",
                "url": "http://213.180.204.3/"
            }
        ]
    }
}
```

Each key in json represents service. 
* `method` keys is a health-check name (see below). 
* `NODES` is list of service mirrors. Each node need `addr` variable to set. Other variables is optional and health-check specific.

### Health checks
Now supports:
* `http_any_response` - Server responded any answer on given url
* `http_200_response` - Server responded http 200 on given url

Adding your checks is very easy if you python-developer. See `methods` package for examples.

## Run
Run via sudo because we need to bind port 53.

```bash
$ sudo python ./route666d.py
```
