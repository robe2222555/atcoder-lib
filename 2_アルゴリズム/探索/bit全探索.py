N=0

for i in range(2**N):
	for j in range(N):
		if ((i>>j) & 1):
			
			i=12345 #何かしらの処理

# if (i>>j) ^ 1: はつかえない
