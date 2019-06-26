def calculate_minimum_HP(dungeon):
    """
    :type dungeon: List[List[int]]
    :rtype: int
    """
    if not dungeon or not dungeon[0]:
        return 0
    row, col = len(dungeon), len(dungeon[0])
    dp = [[0] * col for _ in range(row)]
    dp[-1][-1] = max(1, 1 - dungeon[-1][-1])

    for i in range(row - 2, -1, -1):
        dp[i][-1] = max(1, dp[i+1][-1] - dungeon[i][-1])

    for j in range(col - 2, -1, -1):
        dp[-1][j] = max(1, dp[-1][j + 1] - dungeon[-1][j])

    for i in range(row - 2, -1, -1):
        for j in range(col - 2, -1, -1):
            dp[i][j] = min(max(1, dp[i][j + 1] - dungeon[i][j]), max(1, dp[i + 1][j] - dungeon[i][j]))

    return dp[0][0]