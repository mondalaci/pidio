pidio
=====

Pidio is a Raspberry Pi based wifi radio player featuring a blind-friendly pushbutton user interface.

Below is the picture of the pushbutton user interface.

![front side of the button panel](photos/panel-front.jpg)

The important thing to realize is that I've created this gadget for the grandmother of my girlfriend who is blind so I specifically designed the user interface to be blind-friendly.

Pushbutton feature matrix

| button           | short press      | long press (at least 2 seconds)  |
|------------------|------------------|----------------------------------|
| button 1 (black) | load preset 1    | save current station as preset 1 |
| button 2 (black) | load preset 2    | save current station as preset 2 |
| button 3 (black) | load preset 3    | save current station as preset 3 |
| button 4 (black) | load preset 4    | save current station as preset 4 |
| button 5 (black) | load preset 5    | save current station as preset 5 |
| button 6 (white) | previous station | n/a                              |
| button 7 (white) | next station     | stop / resume playback           |

* concept, hardware, software, radio list
* apt-get xyz

pidio 3w idle, playing 3.4w
playback delay from bootup: 93s

Building the hardware
---------------------

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

