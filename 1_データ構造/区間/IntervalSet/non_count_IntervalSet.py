# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/区間/IntervalSet/non_count_IntervalSet.py
# verified by ABC435E (add, count_covered)
# verified by ABC330E (add, erase, mex)
# verified by code-festival-2015-qualb D (add, get, contains)

# https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py
# SortedSet は tatyam-prime 氏作 (Unlicense / パブリックドメイン) をそのまま使用
import math
from bisect import bisect_left, bisect_right
from typing import Generic, Iterable, Iterator, TypeVar
T = TypeVar('T')

class SortedSet(Generic[T]):
	BUCKET_RATIO = 16
	SPLIT_RATIO = 24
	
	def __init__(self, a: Iterable[T] = []) -> None:
		"Make a new SortedSet from iterable. / O(N) if sorted and unique / O(N log N)"
		a = list(a)
		n = len(a)
		if any(a[i] > a[i + 1] for i in range(n - 1)):
			a.sort()
		if any(a[i] >= a[i + 1] for i in range(n - 1)):
			a, b = [], a
			for x in b:
				if not a or a[-1] != x:
					a.append(x)
		n = self.size = len(a)
		num_bucket = int(math.ceil(math.sqrt(n / self.BUCKET_RATIO)))
		self.a = [a[n * i // num_bucket : n * (i + 1) // num_bucket] for i in range(num_bucket)]

	def __iter__(self) -> Iterator[T]:
		for i in self.a:
			for j in i: yield j

	def __reversed__(self) -> Iterator[T]:
		for i in reversed(self.a):
			for j in reversed(i): yield j
	
	def __eq__(self, other) -> bool:
		return list(self) == list(other)
	
	def __len__(self) -> int:
		return self.size
	
	def __repr__(self) -> str:
		return "SortedSet" + str(self.a)
	
	def __str__(self) -> str:
		s = str(list(self))
		return "{" + s[1 : len(s) - 1] + "}"

	def _position(self, x: T) -> tuple[list[T], int, int]:
		"return the bucket, index of the bucket and position in which x should be. self must not be empty."
		for i, a in enumerate(self.a):
			if x <= a[-1]: break
		return (a, i, bisect_left(a, x))

	def __contains__(self, x: T) -> bool:
		if self.size == 0: return False
		a, _, i = self._position(x)
		return i != len(a) and a[i] == x

	def add(self, x: T) -> bool:
		"Add an element and return True if added. / O(√N)"
		if self.size == 0:
			self.a = [[x]]
			self.size = 1
			return True
		a, b, i = self._position(x)
		if i != len(a) and a[i] == x: return False
		a.insert(i, x)
		self.size += 1
		if len(a) > len(self.a) * self.SPLIT_RATIO:
			mid = len(a) >> 1
			self.a[b:b+1] = [a[:mid], a[mid:]]
		return True
	
	def _pop(self, a: list[T], b: int, i: int) -> T:
		ans = a.pop(i)
		self.size -= 1
		if not a: del self.a[b]
		return ans

	def discard(self, x: T) -> bool:
		"Remove an element and return True if removed. / O(√N)"
		if self.size == 0: return False
		a, b, i = self._position(x)
		if i == len(a) or a[i] != x: return False
		self._pop(a, b, i)
		return True
	
	def lt(self, x: T) -> T | None:
		"Find the largest element < x, or None if it doesn't exist."
		for a in reversed(self.a):
			if a[0] < x:
				return a[bisect_left(a, x) - 1]

	def le(self, x: T) -> T | None:
		"Find the largest element <= x, or None if it doesn't exist."
		for a in reversed(self.a):
			if a[0] <= x:
				return a[bisect_right(a, x) - 1]

	def gt(self, x: T) -> T | None:
		"Find the smallest element > x, or None if it doesn't exist."
		for a in self.a:
			if a[-1] > x:
				return a[bisect_right(a, x)]

	def ge(self, x: T) -> T | None:
		"Find the smallest element >= x, or None if it doesn't exist."
		for a in self.a:
			if a[-1] >= x:
				return a[bisect_left(a, x)]
	
	def __getitem__(self, i: int) -> T:
		"Return the i-th element."
		if i < 0:
			for a in reversed(self.a):
				i += len(a)
				if i >= 0: return a[i]
		else:
			for a in self.a:
				if i < len(a): return a[i]
				i -= len(a)
		raise IndexError
	
	def pop(self, i: int = -1) -> T:
		"Pop and return the i-th element."
		if i < 0:
			for b, a in enumerate(reversed(self.a)):
				i += len(a)
				if i >= 0: return self._pop(a, ~b, i)
		else:
			for b, a in enumerate(self.a):
				if i < len(a): return self._pop(a, b, i)
				i -= len(a)
		raise IndexError
	
	def index(self, x: T) -> int:
		"Count the number of elements < x."
		ans = 0
		for a in self.a:
			if a[-1] >= x:
				return ans + bisect_left(a, x)
			ans += len(a)
		return ans

	def index_right(self, x: T) -> int:
		"Count the number of elements <= x."
		ans = 0
		for a in self.a:
			if a[-1] > x:
				return ans + bisect_right(a, x)
			ans += len(a)
		return ans


# 番兵あり & 半開区間 実装
class IntervalSet():
	INF = 1<<60
	__slots__ = ["data", "num_covered"]

	def __init__(self):
		self.data = SortedSet([])
		self.data.add((-self.INF, -self.INF))
		self.data.add((self.INF, self.INF))
		self.num_covered = 0
		
	def contains(self, x):
		"x を含む区間が存在するか？"
		ls,le = self.data.lt((x+1, x+1))
		return x<le
	
	def get(self, x):
		"x を含む区間 or None を返す"
		res = self.data.lt((x+1, x+1))
		return res if x<res[1] else None

	def covered(self, l, r):
		"[l,r) を含む区間が存在するか？"
		rs,re = self.data.lt((r+1, r+1))
		return rs<=l and r<=re

	def add(self, l, r):
		"区間 [l,r) を追加"
		ls,le = self.data.lt((l+1, l+1))

		if r<=le:
			return
		elif l<=le:
			self.data.discard((ls,le))
			self.num_covered -= le-ls
			le = max(le, r)
		else:
			ls=l
			le=r

		while 1:
			rs,re = self.data.gt((l, l))
			if le<rs:
				break
			else:
				le = max(le, re)
				self.data.discard((rs, re))
				self.num_covered -= re-rs
				continue

		self.data.add((ls,le))
		self.num_covered += le-ls
		return
	
	def erase(self, l, r):
		"区間 [l,r) を削除"

		ls,le = self.data.lt((l+1, l+1))
		if l<le:
			self.data.discard((ls, le))
			self.num_covered -= le-ls
			if ls<l:
				self.data.add((ls, l))
				self.num_covered += l-ls
			if r<le:
				self.data.add((r, le))
				self.num_covered += le-r
				return

		while 1:
			ls,le = self.data.gt((l, l))
			if r<=ls:
				return
			
			self.data.discard((ls,le))
			self.num_covered -= le-ls
			if r<le:
				self.data.add((r, le))
				self.num_covered += le-r
				return
		return
	
	def count_covered(self):
		return self.num_covered
	
	def mex(self, x):
		"x 以上の mex"
		ls,le = self.data.lt((x+1, x+1))
		if x < le:
			return le
		else:
			return x