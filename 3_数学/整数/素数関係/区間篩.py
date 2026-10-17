# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/素数関係/区間篩.py

# [a, b) 区間内の素数のリストP2  fromアリ本
a,b=LI()
def sieve(n):
	# 0~nの素数リスト
	Prime=[1]*(n+1)
	Prime[0]=Prime[1]=0
	for i in range(2, n+1):
		if Prime[i]:
			for j in range(i*2, n+1, i):
				Prime[j]=0
	return Prime

P1=sieve(int(pow(b, 0.5)))
P2=[1]*(b-a)

for p in range(2, int(pow(b, 0.5)+1)):
	if P1[p]:
		for j in range((a+p-1)//p*p, b, p):
			P2[j-a]=0
