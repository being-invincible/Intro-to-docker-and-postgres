import pandas as pd
import sys

# play with arguments
filename = sys.argv[0]
date = sys.argv[1]

print(f"Hello from {filename}! on {date}")
print("Pandas successfully imported!", pd.__version__)