#!/usr/local/bin/zsh
filename="/Users/jhunt3/Dropbox/Apps/whereapp/auto-selfie/$(date +%s).jpg"
/usr/local/bin/imagesnap -q -w 1.0 /tmp/snapshot.jpg
latitude=$(/Users/jhunt3/bin/CoreLocationCLI -once yes -format '%latitude')
latituderef="N"
if [[ ${latitude:0:1} == "-" ]] ; then
	latituderef="S"
fi
longitude=$(/Users/jhunt3/bin/CoreLocationCLI -once yes -format '%longitude')
longituderef="W"
if [[ ${longitude:0:1} == "-" ]] ; then
	longituderef="W"
fi
/usr/local/bin/exiftool -q -exif:gpslatitude="$latitude" -exif:gpslatituderef=$latituderef \
            -exif:gpslongitude="$longitude" -exif:gpslongituderef=$longituderef \
            /tmp/snapshot.jpg
mv /tmp/snapshot.jpg "$filename"
