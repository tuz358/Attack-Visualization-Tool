# Attack Visualization Tool

<img src="http://tuz358.github.io/img/avt.gif" width="480px">

## Description
SSH attack visualization tool

## Requirements
- Your own Mapbox account
- Mapbox API access token

## Usage
```
$ ./avt.py -f /var/log/access.log -o ./ssh-mapbox-gl.html
```

**osx**
```
$ open ./ssh-mapbox-gl.html
```

**Linux**
```
$ gnome-open ./ssh-mapbox-gl.html
```
If gnome-open is not available, click on the generated html file, and open it in a browser.

## Link
- [MapboxでSSHの不正アクセスを可視化してみる - kanta's Tech-Note](http://tuz.hatenablog.com/entry/2017/09/10/200101)

## Author
[tuz358](https://github.com/tuz358)

## License
[GPLv3](https://github.com/tuz358/Attack-Visualization-Tool/blob/master/LICENSE)
