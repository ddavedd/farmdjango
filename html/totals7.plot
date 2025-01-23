set terminal png size 800,600
set output 'totalbyweek.png' 
set title 'Totals Plot Weekly'
set ylabel 'Cumulative $'
set xlabel 'Date'
set xdata time
set timefmt '%m-%d'
set grid
set key top left
plot 'cleaner7.data' u 1:29 lc rgb '#0000ff' t '2015' w lp, '' u 4:30 lc rgb '#00ffff' t '2016' w lp, '' u 9:31 lc rgb '#00ff00' t '2017' w lp, '' u 14:32 lc rgb '#000000' t '2018' w lp, '' u 19:33 lc rgb '#ff0000' t '2019' w lp, '' u 24:34 lc rgb '#ffaa00' t '2020' w lp
replot
