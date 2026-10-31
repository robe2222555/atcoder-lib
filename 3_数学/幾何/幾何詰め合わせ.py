# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/幾何/幾何詰め合わせ.py

def inner(a, b):
	"""
	ベクトル a,b の内積
	"""
	return a[0]*b[0] + a[1]*b[1]

def cross(a, b):
	"""
	ベクトル a,b の外積 a x b
	"""
	return a[0]*b[1] - a[1]*b[0]

def ccw(a, b, c):
	"""
	点a,b,cについて，ベクトルacはベクトルabから見て反時計回り or 時計回り or 同一直線
	"""
	v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
	if v > 0:
		return 1	# 点c が a->b の左側
	if v < 0:
		return -1	# 点c が a->b の右側
	return 0		# a,b,c が同一直線上

def on_segment(a, b, p):
	"""
	点pが線分ab上にある（端点を含む）
	"""
	if ccw(a, b, p) != 0:
		return False
	return inner((a[0]-p[0], a[1]-p[1]), (b[0]-p[0], b[1]-p[1])) <= 0

def opposite_sides(a, b, c, d):
	"""
	点c,d が直線ab をはさんで反対側にある（どちらかが直線上でもよい）
	"""
	return ccw(a, b, c) * ccw(a, b, d) <= 0

def intersect(a, b, c, d):
	"""
	線分ab と線分cd が共有点を持つ（端点・重なりを含む）
	"""
	if ccw(a, b, c) == 0 and ccw(a, b, d) == 0:  # 4点が一直線上
		return on_segment(a, b, c) or on_segment(a, b, d) or on_segment(c, d, a) or on_segment(c, d, b)
	return opposite_sides(a, b, c, d) and opposite_sides(c, d, a, b)