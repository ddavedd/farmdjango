#!/bin/bash
cd /home/farmer21/farmdjango/dates/
rm westchestertoday.html
a=(*)
cp ${a[@]: -1} westchestertoday.html
cd /home/farmer21/farmdjango
ftp -nvi ftp.thefarmwestmont.com << END_SCRIPT
user thefarmwestmontcom REPLACE_WITH_PASSWORD
cd s
cd ales
cd westchester
cd 2024
mput *.html
mput *.png
lcd dates
cd dates
mput *.html
bye
END_SCRIPT
