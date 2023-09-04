from ECAnalyse.RFB import *
from ECAnalyse.SuperCap import *

x = [1, 2, 3, 4, 5]
y1 = [1, 4, 9, 16, 25]
y2 = [2, 3, 4, 5, 6]
y3 = [3, 4, 5, 6, 7]
y4 = [1, 2, 3, 3, 2]
y5 = [0, 3, 8, 15, 24]
plt.plot(x, y1, label='Something')
plt.plot(x, y2, label='Nothing')
plt.plot(x, y3, label='Another Thing')
plt.plot(x, y4, label='CO$_2$ Capture')
plt.plot(x, y5, label = 'RARRRGH')
plt.legend()
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
plt.show()