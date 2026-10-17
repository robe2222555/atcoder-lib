# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/素数関係/素因数分解.py
# nを素因数分解し、{素因数:その指数} の辞書を返す

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
