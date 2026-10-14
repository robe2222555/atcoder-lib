# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/組み合わせ/組み合わせ列挙.py


L=[1,2,33,4]

# 順列列挙
from itertools import permutations
P=permutations(L, r=None)

# 組み合わせ列挙
from itertools import combinations
C=combinations(L, r=1)

# 直積集合
from itertools import product
Pr=product(L, r=1)