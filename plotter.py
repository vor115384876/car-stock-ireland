#plotter for the private vehicle car stock model
import sys
sys.path
#sys.executable
import numpy as np

time = [0, 1, 2, 3]
position = [0, 100, 200, 300]

plt.plot(time, position)
plt.xlabel('Time (hr)')
plt.ylabel('Position (km)')