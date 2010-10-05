#!/bin/bash

calibredb add "$1"


if [ -n "$2" ]
then 
   LIST_ID=$(calibredb list | tail -n 2 | head -n 1 | cut -d\  -f 1) 
   ebook-convert "$1" "$1$2"
   calibredb add_format "$LIST_ID" "$1$2"
   rm  "$1$2"
fi


