from math import pi, sin, cos, radians

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
# from direct.interval.IntervalGlobal import Sequence
# from panda3d.core import Point3


class MyApp(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        
        self.scene = Actor("./boxes.bam", {"walk": "./boxes_squish.bam"})
        
        self.scene.reparentTo(self.render)
        # self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(0, 5,0)
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.scene.loop("walk")
        
    def spinCameraTask(self, task):
        angleDegrees = task.time * 12.0
        angleRadians = radians(angleDegrees)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians),3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()

