# class Solution:
#     def letterCombinations(self, digits: str) -> List[str]:
        







# Claude's Solution 

class Solution:
    """
    PROBLEM: Letter Combinations of a Phone Number (LeetCode 17 - Medium)
    ======================================================================
    
    PROBLEM STATEMENT:
    Given a string `digits` made of digits 2-9, each digit maps to a set of letters
    (like an old phone keypad). Return all possible letter strings that `digits`
    could represent, in any order.
    
        2 → abc    3 → def    4 → ghi    5 → jkl
        6 → mno    7 → pqrs   8 → tuv    9 → wxyz
    
    EXAMPLES:
    Example 1: digits = "34"
        Output: ["dg","dh","di","eg","eh","ei","fg","fh","fi"]
        (3 → def 有 3 种，4 → ghi 有 3 种，一共 3 × 3 = 9 个)
    
    Example 2: digits = ""
        Output: []
    
    ==============================================================================
    SOLUTION APPROACH: Backtracking (one level per digit, pick one letter per level)
    ==============================================================================
    
    INTUITION (核心思路):
    ====================
    
    如果长度固定，就是嵌套 for 循环
    ------------------------------
    digits = "34" 时，答案就是：
        for first in "def":
            for second in "ghi":
                记录 first + second
    但 digits 有几位是变量，没法写「len(digits) 层嵌套 for」。
    和 Subsets 一样的思路：用递归代替嵌套循环，递归深度 = 数字个数。

    每一层做什么
    -----------
    digit_index 表示「现在轮到给 digits[digit_index] 这个数字选字母」。
    这一层的 for 循环遍历这个数字对应的所有字母，每个字母都试一次：
        选这个字母（append）→ 递归去给下一个数字选字母 → 撤销（pop）
    当 digit_index == len(digits)，每个数字都选好了字母 → 记录一个答案。

    和前几题对比
    -----------
    - Subsets：每层 2 种选择（选 / 不选），深度 = 元素个数
    - 这题：  每层 3 或 4 种选择（选哪个字母），深度 = 数字个数
    结构一样：「一层处理一个位置，这一层的 for 试所有选择」。
    区别：这题 for 循环遍历的是「当前数字的字母」，不是数组下标，
    所以不需要 start_index，也不会出现重复，不需要去重。

    每次调用的 letter 是自己的
    -------------------------
    两层调用的 for 循环都叫 letter，但每次调用有自己的局部变量，互不影响。
    外层停在 letter="d" 等内层跑完时，内层的 letter 在 "g"/"h"/"i" 之间换，
    外层的 letter 一直还是 "d"。

    为什么 digits 为空要特判
    -----------------------
    如果不特判，build_combinations(0) 一进门 digit_index == 0 == len(digits)，
    会记录一个空字符串，返回 [""]。但题目要求返回 []。所以开头直接 return []。

    为什么记录时用 "".join(current_letters)
    --------------------------------------
    current_letters 是一个字符列表，被 append/pop 反复修改。"".join 生成一个新字符串，
    相当于拍快照（作用同前几题的 .copy()）。

    HELPER 在做什么 (build_combinations):
    ------------------------------------
        build_combinations(digit_index)

    心里读成：
        current_letters 里已经给 digits[:digit_index] 的每个数字选好了字母。
        给剩下的 digits[digit_index:] 每个数字各选一个字母，
        找出所有以 current_letters 开头的字符串，加入 result。

    例：digits = "34"，current_letters = ["d"]，digit_index = 1
        → 轮到数字 "4"，对应 "ghi" → 加入 "dg"、"dh"、"di"

    核心思路 (Chinese):
    ------------------
    一个数字一层。这一层的 for 循环试这个数字的每个字母：放进 current_letters，
    递归去处理下一个数字，回来后 pop 掉换下一个字母。所有数字都选完就记录。
    
    ALGORITHM:
    ==========
    1. 若 digits 为空，return []
    2. 建立 digit_to_letters 映射；result = []；current_letters = []
    3. build_combinations(digit_index):
       a. Base case: digit_index == len(digits) → 记录 "".join(current_letters)，return
       b. for letter in digit_to_letters[digits[digit_index]]:
          - 选:   current_letters.append(letter)
          - 递归: build_combinations(digit_index + 1)
          - 撤销: current_letters.pop()
    4. 调用 build_combinations(0)，返回 result
    
    WHY THIS WORKS (为什么这个解法正确):
    ===================================
    (1) 不漏：第 k 层把 digits[k] 的每个字母都试了，所以「每个数字选哪个字母」的
        所有组合都对应树里的一条路径，都会被记录。

    (2) 不重：同一层不同的 letter 生成的字符串在这一位上不同，所以每条路径记录的
        字符串都不一样。

    (3) 记录的都合法：只有 digit_index 走到末尾才记录，此时每个数字恰好选了一个字母，
        长度等于 len(digits)。
    
    TIME COMPLEXITY: O(n * 4^n)
    ===========================
    - n = len(digits)。每个数字最多 4 个字母（7 和 9），最多 4^n 个答案。
    - 每个答案 join 一次是 O(n) → O(n * 4^n)。
    - 这是下界：光输出所有答案就要这么多。
    
    SPACE COMPLEXITY: O(n)
    ======================
    - 递归最深 n 层，current_letters 最长 n → O(n)。
    - 映射表是固定大小 O(1)；输出不计入。
    
    ==============================================================================
    """
    
    def letterCombinations(self, digits: str) -> List[str]:
        
        # Edge case: no digits → no combinations (must return [], not [""])
        if not digits:
            return []
        
        # Each digit maps to its letters on a phone keypad
        digit_to_letters = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
        }
        
        # result collects every complete letter string
        result = []
        
        # current_letters = letters chosen so far, one per digit (shared, mutated list)
        current_letters = []
        
        def build_combinations(digit_index):
            # This helper finds every letter string that starts with current_letters
            # and picks one letter for each digit in digits[digit_index:],
            # and adds them to result.
            # e.g. digits="34", current_letters=["d"], digit_index=1
            #      → digit "4" maps to "ghi" → adds "dg", "dh", "di"
            
            # Base case: every digit has a letter → current_letters is one answer.
            # "".join makes a new string = a snapshot.
            if digit_index == len(digits):
                result.append("".join(current_letters))
                return
            
            # Try every letter that digits[digit_index] can stand for
            for letter in digit_to_letters[digits[digit_index]]:
                
                # CHOOSE: use this letter for the current digit
                current_letters.append(letter)
                
                # EXPLORE: pick letters for the remaining digits
                build_combinations(digit_index + 1)
                
                # UN-CHOOSE (backtrack): remove it so the next letter starts
                # from the same current_letters
                current_letters.pop()
        
        # Start from the first digit with nothing chosen
        build_combinations(0)
        return result


# ==============================================================================
# DETAILED WALKTHROUGH
# ==============================================================================
"""
Example: digits = "34"
         digits[0] = "3" → "def"
         digits[1] = "4" → "ghi"
Expected output: ["dg","dh","di","eg","eh","ei","fg","fh","fi"]

DECISION TREE:

build_combinations(digit_index=0)  current_letters=[]       数字 "3" → "def"
├─ letter="d" → current_letters=["d"]
│   build_combinations(digit_index=1)                        数字 "4" → "ghi"
│   ├─ letter="g" → ["d","g"] → build_combinations(2) ★ "dg"
│   ├─ letter="h" → ["d","h"] → build_combinations(2) ★ "dh"
│   └─ letter="i" → ["d","i"] → build_combinations(2) ★ "di"
├─ letter="e" → current_letters=["e"]
│   build_combinations(digit_index=1)
│   ├─ letter="g" → ["e","g"] → build_combinations(2) ★ "eg"
│   ├─ letter="h" → ["e","h"] → build_combinations(2) ★ "eh"
│   └─ letter="i" → ["e","i"] → build_combinations(2) ★ "ei"
└─ letter="f" → current_letters=["f"]
    build_combinations(digit_index=1)
    ├─ letter="g" → ["f","g"] → build_combinations(2) ★ "fg"
    ├─ letter="h" → ["f","h"] → build_combinations(2) ★ "fh"
    └─ letter="i" → ["f","i"] → build_combinations(2) ★ "fi"

第一层 3 个分支 × 第二层 3 个分支 = 9 个 ★。

═══════════════════════════════════════════════════════════════════
STEP-BY-STEP TRACE (FULL — ⏸ = 暂停等子调用，▶ = 恢复，★ = 记录):

build_combinations(digit_index=0)    current_letters=[]
  0 ≠ len(digits)=2，不是 base case
  digits[0]="3" → for letter in "def":
    letter="d": append → current_letters=["d"]
        ⏸ 调用 build_combinations(1)
        build_combinations(digit_index=1)    current_letters=["d"]
          1 ≠ 2，不是 base case
          digits[1]="4" → for letter in "ghi":
            letter="g": append → current_letters=["d","g"]
                ⏸ 调用 build_combinations(2)
                build_combinations(digit_index=2): 2 == len(digits)
                    ★ 记录 "dg"    result=["dg"]
                    return
                ▶ pop → current_letters=["d"]
            letter="h": append → current_letters=["d","h"]
                ⏸ 调用 build_combinations(2)
                build_combinations(digit_index=2): ★ 记录 "dh"
                    result=["dg","dh"]
                    return
                ▶ pop → current_letters=["d"]
            letter="i": append → current_letters=["d","i"]
                ⏸ 调用 build_combinations(2)
                build_combinations(digit_index=2): ★ 记录 "di"
                    result=["dg","dh","di"]
                    return
                ▶ pop → current_letters=["d"]
          for 结束 → return
        ▶ pop → current_letters=[]
    letter="e": append → current_letters=["e"]
        ⏸ 调用 build_combinations(1)
        build_combinations(digit_index=1)    current_letters=["e"]
          for letter in "ghi":
            letter="g": append → current_letters=["e","g"]
                build_combinations(2): ★ 记录 "eg"
                    result=["dg","dh","di","eg"]
                ▶ pop → current_letters=["e"]
            letter="h": append → current_letters=["e","h"]
                build_combinations(2): ★ 记录 "eh"
                    result=["dg","dh","di","eg","eh"]
                ▶ pop → current_letters=["e"]
            letter="i": append → current_letters=["e","i"]
                build_combinations(2): ★ 记录 "ei"
                    result=["dg","dh","di","eg","eh","ei"]
                ▶ pop → current_letters=["e"]
          for 结束 → return
        ▶ pop → current_letters=[]
    letter="f": append → current_letters=["f"]
        ⏸ 调用 build_combinations(1)
        build_combinations(digit_index=1)    current_letters=["f"]
          for letter in "ghi":
            letter="g": append → current_letters=["f","g"]
                build_combinations(2): ★ 记录 "fg"
                    result=["dg","dh","di","eg","eh","ei","fg"]
                ▶ pop → current_letters=["f"]
            letter="h": append → current_letters=["f","h"]
                build_combinations(2): ★ 记录 "fh"
                    result=["dg","dh","di","eg","eh","ei","fg","fh"]
                ▶ pop → current_letters=["f"]
            letter="i": append → current_letters=["f","i"]
                build_combinations(2): ★ 记录 "fi"
                    result=["dg","dh","di","eg","eh","ei","fg","fh","fi"]
                ▶ pop → current_letters=["f"]
          for 结束 → return
        ▶ pop → current_letters=[]
  for 结束 → return，全部结束

═══════════════════════════════════════════════════════════════════
FINAL: result = ["dg","dh","di","eg","eh","ei","fg","fh","fi"]

9 combinations. ✓（顺序和题目示例一样）

看懂 trace 的关键:
- build_combinations(digit_index=1) 被调用了 3 次，进门时 current_letters 分别是
  ["d"]、["e"]、["f"]。每次它做的事一样（给 "4" 选字母），只是前缀不同。
- 外层 letter="d" 在等内层跑 "g"/"h"/"i" 的时候，外层自己的 letter 一直是 "d"，
  内层的 letter 不会覆盖它。

KEY POINTS for interview:
- 定性：backtracking，一个数字一层，每层从这个数字的字母里选一个。
- 用递归代替「len(digits) 层嵌套 for 循环」（和 Subsets 同一个动机）。
- base case：digit_index == len(digits) → 记录 "".join(current_letters)。
- 必须特判 digits 为空，否则会返回 [""] 而不是 []。
- 没有去重、没有剪枝、没有死路。
- 复杂度 O(n·4^n) 时间，O(n) 空间。
"""