"""
Binomial lattice option pricer for american put or call option
Also visualises the call or put option lattice next to the stock price lattice
"""



import numpy as np
import matplotlib.pyplot as plt

def binomial_option_pricer(S, K, T, r, sigma, N, option_type='call'):
    
    # Time step
    delta_t = T / N
    
    # Calculate up and down factors
    u = np.exp(sigma * np.sqrt(delta_t))  # Up factor
    d = np.exp(-sigma * np.sqrt(delta_t))  # Down factor
    
    # Calculate the risk-neutral probability
    R = np.exp(r * delta_t)  # Risk-free discount factor per time step
    q = (R - d) / (u - d)    # Risk-neutral probability of upward movement
    
    stock_prices = np.zeros((N+1, N+1))
    stock_prices[0, 0] = S
    
    for i in range(1, N+1):
        stock_prices[i, 0] = stock_prices[i-1, 0] * u  # Up moves
        for j in range(1, i+1):
            stock_prices[i, j] = stock_prices[i-1, j-1] * d  # Down moves
    
    # Initialise the option value at maturity
    option_values = np.zeros((N+1, N+1))
    
    if option_type == 'call':
        # Call option payoff at maturity
        option_values[N, :] = np.maximum(0, stock_prices[N, :] - K)
    elif option_type == 'put':
        # Put option payoff at maturity
        option_values[N, :] = np.maximum(0, K - stock_prices[N, :])
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    # Work backwards to calculate the option price at each node
    for i in range(N-1, -1, -1):
        for j in range(i+1):
            option_values[i, j] = (q * option_values[i+1, j] + (1 - q) * option_values[i+1, j+1]) / R
    
    # Visualise the binomial tree
    visualize_binomial_tree(stock_prices, option_values, N, option_type)
    
    # The option price at the root of the tree is the final result
    return option_values[0, 0]

def visualize_binomial_tree(stock_prices, option_values, N, option_type):

    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot stock price tree
    ax[0].set_title("Stock Price Binomial Tree", fontsize=14, weight='bold')
    for i in range(N+1):
        for j in range(i+1):
            ax[0].scatter(i, stock_prices[i, j], color='blue')
            ax[0].text(i, stock_prices[i, j], f'{stock_prices[i, j]:.2f}', 
                       ha='center', va='bottom', fontsize=10)
    ax[0].set_xlabel('Steps')
    ax[0].set_ylabel('Stock Price')
    
    # Plot option price tree
    ax[1].set_title(f"Option Price Binomial Tree ({option_type.capitalize()})", fontsize=14, weight='bold')
    for i in range(N+1):
        for j in range(i+1):
            ax[1].scatter(i, option_values[i, j], color='green')
            ax[1].text(i, option_values[i, j], f'{option_values[i, j]:.2f}', 
                       ha='center', va='bottom', fontsize=10)
    ax[1].set_xlabel('Steps')
    ax[1].set_ylabel('Option Price')
    
    plt.tight_layout()
    plt.show()

# Example usage:
S = 100  # Current stock price
K = 105  # Strike price
T = 1    # Time to maturity in years
r = 0.05 # Risk-free interest rate 
sigma = 0.2 # Volatility 
N = 3    # Number of time steps
option_type = 'both' #Option type; enter 'put', 'call' or both depending on which option you want to see with both displaying both a put and a call option

if option_type == 'call':
    # Price a European call option
    call_price = binomial_option_pricer(S, K, T, r, sigma, N, option_type = 'call')
    print(f"European Call Option Price: {call_price:.2f}")
elif option_type == 'put':
    # Price a European put option
    put_price = binomial_option_pricer(S, K, T, r, sigma, N, option_type = 'put')
    print(f"European Put Option Price: {put_price:.2f}")
elif option_type == 'both':
    call_price = binomial_option_pricer(S, K, T, r, sigma, N, option_type = 'call')
    put_price = binomial_option_pricer(S, K, T, r, sigma, N, option_type = 'put')
    print(f"European Call Option Price: {call_price:.2f}")
    print(f"European Put Option Price: {put_price:.2f}")
else:
    print("Please input call, put or both as the option type!!")