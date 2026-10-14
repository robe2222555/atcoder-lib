# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/探索/binary_search.py
# 半開区間[ok,ng) or (ng,ok]　が探索範囲　=　okの範囲
# okとngが隣だったらokが一つに定まる

ng=10**18+1
ok=0
while abs(ok-ng)>1:
	c=(ok+ng)//2
	
	flag=True
	# cの判定

	if flag:
		ok=c
	else:
		ng=c

##########################

def bi_search(exp):
	" return max(a) satisfied a**exp <= N  "
	ok = 1
	ng = N+1

	while ng-ok > 1:
		c = (ok+ng)//2

		tmp = c
		flag = True
		for i in range(2, exp+1):
			tmp *= c
			if tmp > N:
				flag = False
				break


		if flag:
			ok = c
		else:
			ng = c
		continue
	return ok


from bisect import bisect_left, bisect_right
pos = bisect_left(sorted_List=[], value=0)  #挿入するインデックスを返す