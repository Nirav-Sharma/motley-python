"""
Calculates (European) call and put option prices through the Black-Scholes formula without dividends
Calculates the implied volatility of the option
Gives the probability of the call or put option being in the money
Provides 3 visualisations
    Visualisation 1: Call and Put price vs. Stock Price (S)
    Visualisation 2: Call and Put price vs. Time to Maturity (T)
    Visualisation 3: Call and Put price vs. Volatility (sigma)
    Visualisation 4: Implied Volatility vs. Option Price
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class BlackScholes:
   
    @staticmethod
    def _d1(S, K, T, r, sigma):
        return (1 / (sigma * np.sqrt(T))) * (np.log(S/K) + (r + sigma**2 / 2) * T)
    
    def _d2(self, S, K, T, r, sigma):
        return self._d1(S, K, T, r, sigma) - sigma * np.sqrt(T)
    
    def call_price(self, S, K, T, r, sigma):
        # Price of a European call option
        d1 = self._d1(S, K, T, r, sigma)
        d2 = self._d2(S, K, T, r, sigma)
        return norm.cdf(d1) * S - norm.cdf(d2) * K * np.exp(-r*T)
    
    def put_price(self, S, K, T, r, sigma):
        # Price of a European put option
        d1 = self._d1(S, K, T, r, sigma)
        d2 = self._d2(S, K, T, r, sigma)
        return norm.cdf(-d2) * K * np.exp(-r*T) - norm.cdf(-d1) * S
    
    def call_in_the_money(self, S, K, T, r, sigma):
        # Probability that a call option will be in the money at maturity
        d2 = self._d2(S, K, T, r, sigma)
        return norm.cdf(d2)
    
    def put_in_the_money(self, S, K, T, r, sigma):
        # Probability that a put option will be in the money at maturity
        d2 = self._d2(S, K, T, r, sigma)
        return 1 - norm.cdf(d2)

def implied_volatility(option_price, S, K, T, r, option_type="call"):
    
    def option_price_function(sigma):
        if option_type == "call":
            return BlackScholes().call_price(S, K, T, r, sigma)
        else:
            return BlackScholes().put_price(S, K, T, r, sigma)

    # Using bisection method to find implied volatility
    sigma_low, sigma_high = 0.0001, 1
    tolerance = 0.0001
    
    while sigma_high - sigma_low > tolerance:
        sigma_mid = (sigma_low + sigma_high) / 2
        price_mid = option_price_function(sigma_mid)
        
        if price_mid < option_price:
            sigma_low = sigma_mid
        else:
            sigma_high = sigma_mid
    
    return round(sigma_mid, 4)

# Parameters
S = 36  # Stock price
K = 35  # Strike price
T = 2/12  # Time till expiration (in years)
r = 0.05  # Risk-free interest rate
market_price = 1.5  # Price of the option in the market

# Implied Volatility for Call and Put
call_imp_vol = implied_volatility(market_price, S, K, T, r, option_type="call")
put_imp_vol = implied_volatility(market_price, S, K, T, r, option_type="put")

print(f"Implied volatility for call option = {round(call_imp_vol*100, 3)}%")
print(f"Implied volatility for put option = {round(put_imp_vol*100, 3)}%")

# Calculate Call and Put Prices
sigma = np.sqrt(0.2)  # Historical volatility (standard deviation)

call_price = BlackScholes().call_price(S, K, T, r, sigma)
put_price = BlackScholes().put_price(S, K, T, r, sigma)
call_probability = BlackScholes().call_in_the_money(S, K, T, r, sigma)
put_probability = BlackScholes().put_in_the_money(S, K, T, r, sigma)

print(f"Call price: {round(call_price, 2)}")
print(f"Put price: {round(put_price, 2)}")
print("Probability that the call option will be in the money:", round(call_probability, 4))
print("Probability that the put option will be in the money:", round(put_probability, 4))

# --- Visualisations ---

# 1. Call and Put price vs. Stock Price 
S_range = np.linspace(30, 60, 100)
call_prices = [BlackScholes().call_price(S, K, T, r, sigma) for S in S_range]
put_prices = [BlackScholes().put_price(S, K, T, r, sigma) for S in S_range]

plt.figure(figsize=(10, 6))
plt.plot(S_range, call_prices, label='Call Option Price', color='b', lw=2)
plt.plot(S_range, put_prices, label='Put Option Price', color='r', lw=2)
plt.title('Option Prices vs. Stock Price')
plt.xlabel('Stock Price (S)')
plt.ylabel('Option Price')
plt.legend()
plt.grid(True)
plt.show()

# 2. Call and Put price vs. Time to Maturity 
T_range = np.linspace(0.01, 1, 100)
call_prices_T = [BlackScholes().call_price(S, K, T, r, sigma) for T in T_range]
put_prices_T = [BlackScholes().put_price(S, K, T, r, sigma) for T in T_range]

plt.figure(figsize=(10, 6))
plt.plot(T_range, call_prices_T, label='Call Option Price', color='b', lw=2)
plt.plot(T_range, put_prices_T, label='Put Option Price', color='r', lw=2)
plt.title('Option Prices vs. Time to Maturity')
plt.xlabel('Time to Maturity (T in years)')
plt.ylabel('Option Price')
plt.legend()
plt.grid(True)
plt.show()

# 3. Call and Put price vs. Volatility (sigma)
sigma_range = np.linspace(0.01, 1, 100)
call_prices_sigma = [BlackScholes().call_price(S, K, T, r, sigma) for sigma in sigma_range]
put_prices_sigma = [BlackScholes().put_price(S, K, T, r, sigma) for sigma in sigma_range]

plt.figure(figsize=(10, 6))
plt.plot(sigma_range, call_prices_sigma, label='Call Option Price', color='b', lw=2)
plt.plot(sigma_range, put_prices_sigma, label='Put Option Price', color='r', lw=2)
plt.title('Option Prices vs. Volatility')
plt.xlabel('Volatility (sigma)')
plt.ylabel('Option Price')
plt.legend()
plt.grid(True)
plt.show()

# 4. Implied Volatility vs. Option Price
option_price_range = np.linspace(1, 5, 100)
implied_vols_call = [implied_volatility(price, S, K, T, r, "call") for price in option_price_range]
implied_vols_put = [implied_volatility(price, S, K, T, r, "put") for price in option_price_range]

plt.figure(figsize=(10, 6))
plt.plot(option_price_range, implied_vols_call, label='Implied Volatility (Call)', color='b', lw=2)
plt.plot(option_price_range, implied_vols_put, label='Implied Volatility (Put)', color='r', lw=2)
plt.title('Implied Volatility vs. Option Price')
plt.xlabel('Option Price')
plt.ylabel('Implied Volatility')
plt.legend()
plt.grid(True)
plt.show()
