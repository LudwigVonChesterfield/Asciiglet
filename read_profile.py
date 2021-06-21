import pstats
p = pstats.Stats('results.prof')
p.sort_stats('cumulative').print_stats(50)
