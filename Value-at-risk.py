"""Calculates the Value at Risk (VaR) for a financial portfolio at several confidence intervals (95%, 98%, and 99%) using the normal distribution
Plot to visualize the normal distribution of the portfolio's possible future values.
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Characteristics of portfolio
initial_investment = 100_000
portfolio_mean = 0.2  # Average Returns (20%)
portfolio_std = np.sqrt(0.044)  # Standard deviation of portfolio

mean_investment = (1 + portfolio_mean) * initial_investment
std_investment = portfolio_std * initial_investment

# Cutoff point in distribution for several confidence intervals (95%, 98% and 99%)
cutoff1 = norm.ppf(0.05, mean_investment, std_investment)
cutoff2 = norm.ppf(0.02, mean_investment, std_investment)
cutoff3 = norm.ppf(0.01, mean_investment, std_investment)

# Calculate VaR for several confidence intervals
VaR5 = initial_investment - cutoff1
VaR2 = initial_investment - cutoff2
VaR1 = initial_investment - cutoff3

print(f"The total value at risk (VaR) with 95% confidence is: {VaR5.round(2)}")
print(f"The total value at risk (VaR) with 98% confidence is: {VaR2.round(2)}")
print(f"The total value at risk (VaR) with 99% confidence is: {VaR1.round(2)}")

# Visualisation: Plot the distribution and VaR thresholds
# Define the x range for the distribution
x = np.linspace(mean_investment - 4 * std_investment, mean_investment + 4 * std_investment, 1000)

plt.figure(figsize=(10, 6))
plt.plot(x, norm.pdf(x, mean_investment, std_investment), label='Portfolio Value Distribution')

plt.axvline(cutoff1, color='r', linestyle='--', label='VaR 95%')
plt.axvline(cutoff2, color='b', linestyle='--', label='VaR 98%')
plt.axvline(cutoff3, color='g', linestyle='--', label='VaR 99%')

plt.title('Normal Distribution of Portfolio Value with VaR Thresholds')
plt.xlabel('Portfolio Value')
plt.ylabel('Probability Density')
plt.legend()

plt.grid(True)
plt.show()
