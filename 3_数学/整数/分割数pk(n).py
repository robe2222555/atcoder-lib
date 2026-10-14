
# https://manabitimes.jp/math/888
# 「整数nをk分割する通り」＝「最大がkであるいくつかの分割の通り」
# ヤング図形を反転させると，二者が全単射の対応になる
# pk(n):=nをk個に分割 n,k>0
# pk(n)= pk(n-k) +pk-1(n-1)
#        1を含む  1を含まない

# O(nm)
n,m=5, 3
# 5=3+1+1=2+2+1  p3(5)

# p[i][j]:=jをi個に分割   =pi(j)
p=[[0]*(n+1) for _ in range(m+1)]
p[0][0]=1

for i in range(1, m+1):
    for j in range(1,n+1):
        if j-i>=0:
            p[i][j]=p[i][j-i]+p[i-1][j-1]
        else:
            p[i][j]=p[i-1][j-1]


# カタラン数https://zenn.dev/koboshi/articles/306304c0381c1e
# 括弧列の個数, 二分木の個数, 対角線を跨がない経路の個数
# C_n = 2nCn/(n+1)
# 導出方法は, 対角線を跨がない経路から漸化式導出-->母関数２乗のx^n係数を注目


#########################################################
# 分割数の列挙
# num を cnt個に分割  最小値はMIN
# p=[x1, x2, .., x_cnt]  sum(x_i)=num
# abc268d

MIN=1
p_list=[]
def partition(num, cnt, p=[]):
    if cnt==0:
        if num==0:
            global p_list
            p_list.append(p)
        return

    for i in range(num-cnt*MIN+1):
        partition(num-(MIN+i), cnt-1, p+[MIN+i])

partition(5, 3)
print(p_list)

