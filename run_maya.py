import maya.cmds as cmds
import pymel.core as pmc

# print("Hello World!")

# using PyMel
pmc.spaceLocator(n = "my_loc1")
# using Maya commands
cmds.spaceLocator(n = "my_loc2")

a = pmc.PyNode("my_loc1")
cmds.AbcImport()
cmds.skinCluster()