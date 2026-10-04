# class Solution:
#     def solveNQueens(self, n: int) -> List[List[str]]:
        





class Solution:
    """
    PROBLEM: N-Queens (LeetCode 51 - Hard)
    =======================================
    
    PROBLEM STATEMENT:
    Place n queens on an n x n chessboard so that no two queens attack each other
    (a queen attacks along its row, column, and both diagonals).
    Return all distinct solutions. Each solution is a board as a list of strings,
    'Q' = queen, '.' = empty. Return in any order.
    
    EXAMPLES:
    Example 1: n = 4
        Output: [[".Q..","...Q","Q...","..Q."],
                 ["..Q.","Q...","...Q",".Q.."]]
    
        Solution 1:       Solution 2:
        . Q . .           . . Q .
        . . . Q           Q . . .
        Q . . .           . . . Q
        . . Q .           . Q . .
    
    Example 2: n = 1
        Output: [["Q"]]
    
    ==============================================================================
    SOLUTION APPROACH: Backtracking (one row per level + sets for cols/diagonals)
    ==============================================================================
    
    INTUITION (核心思路):
    ====================
    
    第一步观察：每一行恰好放一个皇后
    -------------------------------
    n 个皇后放在 n 行里，同一行不能有两个（会互相攻击）→ 每行正好一个。
    所以不用在整个棋盘上乱试，只要一行一行地决定「这一行的皇后放在哪一列」。
    这就和 Letter Combinations 一样：一行是一层，这一层的 for 循环试所有列。
    「同行冲突」这个条件就自动满足了，不用检查。

    剩下要检查的：列、两条对角线
    ---------------------------
    在 (row, col) 放皇后之前，要确认：
        - 这一列上面没有皇后
        - 这个格子所在的 "/" 对角线上没有皇后
        - 这个格子所在的 "\" 对角线上没有皇后
    每次都去扫棋盘太慢，所以用三个 set 记录「已经被占的列 / 对角线」，查一次 O(1)。

    怎么给对角线编号（这题最关键的技巧）
    ----------------------------------
    "/" 方向的对角线上，row + col 都相同：

             col 0  1  2  3
        row 0    0  1  2  3
        row 1    1  2  3  4
        row 2    2  3  4  5
        row 3    3  4  5  6
        比如 (0,2)、(1,1)、(2,0) 的 row+col 都是 2，它们在同一条 "/" 上。

    "\" 方向的对角线上，row - col 都相同：

             col  0   1   2   3
        row 0     0  -1  -2  -3
        row 1     1   0  -1  -2
        row 2     2   1   0  -1
        row 3     3   2   1   0
        比如 (0,0)、(1,1)、(2,2) 的 row-col 都是 0，它们在同一条 "\" 上。

    所以：
        occupied_cols                 存已经有皇后的 col
        occupied_slash_diagonals      存已经有皇后的 row + col   （"/" 对角线）
        occupied_backslash_diagonals  存已经有皇后的 row - col   （"\" 对角线）
    放皇后前，三个 set 都查一下，有一个命中就不能放。

    和 Permutations 的关系
    ---------------------
    如果只看「每行一个、每列一个」，这就是在给每一行分配一个不同的列，也就是列号的
    一个排列（occupied_cols 就是 Permutations 里的 used[]）。N-Queens 只是多了
    对角线的限制，把很多排列挡掉了。所以答案最多 n! 种。

    choose / un-choose 要改四样东西
    ------------------------------
    放一个皇后（choose）：
        board[row][col] = "Q"
        occupied_cols.add(col)
        occupied_slash_diagonals.add(row + col)
        occupied_backslash_diagonals.add(row - col)
    撤销（un-choose）：四样全部改回去。少撤一个，后面的格子会被误判成「被攻击」。
    行不用记录：递归调用 place_queens(row + 1) 本身就保证了下一层处理下一行。

    这题有死路
    ---------
    某一行所有列都被攻击时，for 循环一个都放不进去，函数什么都不记录就 return。
    上一行收到后撤销自己的皇后，换下一列再试。这就是 backtracking 的「走不通就退回去」。
    （Generate Parentheses / Palindrome Partitioning 没有死路，这题有。）

    base case
    ---------
    row == n：0 到 n-1 每一行都放好了皇后 → 记录这个棋盘。
    记录时用 ["".join(board_row) for board_row in board]：把每一行的字符列表拼成
    新字符串，相当于拍快照（作用同 .copy()），之后 board 再改也不影响已记录的答案。

    为什么 board 用字符列表，不用字符串
    ---------------------------------
    Python 字符串不能改，board[row][col] = "Q" 对字符串会报错。所以 board 每一行
    是一个字符列表，记录答案时再 join 成字符串。

    HELPER 在做什么 (place_queens):
    ------------------------------
        place_queens(row)

    心里读成：
        第 0 到 row-1 行已经各放好一个皇后（记在 board 和三个 set 里）。
        在第 row 到 n-1 行各放一个皇后，而且不和已有的皇后互相攻击，
        找出所有这样的放法，每找到一种就把整个棋盘加入 result。

    例：n = 4，(0,1) 已经有皇后，row = 1
        → 找到以 (0,1) 开头的唯一一种放法：[".Q..","...Q","Q...","..Q."]

    核心思路 (Chinese):
    ------------------
    一行一行放。这一行试每一列：列和两条对角线都没被占才放，放了就把四样东西标记上，
    递归去放下一行，回来后四样全部撤销，再试下一列。放满 n 行就记录棋盘。
    某一行哪都放不了就直接返回，让上一行换位置。
    
    ALGORITHM:
    ==========
    1. result = []；board = n x n 的 "."；三个空 set
    2. place_queens(row):
       a. Base case: row == n → 记录每行 join 后的棋盘，return
       b. for col in range(n):
          - 若 col 或 row+col 或 row-col 已被占 → continue
          - 放:   board[row][col]="Q"，三个 set 加入 col / row+col / row-col
          - 递归: place_queens(row + 1)
          - 撤销: board[row][col]="."，三个 set 删除对应的值
    3. 调用 place_queens(0)，返回 result
    
    WHY THIS WORKS (为什么这个解法正确):
    ===================================
    (1) 不会同行冲突：每层只放一个皇后，一层就是一行。

    (2) 不会同列、同对角线冲突：放之前查三个 set，被占就跳过。同一条 "/" 上
        row+col 相同，同一条 "\" 上 row-col 相同，所以查 set 等于查整条线。

    (3) 不漏：每一行都试了所有列。任何一个合法解，它在每一行选的列都不会被挡
        （因为它本身没有冲突），所以 DFS 一定会沿着它走到 row == n。

    (4) 不重：两条不同的路径至少有一行选的列不同 → 记录的棋盘不同。

    (5) 撤销正确：每次递归回来都把四样东西改回去，所以 for 循环的下一列、
        以及上一行接下来的尝试，看到的都是正确的「已占」状态。
    
    TIME COMPLEXITY: O(n!)
    ======================
    - 第 0 行最多 n 种选择，第 1 行至少少一列（列被占）→ 最多 n-1 种，……
      → 最多 n * (n-1) * ... * 1 = n! 条路径，对角线限制会剪掉其中很多。
    - 每找到一个解要 O(n^2) 拼出棋盘，但解的个数远小于 n!，一般就说 O(n!)。
    
    SPACE COMPLEXITY: O(n^2)
    ========================
    - board 是 n x n → O(n^2)。
    - 三个 set 各最多 n 个元素、递归最深 n 层 → O(n)。
    - （输出不计入。）
    
    ==============================================================================
    """
    
    def solveNQueens(self, n: int) -> List[List[str]]:
        
        # result collects every finished board
        result = []
        
        # board[row][col] is "Q" or "."; rows are lists so cells can be changed
        board = [["."] * n for _ in range(n)]
        
        # Columns that already have a queen
        occupied_cols = set()
        # "/" diagonals that already have a queen (every cell on one has the same row + col)
        occupied_slash_diagonals = set()
        # "\" diagonals that already have a queen (every cell on one has the same row - col)
        occupied_backslash_diagonals = set()
        
        def place_queens(row):
            # This helper finds every way to put one queen in each of rows row..n-1
            # without attacking the queens already placed in rows 0..row-1,
            # and adds each finished board to result.
            # e.g. n=4, a queen already at (0,1), row=1
            #      → finds the one board that starts with (0,1):
            #        [".Q..","...Q","Q...","..Q."]
            
            # Base case: every row has a queen → record a snapshot of the board.
            # "".join turns each row's list into a new string.
            if row == n:
                result.append(["".join(board_row) for board_row in board])
                return
            
            # Try putting this row's queen in each column
            for col in range(n):
                
                # Skip if this column or either diagonal already has a queen
                if (col in occupied_cols
                        or (row + col) in occupied_slash_diagonals
                        or (row - col) in occupied_backslash_diagonals):
                    continue
                
                # CHOOSE: place the queen and mark its column and both diagonals
                board[row][col] = "Q"
                occupied_cols.add(col)
                occupied_slash_diagonals.add(row + col)
                occupied_backslash_diagonals.add(row - col)
                
                # EXPLORE: place queens in the remaining rows
                place_queens(row + 1)
                
                # UN-CHOOSE (backtrack): undo all four changes so the next column
                # (and the rows above) see the correct occupied state
                board[row][col] = "."
                occupied_cols.remove(col)
                occupied_slash_diagonals.remove(row + col)
                occupied_backslash_diagonals.remove(row - col)
        
        # Start from the top row with an empty board
        place_queens(0)
        return result


# ==============================================================================
# DETAILED WALKTHROUGH
# ==============================================================================
"""
Example: n = 4

trace 里三个 set 简写：
    cols      = occupied_cols
    slash     = occupied_slash_diagonals      (存 row + col)
    backslash = occupied_backslash_diagonals  (存 row - col)
(r,c) 表示第 r 行第 c 列的皇后。

DECISION TREE（只画通过检查、真的放下去的列）:

place_queens(0)
├─ col=0 → 放 (0,0)
│   place_queens(1)
│   ├─ col=2 → 放 (1,2)
│   │   place_queens(2): 4 列都被攻击 → 死路
│   └─ col=3 → 放 (1,3)
│       place_queens(2)
│       └─ col=1 → 放 (2,1)
│           place_queens(3): 4 列都被攻击 → 死路
├─ col=1 → 放 (0,1)
│   place_queens(1)
│   └─ col=3 → 放 (1,3)
│       place_queens(2)
│       └─ col=0 → 放 (2,0)
│           place_queens(3)
│           └─ col=2 → 放 (3,2)
│               place_queens(4) ★ [".Q..","...Q","Q...","..Q."]
├─ col=2 → 放 (0,2)
│   place_queens(1)
│   └─ col=0 → 放 (1,0)
│       place_queens(2)
│       └─ col=3 → 放 (2,3)
│           place_queens(3)
│           └─ col=1 → 放 (3,1)
│               place_queens(4) ★ ["..Q.","Q...","...Q",".Q.."]
└─ col=3 → 放 (0,3)
    place_queens(1)
    ├─ col=0 → 放 (1,0)
    │   place_queens(2)
    │   └─ col=2 → 放 (2,2)
    │       place_queens(3): 4 列都被攻击 → 死路
    └─ col=1 → 放 (1,1)
        place_queens(2): 4 列都被攻击 → 死路

═══════════════════════════════════════════════════════════════════
STEP-BY-STEP TRACE (FULL — ⏸ = 暂停等子调用，▶ = 恢复，★ = 记录，✗ = 被攻击跳过)

place_queens(row=0)    已有皇后: 无
  for col in range(4):
  col=0: 没被占 → 放 (0,0)
         cols={0}  slash={0}  backslash={0}
      ⏸ 调用 place_queens(1)
      place_queens(row=1)    已有皇后: (0,0)
        col=0: 0 in cols ✗              (和 (0,0) 同列)
        col=1: 1-1=0 in backslash ✗     (和 (0,0) 同一条 "\")
        col=2: col 2、2+1=3、1-2=-1 都没被占 → 放 (1,2)
               cols={0,2}  slash={0,3}  backslash={0,-1}
            ⏸ 调用 place_queens(2)
            place_queens(row=2)    已有皇后: (0,0),(1,2)
              col=0: 0 in cols ✗          (和 (0,0) 同列)
              col=1: 2+1=3 in slash ✗     (和 (1,2) 同一条 "/")
              col=2: 2 in cols ✗          (和 (1,2) 同列)
              col=3: 2-3=-1 in backslash ✗ (和 (1,2) 同一条 "\")
              死路：for 结束，什么都没记录 → return
            ▶ 撤销 (1,2): cols={0}  slash={0}  backslash={0}
        col=3: col 3、1+3=4、1-3=-2 都没被占 → 放 (1,3)
               cols={0,3}  slash={0,4}  backslash={0,-2}
            ⏸ 调用 place_queens(2)
            place_queens(row=2)    已有皇后: (0,0),(1,3)
              col=0: 0 in cols ✗          (和 (0,0) 同列)
              col=1: col 1、2+1=3、2-1=1 都没被占 → 放 (2,1)
                     cols={0,3,1}  slash={0,4,3}  backslash={0,-2,1}
                  ⏸ 调用 place_queens(3)
                  place_queens(row=3)    已有皇后: (0,0),(1,3),(2,1)
                    col=0: 0 in cols ✗          (和 (0,0) 同列)
                    col=1: 1 in cols ✗          (和 (2,1) 同列)
                    col=2: 3-2=1 in backslash ✗ (和 (2,1) 同一条 "\")
                    col=3: 3 in cols ✗          (和 (1,3) 同列)
                    死路 → return
                  ▶ 撤销 (2,1): cols={0,3}  slash={0,4}  backslash={0,-2}
              col=2: 2+2=4 in slash ✗     (和 (1,3) 同一条 "/")
              col=3: 3 in cols ✗          (和 (1,3) 同列)
              for 结束 → return
            ▶ 撤销 (1,3): cols={0}  slash={0}  backslash={0}
        for 结束 → return
      ▶ 撤销 (0,0): cols={}  slash={}  backslash={}

  col=1: 没被占 → 放 (0,1)
         cols={1}  slash={1}  backslash={-1}
      ⏸ 调用 place_queens(1)
      place_queens(row=1)    已有皇后: (0,1)
        col=0: 1+0=1 in slash ✗         (和 (0,1) 同一条 "/")
        col=1: 1 in cols ✗              (和 (0,1) 同列)
        col=2: 1-2=-1 in backslash ✗    (和 (0,1) 同一条 "\")
        col=3: col 3、1+3=4、1-3=-2 都没被占 → 放 (1,3)
               cols={1,3}  slash={1,4}  backslash={-1,-2}
            ⏸ 调用 place_queens(2)
            place_queens(row=2)    已有皇后: (0,1),(1,3)
              col=0: col 0、2+0=2、2-0=2 都没被占 → 放 (2,0)
                     cols={1,3,0}  slash={1,4,2}  backslash={-1,-2,2}
                  ⏸ 调用 place_queens(3)
                  place_queens(row=3)    已有皇后: (0,1),(1,3),(2,0)
                    col=0: 0 in cols ✗          (和 (2,0) 同列)
                    col=1: 1 in cols ✗          (和 (0,1) 同列)
                    col=2: col 2、3+2=5、3-2=1 都没被占 → 放 (3,2)
                           cols={1,3,0,2}  slash={1,4,2,5}  backslash={-1,-2,2,1}
                        ⏸ 调用 place_queens(4)
                        place_queens(row=4): row == n
                            ★ 记录 [".Q..","...Q","Q...","..Q."]
                            result = [[".Q..","...Q","Q...","..Q."]]
                            return
                        ▶ 撤销 (3,2): cols={1,3,0}  slash={1,4,2}  backslash={-1,-2,2}
                    col=3: 3 in cols ✗          (和 (1,3) 同列)
                    for 结束 → return
                  ▶ 撤销 (2,0): cols={1,3}  slash={1,4}  backslash={-1,-2}
              col=1: 1 in cols ✗          (和 (0,1) 同列)
              col=2: 2+2=4 in slash ✗     (和 (1,3) 同一条 "/")
              col=3: 3 in cols ✗          (和 (1,3) 同列)
              for 结束 → return
            ▶ 撤销 (1,3): cols={1}  slash={1}  backslash={-1}
        for 结束 → return
      ▶ 撤销 (0,1): cols={}  slash={}  backslash={}

  col=2: 没被占 → 放 (0,2)
         cols={2}  slash={2}  backslash={-2}
      ⏸ 调用 place_queens(1)
      place_queens(row=1)    已有皇后: (0,2)
        col=0: col 0、1+0=1、1-0=1 都没被占 → 放 (1,0)
               cols={2,0}  slash={2,1}  backslash={-2,1}
            ⏸ 调用 place_queens(2)
            place_queens(row=2)    已有皇后: (0,2),(1,0)
              col=0: 0 in cols ✗          (和 (1,0) 同列)
              col=1: 2-1=1 in backslash ✗ (和 (1,0) 同一条 "\")
              col=2: 2 in cols ✗          (和 (0,2) 同列)
              col=3: col 3、2+3=5、2-3=-1 都没被占 → 放 (2,3)
                     cols={2,0,3}  slash={2,1,5}  backslash={-2,1,-1}
                  ⏸ 调用 place_queens(3)
                  place_queens(row=3)    已有皇后: (0,2),(1,0),(2,3)
                    col=0: 0 in cols ✗          (和 (1,0) 同列)
                    col=1: col 1、3+1=4、3-1=2 都没被占 → 放 (3,1)
                           cols={2,0,3,1}  slash={2,1,5,4}  backslash={-2,1,-1,2}
                        ⏸ 调用 place_queens(4)
                        place_queens(row=4): row == n
                            ★ 记录 ["..Q.","Q...","...Q",".Q.."]
                            result = [[".Q..","...Q","Q...","..Q."],
                                      ["..Q.","Q...","...Q",".Q.."]]
                            return
                        ▶ 撤销 (3,1): cols={2,0,3}  slash={2,1,5}  backslash={-2,1,-1}
                    col=2: 2 in cols ✗          (和 (0,2) 同列)
                    col=3: 3 in cols ✗          (和 (2,3) 同列)
                    for 结束 → return
                  ▶ 撤销 (2,3): cols={2,0}  slash={2,1}  backslash={-2,1}
              for 结束 → return
            ▶ 撤销 (1,0): cols={2}  slash={2}  backslash={-2}
        col=1: 1+1=2 in slash ✗         (和 (0,2) 同一条 "/")
        col=2: 2 in cols ✗              (和 (0,2) 同列)
        col=3: 1-3=-2 in backslash ✗    (和 (0,2) 同一条 "\")
        for 结束 → return
      ▶ 撤销 (0,2): cols={}  slash={}  backslash={}

  col=3: 没被占 → 放 (0,3)
         cols={3}  slash={3}  backslash={-3}
      ⏸ 调用 place_queens(1)
      place_queens(row=1)    已有皇后: (0,3)
        col=0: col 0、1+0=1、1-0=1 都没被占 → 放 (1,0)
               cols={3,0}  slash={3,1}  backslash={-3,1}
            ⏸ 调用 place_queens(2)
            place_queens(row=2)    已有皇后: (0,3),(1,0)
              col=0: 0 in cols ✗          (和 (1,0) 同列)
              col=1: 2+1=3 in slash ✗     (和 (0,3) 同一条 "/")
              col=2: col 2、2+2=4、2-2=0 都没被占 → 放 (2,2)
                     cols={3,0,2}  slash={3,1,4}  backslash={-3,1,0}
                  ⏸ 调用 place_queens(3)
                  place_queens(row=3)    已有皇后: (0,3),(1,0),(2,2)
                    col=0: 0 in cols ✗          (和 (1,0) 同列)
                    col=1: 3+1=4 in slash ✗     (和 (2,2) 同一条 "/")
                    col=2: 2 in cols ✗          (和 (2,2) 同列)
                    col=3: 3 in cols ✗          (和 (0,3) 同列)
                    死路 → return
                  ▶ 撤销 (2,2): cols={3,0}  slash={3,1}  backslash={-3,1}
              col=3: 3 in cols ✗          (和 (0,3) 同列)
              for 结束 → return
            ▶ 撤销 (1,0): cols={3}  slash={3}  backslash={-3}
        col=1: col 1、1+1=2、1-1=0 都没被占 → 放 (1,1)
               cols={3,1}  slash={3,2}  backslash={-3,0}
            ⏸ 调用 place_queens(2)
            place_queens(row=2)    已有皇后: (0,3),(1,1)
              col=0: 2+0=2 in slash ✗     (和 (1,1) 同一条 "/")
              col=1: 1 in cols ✗          (和 (1,1) 同列)
              col=2: 2-2=0 in backslash ✗ (和 (1,1) 同一条 "\")
              col=3: 3 in cols ✗          (和 (0,3) 同列)
              死路 → return
            ▶ 撤销 (1,1): cols={3}  slash={3}  backslash={-3}
        col=2: 1+2=3 in slash ✗         (和 (0,3) 同一条 "/")
        col=3: 3 in cols ✗              (和 (0,3) 同列)
        for 结束 → return
      ▶ 撤销 (0,3): cols={}  slash={}  backslash={}

  for 结束 → return，全部结束

═══════════════════════════════════════════════════════════════════
FINAL: result = [[".Q..","...Q","Q...","..Q."],
                 ["..Q.","Q...","...Q",".Q.."]]

2 solutions. ✓

看懂 trace 的关键:
- 每个 ✗ 后面都写了是被哪个皇后、哪条线挡住的，对照上面 row+col / row-col 的表格看。
- 「死路」出现了 4 次：那一行 4 列全是 ✗，函数什么都不记录就 return，
  上一行撤销自己的皇后、换下一列。这就是 backtracking 退回去的地方。
- 每次「撤销」之后三个 set 都恢复到放这个皇后之前的样子
  （对比放之前那一行打印的 set）。

KEY POINTS for interview:
- 定性：backtracking，一行一层，每层试所有列（同行冲突自动避免）。
- 三个 set：列 col、"/" 对角线 row+col、"\" 对角线 row-col，O(1) 判断是否被攻击。
- choose / un-choose 各改四样：board + 三个 set，必须成对。
- 有死路：某行无处可放 → 不记录直接 return → 上一行换列。
- base case：row == n → 记录 ["".join(r) for r in board]（快照）。
- 复杂度 O(n!) 时间（本质是列的排列 + 对角线剪枝），O(n^2) 空间（棋盘）。
"""