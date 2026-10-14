

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