# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/幾何/偏角.py

##############################
# 偏角ソート
# verified by ABC442 E
##############################
from functools import cmp_to_key
def cmp(p1: tuple[int], p2: tuple[int]):
	c1 = (p1[1] > 0) or (p1[1] == 0 and p1[0] > 0)
	c2 = (p2[1] > 0) or (p2[1] == 0 and p2[0] > 0)

	if c1 != c2:
		c = (p1[1] < p2[1]) or (p1[1] == p2[1] and p1[0] < p2[0])
		if c: return 1
		else: return -1

	if p1[0]*p2[1] - p1[1]*p2[0] < 0: return 1
	else: return -1

Cood = [(1,2), (100,20)]
Cood = sorted(Cood, key=cmp_to_key(cmp))



##############################
# 二次元ベクトルの回転行列
##############################
from math import cos, sin, pi, atan
# cos,sinの引数, atanの返り値はradian
kakudo=150
Radian=pi/180*kakudo

#RR=[[cos(Radian),-sin(Radian)],[sin(Radian),cos(Radian)]]
def R(vec, rad):
	x=vec[0]*cos(rad)-vec[1]*sin(rad)
	y=vec[0]*sin(rad)+vec[1]*cos(rad)
	return [x,y]


##############################
# 二次元座標 (xi, yi) と (xj, yj) の偏角を度数法で返す
# typical90 - 問題9
##############################
def cul_angle(xi,yi, xj,yj):
	# 90, 270以外
	if xj != xi:    
		angle = atan((yj-yi)/(xj-xi)) * (180/pi)

		if xj < xi:     # 第2,3象限
			angle += 180

		if angle < 0:
			angle += 360
	
	# 90, 270以外
	else:
		if yi < yj:
			angle = 90
		else:
			angle = 270

	return angle