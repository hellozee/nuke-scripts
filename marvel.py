import nuke
images = nuke.getFilename("Select Images",multiple=True)

length = len(images)
if length < 2 :
    nuke.warning("At least 2 images required to create the effect")
    nuke.message("At least 2 images required to create the effect")

def get_transform(height):
    transform = nuke.nodes.Transform()
    transform['translate'].setAnimated()
    transform['translate'].setValue([0,height],time=1)
    transform['translate'].setValue([0,0],time=3)
    return transform

def get_reformat():
    reformat = nuke.nodes.Reformat()
    reformat['resize'].setValue('fill')
    return reformat

def get_timeoffset(pos):
    timeoffset = nuke.nodes.TimeOffset()
    timeoffset['time_offset'].setValue(pos*4)
    return timeoffset

def manipulate_node(filename,pos):
    read = nuke.nodes.Read(file=images[i],auto_alpha=True,premultiplied=True)
    reformat = get_reformat()
    reformat.setInput(0,read)
    crop = nuke.nodes.Crop()
    crop.setInput(0,reformat)
    transform = get_transform(read['format'].value().height())
    transform.setInput(0,crop)
    timeoffset = get_timeoffset(pos)
    timeoffset.setInput(0,transform)
    return timeoffset
    
i = 0
node1 = manipulate_node(images[i],i)
i += 1
node2 = manipulate_node(images[i],i)
i += 1
merge = nuke.nodes.Merge(inputs=[node1, node2])

while i < length:
    node = manipulate_node(images[i],i)
    merge = nuke.nodes.Merge(inputs=[merge, node])
    i += 1

motionblur = nuke.nodes.MotionBlur()
motionblur.setInput(0,merge)
motionblur.setSelected(True)
