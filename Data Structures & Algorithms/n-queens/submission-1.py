# 这题 先看上一个submission claude的怎么给对角线编号的部分大概了解整个题目的技巧
# 然后去看GPT的回答（写的真非常好）


"""
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

"""

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        board = [["."] * n for _ in range(n)]

        occupied_cols = set()
        occupied_slash_diagonals = set()
        occupied_backslash_diagonals = set()


        def place_queens(row):
            # 一句话版本：前面的第 0 到第 row - 1 行已经放好了皇后。找出所有给第 row 行到最后一行各放一个皇后的合法方案，并把完整棋盘加入 result
            # 或者理解成 从第 row 行开始往下放皇后,一直放到最后一行,把所有能放成功的棋盘都记下来 
            # This helper finds every way to put one queen in each of rows row...n-1 without attacking the queens already placed in rows 0..row-1, and adds each finished board to result
            # e.g. n = 4, a queen already at (0,1), row = 1
            # 如果你手动假设第 0 行已经放了皇后在第 1 列(也就是 (0,1)),然后你调用 place_queens(1)——注意参数是 1,表示"从第 1 行开始继续放"——那么这个函数会帮你找完第 1、2、3 行该怎么放,最终你会得到唯一一个解:[".Q..","...Q","Q...","..Q."]"。

            # base case: every row has a queen -> recoard a snapshot of the board
            # "".join turns each row's list into a new string
            if row == n: 
                result.append(["".join(board_row) for board_row in board])
                return 
            
            # Try putting this row's queen in each colum，固定当前行，逐个检查这一行的所有列，尝试把皇后放在允许的位置，因为题目要求所有合法的棋盘，所以每个候选位置都要检查。
            for col in range(n):

                if (col in occupied_cols
                        or (row + col) in occupied_slash_diagonals
                        or (row - col) in occupied_backslash_diagonals):
                    continue

                board[row][col] = "Q"
                occupied_cols.add(col)
                occupied_slash_diagonals.add(row + col)
                occupied_backslash_diagonals.add(row-col)

                place_queens(row + 1)
                board[row][col] = "."
                occupied_cols.remove(col)
                occupied_slash_diagonals.remove(row+col)
                occupied_backslash_diagonals.remove(row-col)

        
        place_queens(0)
        return result
   


# result.append(["".join(board_row) for board_row in board])
"""
4 steps:
Step 1 — board 是什么
一个大 list，里面装着 4 个小 list，每个小 list = 棋盘的一行。
['.', 'Q', '.', '.']
['.', '.', '.', 'Q']
['Q', '.', '.', '.']
['.', '.', 'Q', '.']

Step 2 — for board_row in board
每次循环，board_row 就是其中一行，比如第一次是 ['.', 'Q', '.', '.']。
Step 3 — "".join(board_row)
把那一行的字符直接粘在一起，变成一个字符串：
['.', 'Q', '.', '.']  →  ".Q.."
['.', '.', '.', 'Q']  →  "...Q"
['Q', '.', '.', '.']  →  "Q..."
['.', '.', 'Q', '.']  →  "..Q."

Step 4 — 整句放进 list comprehension
对每一行都做 join，收集成一个新 list = 这个棋盘的快照：
['.Q..', '...Q', 'Q...', '..Q.']

这就是 result.append(...) 存进去的东西。
"""


# GPT's answer:


"""
这份代码是正确的。**这一题每一步要决定的是：当前这一行的皇后，放在哪一列？**

我们继续按你认可的顺序：先推导逐行放皇后的任务，写出递归主流程；到了“这个位置能不能放”的检查，再引出记录列和对角线的三个集合。

**一、拿到题目，怎么想到这个解法？**

**1. 先弄清楚：皇后之间不能有什么冲突？**

两个皇后不能处在：

- 同一行。
- 同一列。
- 同一条斜对角线上。

题目要求在 `n × n` 的棋盘上，放下 `n` 个皇后，返回所有合法棋盘。

例如 `n = 4`，一种合法答案是：

```python
[
    ".Q..",
    "...Q",
    "Q...",
    "..Q."
]
```

对应：

| 行 | 皇后所在列 |
|---:|---:|
| 0 | 1 |
| 1 | 3 |
| 2 | 0 |
| 3 | 2 |

**2. 为什么可以逐行放皇后？**

因为：

- 棋盘有 `n` 行。
- 需要放 `n` 个皇后。
- 每一行最多放一个皇后，否则同一行的皇后会互相攻击。

所以任何合法答案都必须：

> **每一行恰好放一个皇后。**

于是可以把任务拆成：

```text
第 0 行的皇后放在哪一列？
第 1 行的皇后放在哪一列？
……
第 n-1 行的皇后放在哪一列？
```

每次只给当前这一行放一个皇后，再处理下一行。

这样，“不能同一行”的限制就由构建方式保证了，不需要额外记录哪些行已经使用。

**3. 为什么会想到递归？**

假设第 0 行已经选择了第 1 列：

```python
".Q.."
```

剩下的任务是：

> 在不攻击这个皇后的前提下，给第 1 行到最后一行各放一个皇后。

如果第 1 行又选择了第 3 列：

```python
[
    ".Q..",
    "...Q",
    "....",
    "...."
]
```

剩下的任务仍然是：

> 在不攻击已有皇后的前提下，给后面的每一行各放一个皇后。

这就是递归：

> **给当前行放一个皇后以后，剩下的仍然是“给剩余行放皇后”的任务，只是需要处理的行少了一行。**

**4. 再问：完成剩下的任务，需要记住什么？**

先从最基本的状态开始：

| 必须知道的事 | 用什么表示 | 为什么 |
|---|---|---|
| 已经放好的皇后在哪里 | `board` | 判断当前选择，也用于最后生成答案 |
| 下一步处理哪一行 | `row` | 当前调用只给这一行放皇后 |
| 已经找到哪些完整棋盘 | `result` | 题目要求所有答案 |

一开始棋盘是空的：

```python
board = [["."] * n for _ in range(n)]
```

例如 `n = 4`：

```python
[
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."]
]
```

每行用列表表示，是为了能够修改单个格子：

```python
board[row][col] = "Q"
```

搜索结束后，再把这些行转换成题目要求的字符串。

**5. 现在定义递归 helper 的任务**

```python
def place_queens(row):
```

它的一句话定义是：

> 前面的第 `0` 到第 `row - 1` 行已经放好了皇后。找出所有给第 `row` 行到最后一行各放一个皇后的合法方案，并把完整棋盘加入 `result`。

例如：

```python
n = 4
row = 1
```

且第 0 行的皇后已经放在 `(0, 1)`。

那么这次调用负责：

> 保留第 0 行的这个选择，找出后面三行的所有合法放法。

---

**二、实际写代码的顺序**

**Step 1：先写完整外层骨架**

我要收集所有答案，所以创建 `result`。

我要实际放置皇后，所以创建一个能够修改的棋盘。

helper 暂时留空：

```python
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        board = [["."] * n for _ in range(n)]

        def place_queens(row):
            pass

        place_queens(0)
        return result
```

第一次调用：

```python
place_queens(0)
```

表示：

```text
目前棋盘为空。
从第 0 行开始放皇后。
```

此时还没有引入三个集合。先把逐行放皇后的主流程搭起来。

**Step 2：先写 base case**

每次进入 helper，先问：

> 所有行是不是都已经放好皇后了？

如果：

```python
row == n
```

说明第 `0` 到第 `n - 1` 行都已经完成。

这时保存棋盘，然后返回：

```python
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        board = [["."] * n for _ in range(n)]

        def place_queens(row):
            if row == n:
                result.append(
                    ["".join(board_row) for board_row in board]
                )
                return

            pass

        place_queens(0)
        return result
```

**这句保存操作具体做了什么？**

```python
["".join(board_row) for board_row in board]
```

它把：

```python
[
    [".", "Q", ".", "."],
    [".", ".", ".", "Q"],
    ["Q", ".", ".", "."],
    [".", ".", "Q", "."]
]
```

转换成：

```python
[
    ".Q..",
    "...Q",
    "Q...",
    "..Q."
]
```

外层列表是新创建的，每一行也被拼成了新的字符串。

因此，后面修改搜索用的 `board`，不会改变已经保存的答案。

**Step 3：为了找全答案，逐个尝试“当前行放在哪一列”**

假设：

```python
n = 4
row = 1
```

第 0 行已经放好了皇后，现在这次调用要决定：

> 第 1 行的皇后放在哪一列？

有四个候选位置：

| `col` | 候选格子 |
|---:|---|
| 0 | `(1, 0)` |
| 1 | `(1, 1)` |
| 2 | `(1, 2)` |
| 3 | `(1, 3)` |

题目要求所有合法棋盘，所以每个候选位置都需要检查。

这一层需要完成的工作是：

> **固定当前行 `row`，逐个检查这一行的所有列，尝试把皇后放在允许的位置。**

因此写：

```python
for col in range(n):
    pass
```

注意：

- `row` 决定这次调用处理哪一行。
- `col` 决定当前这轮循环尝试这一行的哪个位置。

把循环骨架写进去：

```python
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        board = [["."] * n for _ in range(n)]

        def place_queens(row):
            if row == n:
                result.append(
                    ["".join(board_row) for board_row in board]
                )
                return

            for col in range(n):
                pass

        place_queens(0)
        return result
```

每一行都需要检查全部列。

例如一种合法答案中，前两行选了列 `1`、`3`，第三行却需要选择列 `0`。不同的行没有要求皇后所在列递增。

**Step 4：先写“放皇后 → 处理下一行 → 撤销皇后”**

对于当前候选位置 `(row, col)`：

先放皇后：

```python
board[row][col] = "Q"
```

再处理下一行：

```python
place_queens(row + 1)
```

子调用返回后，撤销本层放的皇后：

```python
board[row][col] = "."
```

得到主流程草稿：

```python
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        board = [["."] * n for _ in range(n)]

        def place_queens(row):
            if row == n:
                result.append(
                    ["".join(board_row) for board_row in board]
                )
                return

            for col in range(n):
                board[row][col] = "Q"

                place_queens(row + 1)

                board[row][col] = "."

        place_queens(0)
        return result
```

**这是未完成的草稿：它保证每行一个皇后，但还没有排除同列或同对角线的冲突。**

这三步分别意味着：

**① 做选择**

```python
board[row][col] = "Q"
```

本层暂时决定：

> 当前行的皇后放在这一列。

**② 把后面的任务交给递归**

```python
place_queens(row + 1)
```

当前行已经放好了，子调用负责给剩下的行放皇后。

**③ 撤销本层选择，为下一列恢复状态**

```python
board[row][col] = "."
```

当前候选下面的搜索结束了，先拿走本层放的皇后，再尝试本行的其他列。

例如第 0 行先试第 0 列，接下来还要试第 1 列：

```python
"Q..." → "...." → ".Q.."
```

撤销操作保证这两次尝试分别从同一个空行出发。

**Step 5：现在回头问，这个位置在什么情况下不能放？**

到了这里，才需要补上：

> 在执行 `board[row][col] = "Q"` 之前，怎样判断这个候选位置会不会攻击已有皇后？

同一行已经由逐行构建保证了。

剩下需要检查：

1. 同一列是否已经有皇后。
2. `/` 对角线上是否已经有皇后。
3. `\` 对角线上是否已经有皇后。

可以用三个集合记录当前路径占用了哪些列和对角线，这样每次尝试位置时就能直接检查。

**① 怎样记录列？**

用：

```python
occupied_cols = set()
```

如果之前的某个皇后在第 1 列，就记录：

```python
occupied_cols = {1}
```

以后尝试当前行的第 1 列时：

```python
col in occupied_cols
```

成立，说明同列冲突。

**② 怎样用一个数表示 `/` 对角线？**

棋盘的行号向下增加，列号向右增加。

沿着 `/` 对角线向左下移动时：

```text
row 增加 1
col 减少 1
```

所以：

```python
row + col
```

保持不变。

例如：

| 格子坐标 | `row + col` |
|---|---:|
| `(0, 3)` | 3 |
| `(1, 2)` | 3 |
| `(2, 1)` | 3 |
| `(3, 0)` | 3 |

这些格子都在同一条 `/` 对角线上。

因此，可以用 `row + col` 作为这条对角线的编号：

```python
occupied_slash_diagonals = set()
```

尝试 `(row, col)` 时，检查：

```python
(row + col) in occupied_slash_diagonals
```

**③ 怎样用一个数表示 `\` 对角线？**

沿着 `\` 对角线向右下移动时：

```text
row 增加 1
col 增加 1
```

所以：

```python
row - col
```

保持不变。

例如：

| 格子坐标 | `row - col` |
|---|---:|
| `(0, 1)` | -1 |
| `(1, 2)` | -1 |
| `(2, 3)` | -1 |

这些格子在同一条 `\` 对角线上。

因此，创建：

```python
occupied_backslash_diagonals = set()
```

检查：

```python
(row - col) in occupied_backslash_diagonals
```

编号是负数也没有问题，它只是集合中的整数标记。

**把检查放在具体状态里看一次**

假设已经在 `(0, 1)` 放了皇后：

```python
occupied_cols = {1}
occupied_slash_diagonals = {1}
occupied_backslash_diagonals = {-1}
```

现在处理：

```python
row = 1
```

四个候选位置是：

| 候选位置 | 列检查 | `/` 编号 | `\` 编号 | 能否放 |
|---|---|---:|---:|---|
| `(1, 0)` | 列未占用 | 1，已占用 | 1 | 不能，`/` 对角线冲突 |
| `(1, 1)` | 列已占用 | 2 | 0 | 不能，同列冲突 |
| `(1, 2)` | 列未占用 | 3 | -1，已占用 | 不能，`\` 对角线冲突 |
| `(1, 3)` | 列未占用 | 4，未占用 | -2，未占用 | 可以 |

所以本层只有第 3 列能够继续搜索。

**Step 6：补上检查，并同步维护三个集合**

现在先在外层初始化三个集合：

```python
occupied_cols = set()
occupied_slash_diagonals = set()
occupied_backslash_diagonals = set()
```

在放皇后之前，排除冲突位置：

```python
if (col in occupied_cols
        or (row + col) in occupied_slash_diagonals
        or (row - col) in occupied_backslash_diagonals):
    continue
```

选择一个合法位置以后，除了修改棋盘，还要记录它占用的列和两条对角线：

```python
board[row][col] = "Q"
occupied_cols.add(col)
occupied_slash_diagonals.add(row + col)
occupied_backslash_diagonals.add(row - col)
```

子调用返回以后，要撤销这四项修改：

```python
board[row][col] = "."
occupied_cols.remove(col)
occupied_slash_diagonals.remove(row + col)
occupied_backslash_diagonals.remove(row - col)
```

得到最终代码：

```python
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        board = [["."] * n for _ in range(n)]

        occupied_cols = set()
        occupied_slash_diagonals = set()
        occupied_backslash_diagonals = set()

        def place_queens(row):
            if row == n:
                result.append(
                    ["".join(board_row) for board_row in board]
                )
                return

            for col in range(n):
                if (col in occupied_cols
                        or (row + col) in occupied_slash_diagonals
                        or (row - col) in occupied_backslash_diagonals):
                    continue

                board[row][col] = "Q"
                occupied_cols.add(col)
                occupied_slash_diagonals.add(row + col)
                occupied_backslash_diagonals.add(row - col)

                place_queens(row + 1)

                board[row][col] = "."
                occupied_cols.remove(col)
                occupied_slash_diagonals.remove(row + col)
                occupied_backslash_diagonals.remove(row - col)

        place_queens(0)
        return result
```

---

**三、递归返回以后，到底是谁在撤销？为什么四项都要恢复？**

假设第 0 行已经选中了 `(0, 1)`。

某次调用 F1 进入时：

```python
row = 1
```

棋盘是：

```python
[
    ".Q..",
    "....",
    "....",
    "...."
]
```

集合是：

```python
occupied_cols = {1}
occupied_slash_diagonals = {1}
occupied_backslash_diagonals = {-1}
```

F1 选择第 3 列：

```python
board[1][3] = "Q"
```

并记录占用：

```python
occupied_cols = {1, 3}
occupied_slash_diagonals = {1, 4}
occupied_backslash_diagonals = {-1, -2}
```

然后调用：

```python
place_queens(2)
```

子调用的任务是：

> 前两行已经确定为 `(0, 1)`、`(1, 3)`。检查后两行的所有合法放法，并保存完整棋盘。

在 `n = 4` 时，它会找到：

```python
[
    ".Q..",
    "...Q",
    "Q...",
    "..Q."
]
```

子调用记录答案以后，会撤销它在第 2 行、第 3 行放的皇后及对应标记。

所以返回 F1 时，棋盘恢复为：

```python
[
    ".Q..",
    "...Q",
    "....",
    "...."
]
```

集合仍然保留前两行皇后的标记：

```python
occupied_cols = {1, 3}
occupied_slash_diagonals = {1, 4}
occupied_backslash_diagonals = {-1, -2}
```

**现在 F1 要撤销谁？**

撤销 F1 自己选择的 `(1, 3)`：

```python
board[1][3] = "."
occupied_cols.remove(3)
occupied_slash_diagonals.remove(4)
occupied_backslash_diagonals.remove(-2)
```

恢复到 F1 进入时的状态：

```python
occupied_cols = {1}
occupied_slash_diagonals = {1}
occupied_backslash_diagonals = {-1}
```

第 0 行的皇后仍然保留，因为它是上一层选择的。

规则还是：

> **我放了哪个皇后，就在子调用返回以后，由我撤销这个皇后及它的三个标记。子调用负责撤销它自己放的皇后。**

**为什么不能只把棋盘上的 `"Q"` 改回 `"."`？**

因为三个集合也参与后续的合法性检查。

如果皇后已经拿走，但集合里仍然保留它的列或对角线编号，后面的候选位置就会被错误地判断为冲突。

所以棋盘和三个集合必须一起恢复。

**为什么 `remove()` 不会误删其他皇后的标记？**

因为这个位置在选择之前已经通过检查：

```text
它的列编号不在集合中。
它的两条对角线编号也不在集合中。
```

这三个编号都是本层新添加的。子调用又会恢复自己的修改，所以本层返回后移除的正是自己的标记。

每次函数调用都有自己的 `row`、`col`。子调用不会改变父调用正在处理的行和列。

---

**四、完整执行一次 `n = 4`**

为了缩短记录，用一个列列表表示当前放法。

例如：

```python
[1, 3]
```

表示：

```text
第 0 行的皇后在第 1 列。
第 1 行的皇后在第 3 列。
后面的行还没有放皇后。
```

这个列表只是跟踪过程的记号，代码实际使用的是 `board` 和三个集合。

下面每次“撤销”都包含：

- 把对应格子改回 `"."`。
- 移除它的列标记。
- 移除它的两条对角线标记。

**1. 第 0 行先选择第 0 列**

```text
进入 F0：row=0，当前放法=[]

F0 的 col=0：可以放
选择 (0, 0) → [0]
调用 F1：row=1
```

F1 检查第 1 行：

```text
col=0：同列冲突，跳过
col=1：对角线冲突，跳过

col=2：可以放
选择 (1, 2) → [0, 2]
调用 F2：row=2
```

F2 检查第 2 行：

| 列 | 检查结果 |
|---:|---|
| 0 | 同列冲突 |
| 1 | `/` 对角线冲突 |
| 2 | 同列冲突 |
| 3 | `\` 对角线冲突 |

没有合法位置：

```text
F2 的循环结束，返回 F1

F1 撤销自己选的 (1, 2) → [0]
```

F1 继续检查下一列：

```text
col=3：可以放
选择 (1, 3) → [0, 3]
调用 F3：row=2
```

F3 检查：

```text
col=0：同列冲突，跳过

col=1：可以放
选择 (2, 1) → [0, 3, 1]
调用 F4：row=3
```

F4 检查最后一行：

| 列 | 检查结果 |
|---:|---|
| 0 | 同列冲突 |
| 1 | 同列冲突 |
| 2 | `\` 对角线冲突 |
| 3 | 同列冲突 |

所以：

```text
F4 返回 F3
F3 撤销 (2, 1) → [0, 3]

F3 继续检查：
col=2：对角线冲突，跳过
col=3：同列冲突，跳过

F3 返回 F1
F1 撤销 (1, 3) → [0]

F1 的循环结束，返回 F0
F0 撤销 (0, 0) → []
```

至此，所有第 0 行放在第 0 列的方案都搜索完了，没有答案。

**2. 第 0 行选择第 1 列，找到第一份答案**

```text
F0 的 col=1：可以放
选择 (0, 1) → [1]
调用 F5：row=1
```

F5 检查：

```text
col=0：对角线冲突，跳过
col=1：同列冲突，跳过
col=2：对角线冲突，跳过

col=3：可以放
选择 (1, 3) → [1, 3]
调用 F6：row=2
```

F6 检查：

```text
col=0：可以放
选择 (2, 0) → [1, 3, 0]
调用 F7：row=3
```

F7 检查：

```text
col=0：同列冲突，跳过
col=1：同列冲突，跳过

col=2：可以放
选择 (3, 2) → [1, 3, 0, 2]
调用 F8：row=4
```

F8 达到 base case：

```text
row == n

保存：
[".Q..", "...Q", "Q...", "..Q."]

F8 return
```

开始返回并继续检查剩余候选：

```text
回到 F7：
撤销 (3, 2) → [1, 3, 0]
col=3：同列冲突，跳过
F7 返回 F6
```

```text
回到 F6：
撤销 (2, 0) → [1, 3]

继续检查：
col=1：同列冲突，跳过
col=2：对角线冲突，跳过
col=3：同列冲突，跳过

F6 返回 F5
```

```text
回到 F5：
撤销 (1, 3) → [1]
F5 的循环结束，返回 F0

F0 撤销 (0, 1) → []
```

第一份答案已经保存，但仍然需要继续搜索其他起始列。

**3. 第 0 行选择第 2 列，找到第二份答案**

```text
F0 的 col=2：可以放
选择 (0, 2) → [2]
调用 F9：row=1
```

F9：

```text
col=0：可以放
选择 (1, 0) → [2, 0]
调用 F10：row=2
```

F10：

```text
col=0：同列冲突，跳过
col=1：对角线冲突，跳过
col=2：同列冲突，跳过

col=3：可以放
选择 (2, 3) → [2, 0, 3]
调用 F11：row=3
```

F11：

```text
col=0：同列冲突，跳过

col=1：可以放
选择 (3, 1) → [2, 0, 3, 1]
调用 F12：row=4
```

F12 达到 base case：

```text
保存：
["..Q.", "Q...", "...Q", ".Q.."]

F12 return
```

返回：

```text
回到 F11：
撤销 (3, 1) → [2, 0, 3]

col=2：同列冲突，跳过
col=3：同列冲突，跳过

F11 返回 F10
```

```text
回到 F10：
撤销 (2, 3) → [2, 0]
F10 的循环结束，返回 F9
```

```text
回到 F9：
撤销 (1, 0) → [2]

继续检查：
col=1：对角线冲突，跳过
col=2：同列冲突，跳过
col=3：对角线冲突，跳过

F9 返回 F0
F0 撤销 (0, 2) → []
```

**4. 第 0 行选择第 3 列，没有找到新答案**

```text
F0 的 col=3：可以放
选择 (0, 3) → [3]
调用 F13：row=1
```

F13：

```text
col=0：可以放
选择 (1, 0) → [3, 0]
调用 F14：row=2
```

F14：

```text
col=0：同列冲突，跳过
col=1：对角线冲突，跳过

col=2：可以放
选择 (2, 2) → [3, 0, 2]
调用 F15：row=3
```

F15：

| 列 | 检查结果 |
|---:|---|
| 0 | 同列冲突 |
| 1 | `/` 对角线冲突 |
| 2 | 同列冲突 |
| 3 | 同列冲突 |

因此：

```text
F15 返回 F14
F14 撤销 (2, 2) → [3, 0]

F14 的 col=3：同列冲突，跳过
F14 返回 F13

F13 撤销 (1, 0) → [3]
```

F13 继续：

```text
col=1：可以放
选择 (1, 1) → [3, 1]
调用 F16：row=2
```

F16：

| 列 | 检查结果 |
|---:|---|
| 0 | `/` 对角线冲突 |
| 1 | 同列冲突 |
| 2 | `\` 对角线冲突 |
| 3 | 同列冲突 |

因此：

```text
F16 返回 F13
F13 撤销 (1, 1) → [3]

F13 继续检查：
col=2：对角线冲突，跳过
col=3：同列冲突，跳过

F13 返回 F0
F0 撤销 (0, 3) → []
```

最后：

```text
F0 的循环结束
F0 返回

外层 solveNQueens 返回 result
```

最终结果：

```python
[
    [".Q..", "...Q", "Q...", "..Q."],
    ["..Q.", "Q...", "...Q", ".Q.."]
]
```

---

**五、为什么能找到所有答案，而且不重复？**

**为什么生成的答案都合法？**

每次递归只给当前行放一个皇后，因此不会同一行冲突。

选择之前又检查列和两条对角线，所以新皇后不会攻击之前的皇后。

只有所有行都完成时才记录答案，因此每个答案恰好有 `n` 个皇后，并且两两不攻击。

**为什么不会漏掉答案？**

任何合法棋盘，在每一行都有一个确定的皇后所在列。

本层循环会检查当前行的所有列。合法答案对应的那个位置不会和前面已放好的皇后冲突，因此对应分支一定会被进入。

递归再继续处理后面的行，所以任何合法棋盘对应的逐行选择过程都会被走到。

**为什么不会重复？**

一个棋盘对应唯一的一组逐行列选择。

例如：

```python
[1, 3, 0, 2]
```

唯一确定了每个皇后的位置。

每层循环只尝试每个列一次，因此相同的逐行选择不会重复生成。

**复杂度**

记 `S` 为合法棋盘的数量。

| 项目 | 复杂度 | 原因 |
|---|---|---|
| 时间，保守上界 | `O(n × n! + S × n²)` | 同列限制使搜索路径不超过排列规模；每个未完成状态扫描 `n` 列，每份答案需要转换整个棋盘 |
| 辅助空间 | `O(n²)` | 棋盘占 `n²`；三个集合及递归栈各占 `O(n)` |
| 输出空间 | `O(S × n²)` | 每份答案包含 `n` 个长度为 `n` 的字符串 |

这里把生成答案的成本单独列出来，是因为这份实现每找到一个答案，都需要拼接完整的 `n × n` 棋盘。

---

**六、下次从空白写时，脑子里的顺序**

1. **合法答案有什么结构？**`n` 个皇后分布在 `n` 行，每行恰好一个。
2. **每一步决定什么？**当前行的皇后放在哪一列。
3. **为什么递归？**放好当前行以后，剩下的仍然是给剩余行放皇后的任务。
4. **先需要什么状态？**工作棋盘 `board`、当前行 `row`、结果 `result`。
5. **helper 负责什么？**保留前面行的选择，搜索后面行的所有合法放法。
6. 写外层骨架，从 `place_queens(0)` 开始。
7. 写 base case：所有行完成，把棋盘转换成字符串列表并保存。
8. 写循环：逐个尝试当前行的所有列。
9. 写主流程：**放皇后 → 递归处理下一行 → 拿走皇后**。
10. 回头检查选择是否合法：不能同列，也不能同对角线。
11. 此时引入三个集合：列编号、`row + col`、`row - col`。
12. 在放置之前检查冲突；放置以后添加标记；子调用返回以后，**同时撤销棋盘和三个集合的修改**。

"""
