# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/Matrix/回転行列.py
# 二次元ベクトルの回転行列

from math import cos, sin, pi
# cos,sinの引数, atanの返り値はradian
kakudo=150
Radian=pi/180*kakudo

#RR=[[cos(Radian),-sin(Radian)],[sin(Radian),cos(Radian)]]
def R(vec, rad):
	x=vec[0]*cos(rad)-vec[1]*sin(rad)
	y=vec[0]*sin(rad)+vec[1]*cos(rad)
	return [x,y]
