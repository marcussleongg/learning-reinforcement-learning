# Chapter 3 Markov Decision Processes Learning Summary

## 1. The Markov Property & The "Goldilocks Zone"

- **The Concept:** The Markov property means the current state $S_t$ is a "sufficient summary" of the past.
- **The Misconception:** Thinking the Markov property is about the agent's _action_.
- **The Correction:** It's actually about the _environment's dynamics_. If your state representation is too "high-level" (e.g., missing road conditions), you break the Markov property because you can't predict the future without looking at the past. You need to find the "Goldilocks Zone" of detail.

## 2. Episodic vs. Continuing Tasks

- **The Difference:** Episodic tasks have a terminal state; continuing tasks do not.
- **Equation 3.3 Modification:** In episodic tasks, the summation of next states includes the terminal state ($s' \in \mathcal{S}^+$).
- **Reward Traps:**
  - Giving a **positive reward** for failure in an episodic task (even with discounting) makes the agent want to "suicide" to get the reward immediately.
  - A **zero reward** for everything except the goal makes the agent lazy; it has no incentive to find the goal _quickly_.

## 3. The Return ($G_t$) vs. Value ($v_\pi, q_\pi$)

- **The Misconception:** Treating $G_t$ as a running total from the start of the episode.
- **The Correction:** $G_t$ is **forward-looking**. It is the sum of rewards _after_ time $t$.
- **Recursive Property:** $G_t = R_{t+1} + \gamma G_{t+1}$. This is the foundation of the Bellman Equation.
- **Infinite Returns:** When rewards are constant ($R$) forever, $G_t = \frac{R}{1-\gamma}$.

## 4. The Two Layers of Randomness

There are two distinct probability distributions at play in every step:

1.  **The Policy ($\pi(a|s)$):** The agent's choice (The "Agent's Dice").
2.  **The Dynamics ($p(s', r | s, a)$):** The environment's response (The "Environment's Dice").

- **Outcome Packages:** The environment doesn't just pick a next state; it picks a **joint package** of (next state $s'$, reward $r$).

## 5. The Anatomy of the Bellman Equation

The equation $v_\pi(s) = \sum_a \pi(a|s) \sum_{s', r} p(s', r | s, a) [r + \gamma v_\pi(s')]$ breaks down as:

- **$\sum_a \pi(a|s)$**: Averaging over the agent's possible choices.
- **$\sum_{s', r} p(s', r | s, a)$**: Averaging over the environment's possible responses.
- **$[r + \gamma v_\pi(s')]$**: The total value of a single future branch.
  - **$r$**: Immediate gratification.
  - **$\gamma v_\pi(s')$**: The discounted "summary" of the entire infinite future starting from the next state.

> **Why is $\gamma$ not a power?** Because $v_\pi(s')$ already contains the future powers ($1, \gamma, \gamma^2 \dots$). Multiplying it by $\gamma$ once shifts all those internal powers to the correct value for the current time step.
