# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/最短路/Bellman-Ford.py
# https://kuruton.hatenablog.com/entry/2020/11/23/080000

def LI(): return list(map(int, input().split()))
def II(): return int(input())
"""     単一始点最短路問題
    （辺のコスト全てプラスの場合）
stからすべての頂点への最短路を計算

ベルマンフォード法 計算量 O(V*E)
"""

INF=float("inf")
V, E=LI()
# 始点，終点，コスト
Edge=[LI() for _ in range(E)]

# d[i]=min(d[j]+j~iの辺のコスト)
d=[INF]*V

def shortest_path(s):
    d[s]=0
    while True:
        update=False
        for st, to, cost in Edge:
            if d[st]!=INF and d[to]>d[st]+cost:
                d[to]=d[st]+cost
                update=True

        if not update:
            break

shortest_path(0)
print(d)



###################################
"""     負閉路検出問題
  辺のコストにマイナスが含まれる場合

負閉路があるとTrueを返す
"""

V, E=LI()
Edge=[LI() for _ in range(E)]

def find_negative_loop():
    d=[0]*V

    # 負閉路がなければ，更新はV-1回
    for i in range(V-1):
        update=False
        for st, to, cost in Edge:
            if d[st]!=INF and d[to]>d[st]+cost:
                d[to]=d[st]+cost
                update=True
        if not update:
            break

    # 更新がまだある＝負閉路が存在
    if update:
        return True
    else:
        return False



####################################
""" 単一始点最短路問題の負閉路が含まれるver
  辺のコストにマイナスが含まれる場合

負閉路で最短路が発散するものは-INF
[0, 2, -inf, -inf, -inf, -inf]
O(V*E)
"""

INF=float("inf")
V, E=LI()
Edge=[LI() for _ in range(E)]

def bellmanford(s):
    # d[i]=min(d[j]+j~iの辺のコスト)
    d=[INF]*V
    d[s]=0

    # 負閉路がなければ，更新はV-1回
    for i in range(V-1):
        update=False
        for st, to, cost in Edge:
            if d[st]!=INF and d[to]>d[st]+cost:
                d[to]=d[st]+cost
                update=True
        if not update:
            break

    # 更新がまだある＝負閉路が存在
    if update:
        for st, to, cost in Edge:
            if d[st]!=INF and d[to]>d[st]+cost:
                d[to]=-INF

        while True:
            flag=False
            for st, to, cost in Edge:
                if d[to] != -INF and d[st] == -INF:
                    d[to]=-INF
                    flag=True
            if not flag:
                break

    return d

print(bellmanford(0))