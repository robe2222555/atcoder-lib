# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/素数関係.py
def LI(): return list(map(int, input().split()))
def II(): return int(input())

##########################################
# 1. 素数判定
#
# 2.エラトステネスの篩
# 	2.1.区間付きの篩
#
# 3. 素因数分解
# 	3.1. 高速素因数分解
#
# 4. 約数列挙
##########################################




# 一つの値の素数判定
N=II()
def is_prime(n):
	for i in range(2, int(pow(n, 0.5))):
		if n%i==0:
			return False
	return True

##########################################
#エラトステネスの篩 O(n loglog n)
N=II()
def sieve(n):
	Prime=[1]*(n+1)
	Prime[0]=Prime[1]=0
	for i in range(2, n+1):
		if Prime[i]:
			for j in range(i*2, n+1, i):
				Prime[j]=0
	return Prime


######################################
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



##################################################
# nを素因数分解し、{素因数:その指数} の辞書を返す
##################################################
def Primefact(n):
	Dic={}
	for i in range(2,int(pow(n,0.5))+1):
		if n%i==0:
			Dic[i]=0
			while True:
				n/=i
				Dic[i]+=1
				if n%i!=0:
					break
		if n==1:
			break
	if n!=1:
		Dic[int(n)]=1
	return Dic

##################################################
# 1～i～nについて、iの最小の素因数をリストで返す
# 　　　i / List[i] を繰り返す
##################################################
def Fast_PFact(n):
	List=[0 for i in range(n+1)]
	List[1]=1
	for i in range(2,n+1):
		if List[i]==0:
			cnt=1
			while i*cnt<=n:
				List[i*cnt]=i
				cnt+=1
	return List



# 約数列挙
def enumDivisions(n):
	res = []
	for i in range(1, int(pow(n, 0.5))+1):
		if n%i == 0:
			res.append(i)
			if n//i != i:
				res.append(n//i)
	return res