# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/Mo's_Algorithm.py
# 参考: https://snuke.hatenablog.com/entry/2016/07/01/000000

# ---- Mo's algorithm ----
B = max(1, N // int(pow(Q, 0.5)))
order = [(l//B, r) if (l//B)%2==0 else (l//B, -r) for l, r in queries]
Idx = sorted(range(Q), key=lambda i: order[i])

def add(p):
	return

def delete(p):
	return

ans = [None]*Q
l, r = 0, 0
for i in Idx:
	nl, nr = queries[i]
	while nl < l: l -= 1; add(l)
	while r < nr: add(r); r += 1
	while l < nl: delete(l); l += 1
	while nr < r: r -= 1; delete(r)
	ans[i] = get_answer()
# ---- end Mo's algorithm ----