# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/Tree/二分探索木アリ本.py

# insert, find, remove がO(logN)
# 木が偏ることがあるため，最悪時間O(N)
#
# 別の方法として，listをソートしてbisectで検索
# しかし挿入がO(N)


# ノードを表す構造体
# valが値，lchとrchはそれぞれnodeで宣言する
class node:
    def __init__(self):
        self.val = None
        self.lch = None
        self.rch = None

# pを根とする二部探索木に，数xを追加
# p=Noneで初期の木構築
def insert(p, x):
    if p == None:
        q = node()
        q.val = x
        return q
    else:
        if x < p.val:
            p.lch = insert(p.lch, x)
        else:
            p.rch = insert(p.rch, x)
        return p

# pを根とする二部探索木で，xを検索ー＞True or False
def find(p, x):
    if p == None:
        return False
    elif x == p.val:
        return True
    elif x < p.val:
        return find(p.lch, x)
    else:
        return find(p.rch, x)

# 数xを削除
def remove(p, x):
    if p == None:
        return None

    # xを探索
    elif x < p.val:
        p.lch = remove(p.lch, x)
    elif x > p.val:
        p.rch = remove(p.rch, x)

    # 削除したいノードが左の子をもっていなければ，右の子をもってくる
    elif p.lch == None:
        q = p.rch
        del p
        return q
    # 削除したいノードの左の子が右の子を持っていなければ，左の子をもってくる
    elif p.lch.rch == None:
        q = p.lch
        q.rch = p.rch
        del p
        return q
    # 左の子以下で最も大きいノードをもってくる
    else:
        q = node()
        q = p.lch
        while q.rch.rch != None:
            q = q.rch
        r = q.rch
        q.rch = r.lch
        r.lch = p.lch
        r.rch = p.rch
        del p
        return r
    return p