# Claude's solution (optimal) #也可以看之前的submission,只是不是optimal,但思路很类似，都很简单。

"""
LeetCode 70. Climbing Stairs  (1D Dynamic Programming)

==============================================================================
PROBLEM STATEMENT
==============================================================================
You are given an integer n representing the number of steps to reach the top
of a staircase. You can climb with either 1 or 2 steps at a time.
Return the number of distinct ways to climb to the top of the staircase.

Constraints: 1 <= n <= 45

==============================================================================
EXAMPLES
==============================================================================
Example 1:  n = 2  ->  2      (1+1, 2)
Example 2:  n = 3  ->  3      (1+1+1, 1+2, 2+1)

==============================================================================
SOLUTION APPROACH
==============================================================================
Bottom-up 1D DP with two rolling variables (space-optimized Fibonacci).
Each state only depends on the previous two, so no dp array is needed.
每个状态只依赖前两个，所以不需要 dp 数组，两个变量滚动即可。

==============================================================================
DP STATE 在做什么
==============================================================================
ways(step) = 恰好站到第 step 阶的不同走法数。
    e.g. ways(3) = 3：1+1+1, 1+2, 2+1
最终答案就是 ways(n)。

代码里没有 ways 数组，用两个滚动变量表示：
    ways_one_below = ways(current_step - 1)
    ways_two_below = ways(current_step - 2)

==============================================================================
RECURRENCE（状态转移）
==============================================================================
ways(step) = ways(step - 1) + ways(step - 2)

Why: look at the LAST move onto `step`.
    (a) last move was a 1-step -> came from step - 1 -> ways(step - 1) paths
    (b) last move was a 2-step -> came from step - 2 -> ways(step - 2) paths
看"最后一步"：(a)、(b) 两组的最后一步不同，所以互不重叠；
又只有这两种可能，所以覆盖全部路径。不重不漏 -> 直接相加。

    e.g. ways(4) = ways(3) + ways(2) = 3 + 2 = 5
         from step 3 (+1): 1+1+1+1, 1+2+1, 2+1+1
         from step 2 (+2): 1+1+2,   2+2

==============================================================================
BASE CASE
==============================================================================
ways(1) = 1    only "1"
ways(2) = 2    "1+1" and "2"

Why two base cases: the recurrence reaches back two steps, so the first
state it can compute is ways(3). Everything below that must be given.
递推式往回看两步，所以第一个能算出来的是 ways(3)，ways(1) 和 ways(2)
必须直接给出。

==============================================================================
INTUITION
==============================================================================
Brute force would enumerate every path (backtracking) — but we only need
the COUNT, not the paths. The count for a given step never changes, so
compute it once and reuse it. ways(n) turns out to be Fib(n + 1).
暴力枚举（backtracking）会把每条路径列出来，但题目只要数量。
每个 step 的数量是固定的，算一次就够，这就是 DP 和枚举的区别。

==============================================================================
ALGORITHM
==============================================================================
1. If n <= 2, return n (base cases).
2. ways_two_below = ways(1) = 1, ways_one_below = ways(2) = 2.
3. For current_step from 3 to n:
       ways_current   = ways_one_below + ways_two_below
       ways_two_below = ways_one_below     # slide window up one step
       ways_one_below = ways_current
4. Return ways_one_below (= ways(n)).

==============================================================================
WHY THIS WORKS
==============================================================================
- The "last move" split is exhaustive and disjoint, so every ordered
  sequence of moves is counted exactly once (1+2 and 2+1 are distinct).
- Bottom-up order guarantees ways(step-1) and ways(step-2) are ready
  before ways(step) is computed. 自底向上，用到前两个值时它们一定已经算好。

==============================================================================
TIME COMPLEXITY
==============================================================================
Loop runs n - 2 times, O(1) work each.
Total = O(n - 2) * O(1) = O(n).

==============================================================================
SPACE COMPLEXITY
==============================================================================
Three integer variables regardless of n; no array, no recursion stack.
Total = O(1).

==============================================================================
ALTERNATIVES (brief)
==============================================================================
- Top-down memoized recursion (dfs(step) + cache) or a full dp array:
  O(n) time but O(n) space. Top-down is the natural bridge from backtracking.
- Matrix exponentiation: O(log n), overkill for n <= 45.
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        # Base cases: ways(1) = 1, ways(2) = 2, i.e. the answer is n itself.  # Time O(1), Space O(1)
        if n <= 2:
            return n

        ways_two_below = 1  # ways(1) = ways(current_step - 2) when current_step = 3  # Time O(1), Space O(1)
        ways_one_below = 2  # ways(2) = ways(current_step - 1) when current_step = 3  # Time O(1), Space O(1)

        for current_step in range(3, n + 1):  # n - 2 iterations  # Time O(n), Space O(1)
            # Recurrence: last move was 1-step (from current_step-1) or 2-step (from current_step-2)
            # 最后一步跨 1 阶或跨 2 阶，两种情况相加
            ways_current = ways_one_below + ways_two_below  # Time O(1), Space O(1)

            # Slide the window up one step for the next iteration
            # 窗口整体往上挪一阶：旧的 "one below" 变成新的 "two below"
            ways_two_below = ways_one_below  # Time O(1), Space O(1)
            ways_one_below = ways_current    # Time O(1), Space O(1)

        return ways_one_below  # after the loop, ways_one_below = ways(n)  # Time O(1)


"""
==============================================================================
WALKTHROUGH
==============================================================================

---------- Example A: n = 3 (expected 3) ----------
n = 3 > 2, skip base case.
Init: ways_two_below = 1 (ways(1)), ways_one_below = 2 (ways(2))

current_step = 3:
    ways_current   = 2 + 1 = 3          -> ways(3) = 3
    ways_two_below = 2                  (= ways(2))
    ways_one_below = 3                  (= ways(3))
Loop ends (range(3, 4) = 3 only).
return ways_one_below = 3  ✓

---------- Example B: n = 5 (expected 8) ----------
n = 5 > 2, skip base case.
Init: ways_two_below = 1 (ways(1)), ways_one_below = 2 (ways(2))

current_step = 3:
    ways_current   = 2 + 1 = 3          -> ways(3) = 3
    ways_two_below = 2                  (= ways(2))
    ways_one_below = 3                  (= ways(3))

current_step = 4:
    ways_current   = 3 + 2 = 5          -> ways(4) = 5
    ways_two_below = 3                  (= ways(3))
    ways_one_below = 5                  (= ways(4))

current_step = 5:
    ways_current   = 5 + 3 = 8          -> ways(5) = 8
    ways_two_below = 5                  (= ways(4))
    ways_one_below = 8                  (= ways(5))

Loop ends (range(3, 6) = 3, 4, 5).
return ways_one_below = 8  ✓

Sanity check, ways(5) = 8 enumerated:
    1+1+1+1+1
    1+1+1+2, 1+1+2+1, 1+2+1+1, 2+1+1+1
    1+2+2,   2+1+2,   2+2+1
    = 1 + 4 + 3 = 8  ✓

---------- Example C: n = 2 (expected 2) ----------
n = 2 <= 2, return n = 2  ✓
"""