# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/Tree/HL_decomposition.py
# 参考: https://info.atcoder.jp/entry/algorithm_lectures/heavy_light_decomposition

class HeavyLightDecomposition:
	def __init__(self,G):
		self.G = G
		self.N = len(self.G)
		self.parent = [0]*self.N
		self.group = [0]*self.N
		self.pos = [0]*self.N
		self.top = []
		self.depth = []
		self.arr = [0]*self.N #heavy-node上の頂点列

	def solve(self):
		G,parent,group,pos,top,depth,arr = self.G,self.parent,self.group,self.pos,self.top,self.depth,self.arr

		subtree_size = [0]*self.N
		stack = [(0,-1)]
		while stack:
			v,par = stack[-1]
			if subtree_size[v] == 0:
				subtree_size[v] = 1
				parent[v] = par
				for nv in G[v]:
					if nv == par:
						continue
					stack.append((nv,v))
			else:
				stack.pop()
				if par != -1:
					subtree_size[par] += subtree_size[v]

		K = 0
		cnt = -1
		#heavy-edge -> f = 1, light-edge -> f = 0
		stack = [(0,-1,0)]
		while stack:
			v,par,f = stack.pop()
			cnt += 1
			if f:
				#heavy-edge
				group[v],pos[v] = group[par],pos[par]+1
				arr[pos[v]] = v
			else:
				#light-edge
				K += 1
				group[v],pos[v] = K-1,cnt
				top.append(v)
				arr[pos[v]] = v
				if par < 0:
					depth.append(0)
				else:
					depth.append(depth[group[par]]+1)

			max_size,max_v = 0,-1
			for nv in G[v]:
				if nv == par:
					continue
				if subtree_size[nv] > max_size:
					max_size,max_v = subtree_size[nv],nv
			for nv in G[v]:
				if nv == par or nv == max_v:
					continue
				#light-edge
				stack.append((nv,v,0))
			if max_v != -1:
				#heavy-edge
				stack.append((max_v,v,1))

	def path(self,l,r):
		parent,group,pos,top,depth = self.parent,self.group,self.pos,self.top,self.depth

		l_path,r_path = [],[]
		while depth[group[l]] != depth[group[r]]:
			if depth[group[l]] > depth[group[r]]:
				i = group[l]
				l_path.append((pos[top[i]],pos[l]+1))
				l = parent[top[i]]
			else:
				i = group[r]
				r_path.append((pos[top[i]],pos[r]+1))
				r = parent[top[i]]

		while group[l] != group[r]:
			i = group[l]
			l_path.append((pos[top[i]],pos[l]+1))
			l = parent[top[i]]
			i = group[r]
			r_path.append((pos[top[i]],pos[r]+1))
			r = parent[top[i]]

		i,j = pos[l],pos[r]
		if i < j:
			r_path.append((i,j+1))
		else:
			l_path.append((j,i+1))

		return l_path,r_path

	def lca(self,u,v):
		parent,group,pos,top,depth = self.parent,self.group,self.pos,self.top,self.depth

		while depth[group[u]] != depth[group[v]]:
			if depth[group[u]] > depth[group[v]]:
				u = parent[top[group[u]]]
			else:
				v = parent[top[group[v]]]

		while group[u] != group[v]:
			u,v = parent[top[group[u]]],parent[top[group[v]]]

		if pos[u] < pos[v]:
			return u
		else:
			return v

	def jump(self,u,v,k):
		arr = self.arr

		l_path,r_path = self.path(u,v)
		for l,r in l_path:
			if k < r-l:
				return arr[r-1-k]
			k -= r-l
		for l,r in r_path[::-1]:
			if k < r-l:
				return arr[l+k]
			k -= r-l

		return -1