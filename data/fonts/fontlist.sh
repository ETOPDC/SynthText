#!/bin/bash

> fontlist.txt

for file in `ls`
do
	if test -f ${file}
	then
		echo "${file}"
		echo "${file}" >> fontlist.txt
	fi
done
