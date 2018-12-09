"""
    File name: marvel.py
    Author: Kuntal Majumder
"""

import nuke
images = nuke.getFilename("Select Images",multiple=True)

length = len(images)
if length < 2 :
    nuke.warning("At least 2 images required to create the effect")
    nuke.message("At least 2 images required to create the effect")

def get_transform(height):
    """The transform node does the animation of dropping the image"""
    transform = nuke.nodes.Transform()
    transform['translate'].setAnimated()
    transform['translate'].setValue([0,height],time=1)
    transform['translate'].setValue([0,0],time=3)
    return transform

def get_reformat():
    """Resizes the image according to the project settings"""
    reformat = nuke.nodes.Reformat()
    reformat['resize'].setValue('fill')
    return reformat

def get_timeoffset(pos):
    """Shifts the image to the given position in the timeline"""
    timeoffset = nuke.nodes.TimeOffset()
    timeoffset['time_offset'].setValue(pos*4)
    return timeoffset

def manipulate_node(filename,pos):
    """The man who generates the node graph"""
    read = nuke.nodes.Read(file=images[i],auto_alpha=True,premultiplied=True)
    reformat = get_reformat()
    reformat.setInput(0,read)

    """Crops the node if it is larger to avoid residue while it is off the screen"""
    crop = nuke.nodes.Crop()
    crop.setInput(0,reformat)
    transform = get_transform(read['format'].value().height())
    transform.setInput(0,crop)
    timeoffset = get_timeoffset(pos)
    timeoffset.setInput(0,transform)
    return timeoffset
    
i = 0
merge = manipulate_node(images[i],i)
i += 1

while i < length:
    node = manipulate_node(images[i],i)
    merge = nuke.nodes.Merge(inputs=[merge, node])
    i += 1

# A generic touch to make it similar to the original one,
# a trick which really makes difference, have to play with
# the shutter samples for more accuracy
motionblur = nuke.nodes.MotionBlur()
motionblur.setInput(0,merge)

# For keeping track of the nodegraph if you have too many pictures
motionblur.setSelected(True)
