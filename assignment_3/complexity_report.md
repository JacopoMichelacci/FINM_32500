# Complexity Report

## 1. Overview
This report compares the performance of three moving-average trading strategies:
**NaiveMovingAverage**, **WindowedMovingAverage**, and **RefactoredMovingAverage**.
Profiling measured runtime and peak memory for 1k, 10k, and 100k ticks.

---

## 2. Theoretical Complexity
| Strategy | Time | Space | Notes |
|-----------|------|--------|-------|
| NaiveMovingAverage | O(n) | O(n) | Recomputes full mean each tick |
| WindowedMovingAverage | O(1) | O(k) | Uses deque for sliding window |
| RefactoredMovingAverage | O(1) | O(k) | Incremental update, optimized version |

---

## 3. Empirical Results
| nTicks | Naive Time (s) | Windowed Time (s) | Refactored Time (s) | Naive Mem (MB) | Windowed Mem (MB) | Refactored Mem (MB) |
|---------|----------------|-------------------|---------------------|----------------|-------------------|---------------------|
| 1k | 0.0038 | 0.0013 | 0.0011 | 0.0086 | 0.0006 | 0.0001 |
| 10k | 0.2525 | 0.0105 | 0.0096 | 0.0915 | 0.0001 | 0.0001 |
| 100k | 24.2111 | 0.1051 | 0.0964 | 0.8595 | 0.0001 | 0.0001 |

---

## 4. Plots
![RunTime Scaling](assignment_3/plots/runtime_vs_input.png)
![RunTime Scaling](assignment_3/plots/memory_vs_input.png)


## 5. Analysis
- **Naive** runtime grows linearly, showing O(n) behavior, while memory also scales with tick count.  
- **Windowed** and **Refactored** maintain near-constant time and negligible memory growth.  
- The **Refactored** version performs best overall — slightly faster, same minimal memory.  
- Optimization improves scalability from seconds → milliseconds for small data and from ~24s → 0.1s at 100k ticks.
