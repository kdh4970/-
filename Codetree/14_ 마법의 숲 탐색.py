# 1550 ~ 1627 솔루션 구상 37m
# 1654 ~ 1740 구현 46m
# 2040

# 지도의 기본값은 0, 정령의 위치는 1, 골렘의 위치는 2, 골렘 출구는 3으로 가정한다.
# 남하가 완료된 골렘의 위치는 남하 순으로 갯수 *-1  고정 출구는 배열에 저장
# 현재 정령의 위치 출구를 저장
# 출구 인덱스 0123은 북동남서

# 1. 정령은 십자모양 골렘의 정중앙에 있으며, 골렘은 남쪽으로 이동한다.(단 아래 세칸이 빈 경우)
## 정령의 현 위치 기반으로 좌,우,아래 좌표에서 각각 아래쪽이 비었는지 확인한다.
## 빈 경우, 현 정령 및 골렘 위치를 지우고, 정령 및 출구 값을 업데이트하고 지도에 반영한다.

# 2. 1이 불가한 경우, 서쪽으로 회전하며 한칸 내려간다. 출구가 반시계 회전 (서쪽 세칸이 비었고, 그 아래 두칸이 빈경우)
## 정령의 현 위치 기반으로 상,하,좌 좌표에서 각각 서쪽이 비었는지 확인한다.
## 빈 경우, 현 정령 및 골렘 위치를 지우고, 정령 및 출구 값을 업데이트하고 지도에 반영한다.

# 3. 2가 불가한 경우, 동쪽으로 회전하며 한칸 내려간다. 출구가 시계 회전 (동쪽 세칸이 비었고, 그 아래 두칸이 빈경우)
## 정령의 현 위치 기반으로 상,하,우 좌표에서 각각 동쪽이 비었는지 확인한다.
## 빈 경우, 현 정령 및 골렘 위치를 지우고, 정령 및 출구 값을 업데이트하고 지도에 반영한다.

# 4. 위 과정을 반복하여 골렘이 최대한 남하한 경우, 골렘 내부에서 정령이 남하한다. (단, 골렘 출구가 다른 골렘과 인접하면 넘어 갈 수 있다.)
## 이후 해당 위치가 출구이고, 인접 삼면 중 골렘이 존재하면 다시 이동이 가능하다.
## visited배열을 만든다.
## 정령위치에서 탐색을 수행한다. 단, 기본적으로 한 골렘(-2 or -3... etc)에서 탐색하며, 출구(-1)를 발견하면 해당 위치중 인접한 골렘이동이 가능하다.
## 인접 골렘 이동 시 해당 인덱스를 기반으로 해당 골렘을 계속 서치 가능하다.
## 순간순간 max row 값을 갱신한다.

# 5. 정령의 남하가 끝나면, 해당 행수를 누적한다.
# 6. 골렘이 숲을 초과하면, 해당 골렘을 포함하여 이전 골렘들을 모두 지우고, 다음 골렘을 투입한다.
## 현재 골렘의 아래부분 0,c가 비어있는가?
## (0,c-1), (0,c+1), (1,c)가 비어있는가?
## 아니라면 서쪽아래를 체크,
from collections import deque

R, C, K = map(int, input().rstrip().split(" "))
forest = [[0] * C for _ in range(R)]
golems = [list(map(int, input().rstrip().split(" "))) for _ in range(K)]

dgolem = [(0, 0), (-1, 0), (0, 1), (1, 0), (0, -1)]
ddown = [(2, 0), (1, -1), (1, 1)]
dleft = [(0, -2), (-1, -1), (1, -1), (2, -1),(1,-2)]
dright = [(0, 2), (-1, 1), (1, 1), (2, 1),(1,2)]
fixed_golem_cnt = 0
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
init_boost_col = []
exit = [[0] * C for _ in range(R)]
res = 0
visited = [[False] * C for _ in range(R)]


def scan(arr, now_r, now_c, temp):
    global visited
    for _ in range(4):
        r = now_r + dr[_]
        c = now_c + dc[_]

        if 0 <= r <= R - 1 and 0 <= c <= C - 1 and not visited[r][c]:
            if exit[now_r][now_c]:  # 출구인지
                visited[r][c] = True
                arr.append((r, c))
            elif forest[r][c] == forest[now_r][now_c]:  # 골렘 내부인지
                arr.append((r, c))
                visited[r][c] = True
                temp = max(temp, r + 1)
    return arr, temp


def go_spirit(now):
    global res, visited
    visited = [[False] * C for _ in range(R)]
    q = deque([now])
    visited[now[0]][now[1]] = True
    temp = 0
    while q:
        r, c = q.popleft()

        # print(f"{r},{c},{forest[r][c]}")
        if forest[r][c] < 0:
            q, temp = scan(q, r, c, temp)
    res += temp
    # print(f"max {temp}")


def end_golem(r, c, exit_dir):
    global fixed_golem_cnt, exit, forest
    fixed_golem_cnt += 1
    for _ in range(5):
        dr, dc = dgolem[_]
        forest[r + dr][c + dc] = fixed_golem_cnt * (-1)
    dr, dc = dgolem[exit_dir + 1]
    exit[r + dr][c + dc] = fixed_golem_cnt
    # print(f"golem {fixed_golem_cnt} arrived in {r},{c}")
    # print(f"exit {exit_arr}")
    ## 정령 남하
    go_spirit((r, c))


def in_range(y, x):
    return 0 <= y and y < R and 0 <= x and x < C


def go_golem(r, c, exit_dir):
    global fixed_golem_cnt, exit, forest, init_boost_col
    end = False
    # if not init_boost_col or (len(init_boost_col) == 1 and abs(init_boost_col[0] - c) > 2):
    #     end_golem(R - 2, c, exit_dir)
    #     init_boost_col.append(c)
    #     return 0
    # init_boost_col.append(c)

    while True:
        # if fixed_golem_cnt == 39 and r==40: breakpoint()
        skip = False

        if r == R - 2 or end:
            if r in [-2, -1, 0]:
                fixed_golem_cnt = 0
                init_boost_col = []
                exit = [[0] * C for _ in range(R)]
                forest = [[0] * C for _ in range(R)]
                return -1
            # 4번 로직
            ## 골렘 픽스 및 출구 배열 저장
            end_golem(r, c, exit_dir)
            return 0
        # 1번 로직 시도
        for _ in range(3):
            dr, dc = ddown[_]
            if in_range(r + dr, c + dc) and forest[r + dr][c + dc] != 0:
                break
            if _ == 2:
                skip = True
                r += 1
                break
        # if fixed_golem_cnt==39:print(f"after 1 {r,c}")
        if skip: continue

        # 2번 로직 시도
        for _ in range(5):
            dr, dc = dleft[_]
            if not (0 <= c + dc <= C - 1):
                break
            if r + dr not in [-1, -2] and forest[r + dr][c + dc] != 0:
                break
            if _ == 4:
                c -= 1
                exit_dir = exit_dir - 1 if exit_dir > 0 else 3
                skip = True
        # if fixed_golem_cnt==39:print(f"after 2 {r, c}")
        if skip: continue

        # 3번 로직 시도
        for _ in range(5):
            dr, dc = dright[_]
            if not (0 <= c + dc <= C - 1):
                end = True
                break
            if r + dr not in [-1, -2] and forest[r + dr][c + dc] != 0:
                end = True
                break
            if _ == 4:
                c += 1
                exit_dir = exit_dir + 1 if exit_dir < 3 else 0
                skip = True
#         if fixed_golem_cnt==39:print(f"after 3 {r, c}")


for idx,golem in enumerate(golems):
    start_col, exit_dir = golem

    ## 못 내려갈 때 까지 남하
    go_golem(-2, start_col - 1, exit_dir)
    # print(f"======{idx}========")
    # for line in forest:print(line)
    # print("==============")
print(res)