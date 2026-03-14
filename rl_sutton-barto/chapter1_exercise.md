# Chapter 1 Tic-Tac-Toe Self-Play Exercise Summary

This document summarizes the core concepts and common pitfalls encountered when analyzing Reinforcement Learning (RL) in the context of a simple game like Tic-Tac-Toe, as per the exercises in Chapter 1. Note that this was generated with Gemini as I chatted with it to work through my understanding of these exercises.

---

## 1. Self-Play vs. Random Opponent

**The Question:** Does the agent learn a different policy when playing against itself (Self-Play) compared to a random opponent?

- **Initial Intuition:** I suspected the policy wouldn't change because the agent is still just observing specific board states regardless of the opponent's identity.
- **The RL Reality:** The **Value** ($V$) of a state is tied to the probability of winning from that position.
  - **Against Random:** The agent learns an _opportunistic_ policy. It might take risky moves that a pro would punish, because it "knows" a random player will likely miss the block.
  - **Against Self:** The agent learns a **Minimax** (optimal) policy. It assumes the opponent is as smart as itself and eventually converges to a draw-heavy, defensive strategy.

---

## 2. Exploiting Symmetries

**The Question:** Should we use board symmetries (rotations/reflections) to shrink the state-space if the opponent does not?

- **Initial Intuition:** Yes, because the opponent not using symmetry doesn't change the underlying game math for us.
- **The RL Reality:** It depends on your goal.
  - **To be a "Pro" (Optimal):** Yes. Using symmetry allows for ~8x faster learning and discovers the "mathematical truth" of the board.
  - **To be a "Shark" (Exploitative):** No. If your opponent has a "tell" (e.g., they always miss blocks in the bottom-right corner but never the top-left), using symmetry **smears** that data. You would lose the ability to specifically exploit that one weak corner.

---

## 3. Greedy Play (The Exploration Problem)

**The Question:** What happens if the agent is 100% greedy from the start?

- **Initial Intuition:** A mental model to think about it is that: a completely greedy player ignores exploration and focuses entirely on exploitation.
- **The RL Reality:** You were exactly right. This leads to the **Local Optimum** trap.
  - If a greedy agent wins its first game using a mediocre move, it will repeat that move forever.
  - It never "explores" the rest of the game tree, so it may never find the truly optimal strategy (the Global Optimum).

---

## 4. Learning from Exploratory Moves

**The Question:** If we continue to explore, should we update our values based on those "random" moves?

- **Initial Intuition:** Learning from exploration makes the knowledge more "generalizable."
- **The RL Reality:** It’s a choice between **On-Policy** (e.g., SARSA) and **Off-Policy** (e.g., Q-Learning).
  - **Learning from all moves:** You learn the value of your _current, clumsy self_. The agent becomes "self-aware" that it might make a random mistake, so it chooses safer paths. (Results in more wins if you _must_ keep exploring).
  - **Learning only from greedy moves:** You learn the value of _perfection_. It ignores the "noise" of its own practice mistakes to find the absolute best theoretical path. (Results in more wins if you eventually _stop_ exploring).

---

## 5. Better ways to Solve the Tic-Tac-Toe Problem

**The Question:** Can you think of other ways to improve the reinforcement learning player? Can you think of any better way to solve the tic-tac-toe problem as posed?

- **Initial Intuition:** Not learn from exploratory moves, and also stop making exploratory moves to increase the probability of winning.
- **The RL Reality:** Use neural networks, look-ahead, experience replay, or most simply a Minimax Algorithm with Alpha-Beta Pruning.

---

## 6. Summary Table of Key Shifts

| Concept              | Your Logical Starting Point | The Deep RL Insight                                                               |
| :------------------- | :-------------------------- | :-------------------------------------------------------------------------------- |
| **Opponent Type**    | "A state is a state."       | The environment is "non-stationary"; value depends on opponent skill.             |
| **Symmetry**         | "Always more efficient."    | Efficiency comes at the cost of being unable to exploit specific opponent biases. |
| **Greedy Play**      | "Play to win now."          | Playing to win now prevents you from learning how to win bigger later.            |
| **Exploration Data** | "It's just extra data."     | It determines if you are learning "Safe Play" or "Optimal Play."                  |

---
