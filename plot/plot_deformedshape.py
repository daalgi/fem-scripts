import sys
import matplotlib

for line in range(0,len(sys.argv)):
    if "ipykernel_launcher.py" in sys.argv[line]:
        matplotlib.use('nbagg')
        break
    else:
        pass

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from math import asin, sqrt

from openseespy.opensees import *

def recordNodeDisp(filename = 'nodeDisp.txt'):
	# This function is meant to be run before an analysis and saves the displacements of all nodes into filename. 
	# It can be used later in the plot_deformedshape function.
    nodeList = getNodeTags()
    if len(nodeCoord(nodeList[0])) == 2:
        dofList = [1, 2]
    if len(nodeCoord(nodeList[0])) == 3:
        dofList = [1, 2, 3]
    # recorder('Node', '-file', filename, '–time', '–node', *nodeList, '-dof', *dofList, 'disp')
    recorder('Node', '-file', filename, '–node', *nodeList, '-dof', *dofList, 'disp')

def plot_deformedshape(filename = 'nodeDisp.txt', tstep = -1, scale = 200):
	# Expected input argv : filename contains the displacements of all nodes in the same order they are returned by getNodeTags().
	# First column in filename is time. 
	# tstep is the number of the step of the analysis to be ploted (starting from 1), 
	# and scale is the scale factor for the deformed shape.

	nodeList = getNodeTags()
	eleList = getEleTags()
	nodeDispArray = np.loadtxt(filename)
	if len(nodeDispArray[0, :]) == len(nodeList) * len(nodeCoord(nodeList[0])):
		tarray = np.zeros((len(nodeDispArray), 1))
		nodeDispArray = np.append(tarray, nodeDispArray, axis = 1) 
        
	if tstep == -1:
		tstep = len(nodeDispArray)
	ele_style = {'color':'black', 'linewidth':1, 'linestyle':':'} # elements
	Disp_style = {'color':'red', 'linewidth':1, 'linestyle':'-'} # elements
	node_style = {'color':'black', 'marker':'.', 'linestyle':''} 

	def plotCubeSurf(NodeList):
			# Define procedure to plot a 3D solid element
			aNode = NodeList[0]
			bNode = NodeList[1]
			cNode = NodeList[2]
			dNode = NodeList[3]
			plt.plot((aNode[0], bNode[0], cNode[0], dNode[0], aNode[0]), 
						(aNode[1], bNode[1], cNode[1], dNode[1], aNode[1]),
						(aNode[2], bNode[2], cNode[2], dNode[2], aNode[2]), marker='', **ele_style)

			ax.plot_surface(np.array([[aNode[0], dNode[0]], [bNode[0], cNode[0]]]), 
							np.array([[aNode[1], dNode[1]], [bNode[1], cNode[1]]]), 
							np.array([[aNode[2], dNode[2]], [bNode[2], cNode[2]]]), color='g', alpha=.5)
#
	# Check if the model is 2D or 3D
	if len(nodeCoord(nodeList[0])) == 2:
		print('2D model')
		x = []
		y = []
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		for element in eleList:
			Nodes = eleNodes(element)
			if len(Nodes) == 2:
				# 3D Beam-Column Elements
				iNode = nodeCoord(Nodes[0])
				jNode = nodeCoord(Nodes[1])
				iNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[0])*2 + 1: nodeList.index(Nodes[0])*2 + 3]
				jNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[1])*2 + 1: nodeList.index(Nodes[1])*2 + 3]

				# Get final node coordinates
				iNode_final = [iNode[0]+ scale*iNode_Disp[0], iNode[1]+ scale*iNode_Disp[1]]
				jNode_final = [jNode[0]+ scale*jNode_Disp[0], jNode[1]+ scale*jNode_Disp[1]]

				x.append(iNode_final[0])  # list of x coordinates to define plot view area
				y.append(iNode_final[1])	# list of y coordinates to define plot view area

				plt.plot((iNode[0], jNode[0]), (iNode[1], jNode[1]),marker='', **ele_style)
				plt.plot((iNode_final[0], jNode_final[0]), 
							(iNode_final[1], jNode_final[1]),marker='', **Disp_style)

			if len(Nodes) == 3:
				# 2D Planer three-node shell elements
				iNode = nodeCoord(Nodes[0])
				jNode = nodeCoord(Nodes[1])
				kNode = nodeCoord(Nodes[2])
				iNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[0])*2 + 1: nodeList.index(Nodes[0])*2 + 3]
				jNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[1])*2 + 1: nodeList.index(Nodes[1])*2 + 3]
				kNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[2])*2 + 1: nodeList.index(Nodes[2])*2 + 3]				# Get final node coordinates
				iNode_final = [iNode[0]+ scale*iNode_Disp[0], iNode[1]+ scale*iNode_Disp[1]]
				jNode_final = [jNode[0]+ scale*jNode_Disp[0], jNode[1]+ scale*jNode_Disp[1]]
				kNode_final = [kNode[0]+ scale*kNode_Disp[0], kNode[1]+ scale*kNode_Disp[1]]

				x.append(iNode_final[0])  # list of x coordinates to define plot view area
				y.append(iNode_final[1])	# list of y coordinates to define plot view area

				plt.plot((iNode[0], jNode[0], kNode[0]), (iNode[1], jNode[1], kNode[1]),marker='', **ele_style)

				plt.plot((iNode_final[0], jNode_final[0], kNode_final[0]), (iNode_final[1], jNode_final[1], kNode_final[1]),marker='', **Disp_style)
				ax.fill([iNode_final[0], jNode_final[0], kNode_final[0]],[iNode_final[1], jNode_final[1], kNode_final[1]],"b", alpha=.6)


			if len(Nodes) == 4:
				# 2D Planer four-node shell elements
				iNode = nodeCoord(Nodes[0])
				jNode = nodeCoord(Nodes[1])
				kNode = nodeCoord(Nodes[2])
				lNode = nodeCoord(Nodes[3])
				iNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[0])*2 + 1: nodeList.index(Nodes[0])*2 + 3]
				jNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[1])*2 + 1: nodeList.index(Nodes[1])*2 + 3]
				kNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[2])*2 + 1: nodeList.index(Nodes[2])*2 + 3]
				lNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[3])*2 + 1: nodeList.index(Nodes[3])*2 + 3]

				# Get final node coordinates
				iNode_final = [iNode[0]+ scale*iNode_Disp[0], iNode[1]+ scale*iNode_Disp[1]]
				jNode_final = [jNode[0]+ scale*jNode_Disp[0], jNode[1]+ scale*jNode_Disp[1]]
				kNode_final = [kNode[0]+ scale*kNode_Disp[0], kNode[1]+ scale*kNode_Disp[1]]
				lNode_final = [lNode[0]+ scale*lNode_Disp[0], lNode[1]+ scale*lNode_Disp[1]]

				x.append(iNode_final[0])  # list of x coordinates to define plot view area
				y.append(iNode_final[1])	# list of y coordinates to define plot view area

				plt.plot((iNode[0], jNode[0], kNode[0], lNode[0]), (iNode[1], jNode[1], kNode[1], lNode[1]),marker='', **ele_style)
				plt.plot((iNode_final[0], jNode_final[0], kNode_final[0], lNode_final[0]), (iNode_final[1], jNode_final[1], kNode_final[1], lNode_final[1]),marker='', **Disp_style)
				ax.fill([iNode_final[0], jNode_final[0], kNode_final[0], lNode_final[0]],[iNode_final[1], jNode_final[1], kNode_final[1], lNode_final[1]],"b", alpha=.6)


		nodeMins = np.array([min(x),min(y)])
		nodeMaxs = np.array([max(x),max(y)])

		xViewCenter = (nodeMins[0]+nodeMaxs[0])/2
		yViewCenter = (nodeMins[1]+nodeMaxs[1])/2
		view_range = max(max(x)-min(x), max(y)-min(y))
		ax.set_xlim(xViewCenter-(1.1*view_range/1), xViewCenter+(1.1*view_range/1))
		ax.set_ylim(yViewCenter-(1.1*view_range/1), yViewCenter+(1.1*view_range/1))
		ax.text(0.05, 0.95, "Deformed shape ", transform=ax.transAxes)

	if len(nodeCoord(nodeList[0])) == 3:
		print('3D model')
		x = []
		y = []
		z = []
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1, projection='3d')
		for element in eleList:
			Nodes = eleNodes(element)
			if len(Nodes) == 2:
				# 3D beam-column elements
				iNode = nodeCoord(Nodes[0])
				jNode = nodeCoord(Nodes[1])
				iNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[0])*3 + 1: nodeList.index(Nodes[0])*3 + 4]
				jNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[1])*3 + 1: nodeList.index(Nodes[1])*3 + 4]
				# Add original and deformed shape to get final node coordinates
				iNode_final = [iNode[0]+ scale*iNode_Disp[0], iNode[1]+ scale*iNode_Disp[1], iNode[2]+ scale*iNode_Disp[2]]
				jNode_final = [jNode[0]+ scale*jNode_Disp[0], jNode[1]+ scale*jNode_Disp[1], jNode[2]+ scale*jNode_Disp[2]]

				x.append(iNode_final[0])  # list of x coordinates to define plot view area
				y.append(iNode_final[1])	# list of y coordinates to define plot view area
				z.append(iNode_final[2])	# list of z coordinates to define plot view area

				plt.plot((iNode[0], jNode[0]), (iNode[1], jNode[1]),(iNode[2], jNode[2]), marker='', **ele_style)
				plt.plot((iNode_final[0], jNode_final[0]), (iNode_final[1], jNode_final[1]),(iNode_final[2], jNode_final[2]), 
					marker='', **Disp_style)

			if len(Nodes) == 4:
				# 3D four-node Quad/shell element
				iNode = nodeCoord(Nodes[0])
				jNode = nodeCoord(Nodes[1])
				kNode = nodeCoord(Nodes[2])
				lNode = nodeCoord(Nodes[3])
				iNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[0])*3 + 1: nodeList.index(Nodes[0])*3 + 4]
				jNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[1])*3 + 1: nodeList.index(Nodes[1])*3 + 4]
				kNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[2])*3 + 1: nodeList.index(Nodes[2])*3 + 4]
				lNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[3])*3 + 1: nodeList.index(Nodes[3])*3 + 4]

				# Add original and mode shape to get final node coordinates
				iNode_final = [iNode[0]+ scale*iNode_Disp[0], iNode[1]+ scale*iNode_Disp[1], iNode[2]+ scale*iNode_Disp[2]]
				jNode_final = [jNode[0]+ scale*jNode_Disp[0], jNode[1]+ scale*jNode_Disp[1], jNode[2]+ scale*jNode_Disp[2]]
				kNode_final = [kNode[0]+ scale*kNode_Disp[0], kNode[1]+ scale*kNode_Disp[1], kNode[2]+ scale*kNode_Disp[2]]
				lNode_final = [lNode[0]+ scale*lNode_Disp[0], lNode[1]+ scale*lNode_Disp[1], lNode[2]+ scale*lNode_Disp[2]]


				plt.plot((iNode[0], jNode[0], kNode[0], lNode[0], iNode[0]), 
							(iNode[1], jNode[1], kNode[1], lNode[1], iNode[1]),
							(iNode[2], jNode[2], kNode[2], lNode[2], iNode[2]), marker='', **ele_style)

				plt.plot((iNode_final[0], jNode_final[0], kNode_final[0], lNode_final[0], iNode_final[0]), 
							(iNode_final[1], jNode_final[1], kNode_final[1], lNode_final[1], iNode_final[1]),
							(iNode_final[2], jNode_final[2], kNode_final[2], lNode_final[2], iNode_final[2]), 
								marker='', **Disp_style)
				# Plot surfaces on the mode shape
				ax.plot_surface(np.array([[iNode_final[0], lNode_final[0]], [jNode_final[0], kNode_final[0]]]), 
								np.array([[iNode_final[1], lNode_final[1]], [jNode_final[1], kNode_final[1]]]), 
								np.array([[iNode_final[2], lNode_final[2]], [jNode_final[2], kNode_final[2]]]), 
									color='g', alpha=.6)

			if len(Nodes) == 8:
				# 3D eight-node Brick element
				# Nodes in CCW on bottom (0-3) and top (4-7) faces resp
				iNode = nodeCoord(Nodes[0])
				jNode = nodeCoord(Nodes[1])
				kNode = nodeCoord(Nodes[2])
				lNode = nodeCoord(Nodes[3])
				iiNode = nodeCoord(Nodes[4])
				jjNode = nodeCoord(Nodes[5])
				kkNode = nodeCoord(Nodes[6])
				llNode = nodeCoord(Nodes[7])

				iNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[0])*3 + 1: nodeList.index(Nodes[0])*3 + 4]
				jNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[1])*3 + 1: nodeList.index(Nodes[1])*3 + 4]
				kNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[2])*3 + 1: nodeList.index(Nodes[2])*3 + 4]
				lNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[3])*3 + 1: nodeList.index(Nodes[3])*3 + 4]
				iiNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[4])*3 + 1: nodeList.index(Nodes[4])*3 + 4]
				jjNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[5])*3 + 1: nodeList.index(Nodes[5])*3 + 4]
				kkNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[6])*3 + 1: nodeList.index(Nodes[6])*3 + 4]
				llNode_Disp = nodeDispArray[tstep - 1, nodeList.index(Nodes[7])*3 + 1: nodeList.index(Nodes[7])*3 + 4]

				# Add original and mode shape to get final node coordinates
				iNode_final = [iNode[0]+ scale*iNode_Disp[0], iNode[1]+ scale*iNode_Disp[1], iNode[2]+ scale*iNode_Disp[2]]
				jNode_final = [jNode[0]+ scale*jNode_Disp[0], jNode[1]+ scale*jNode_Disp[1], jNode[2]+ scale*jNode_Disp[2]]
				kNode_final = [kNode[0]+ scale*kNode_Disp[0], kNode[1]+ scale*kNode_Disp[1], kNode[2]+ scale*kNode_Disp[2]]
				lNode_final = [lNode[0]+ scale*lNode_Disp[0], lNode[1]+ scale*lNode_Disp[1], lNode[2]+ scale*lNode_Disp[2]]
				iiNode_final = [iiNode[0]+ scale*iiNode_Disp[0], iiNode[1]+ scale*iiNode_Disp[1], iiNode[2]+ scale*iiNode_Disp[2]]
				jjNode_final = [jjNode[0]+ scale*jjNode_Disp[0], jjNode[1]+ scale*jjNode_Disp[1], jjNode[2]+ scale*jjNode_Disp[2]]
				kkNode_final = [kkNode[0]+ scale*kkNode_Disp[0], kkNode[1]+ scale*kkNode_Disp[1], kkNode[2]+ scale*kkNode_Disp[2]]
				llNode_final = [llNode[0]+ scale*llNode_Disp[0], llNode[1]+ scale*llNode_Disp[1], llNode[2]+ scale*llNode_Disp[2]]

				plotCubeSurf([iNode_final, jNode_final, kNode_final, lNode_final])
				plotCubeSurf([iNode_final, jNode_final, jjNode_final, iiNode_final])
				plotCubeSurf([iiNode_final, jjNode_final, kkNode_final, llNode_final])
				plotCubeSurf([lNode_final, kNode_final, kkNode_final, llNode_final])
				plotCubeSurf([jNode_final, kNode_final, kkNode_final, jjNode_final])
				plotCubeSurf([iNode_final, lNode_final, llNode_final, iiNode_final])

		nodeMins = np.array([min(x),min(y),min(z)])
		nodeMaxs = np.array([max(x),max(y),max(z)])
		xViewCenter = (nodeMins[0]+nodeMaxs[0])/2
		yViewCenter = (nodeMins[1]+nodeMaxs[1])/2
		zViewCenter = (nodeMins[2]+nodeMaxs[2])/2
		view_range = max(max(x)-min(x), max(y)-min(y), max(z)-min(z))
		ax.set_xlim(xViewCenter-(view_range/4), xViewCenter+(view_range/4))
		ax.set_ylim(yViewCenter-(view_range/4), yViewCenter+(view_range/4))
		ax.set_zlim(zViewCenter-(view_range/3), zViewCenter+(view_range/3))
		ax.text2D(0.10, 0.95, "Deformed shape ", transform=ax.transAxes)

	plt.axis('off')
	plt.show()
	return fig
