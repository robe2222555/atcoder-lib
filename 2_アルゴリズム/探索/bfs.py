def LI(): return list(map(int, input().split()))
from collections import deque
N,M=LI()

Past=[[] for _ in range(N+1)]
for _ in range(M):
	u,v=LI()
	Past[u].append(v)
	Past[v].append(u)

START=0
Deep=[-1]*(N+1)
q=deque([START])
Deep[START]=0

while q:
	st=q.popleft()
	for to in Past[st]:
		if Deep[to]>=0:
			continue
		Deep[to]=Deep[st]+1
		q.append(to)
		# 何らかの処理



###################
#   関数ver
###################

def LI(): return list(map(int, input().split()))
from collections import deque

N=int(input())

Past=[[] for _ in range(N+1)]
for _ in range(N-1):
	u,v=LI()
	Past[u].append(v)
	Past[v].append(u)

def bfs(START):
	Deep=[-1]*(N+1)

	q=deque([START])
	Deep[START]=0
	while q:
		st=q.popleft()
		for to in Past[st]:
			if Deep[to]>=0:
				continue
			Deep[to]=Deep[st]+1
			q.append(to)
			# 何らかの処理
	return 0


###################
#   0-1 BFS
###################

from collections import deque

INF=1<<30
H,W=LI()
rs,cs=LI()
rt,ct=LI()

S=["#"*(W+2)]+["#"+input()+"#" for _ in range(H)]+["#"*(W+2)]
next_x=[0,0,1,-1]
next_y=[1,-1,0,0]

dp = [[[INF]*4 for _ in range(W+2)] for _ in range(H+2)]
q=deque()
for dir in range(4):
	dp[rs][cs][dir]=0
	q.append((rs, cs, dir, 0))

while q:
	x,y,dirxy,cost=q.popleft()

	for dir in range(4):
		a,b=x+next_x[dir], y+next_y[dir]
		if dirxy == dir:
			if dp[a][b][dir] > cost and S[a][b] == ".":
				dp[a][b][dir] = cost
				q.appendleft((a, b, dir, cost))     # cost=0 -> left
					
		else:
			if dp[a][b][dir] > cost+1 and S[a][b] == ".":
				dp[a][b][dir] = cost+1
				q.append((a, b, dir, cost+1))       # cost=1 -> right
