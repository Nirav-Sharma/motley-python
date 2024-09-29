"""
Black-Scholes option pricer that now accounts for dividends with 2 visualisations
    Visualisation 1: Call and Put price vs. Stock Price
    Visualisation 2: Call and Put price vs. Volatility
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class BlackScholesPeriodicDividend:
    
    @staticmethod
    def _d1(S, K, T, r, sigma, q, periods):
        dividends = BlackScholesPeriodicDividend._discount_for_dividends(S, q, T, periods)
        return (1 / (sigma * np.sqrt(T))) * (np.log(dividends / K) + (r + sigma**2 / 2) * T)
    
    def _d2(self, S, K, T, r, sigma, q, periods):
        return self._d1(S, K, T, r, sigma, q, periods) - sigma * np.sqrt(T)
    
    @staticmethod
    def _discount_for_dividends(S, q, T, periods):
        # Calculates the stock price adjusted for periodic dividends
        dividend_factor = np.exp(-q / periods)  # Dividend adjustment per period
        num_periods = periods * T  # Total number of dividend periods until expiration
        discounted_S = S * (dividend_factor ** num_periods)  # Adjust the stock price
        return discounted_S
    
    def call_price(self, S, K, T, r, sigma, q, periods):
        # Calculating the price of a call option
        d1 = self._d1(S, K, T, r, sigma, q, periods)
        d2 = self._d2(S, K, T, r, sigma, q, periods)
        discounted_S = self._discount_for_dividends(S, q, T, periods)
        return norm.cdf(d1) * discounted_S - norm.cdf(d2) * K * np.exp(-r*T)
    
    def put_price(self, S, K, T, r, sigma, q, periods):
        # Calculating the price of a put option
        d1 = self._d1(S, K, T, r, sigma, q, periods)
        d2 = self._d2(S, K, T, r, sigma, q, periods)
        discounted_S = self._discount_for_dividends(S, q, T, periods)
        return norm.cdf(-d2) * K * np.exp(-r*T) - norm.cdf(-d1) * discounted_S
    
    def call_in_the_money(self, S, K, T, r, sigma, q, periods):
        # Probability that call option will be in the money at maturity
        d2 = self._d2(S, K, T, r, sigma, q, periods)
        return norm.cdf(d2)
    
    def put_in_the_money(self, S, K, T, r, sigma, q, periods):
        # Probability that put option will be in the money at maturity
        d2 = self._d2(S, K, T, r, sigma, q, periods)
        return 1 - norm.cdf(d2)

# Input variables
S = 50  # Stock price
K = 55  # Strike price
T = 1  # Time till expiration (in years)
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Volatility 
q = 0.03  # Annual dividend yield 
periods = 4  # Number of dividend payment periods per year

bs_periodic = BlackScholesPeriodicDividend()

# Visualization 1: Call and Put price vs. Time to Maturity 
T_range = np.linspace(0.01, 2, 100)  # Time to maturity between (a, b, ) years
call_prices_T = [bs_periodic.call_price(S, K, T, r, sigma, q, periods) for T in T_range]
put_prices_T = [bs_periodic.put_price(S, K, T, r, sigma, q, periods) for T in T_range]

plt.figure(figsize=(10, 6))
plt.plot(T_range, call_prices_T, label='Call Option Price', color='b', lw=2)
plt.plot(T_range, put_prices_T, label='Put Option Price', color='r', lw=2)
plt.title('Option Prices vs. Time to Maturity (Quarterly Dividends)')
plt.xlabel('Time to Maturity (T in years)')
plt.ylabel('Option Price')
plt.legend()
plt.grid(True)
plt.show()

# Visualisation 2: Call and Put price vs. Volatility (sigma)
sigma_range = np.linspace(0.01, 1, 100)  # Volatility between (a, b, )
call_prices_sigma = [bs_periodic.call_price(S, K, T, r, sigma, q, periods) for sigma in sigma_range]
put_prices_sigma = [bs_periodic.put_price(S, K, T, r, sigma, q, periods) for sigma in sigma_range]

plt.figure(figsize=(10, 6))
plt.plot(sigma_range, call_prices_sigma, label='Call Option Price', color='b', lw=2)
plt.plot(sigma_range, put_prices_sigma, label='Put Option Price', color='r', lw=2)
plt.title('Option Prices vs. Volatility (Quarterly Dividends)')
plt.xlabel('Volatility (sigma)')
plt.ylabel('Option Price')
plt.legend()
plt.grid(True)
plt.show()
