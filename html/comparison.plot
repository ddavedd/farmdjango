set terminal png size 800,600
set output 'clean7.png' 
set title 'Comparison Plot Weekly'
set ylabel '$'
set xlabel 'Date'
set xdata time
set timefmt '%m-%d'
set grid
plot 'cleaner7.data' u 1:2 lc rgb '#0000ff' t '2015' w lp, '' u 4:5 lc rgb '#00ffff' t '2016' w lp, '' u 9:10 lc rgb '#00ff00' t '2017' w lp, '' u 14:15 lc rgb '#000000' t '2018' w lp, '' u 19:20 lc rgb '#ff0000' t '2019' w lp, '' u 24:25 lc rgb '#ff00ff' t '2020' w lp
replot
