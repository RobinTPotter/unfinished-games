#!/bin/sh

echo converting $1
PPATH=$(dirname $0)

OUTPUT=$1.export.obj
~/blender-2.79-linux-glibc219-i686/blender "$1" --background --python $PPATH/convert_blend_to_obj.py -- "$OUTPUT"

if [ -z "$2" ]
then
	echo not moving
else
	echo moving to $2
	if [ -d "$2" ]
	then
		echo directory exists
	else
		mkdir -p $2
	fi
	mv "$OUTPUT" "$2/"
fi


