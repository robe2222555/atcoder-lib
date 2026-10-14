# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/Tree/根付き木.py
# 273-E

class Tree:
    def __init__(self):
        self.node=0
        self.Par=[]     # 節点iの親
        self.Value=[]   # iの値
        self.Root=[]    # 根の集合

    # 節点xに新たな節点(self.node)を接続
    # x=-1ならば，根を設定
    def add(self, val, x=-1):
        self.Value.append(val)
        self.Par.append(x)
        self.Root.append(self.node)
        self.node+=1

    # 葉xを削除
    def delete(self, x):
        self.Par[x]=-2