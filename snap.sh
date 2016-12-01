#!/bin/sh

filename="/Users/jessepollak/.auto-selfie/$(date +%s).jpg"
/usr/local/bin/imagesnap -q -w 1.0 /tmp/snapshot.jpg
latitude=$(corelocationcli -once yes -format '%latitude')
latituderef="N"
if [[ ${latitude:0:1} == "-" ]] ; then
	latituderef="S"
fi
longitude=$(corelocationcli -once yes -format '%longitude')
longituderef="W"
if [[ ${longitude:0:1} == "-" ]] ; then
	longituderef="W"
fi
/usr/local/bin/exiftool -q -exif:gpslatitude="$latitude" -exif:gpslatituderef=$latituderef \
            -exif:gpslongitude="$longitude" -exif:gpslongituderef=$longituderef \
            /tmp/snapshot.jpg
mv /tmp/snapshot.jpg "$filename"
