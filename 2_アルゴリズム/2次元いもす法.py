# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/2次元いもす法.py
def LI(): return list(map(int, input().split()))
def II(): return int(input())


"""
https://imoz.jp/algorithms/imos_method.html


4点に重み加算し, 横累積和, 縦累積和 をおこなう O(N+HW)
例: (0,1) ~ (2, 4)の長方形に+1

		 C[i] ... D[i]
A[i]	0  1  1  1  1  0  0       0 +1  0  0  0 -1  0
:		0  1  1  1  1  0  0  <=   0  0  0  0  0  0  0
B[i]	0  1  1  1  1  0  0  <=   0  0  0  0  0  0  0
		0  0  0  0  0  0  0       0 -1  0  0  0 +1  0
"""

H,W=LI()
N=II()

Imos=[[0]*(W)  for _ in range(H)]
# 長方形N個 : A[i]<=x<B[i], C[i]<=y<D[i]
A=B=C=D=LI()

# 重みの加算
for i in range(N):
	imos_weight=[[A[i], C[i]], [A[i], D[i]], [B[i], C[i]], [B[i], D[i]]]
	weight=-1
	for x,y in imos_weight:
		weight*=-1
		if x<0:
			x=0
		if y<0:
			y=0
		if 0<=x<H and 0<=y<W:
			Imos[x][y]+=weight

# 横方向に累積
for i in range(H):
	for j in range(1,W):
		Imos[i][j]+=Imos[i][j-1]

# 横方向に累積
for j in range(W):
	for i in range(1,H):
		Imos[i][j]+=Imos[i-1][j]


# 区間 [li, ri] かつ [lj, rj] の累積和を取得
sumlr = 0
sumlr += Imos[ri][rj]
sumlr -= Imos[ri][lj-1] + Imos[li-1][rj]
sumlr += Imos[li-1][lj-1]
