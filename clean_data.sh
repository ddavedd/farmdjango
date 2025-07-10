#!/bin/bash
cd /home/USERNAME/farmdjango
sed -e 's/<[^>]*>//g' year_comparison1.data > clean1.data
sed -e 's/<[^>]*>//g' year_comparison7.data > clean7.data
sed '$d' clean1.data > cleaner1.data
sed '$d' clean7.data > cleaner7.data
