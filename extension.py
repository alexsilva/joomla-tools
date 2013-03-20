# coding: utf-8
from xml.etree.ElementTree import ElementTree
from datetime import datetime
import threading
import shutil
import time
import os


## ---------------------------------------------------------------------------
class ExtEvent(object):
    """ Base for event infos """
    def __init__(self):
        pass
    
    def set(self, info):
        pass
    
## ---------------------------------------------------------------------------
class ExtBase(object):
    prefix = ""
    
    def __init__(self, name, path, joomla, event):
        # full path of joomla
        self.joomlaPath = joomla
        # extension name
        self.extName = name
        # extension path
        self.extPath = path
        # event info interface
        self.event = event
        
        self.root = self.parseXml()
        
    @property
    def name(self):
        return self.extName
    @property
    def joomla(self):
        return self.joomlaPath
    @property
    def path(self):
        return self.extPath
    @property
    def fullname(self):
        return self.prefix +self.name
    
    def parseXml(self):
        etree = ElementTree()
        xmpath = os.path.join(self.path, self.name+".xml")
        return etree.parse(xmpath)
    
    def __getitem__(self, key):
        return self.root.find(key)

## ---------------------------------------------------------------------------
class Component(ExtBase):
    prefix = "com_"
    
    ## -----------------------------------------------------------------------
    class Admin(object):
        basename = os.path.join("administrator", "components")
        
        def __init__(self, extension):
            self.extension = extension
            
        def __getitem__(self, key):
            return self.extension["administration"].find(key)
        
        @property
        def folder(self):
            return self["files"].get("folder")
        
        @property
        def folders(self):
            files = self["files"]
            return [e.text for e in (files.findall("folder") if not files is None else [])]
            
        @property
        def filenames(self):
            files = self["files"]
            return [e.text for e in (files.findall("filename") if not files is None else [])]
        
        @property
        def languages(self):
            lang = self["languages"]
            return [e.text.replace("/",os.sep) for e in (lang.findall("language") if not lang is None else [])]
        
        @property
        def path(self):
            return os.path.join(self.extension.path, self.folder)
        
    ## -----------------------------------------------------------------------
    class Site(object):
        basename = "components"
        
        def __init__(self, extension):
            self.extension = extension
            
        def __getitem__(self, key):
            return self.extension[key]
        
        @property
        def folder(self):
            return self["files"].get("folder")
            
        @property
        def folders(self):
            files = self["files"]
            return [e.text for e in (files.findall("folder") if not files is None else [])]
        
        @property
        def filenames(self):
            files = self["files"]
            return [e.text for e in (files.findall("filename") if not files is None else [])]
        
        @property
        def languages(self):
            lang = self["languages"]
            return [e.text.replace("/",os.sep) for e in (lang.findall("language") if not lang is None else [])]
        
        @property
        def path(self):
            return os.path.join(self.extension.path, self.folder)
        
    ## -----------------------------------------------------------------------
    def __init__(self, name, path, joomla, event):
        super(Component, self).__init__(name, path, joomla, event)
        
        self.admin = Component.Admin(self)
        self.site = Component.Site(self)

## ---------------------------------------------------------------------------
class Plugin(ExtBase):
    
    class Site(object):
        def __init__(self, extension):
            self.extension = extension
        
        @property
        def basename(self):
            return os.path.join("plugins", self.extension.root.get("group"))
            
        def __getitem__(self, key):
            return self.extension[key]
        
        @property
        def folder(self):
            return ""
        
        @property
        def folders(self):
            files = self["files"]
            return [e.text for e in (files.findall("folder") if not files is None else [])]
            
        @property
        def filenames(self):
            files = self["files"]
            return [e.text for e in (files.findall("filename") if not files is None else [])]
        
        @property
        def languages(self):
            lang = self["languages"]
            return [e.text.replace("/",os.sep) for e in (lang.findall("language") if not lang is None else [])]
        
        @property
        def path(self):
            path = os.path.join(self.extension.path, self.folder)
            path = path.rstrip("/").rstrip(os.sep)
            return path
        
    ## -----------------------------------------------------------------------
    def __init__(self, name, path, joomla, event):
        super(Plugin, self).__init__(name, path, joomla, event)
        
        self.site = Plugin.Site(self)

## ---------------------------------------------------------------------------
class ModelBase(object):
    def __init__(self, extension):
        self.extension = extension
        self.conf = {}
    
    def filesIn(self, folder):
        fpath = os.path.join(self.path, folder)
        content = []
        for root, dirs, files in os.walk(fpath):
            for filename in files:
                filepath = os.path.join(root, filename)
                content.append(filepath)
        return content
    
    def updateDir(self, path, mtime=0.0):
        for filepath in self.filesIn(path.replace(self.path+os.sep,'')):
            relpath = filepath.replace(self.path+os.sep,'')
            self.conf[relpath] = os.path.getmtime(filepath)+mtime
        
    def update(self):
        path = self.path
        
        for filename in self.filenames:
            filepath = os.path.join(path, filename)
            self.conf[filename] = os.path.getmtime(filepath)
            
        for folder in self.folders:
            for filepath in self.filesIn(folder):
                relpath = filepath.replace(self.path+os.sep,'')
                self.conf[relpath] = os.path.getmtime(filepath)
                
        for lang in self.languages:
            lpath = os.path.join(self.path, lang)
            self.conf[lang] = os.path.getmtime(lpath)
            
    def check(self):
        changes = {"changed":[],"removed":[]}
        for path in self.conf.copy():
            filepath = os.path.join(self.path, path)
            if os.path.exists(filepath):
                if self.conf[path] != os.path.getmtime(filepath):
                    changes["changed"].append(path)
            else:
                changes["removed"].append(path)
                # reindexando a pasta do arquivo não econtrado.
                self.updateDir(os.path.dirname(filepath), 0.001)
        return changes
        
    def send(self, changes):
        path = self.path
        
        def build_path(file):
            relpath = os.path.dirname(file)
            filename = os.path.basename(file)
            src = os.path.join(path, file)
            dst = os.path.join(self.extension.joomla, self.basename, 
                               self.extension.fullname, relpath)
            if os.path.exists(dst):
                dst = os.path.join(dst, filename)
                
            elif os.path.exists(src):
               dst = os.path.join(self.extension.joomla, os.path.dirname(self.basename), 
                                  relpath, filename)
            else:
                raise RuntimeError, "In make path"
            return src, dst
            
        for file in changes["changed"]:
            src, dst = build_path(file)
            shutil.copyfile(src, dst)
            self.conf[file] = os.path.getmtime(src)
            self.event.set("Updated[%s] %s" %(datetime.now(), dst))
            
        for file in changes["removed"]:
            src, dst = build_path(file)
            if os.path.exists(dst): os.remove(dst)
            # remove o arquivo da atualização.
            self.conf.pop(file, None)
            self.event.set("Removed[%s] %s"%(datetime.now(), dst))
            
## ---------------------------------------------------------------------------
class Admin(ModelBase):
    def __init__(self, extension):
        super(Admin, self).__init__(extension)
        
        for key in dir(extension.admin):
            if key.startswith("__"): continue # private data
            setattr(self, key, getattr(extension.admin, key))
            
## ---------------------------------------------------------------------------
class Site(ModelBase):
    def __init__(self, extension):
        super(Site, self).__init__(extension)
        
        for key in dir(extension.site):
            if key.startswith("__"): continue # private data
            setattr(self, key, getattr(extension.site, key))

## -----------------------------------------------------------------------------
class Runner(threading.Thread):
    """ start the work check """
    def __init__(self, extension=[], rate=1.0):
        super(Runner,self).__init__()
        
        self.extension = extension
        self.rate = rate
        
        self.extmap = self.createExtmap()
        self._continue = True
        
    def createExtmap(self):
        """ atualiza o timer inicial """
        extmap = {}
        for extension in self.extension:
            extmap[extension] = {}
            
            if hasattr(extension,"admin"):
                extmap[extension]["admin"] = Admin(extension)
                extmap[extension]["admin"].update()
            
            if hasattr(extension,"site"):
                extmap[extension]["site"] = Site(extension)
                extmap[extension]["site"].update()
        return extmap
        
    def stop(self):
        self._continue = False
        
    def run():
        while self._continue:
            for extension in self.extension:
                admin =  self.extmap[extension].get("admin",None)
                site =  self.extmap[extension].get("site",None)
                if not admin is None: admin.send(admin.check())
                if not site is None: site.send(site.check())
            time.sleep( self.rate ) # rate check
    














        