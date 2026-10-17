# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/幾何/偏角/二点の偏角.py

from math import atan, pi

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
