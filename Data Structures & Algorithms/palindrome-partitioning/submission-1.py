# 202610.01 手打一遍试试，可以看下面的个人理解和之前的submission更具体的Notes.

# 个人理解：build partitions大概就是从这个start index开始，find every way to cut palindromes. 所以build_partitions(0)的意思就是找到所有把现在的字符串cut成palindromes的方法。然后具体里面就是，里面有递归，建立一个current_parts的list, 然后每进一个palindrome, 我们就在这个palindrome的end_index之后再取做build_partitions(end_index+1),然后到end_index == len(s)的时候就可以停止递归了。大概整个思路就是这样。中途需要一个helper function来查即将append进current_parts的是不是palindrome. 

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        result = []
        # current_parts = the palindromic pieces cut so far (shared, mutated list)
        current_parts = []

        def is_palindrome(left, right):
            while left < right:
                if s[left] != s[right]:
                    return False
                left +=1
                right -=1
            return True
            

        def build_partitions(start_index):
            # finds every way to cut s[start_index:] into palindromes，
            # puts each way after current_parts, and adds the complete lists to result 
            # e.g. s = "aab", current_parts = ["a"], start_index = 1
            # "ab" can only be cut as "a" + "b" -> adds ["a","b","b"]

            # base case: the whole string has been cut 
            if start_index == len(s):
                result.append(current_parts.copy())
                return 
            
            # main logic:
            for end_index in range(start_index, len(s)):

                # append进current_parts之前得确定它是palindrome

                if not is_palindrome(start_index, end_index):
                    continue
                #所以现在的start_index到end_index是一个palindrome, 所以我们append进current_parts
                current_parts.append(s[start_index:end_index+1])
                build_partitions(end_index+1)
                current_parts.pop()


        build_partitions(0)
        return result
