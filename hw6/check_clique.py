import sys
import networkx as nx
if len(sys.argv) != 3:
	print("usage: python check_clique.py [graph] [nodes]")
graph_data = sys.argv[1]
node_data = sys.argv[2]
with open(node_data,'r') as f, open(graph_data,'r') as g:
	UG=nx.Graph()
	nodes = [ line.strip() for line in f.readlines() if line!="\n"]
	for line in g.readlines():
		n=line.strip().split(' ')
		if not UG.has_edge(n[0],n[1]):
			UG.add_edge(n[0],n[1])
	is_clique=True
	for n1 in nodes:
		check_edge=sum([not UG.has_edge(n1,n2) for n2 in nodes if n1!=n2])
		if check_edge != 0:
			print("This is \'not\' a clique !")
			is_clique=False
			break
	if is_clique:
		print("This is a clique !")
		
