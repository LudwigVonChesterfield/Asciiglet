import cProfile

p = cProfile.Profile()
p.enable()

import test

p.disable()

# p.print_stats()

p.dump_stats("results.prof")
