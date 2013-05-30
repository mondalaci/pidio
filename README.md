raspberry-pi-radio
==================

Raspberry Pi based wifi radio player featuring a blind-friendly pushbutton user interface

* concept, hardware, software, radio list
* apt-get xyz
* double sided foam tape

get stations:
visit http://www.listenlive.eu/hungary.html
stations = $x('//table[@id="thetable3"]/tbody/tr/td[4]/a/@href')
for (i=0; i<results.length; i++) console.log(results[i].value);
copy-paste into hungarian-stations.m3u
