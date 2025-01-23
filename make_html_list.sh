#!/bin/bash
for i in *.png *.html; do echo "<p /><a href='./"$i"'>"$i"</a>"; done > all.html
