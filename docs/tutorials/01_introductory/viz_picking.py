
"""
=====================
Simple picking
=====================

Here we present a tutorial of picking objects in the 3D world.

"""

import numpy as np
from fury import actor, window, ui, utils

xyzr = np.array([[0, 0, 0, 10], [100, 0, 0, 50], [200, 0, 0, 100]])

colors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1.]])

###############################################################################
# Let's create a panel to show what is picked

panel = ui.Panel2D(size=(200, 150), color=(1, 1, 1), align="right")
panel.center = (150, 200)

text_block = ui.TextBlock2D(text="Pick")
panel.add_element(text_block, (0.3, 0.3))

###############################################################################
# Build scene and add an actor with many objects.

scene = window.Scene()

sphere_actor = actor.sphere(centers=0.5 * xyzr[:, :3],
                            colors=colors[:],
                            radii=0.1 * xyzr[:, 3])


vertices = utils.vertices_from_actor(sphere_actor)
num_vertices = vertices.shape[0]
num_objects = xyzr.shape[0]


scene.add(sphere_actor)
scene.reset_camera()

global showm

global picker
picker = window.vtk.vtkCellPicker()


def left_click_callback(obj, event):

    global text_block, showm, picker
    x, y, z = obj.GetCenter()
    event_pos = showm.iren.GetEventPosition()

    picker.Pick(event_pos[0], event_pos[1],
                0, showm.scene)

    cell_index = picker.GetCellId()
    point_index = picker.GetPointId()
    text = 'Object ' + str(np.floor((point_index/num_vertices) * num_objects)) + '\n'
    text += 'Point ID ' + str(point_index) + '\n'
    text += 'Face ID ' + str(cell_index)
    text_block.message = text
    showm.render()


sphere_actor.AddObserver('LeftButtonPressEvent', left_click_callback, 1)

showm = window.ShowManager(scene, size=(1024, 768), order_transparent=True)

showm.initialize()
scene.add(panel)
showm.start()
