import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt
import seaborn as sns

MOVE_COST = 2
MAX_CARS = 20
MAX_CARS_MOVED = 5
DISCOUNT_RATE = 0.9
RENTAL_INCOME = 10
MOVE_COST = 2
THETA = 0.01

# Poisson Expectations (Lambda values)
EXPECTED_RENTAL_1 = 3
EXPECTED_RENTAL_2 = 4
EXPECTED_RETURN_1 = 3
EXPECTED_RETURN_2 = 2

# Pre-compute Poisson PMFs (up to a safe cutoff)
POISSON_UPPER_BOUND = 11 
poisson_cache = {}

def get_poisson(lam):
    if lam not in poisson_cache:
        poisson_cache[lam] = [poisson.pmf(n, lam) for n in range(POISSON_UPPER_BOUND)]
    return poisson_cache[lam]

# 2. Policy Evaluation

def calculate_q_value(i, j, action, V):
    """
    Calculates the expected return for taking 'action' in state (i, j)
    using the current value function V.
    """
    # Overnight move (constrained by current stock and move limit)
    # If action > 0, move from L1 to L2. If < 0, move from L2 to L1.
    # We assume the policy is already "legal" (doesn't move more than available)
    morning_n1 = int(min(MAX_CARS, max(0, i - action)))
    morning_n2 = int(min(MAX_CARS, max(0, j + action)))
    
    # Starting reward is the cost of moving cars
    expected_q = -abs(action) * MOVE_COST
    
    # Step 2b: Poisson Summation for Rentals
    # For speed, we use the expected values for returns to find s'
    for req1 in range(POISSON_UPPER_BOUND):
        # in the Poisson distribution of having mean EXPECTED_RENTAL_1, what is the probability that there are req1 requests?
        prob1 = get_poisson(EXPECTED_RENTAL_1)[req1]
        for req2 in range(POISSON_UPPER_BOUND):
            prob2 = get_poisson(EXPECTED_RENTAL_2)[req2]
            
            p_scenario = prob1 * prob2
            
            # Actual rentals based on morning stock
            rent1 = min(morning_n1, req1)
            rent2 = min(morning_n2, req2)
            reward = (rent1 + rent2) * RENTAL_INCOME
            
            # Calculate Next State s'
            # Inventory after rentals + Expected Returns (capped at 20)
            s_prime_1 = min(MAX_CARS, morning_n1 - rent1 + EXPECTED_RETURN_1)
            s_prime_2 = min(MAX_CARS, morning_n2 - rent2 + EXPECTED_RETURN_2)
            
            # Bellman Equation Update
            expected_q += p_scenario * (reward + DISCOUNT_RATE * V[int(s_prime_1), int(s_prime_2)])
            
    return expected_q

def policy_evaluation(V, policy):
    while True:
        delta = 0
        # we use values from V, but update values in new_V so as to allow for direction-independent "sweeps" that still gets information spread
        # there can be information leakage if we use in-place updates, because we can be updating states from "both directions" (left to right will not have info needed)
        new_V = np.copy(V)
        
        # Loop through every possible state (i, j)
        for i in range(MAX_CARS + 1):
            for j in range(MAX_CARS + 1):
                old_v = V[i, j]
                
                # Apply the action from our policy
                action = policy[i, j]
                
                new_v_val = calculate_q_value(i, j, action, V)
                new_V[i, j] = new_v_val

                delta = max(delta, abs(old_v - new_v_val))
        
        V[:] = new_V
        print(f"Sweep Delta: {delta}")
        if delta < THETA:
            break
    return V

# 3. Policy Improvement

def policy_improvement(V, policy):
    policy_stable = True

    for i in range(MAX_CARS + 1):
        for j in range(MAX_CARS + 1):
            old_action = policy[i, j]

            # Test all possible actions
            action_values = []
            for action in range(-MAX_CARS_MOVED, MAX_CARS_MOVED + 1):
                # Check if action is legal (not moving more cars than we have)
                if (action > 0 and i >= action) or (action < 0 and j >= abs(action)):
                    q_value = calculate_q_value(i, j, action, V)
                    action_values.append(q_value)
                else:
                    # Assign a very low value to illegal actions
                    action_values.append(-np.inf)

            # Find the best action (argmax)
            # subtract MAX_CARS_MOVED to go from the index of the array (0 to 10) to the actual move (-5 to 5)
            best_action = np.argmax(action_values) - MAX_CARS_MOVED
            policy[i, j] = best_action

            # Check if policy changed
            if old_action != best_action:
                policy_stable = False
            
    return policy, policy_stable

# MAIN PROGRAM
# 1. Initialization

# [i,j] represents a state

# V[i,j] is V(s), the value of having i cars at location 1 and j cars at location 2
V = np.zeros((MAX_CARS+1,MAX_CARS+1))

# pi[i,j] is pi(s), the action to be taken at the state s based on the policy
pi = np.zeros((MAX_CARS+1,MAX_CARS+1), dtype=int)

policy_stable = False
iteration = 0

# 2. Loop until the policy is optimal
while not policy_stable:
    print(f"--- Policy Iteration {iteration} ---")
    
    # Step 2: Policy Evaluation
    # This runs internal 'while' loops until V is accurate for the current pi
    V = policy_evaluation(V, pi)
    
    # Step 3: Policy Improvement
    # This checks if we can do better than pi given the new V
    pi, policy_stable = policy_improvement(V, pi)
    
    iteration += 1

print("Optimal Policy Found!")
# You can now print pi or visualize it with a heatmap

def plot_policy(policy):
    plt.figure(figsize=(10, 8))
    # We flip the y-axis so that (0,0) is at the bottom-left
    sns.heatmap(np.flipud(policy), 
                annot=True, 
                fmt="d", 
                cmap="RdBu", 
                center=0,
                xticklabels=range(MAX_CARS + 1), 
                yticklabels=list(reversed(range(MAX_CARS + 1))))
    
    plt.title("Optimal Policy (Net Cars Moved)")
    plt.xlabel("Number of Cars at Location 2")
    plt.ylabel("Number of Cars at Location 1")
    plt.show()

# Call the plotting function
plot_policy(pi)