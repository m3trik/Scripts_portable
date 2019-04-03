


convert component selection type

obj = selection[1] --get selected object

vertices = getVertSelection obj --get selected Vertices
edges = polyop.getEdgesUsingVert obj vertices

setEdgeSelection obj edges --select the edges

max modify mode --switch to Modify panel
subObjectLevel =2 --edge selection mode
select(edges)





