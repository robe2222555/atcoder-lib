# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/素数関係/smallest_prime_factor.py
# 1～i～nについて、iの最小の素因数をリストで返す
# 　　　i / List[i] を繰り返す

def Fast_PFact(n):
	List=[0 for i in range(n+1)]
	List[1]=1
	for i in range(2,n+1):
		if List[i]==0:
			cnt=1
			while i*cnt<=n:
				if List[i*cnt]==0:
					List[i*cnt]=i
				cnt+=1
	return List
