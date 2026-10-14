# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/探索/bit全探索.py
N=0

for i in range(2**N):
	for j in range(N):
		if ((i>>j) & 1):
			
			i=12345 #何かしらの処理

# if (i>>j) ^ 1: はつかえない
