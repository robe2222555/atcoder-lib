# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/組み合わせ/個数制限重複組み合わせ.py

# 個数制限ありの重複組み合わせ
# i番目のものがA[i]個あるときにj個とる組み合わせ
# O(nm)

n, m = 3,3
A = [1,2,3]
mod=10**9+7

# dp[i][j]:=0~iのものを合計j個とってくる重複組み合わせ
# dp[i][j] =   (dp[i-1][j])　     + (dp[i][j-1]-dp[i-1][j-ai-1])
#        (ものiが入っていない通り) +    (ものiが入っている通り)

# dp[i-1][j] : 0~i-1でj個とる通り
# dp[i][j-1] : 最初にiを1個とり，残りを全通りでとったもの　　iをai+1個とってしまう通りが含まれている
# dp[i-1][j-ai-1] : 最初にiをai+1個とり，残りを全通りとったもの
dp = [[0]*(m+1) for _ in range(n)]

for j in range(A[0]+1):
    dp[0][j]=1

for i in range(1, n):
    dp[i][0]=1
    for j in range(1,m+1):
        if j-A[i]-1>=0:
            dp[i][j]=(dp[i-1][j]+dp[i][j-1]-dp[i-1][j-A[i]-1]) % mod
        else:
            dp[i][j]=(dp[i-1][j]+dp[i][j-1]) % mod




######################################################
# 上限が等しいときの重複組み合わせ
# A[0]=A[1]=...=A[n-1]=a





# 重複組み合わせと母関数
# https://qiita.com/saikyouyaki/items/4a010b68b47445e203e8