# -----------------------------
# Đồ thị 13 đỉnh (theo thứ tự 1..13)
# -----------------------------
adj_lists = {
    1: [2,3,11],
    2: [1,4,6],
    3: [1,4,6],
    4: [2,3,5,6],
    5: [4,9,10,13],
    6: [2,3,4,7],
    7: [6,8],
    8: [7,10],
    9: [5,13],
    10:[5,8],
    11:[1,12,13],
    12:[11,13],
    13:[5,9,11,12]
}

# Chuyển thành ma trận kề (0-indexed)
n = 13
adj = [[0]*n for _ in range(n)]
for u, neigh in adj_lists.items():
    for v in neigh:
        adj[u-1][v-1] = 1
        adj[v-1][u-1] = 1  # đồ thị vô hướng

# ----------------------------------------
# DFS dùng stack (phi đệ quy)
# ----------------------------------------
def DFS_stack(adj, start=0):
    n = len(adj)
    visited = [False]*n
    res = []
    stack = [start]
    while stack:
        v = stack.pop()
        if not visited[v]:
            visited[v] = True
            res.append(v+1)  # +1 để in 1..13
            # push các đỉnh kề theo thứ tự ngược để pop ra sẽ là nhỏ->lớn
            for i in range(n-1, -1, -1):
                if adj[v][i] == 1 and not visited[i]:
                    stack.append(i)
    return res

# ----------------------------------------
# DFS đệ quy
# ----------------------------------------
def DFS_recursive(adj, v, visited, res):
    visited[v] = True
    res.append(v+1)
    for i in range(len(adj)):
        if adj[v][i] == 1 and not visited[i]:
            DFS_recursive(adj, i, visited, res)

# ----------------------------------------
# Chạy thử và in kết quả
# ----------------------------------------
res_stack = DFS_stack(adj, 0)
visited = [False]*n
res_rec = []
DFS_recursive(adj, 0, visited, res_rec)

print("DFS dùng stack:  ", " ".join(map(str, res_stack)))
print("DFS đệ quy:      ", " ".join(map(str, res_rec)))

if __name__ == "__main__":
    # Danh sách kề (0-indexed)
    adj = [
        [1,2,10],       # 1
        [0,3,5],        # 2
        [0,3,5],        # 3
        [1,2,4,5],      # 4
        [3,8,9,12],     # 5
        [1,2,3,6],      # 6
        [5,7],          # 7
        [6,9],          # 8
        [4,12],         # 9
        [4,7],          # 10
        [0,11,12],      # 11
        [10,12],        # 12
        [4,8,10,11]     # 13
    ]

    ans = bfs(adj, 0)   # bắt đầu từ đỉnh 1 (index 0)
    print("BFS order:", " ".join(map(str, ans)))

