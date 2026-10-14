#
# 双方向リスト
# verified by ABC344E
#


from collections import defaultdict

sentinel_head = 1<<60
sentinel_tail = -(1<<60)

head = defaultdict(lambda : None)
tail = defaultdict(lambda : None)
head[sentinel_tail] = sentinel_head
tail[sentinel_head] = sentinel_tail

def add(x,z):
	"x の直後に z を追加"
	y = tail[x]

	# x-y => x-z-y
	tail[x] = z
	
	head[z] = x
	tail[z] = y

	head[y] = z
	return


def delete(x):
	"x を削除"
	a = head[x]
	b = tail[x]

	# a-x-b => a-b
	tail[a] = b

	head[x] = None
	tail[x] = None

	head[b] = a
	return

def append(x):
	"末尾に x を追加"
	
	add(head[sentinel_tail], x)
	return

def print_list():
	"list 全体をprint O(N)"

	res = []
	v = tail[sentinel_head]
	while v != sentinel_tail:
		res.append(v)
		v = tail[v]
		continue
	print(*res)
	return