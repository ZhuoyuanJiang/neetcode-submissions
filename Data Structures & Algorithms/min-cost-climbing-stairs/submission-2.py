class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        top_floor = len(cost)
        cheapest_one_below = 0 
        cheapest_two_below = 0 

        for current_floor in range(2, top_floor + 1):
            cost_from_one_below = cheapest_one_below + cost[current_floor -1]
            cost_from_two_below = cheapest_two_below + cost[current_floor -2]
            cheapest_current = min(cost_from_one_below, cost_from_two_below)
            
            # 两个变量整体往上挪一层
            cheapest_two_below = cheapest_one_below 
            cheapest_one_below = cheapest_current
        
        return cheapest_one_below # == cheapest_current 
        # return cheapest_one_below而不是优先chepeast_current是因为cheapest_one_below永远存在，而但凡len(cost)小于2， 我们的for loop可能就不会跑或者报错，那样就没有cheapest_current了。但cheapest_current这题也行是因为限制了cost.length>=2
        

# Claude's solution:


# from typing import List


# class Solution:
#     """
#     PROBLEM: Min Cost Climbing Stairs (LeetCode 746 - Easy)
#     =======================================================

#     PROBLEM STATEMENT:
#     cost[i] is the cost of stepping off floor i. After paying, you can climb
#     to floor i+1 or floor i+2. You may start on floor 0 or floor 1.
#     Return the minimum cost to reach the top = floor len(cost)
#     (one past the last index).

#     EXAMPLES:
#     Example 1: cost = [1,2,3]

#         Start on floor 1, pay cost[1] = 2, jump 2 → floor 3 (top)

#         Output: 2

#     Example 2: cost = [1,2,1,2,1,1,1]

#         floor 0 → 2 → 4 → 6 → top
#         pay cost[0] + cost[2] + cost[4] + cost[6] = 1 + 1 + 1 + 1 = 4

#         Output: 4

#     ==============================================================================
#     SOLUTION APPROACH: Bottom-Up DP with Two Variables
#     ==============================================================================

#     INTUITION (核心思路):
#     ====================

#     This is "Climbing Stairs" with prices — instead of COUNTING the ways to
#     reach each floor, we track the CHEAPEST way to reach each floor.

#     Approach: walk up floor by floor, and for each floor record ONE number:
#         "the cheapest total cost to stand on this floor"
#     The number recorded for the top floor is the answer.

#     Why only look at the two floors below?
#     --------------------------------------
#     You can only land on floor i by jumping from floor i-1 (1 step) or from
#     floor i-2 (2 steps). You pay the cost of the floor you jump FROM. So:

#         cheapest(i) = min( cheapest(i-1) + cost[i-1],    ← jumped 1 from i-1
#                            cheapest(i-2) + cost[i-2] )   ← jumped 2 from i-2

#     Why can we forget HOW we got to a floor?
#     ----------------------------------------
#     Once we know "floor 2 costs at least 1", the exact path to floor 2 doesn't
#     matter for anything above it. Brute force would re-explore every path
#     through floor 2 again and again; here each floor is computed once.
#     That's the whole idea of dynamic programming.

#     Where do we start?
#     ------------------
#     Floor 0 and floor 1 are free starting points:
#         cheapest(0) = 0, cheapest(1) = 0
#     The formula looks 2 floors back, so these two are given directly and
#     the formula kicks in from floor 2.

#     Compare with Climbing Stairs (LeetCode 70):

#     | Climbing Stairs               | Min Cost Climbing Stairs             |
#     |-------------------------------|--------------------------------------|
#     | Each floor: # of ways         | Each floor: cheapest total cost      |
#     | Combine two below with  +     | Combine two below with  min          |
#     | Nothing extra to add          | Add cost of the floor you jump from  |
#     | Start: ways(1)=1, ways(2)=2   | Start: cheapest(0)=0, cheapest(1)=0  |

#     Trick: Only keep two numbers
#     ----------------------------
#     Each floor only needs the two floors right below it, so instead of an
#     array we keep two variables and slide them up one floor per iteration.
#     Space O(n) → O(1).

#     面试术语对照:
#     -------------
#     面试官问 "dp[i] 代表什么" → 就是每层记的那个数，这题是 cheapest(i)。
#     面试官问 "状态转移 / recurrence 是什么" → 就是上面那条 min(...) 公式。

#     核心思路 (Chinese):
#     ------------------
#     从下往上一层一层算，每层记一个数：站到这一层最少花多少钱。
#     每层只能从下面一层或两层跳上来，跳的时候付起跳那层的 cost，两种来路取更便宜的。
#     最下面两层免费站，算到 top 那层的数就是答案。
#     每层只依赖下面两层，所以用两个变量滚动，不用存整个数组。

#     Visual (cost = [1,2,3], top = floor 3):
#     ---------------------------------------
#     floor 0: free start                                  → cheapest = 0
#     floor 1: free start                                  → cheapest = 0
#     floor 2: from floor 1: 0 + cost[1] = 0 + 2 = 2
#              from floor 0: 0 + cost[0] = 0 + 1 = 1       → cheapest = 1
#     floor 3: from floor 2: 1 + cost[2] = 1 + 3 = 4
#              from floor 1: 0 + cost[1] = 0 + 2 = 2       → cheapest = 2 ✓

#     ALGORITHM:
#     ==========
#     1. top_floor = len(cost)
#     2. cheapest_two_below = 0 (floor 0), cheapest_one_below = 0 (floor 1)
#     3. For current_floor from 2 to top_floor:
#          - compute both options, take the min → cheapest_current
#          - slide up: cheapest_two_below ← cheapest_one_below
#                      cheapest_one_below ← cheapest_current
#     4. Return cheapest_one_below (= cheapest(top_floor))

#     WHY THIS WORKS:
#     ===============
#     - Every path to floor i ends with a jump from i-1 or i-2, so the two
#       options cover every possibility.
#     - The cheapest path to floor i must use the cheapest path to the floor it
#       jumped from — otherwise swapping in the cheaper one lowers the total.
#     - Going bottom-up, the two floors below are always computed first.
#     - len(cost) >= 2, so the loop always runs at least once.

#     TIME:  O(n) — one pass over floors 2..top_floor, O(1) work each
#     SPACE: O(1) — a few variables, no array
#     """

#     def minCostClimbingStairs(self, cost: List[int]) -> int:
#         # ==================== START: TWO FREE FLOORS ====================
#         top_floor = len(cost)                                                # e.g. [1,2,3] → top is floor 3
#         cheapest_two_below = 0                                               # cheapest(0) = 0, free start
#         cheapest_one_below = 0                                               # cheapest(1) = 0, free start

#         # ==================== CLIMB FLOOR BY FLOOR ====================
#         for current_floor in range(2, top_floor + 1):                        # O(n) — floors 2..top_floor

#             # Option 1: stand on the floor below, pay its cost, jump 1
#             cost_from_one_below = cheapest_one_below + cost[current_floor - 1]   # e.g. floor 3: 1 + cost[2] = 4

#             # Option 2: stand two floors below, pay its cost, jump 2
#             cost_from_two_below = cheapest_two_below + cost[current_floor - 2]   # e.g. floor 3: 0 + cost[1] = 2

#             # Cheapest way onto this floor
#             cheapest_current = min(cost_from_one_below, cost_from_two_below)     # O(1) — e.g. min(4, 2) = 2

#             # Slide both variables up one floor for the next iteration
#             # 两个变量整体往上挪一层
#             cheapest_two_below = cheapest_one_below                          # old "one below" → new "two below"
#             cheapest_one_below = cheapest_current                            # this floor → new "one below"

#         return cheapest_one_below                                            # = cheapest(top_floor)


# # ==============================================================================
# # DETAILED WALKTHROUGH
# # ==============================================================================
# """
# Example 1: cost = [1,2,3]

# top_floor = 3
# cheapest_two_below = 0 (floor 0), cheapest_one_below = 0 (floor 1)

# ═══════════════════════════════════════════════════════════════════
# current_floor = 2:

# cost_from_one_below = 0 + cost[1] = 0 + 2 = 2
# cost_from_two_below = 0 + cost[0] = 0 + 1 = 1
# cheapest_current    = min(2, 1) = 1          → floor 2 costs at least 1

# Slide: cheapest_two_below = 0, cheapest_one_below = 1

# ═══════════════════════════════════════════════════════════════════
# current_floor = 3:

# cost_from_one_below = 1 + cost[2] = 1 + 3 = 4
# cost_from_two_below = 0 + cost[1] = 0 + 2 = 2
# cheapest_current    = min(4, 2) = 2          → floor 3 (top) costs at least 2

# Slide: cheapest_two_below = 1, cheapest_one_below = 2

# ═══════════════════════════════════════════════════════════════════
# Loop ends. Return cheapest_one_below = 2 ✓


# Example 2: cost = [1,2,1,2,1,1,1]

# top_floor = 7
# cheapest_two_below = 0 (floor 0), cheapest_one_below = 0 (floor 1)

# ═══════════════════════════════════════════════════════════════════
# current_floor = 2:
# cost_from_one_below = 0 + cost[1] = 0 + 2 = 2
# cost_from_two_below = 0 + cost[0] = 0 + 1 = 1
# cheapest_current    = min(2, 1) = 1
# Slide: cheapest_two_below = 0, cheapest_one_below = 1

# ═══════════════════════════════════════════════════════════════════
# current_floor = 3:
# cost_from_one_below = 1 + cost[2] = 1 + 1 = 2
# cost_from_two_below = 0 + cost[1] = 0 + 2 = 2
# cheapest_current    = min(2, 2) = 2
# Slide: cheapest_two_below = 1, cheapest_one_below = 2

# ═══════════════════════════════════════════════════════════════════
# current_floor = 4:
# cost_from_one_below = 2 + cost[3] = 2 + 2 = 4
# cost_from_two_below = 1 + cost[2] = 1 + 1 = 2
# cheapest_current    = min(4, 2) = 2
# Slide: cheapest_two_below = 2, cheapest_one_below = 2

# ═══════════════════════════════════════════════════════════════════
# current_floor = 5:
# cost_from_one_below = 2 + cost[4] = 2 + 1 = 3
# cost_from_two_below = 2 + cost[3] = 2 + 2 = 4
# cheapest_current    = min(3, 4) = 3
# Slide: cheapest_two_below = 2, cheapest_one_below = 3

# ═══════════════════════════════════════════════════════════════════
# current_floor = 6:
# cost_from_one_below = 3 + cost[5] = 3 + 1 = 4
# cost_from_two_below = 2 + cost[4] = 2 + 1 = 3
# cheapest_current    = min(4, 3) = 3
# Slide: cheapest_two_below = 3, cheapest_one_below = 3

# ═══════════════════════════════════════════════════════════════════
# current_floor = 7:
# cost_from_one_below = 3 + cost[6] = 3 + 1 = 4
# cost_from_two_below = 3 + cost[5] = 3 + 1 = 4
# cheapest_current    = min(4, 4) = 4
# Slide: cheapest_two_below = 3, cheapest_one_below = 4

# ═══════════════════════════════════════════════════════════════════
# Loop ends. Return cheapest_one_below = 4 ✓
# """