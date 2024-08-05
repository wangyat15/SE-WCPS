import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)

from wdc.coverage.subcoverages.s2_coverage import S2Coverage
from wdc.coverage.subcoverages.average_coverage import AverageCoverage

# Testing the randomize_coverage static methods
# by printing the returned results for two calls per function

# S2Coverage
print("\nOutput 1 for S2Coverage randomizer\n")
name, subset = S2Coverage.randomize_coverage()
print(name)
print(subset, "\n")

print("\nOutput 2 for S2Coverage randomizer\n")
name, subset = S2Coverage.randomize_coverage()
print(name)
print(subset, "\n\n")

# AverageCoverage
print("\nOutput 1 for AverageCoverage randomizer\n")
name, subset = AverageCoverage.randomize_coverage()
print(name)
print(subset, "\n")

print("\nOutput 2 for AverageCoverage randomizer\n")
name, subset = AverageCoverage.randomize_coverage()
print(name)
print(subset, "\n")
