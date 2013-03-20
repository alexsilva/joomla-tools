# coding: utf-8
import sys, os

# insert parent dir in path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import extension

## -----------------------------------------------------------------------------
class Event(extension.ExtEvent):
    """ interface test """
    
    def __init__(self):
        super(Event, self).__init__()
        
    def set(self, info):
        print info

## -----------------------------------------------------------------------------
if __name__ == "__main__":
    event = Event()
    
    name = "pbevents"
    joomla = "C:\wamp\www\web"
    
    path = os.path.join(os.getcwd(), "com_pbevents_0.3")
    component = extension.Component(name, path, joomla)
    
    path = os.path.join(path,"plugin")
    plugin = extension.Plugin(name, path, joomla)
    
    extension.start([component, plugin], True)
    print "Working..."