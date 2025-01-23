set terminal png size 800,600
set output 'count7.png' 
set title 'Customer Count Weekly'
set ylabel 'Customers'
set xlabel 'Date'
set style data histograms
set grid
set style fill solid
set boxwidth .7
set xtics rotate
plot 'cleaner7.data' using 3:xtic(1) title '2014', '' using 7 title '2015', '' using 12 title '2016', '' using 17 title '2017', '' using 22 title '2018', '' using 27 title '2019'
replot
