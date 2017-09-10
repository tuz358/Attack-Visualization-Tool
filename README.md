# Attack Visualization Tool

![AVT](http://tuz358.github.io/img/avt.gif)
(Example: Moonlight style)


## Requirements
- Your own Mapbox account
- Mapbox API access token
- IP2Location database (optional)


## Usage
```
$ ./avt.py ssh -f /var/log/access.log -d ip2location.csv
$ gnome-open ./ssh-mapbox-gl.html
```
If gnome-open is not available, click on the generated html file, and open it.
