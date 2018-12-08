import nuke
images = nuke.getFilename("Select Images",multiple=True)

length = len(images)
if length < 2 :
    nuke.warning("At least 2 images required to create the effect")
    nuke.message("At least 2 images required to create the effect")

i = 0
read1 = nuke.nodes.Read(file=images[i],auto_alpha=True,premultiplied=True)
transform1 = nuke.nodes.Transform()
transform1['translate'].setAnimated()
transform1['translate'].setValue([0,1080],time=1)
transform1['translate'].setValue([0,0],time=3)
transform1.setInput(0,read1)
i += 1

read2 = nuke.nodes.Read(file=images[i],auto_alpha=True,premultiplied=True)
transform2 = nuke.nodes.Transform()
transform2['translate'].setAnimated()
transform2['translate'].setValue([0,1080],time=1)
transform2['translate'].setValue([0,0],time=3)
transform2.setInput(0,read2)
timeoffset1 = nuke.nodes.TimeOffset()
timeoffset1['time_offset'].setValue(i*4)
timeoffset1.setInput(0,transform2)
i += 1

merge = nuke.nodes.Merge(inputs=[transform1, timeoffset1])

while i < length:
    read = nuke.nodes.Read(file=images[i],auto_alpha=True,premultiplied=True)
    transform = nuke.nodes.Transform()
    transform['translate'].setAnimated()
    transform['translate'].setValue([0,1080],time=1)
    transform['translate'].setValue([0,0],time=3)
    transform.setInput(0,read)
    timeoffset = nuke.nodes.TimeOffset()
    timeoffset['time_offset'].setValue(i*4)
    timeoffset.setInput(0,transform)
    merge = nuke.nodes.Merge(inputs=[merge, timeoffset])
    i += 1

motionblur = nuke.nodes.MotionBlur()
motionblur.setInput(0,merge)