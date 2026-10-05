# 2026.10.05 第一次手打，看上一次submission的备注！

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []

        board = [ ["."] * n for _ in range(n)] 
        # if n = 4
        # [[".",".",".","."]
        #  [".",".",".","."]
        #  [".",".",".","."]
        #  [".",".",".","."]]

        occupied_column = set()
        occupied_slash = set()
        occupied_backslash = set()
  

        def place_queens(row):
            # helper function: this helper finds all valid queen placing strategies starting from row n, given that row 0 to row - 1 are already placed. 
            # given that row 0 to row-1 already have queens, find all queen placing strategies by starting placing queen from row row(the argument) all the way to row n. 

            # base case: 
            # when all rows are placed, then we save our current snapshot of the board to result
            if row == len(board):
                result.append(["".join(board_row) for board_row in board])
                return

            # main logic
            # 因为题目要求返回所有可能性，我们就固定行的情况下，我们每一列都试一下能不能摆Queen
            for col in range(n):
                # 因为还要检查是不是可以在这里摆Queen,所以每次加queen时还有看一下if statement过一下那些需要检查的东西
                # 我们要检查，这个queen摆的位置 (1) 同一列不能有queen (2) slash对角线上不能有queen
                # (3) backslash对角线上不能有queen 
                if (col in occupied_column
                    or (row+col) in occupied_slash 
                    or (row-col) in occupied_backslash):
                    continue
                

                board[row][col] = "Q"
                occupied_column.add(col)
                occupied_slash.add(row+col)
                occupied_backslash.add(row-col)
                
                #backtrack
                place_queens(row+1)
                
                board[row][col] = "."
                occupied_column.remove(col)
                occupied_slash.remove(row+col)
                occupied_backslash.remove(row-col)


        place_queens(0)
        return result
        