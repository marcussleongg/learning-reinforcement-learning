# RL Notes: Dynamic Programming & Information Flow

_Context: Sutton & Barto, Chapter 4_

## 1. The Core Shift: Expected vs. Sample Updates

The fundamental hurdle in moving from Chapter 3 to Chapter 4 is distinguishing between **Expected Updates** (DP) and **Sample Updates** (later RL).

- **Expected Updates (DP):** You act with "perfect information." You look at every possible future branch and calculate their weighted average based on the transition dynamics $p(s', r \mid s, a)$.
- **Sample Updates (RL):** You act with "experience." You don't know the probabilities; you take an action, observe one specific result, and update your belief based solely on that single trajectory.

| Feature         | Expected Update (DP)                       | Sample Update (RL)                               |
| :-------------- | :----------------------------------------- | :----------------------------------------------- |
| **Information** | Uses the **probability** of outcomes.      | Uses a **single observed** outcome.              |
| **Requirement** | Needs a full model ($p(s', r \mid s, a)$). | Only needs to "interact" with the environment.   |
| **Analogy**     | Reading a math textbook on Blackjack odds. | Actually playing a hand of Blackjack at a table. |

## 2. Why We Sweep Multiple Times

**Misunderstanding:** "One sweep should be enough to see all states since I visited them all."
**The Reality:** Information in an MDP is **local**. A state only knows what its immediate neighbors tell it.

- **The "Gossip" Protocol:** If a reward is at the end of a chain, it behaves like gossip. In Sweep 1, only the state directly next to the reward learns about it. In Sweep 2, the next state in line hears the "news" from the first state.
- **Information Propagation:** It takes multiple sweeps for the value of a distant goal to "ripple" back to the starting state.
- **The Convergence ($\theta$):** We keep sweeping the same states until the "news" has saturated the entire map and the values stabilize (the change is less than $\theta$).

## 3. Policy Iteration vs. Value Iteration

Both algorithms converge to the same optimal goal ($v_*$), but they manage their "patience" differently.

- **Policy Iteration:** The **Perfectionist**. It insists on running a full inner loop (Policy Evaluation) until the values are 100% accurate for the current plan before it ever considers changing an action.
- **Value Iteration:** The **Pragmatist**. It doesn't wait for perfect evaluation. It updates the value of a state based on the **best possible neighbor** immediately, effectively combining evaluation and improvement into a single sweep.

## 4. Stability Bug & Tie-Breaking

In Policy Iteration, the algorithm can infinite-loop if two actions are equally good.

- **The Fix:** Use a consistent tie-breaking rule (e.g., always pick the action with the lowest index) or only update the policy if an action is **strictly better** than the current one.

---

_Clarifying misconceptions_

# RL Notes: The MDP Framework & Dynamic Programming

_Context: Sutton & Barto, Chapters 3 & 4_

## 1. The MDP (The Problem)

- **The Markov Property:** The current state $S_t$ contains all necessary information. The past doesn't matter for the future.
- **Double Stochasticity:** 1. **Transitions:** Taking action $a$ in state $s$ only gives a _probability_ $p(s'|s,a)$ of landing in $s'$. 2. **Rewards:** The reward $r$ received during a transition is also a random variable.
- **The Goal:** Maximize the **Expected Return** ($G_t$), which is the sum of future discounted rewards: $R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} \dots$

## 2. The Policy (The Solution)

- **Definition:** A mapping $\pi$ from states to actions (a "strategy guide").
- **Optimality:** An optimal policy $\pi_*$ is a mapping that achieves the maximum possible expected return from every state $s$ in the environment.

## 3. The "How" (Dynamic Programming)

- **Expected Updates:** We use the environment's "map" ($p$) to mathematically average out the two layers of stochasticity. We don't "sample" or "guess"; we calculate the exact mean.
- **The Gossip Protocol (Sweeping):** Information is local. We must sweep through the entire state set multiple times to allow the "news" of rewards to ripple across the connections between states.
- **Convergence:** \* **Evaluation:** Stops when the value estimates stop moving ($\Delta < \theta$).
  - **Improvement:** Stops when the actions chosen for each state no longer change (Policy Stability).

## 4. V vs. Q: The "Thereafter" Rule

- **V(s) (State-Value):** "How good is it to be here?" — Expected return if I follow the current plan ($\pi$) from the start.
- **Q(s, a) (Action-Value):** "How good is this action?" — Expected return if I take action $a$ first, then follow the plan ($\pi$) thereafter.
- **Improvement Logic:** If $Q(s, a) > V(s)$, it means action $a$ is better than your current plan. Update the plan to pick $a$.
- **$v_*$ / $q_*$:** How good is it to follow the **best possible** plan? (Calculated via maximums).
