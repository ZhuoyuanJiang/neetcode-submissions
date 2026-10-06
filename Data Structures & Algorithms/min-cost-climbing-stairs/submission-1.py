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
        