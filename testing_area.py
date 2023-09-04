from ECAnalyse.RFB import *
from ECAnalyse.SuperCap import *

x = np.arange(0, 5, 0.01)
y = 2 * x
y_var = np.random.rand(len(x)) - 0.5
y_var *= 100
y += y_var
plt.plot(x, y)

m, c = line_of_best_fit(x, y)
y_lobf = m * x + c
plt.plot(x, y_lobf)

y_zero = np.zeros(len(x))
sigma = standard_deviation_of_mean(y, y_lobf)
print(f'Standard Deviation of Variance: {standard_deviation_of_mean(y_var, y_zero)}')
print(f'Standard Deviation of Line: {sigma}')

print(f'Numpy: y={m}x+{c}, sigma={sigma}')
print(scipy.stats.linregress(x, y))

plt.show()