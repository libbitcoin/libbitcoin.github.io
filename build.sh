#!/bin/bash
for i in *.src.html; do
    FILENAME=${i%.src.html}.html
    cat header.html > $FILENAME
    cat $i >> $FILENAME
    cat footer.html >> $FILENAME
done

