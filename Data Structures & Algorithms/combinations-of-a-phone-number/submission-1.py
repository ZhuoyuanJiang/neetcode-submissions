# 2026.10.01 第一次手打 ， 具体可以看之前claude的answer。

"""
个人理解：这题的思路大概是：

1. 先定义好 result 和 current letters 两个列表，理解current_letters是什么意思和要放什么(current_letters代表了我们已经选了的letters)
2. 定义 build combination 这个 helper function，然后把它壳给写好，然后去写一个buld_combination(0)这个我们最后需要call的东西

然后现在我们去写build_combination，先写它的 base case，再去写 main logic
3. 写main logic时因为里面需要往 current letters 里加东西，current_letters肯定里面是加letter，那么，我们为了表示这些 letter，我们需要去定义一个 把digits map成letters的dictionary，所以我们回头去把 dictionary 写上
4. 写完之后 最后我们再补一个edge case 是 digits 为空的情况，所以在最前面再补一个 if not digits的逻辑"""

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        digit_to_letters = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }

        result = []
        current_letters = [] 

        def build_combination(start_index):
            # a helper function that finds every letter string that starts from current_letters and picks one letter for each of the rest of digits for digits[start_index:]  

            # base case
            # when all digits are being picked for one letter
            if start_index == len(digits):
                result.append("".join(current_letters))
                return
            
            # main logic:           
            # 往current_letters里加letter, 大概就是先加这个数字代表的letter然后pop, 然后递归下一个数字
            for letter in digit_to_letters[digits[start_index]]:
                current_letters.append(letter)
                build_combination(start_index+1)
                current_letters.pop()
            
        build_combination(0)
        return result

