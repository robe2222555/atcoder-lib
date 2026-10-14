class Node:
	__slots__ = ('left', 'right', 'val')

	def __init__(self, val):
		self.left = None
		self.right = None
		self.val = val


class DynamicSegmentTree:
	dat_unit = 1<<30      # セグ木の単位元

	def __init__(self, U):
		"""
		U : 値域のサイズ．添字は [0, U) を扱う
		root : 木の根．必要になったノードだけ遅延生成される
		"""
		self.U = U
		self.root = Node(self.dat_unit)
		return

	def operate(self, x, y):
		return min(x, y)

	def query(self, a, b):
		"""
		区間 [a, b) の集約値を返す
		a, b は 0-based index
		"""
		if a >= b:
			return self.dat_unit

		res = self.dat_unit
		stack = [(self.root, 0, self.U)]

		while stack:
			node, l, r = stack.pop()
			if node is None or b <= l or r <= a:
				continue
			if a <= l and r <= b:
				res = self.operate(res, node.val)
				continue
			mid = (l + r) // 2
			stack.append((node.right, mid, r))
			stack.append((node.left,  l,   mid))

		return res

	def add(self, a, val, replace=False):
		"""
		dat[a] に val を作用
		a は 0-based index
		replace=True で値を書き換える
		"""
		node = self.root
		l, r = 0, self.U
		path = []  # 通過したノードを (node, 左の子か右の子か) で積む

		while r - l > 1:
			mid = (l + r) // 2
			if a < mid:
				if node.left is None:
					node.left = Node(self.dat_unit)
				path.append((node, True))   # True: 左に進んだ
				node = node.left
				r = mid
			else:
				if node.right is None:
					node.right = Node(self.dat_unit)
				path.append((node, False))  # False: 右に進んだ
				node = node.right
				l = mid

		# 葉に到達
		node.val = val if replace else self.operate(node.val, val)

		# 葉 -> 根の向きに val を再計算
		for parent, went_left in reversed(path):
			vL = parent.left.val  if parent.left  is not None else self.dat_unit
			vR = parent.right.val if parent.right is not None else self.dat_unit
			parent.val = self.operate(vL, vR)

	def __repr__(self):
		return "DynamicSeg: U={}".format(self.U)

	###################################











class Node:
	__slots__ = ('left', 'right', 'val')

	def __init__(self, val):
		self.left = None
		self.right = None
		self.val = val


class DynamicSegmentTree:
	dat_unit = 1<<30      # セグ木の単位元

	def __init__(self, U):
		"""
		U : 値域のサイズ．添字は [0, U) を扱う
		root : 木の根．必要になったノードだけ遅延生成される
		"""
		self.U = U
		self.root = Node(self.dat_unit)
		return

	def operate(self, x, y):
		return min(x, y)

	def query(self, a, b):
		"""
		区間 [a, b) の集約値を返す
		a, b は 0-based index
		"""
		return self._query(self.root, 0, self.U, a, b)

	def _query(self, node, l, r, a, b):
		if node is None or b <= l or r <= a:
			return self.dat_unit
		if a <= l and r <= b:
			return node.val
		mid = (l + r) // 2
		vL = self._query(node.left,  l,   mid, a, b)
		vR = self._query(node.right, mid, r,   a, b)
		return self.operate(vL, vR)

	def add(self, a, val, replace=False):
		"""
		dat[a] に val を作用
		a は 0-based index
		replace=True で値を書き換える
		"""
		self.root = self._add(self.root, 0, self.U, a, val, replace)
		return None

	def _add(self, node, l, r, a, val, replace):
		if node is None:
			node = Node(self.dat_unit)
		if r - l == 1:
			node.val = val if replace else self.operate(node.val, val)
			return node
		mid = (l + r) // 2
		if a < mid:
			node.left  = self._add(node.left,  l,   mid, a, val, replace)
		else:
			node.right = self._add(node.right, mid, r,   a, val, replace)
		vL = node.left.val  if node.left  is not None else self.dat_unit
		vR = node.right.val if node.right is not None else self.dat_unit
		node.val = self.operate(vL, vR)
		return node

	def __repr__(self):
		return "DynamicSeg: U={}".format(self.U)