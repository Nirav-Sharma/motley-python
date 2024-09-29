"""
Delta Δ : Rate of change in option price with respect to the underlying stock price (1st derivative).
Gamma Γ : Rate of change in delta with respect to the underlying stock price (2nd derivative).
Vega V : Rate of change in option price with respect to the volatility (σ) of the stock price. 
Theta Θ : Rate of change in option price with respect to time (i.e. time decay). 
Rho P : Rate of change in option price with respect to interest rate. 

Calculates the values for each of the greeks for put and call options then plots them on graphs relative to the stock price
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class BlackScholesGreeks:
    
    def __init__(self, S, K, T, r, sigma, q=0.0):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.q = q
    
    # Private methods to calculate d1 and d2 for the Black-Scholes model
    def _d1(self):
        return (np.log(self.S / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
    
    def _d2(self):
        return self._d1() - self.sigma * np.sqrt(self.T)
    
    # Greeks for Call Option
    def call_delta(self):
        return np.exp(-self.q * self.T) * norm.cdf(self._d1())
    
    def call_gamma(self):
        return norm.pdf(self._d1()) / (self.S * self.sigma * np.sqrt(self.T))
    
    def call_vega(self):
        return self.S * norm.pdf(self._d1()) * np.sqrt(self.T)
    
    def call_theta(self):
        d1 = self._d1()
        d2 = self._d2()
        first_term = -(self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
        second_term = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        return first_term - second_term
    
    def call_rho(self):
        return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self._d2())
    
    # Greeks for Put Option
    def put_delta(self):
        return np.exp(-self.q * self.T) * (norm.cdf(self._d1()) - 1)
    
    def put_gamma(self):
        return self.call_gamma()  # Gamma is the same for both calls and puts
    
    def put_vega(self):
        return self.call_vega()  # Vega is the same for both calls and puts
    
    def put_theta(self):
        d1 = self._d1()
        d2 = self._d2()
        first_term = -(self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
        second_term = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
        return first_term + second_term
    
    def put_rho(self):
        return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self._d2())

    def plot_greeks(self):
       
        prices = np.linspace(20, 50, 100)
        call_deltas = [BlackScholesGreeks(S, self.K, self.T, self.r, self.sigma, self.q).call_delta() for S in prices]
        put_deltas = [BlackScholesGreeks(S, self.K, self.T, self.r, self.sigma, self.q).put_delta() for S in prices]
        gammas = [BlackScholesGreeks(S, self.K, self.T, self.r, self.sigma, self.q).call_gamma() for S in prices]
        vegas = [BlackScholesGreeks(S, self.K, self.T, self.r, self.sigma, self.q).call_vega() for S in prices]
        call_thetas = [BlackScholesGreeks(S, self.K, self.T, self.r, self.sigma, self.q).call_theta() for S in prices]
        put_thetas = [BlackScholesGreeks(S, self.K, self.T, self.r, self.sigma, self.q).put_theta() for S in prices]
        call_rhos = [BlackScholesGreeks(S, self.K, self.T, self.r, self.sigma, self.q).call_rho() for S in prices]
        put_rhos = [BlackScholesGreeks(S, self.K, self.T, self.r, self.sigma, self.q).put_rho() for S in prices]

        plt.figure(figsize=(10, 8))

        # Plot Delta
        plt.subplot(3, 2, 1)
        plt.plot(prices, call_deltas, label='Call Delta')
        plt.plot(prices, put_deltas, label='Put Delta')
        plt.title('Delta')
        plt.xlabel('Stock Price')
        plt.ylabel('Delta')
        plt.legend()

        # Plot Gamma
        plt.subplot(3, 2, 2)
        plt.plot(prices, gammas, label='Gamma', color='g')
        plt.title('Gamma')
        plt.xlabel('Stock Price')
        plt.ylabel('Gamma')
        plt.legend()

        # Plot Vega
        plt.subplot(3, 2, 3)
        plt.plot(prices, vegas, label='Vega', color='r')
        plt.title('Vega')
        plt.xlabel('Stock Price')
        plt.ylabel('Vega')
        plt.legend()

        # Plot Theta
        plt.subplot(3, 2, 4)
        plt.plot(prices, call_thetas, label='Call Theta', color='purple')
        plt.plot(prices, put_thetas, label='Put Theta', color='orange')
        plt.title('Theta')
        plt.xlabel('Stock Price')
        plt.ylabel('Theta')
        plt.legend()

        # Plot Rho
        plt.subplot(3, 2, 5)
        plt.plot(prices, call_rhos, label='Call Rho', color='brown')
        plt.plot(prices, put_rhos, label='Put Rho', color='pink')
        plt.title('Rho')
        plt.xlabel('Stock Price')
        plt.ylabel('Rho')
        plt.legend()

        plt.tight_layout()
        plt.show()

# Example usage
S = 40      # Stock price
K = 30      # Strike price
T = 5 / 12  # Time till expiration (in years)
r = 0.05    # Risk-free interest rate
sigma = 0.15  # Volatility (15%)
q = 0.05    # 5% annual dividend yield

greeks = BlackScholesGreeks(S, K, T, r, sigma, q)

print("Call Option Greeks:")
print(f"Delta: {greeks.call_delta():.4f}")
print(f"Gamma: {greeks.call_gamma():.4f}")
print(f"Vega: {greeks.call_vega():.4f}")
print(f"Theta: {greeks.call_theta():.4f}")
print(f"Rho: {greeks.call_rho():.4f}")

print("\nPut Option Greeks:")
print(f"Delta: {greeks.put_delta():.4f}")
print(f"Gamma: {greeks.put_gamma():.4f}")
print(f"Vega: {greeks.put_vega():.4f}")
print(f"Theta: {greeks.put_theta():.4f}")
print(f"Rho: {greeks.put_rho():.4f}")

greeks.plot_greeks()
