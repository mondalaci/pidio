raspberry-pi-radio
==================

Raspberry Pi based wifi radio player featuring a blind-friendly pushbutton user interface

* concept, hardware, software, radio list
* apt-get xyz

pidio 3w idle, playing 3.4w
playback delay from bootup: 93s

Building the hardware
---------------------

![front side of the button panel](photos/panel-front.jpg)
![back side of the button panel](photos/panel-back.jpg)
![panel half-stickified](photos/panel-half-stickified.jpg)
![almost assembled unit](photos/almost-assembled.jpg)
![fully assembled unit](photos/fully-assembled.jpg)

* double sided foam tape

Retrieving Hungarian radio stations
-----------------------------------

1. I found and visited http://www.listenlive.eu/hungary.html
2. Utilizing the [$x](http://getfirebug.com/wiki/index.php/$x) construct I typed the following into the JavaScript console of Chrome:
`stations = $x('//table[@id="thetable3"]/tbody/tr/td[4]/a/@href');`
`for (i=0; i<results.length; i++) console.log(results[i].value);`
3. Copy-pasted the output into [my-stations.m3u](my-stations.m3u)

