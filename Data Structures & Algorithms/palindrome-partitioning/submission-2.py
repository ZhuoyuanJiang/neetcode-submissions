# 这一版是手打的，没有用之前的否定式 guard clause + continue的逻辑，而是直接用正面肯定式if is_palindrome(start_index, end_index):的逻辑，我个人感觉更顺一点。

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        result = []
        current_parts = [] # to save palindromes that already cut out
        # current_parts is a shared mutable list

        def is_palindrome(left, right):
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True
            

        def find_all_partitions(start_index):
            # a helper function to find all ways of cutting palindormes starting from start_index given "current_parts"; current_parts are existing palindromes derived from index = 0 to start_index.

            # base case: when all substring in s is already handled
            if start_index == len(s): # which means all substring is handled
                result.append(current_parts.copy())
                return
            
            # main logic:
            # now we append palindrome into current_parts first, then backtrack starting from a new end_index, then pop the palindrome
            for end_index in range(start_index, len(s)):
                # 按理说应该写 if s[start_index : end_index+1] is palindrome: 
                # 但那样太麻烦了，我们回去写了一个判断是不是palindrome的helper function, 然后直接用is_palindrome(start_index, end_index)来判断
                if is_palindrome(start_index, end_index):
                    current_parts.append(s[start_index:end_index+1]) # append palindrome
                    find_all_partitions(end_index +1)
                    current_parts.pop()
        

        find_all_partitions(0)
        return result

        