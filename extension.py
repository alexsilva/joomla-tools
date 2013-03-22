# coding: utf-8
from xml.etree.ElementTree import ElementTree
from datetime import datetime
import threading
import filecmp
import shutil
import time
import os
from filecmp import cmpfiles

## ---------------------------------------------------------------------------
class capture_errors(object):
    def __init__(self, func):
        self.fun = func
        
    def __get__(self, inst, cls):
        def wraper(*args, **kwargs):
            try: result = self.fun(inst, *args, **kwargs)
            except Exception as err:
                inst._event.error("Error[%s] %s"%(datetime.now(), err))
                result = False
            return result
        return wraper
    
## ---------------------------------------------------------------------------
class ExtEvent(object):
    """ Base for event infos """
            
    def __init__(self):
        pass
    
    def info(self, value):
        pass
    
    def error(self, value):
        pass
    
    def stop(self, value=''):
        pass
    
## ---------------------------------------------------------------------------
class ExtBase(object):
    prefix = ""
    
    def __init__(self, name, path, joomla):
        # full path of joomla
        self.joomlaPath = joomla
        # extension name
        self.extName = name
        # extension path
        self.extPath = path
        self.root = None
        
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
        self.root =  etree.parse(xmpath)
        
    def __getitem__(self, key):
        return self.root.find(key)

## ---------------------------------------------------------------------------
class Component(ExtBase):
    type = "component"
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
    def __init__(self, name, path, joomla):
        super(Component, self).__init__(name, path, joomla)
        
        self.admin = Component.Admin(self)
        self.site = Component.Site(self)

## ---------------------------------------------------------------------------
class Plugin(ExtBase):
    type = "plugin"
    
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
    def __init__(self, name, path, joomla):
        super(Plugin, self).__init__(name, path, joomla)
        
        self.site = Plugin.Site(self)
        
    @property
    def adminFolder(self):
        return "administrator"
    
## ---------------------------------------------------------------------------
class ModelBase(object):
    
    def __init__(self, extension, event):
        self.extension = extension
        # event info interface
        self.event = event
        self.filelist = None
                
    def getFilesIn(self, folder):
        fpath = os.path.join(self.path, folder)
        content = []
        for root, dirs, files in os.walk(fpath):
            for filename in files:
                filepath = os.path.join(root, filename)
                ## usando o caminho relativo para o arquivo.
                content.append(os.path.relpath(filepath, self.path))
        return content
    
    def scanFiles(self):
        self.filelist = []
        self.filelist.extend(self.filenames)
        
        for folder in self.folders:
            self.filelist.extend(self.getFilesIn(folder))
        
        self.filelist.extend(self.languages)
        
    def check(self):
        changes = {"changed":[], "removed":[], "new":[]}
        
        for file in self.filelist:
            src, dst = self.build_path(self.path, file)
            
            if os.path.exists(src):
                if os.path.exists(dst):
                    if not filecmp.cmp(src, dst):
                        changes["changed"].append(file)
                else:
                    changes["new"].append(file)
            else:
                changes["removed"].append(file)
        return changes
    
    def build_path(self, path, file):
        relpath = os.path.dirname(file)
        filename = os.path.basename(file)
        
        src = os.path.join(path, file)
        dst = os.path.join(self.extension.joomla, self.basename, 
                           self.extension.fullname, relpath)
        
        if os.path.exists(dst):
            dst = os.path.join(dst, filename)
            
        elif os.path.exists(src):
            dst = os.path.join(self.extension.joomla, 
            os.path.dirname(self.basename), relpath)
            
            if os.path.exists(dst):
                dst = os.path.join(dst, filename)
                
            elif self.extension.type == "plugin":
                dst = os.path.join(self.extension.joomla, 
                                   self.extension.adminFolder, 
                                   relpath, filename)
            else: raise RuntimeError, "In make path"
        else: raise RuntimeError, "In make path"
        return src, dst
        
    def send(self, changes):
        path = self.path
        
        for file in changes["new"]:
            src, dst = self.build_path(path, file)
            shutil.copyfile(src, dst)
            
            self.event.info("New[%s] %s" %(datetime.now(), dst))
            
        for file in changes["changed"]:
            src, dst = self.build_path(path, file)
            shutil.copyfile(src, dst)
            
            self.event.info("Updated[%s] %s" %(datetime.now(), dst))
            
        for file in changes["removed"]:
            src, dst = self.build_path(path, file)
            if os.path.exists(dst): os.remove(dst)
            
            self.scanFiles() ## update list files
            self.event.info("Removed[%s] %s"%(datetime.now(), dst))
            
## ---------------------------------------------------------------------------
class Admin(ModelBase):
    """ struct class admin """
    def __init__(self, extension, event):
        super(Admin, self).__init__(extension, event)
        
        self.parseXml() ## refs files
        self.scanFiles() ## update list files
    
    def __getattr__(self, name):
        result = getattr(self.extension.admin, name, getattr(self.extension, name, None))
        return (result if not result is None else super(Admin,self).__getattr__(name))
    
## ---------------------------------------------------------------------------
class Site(ModelBase):
    """ struct class site """
    def __init__(self, extension, event):
        super(Site, self).__init__(extension, event)
        
        self.parseXml() ## refs files
        self.scanFiles() ## update list files
        
    def __getattr__(self, name):
        result = getattr(self.extension.site, name, getattr(self.extension, name, None))
        return (result if not result is None else super(Site,self).__getattr__(name))
        
## -----------------------------------------------------------------------------
class Runner(threading.Thread):
    """ start the work check """
        
    def __init__(self, extension=[], event=None, rate=1.0):
        super(Runner,self).__init__()
        # event info interface
        self._event = event
        
        self.extension = extension
        self.rate = rate
        
        self.extmap = self.createExtmap()
        
        self._continue = True
        self.setDaemon(True)
    
    @capture_errors
    def createExtmap(self):
        """ atualiza o timer inicial """
        extmap = {}
        for extension in self.extension:
            extmap[extension] = {}
            if hasattr(extension,"admin"):
                extmap[extension]["admin"] = Admin(extension, self._event)
            if hasattr(extension,"site"):
                extmap[extension]["site"] = Site(extension, self._event)
        return extmap
        
    def setRate(self, value):
        """ altera o valor da taxa de atualização """
        self.rate = value
    
    def stop(self):
        self._continue = False
    
    @capture_errors
    def execute(self):
        for extension in self.extension:
            admin = self.extmap[extension].get("admin",None)
            site = self.extmap[extension].get("site",None)
            
            if not admin is None: admin.send(admin.check())
            if not site is None: site.send(site.check())
        return True
        
    def run(self):
        self._event.info("Runner Started [%s]" % datetime.now())
        
        while self._continue and self.execute():
            time.sleep( self.rate ) # rate check
            
        self._event.stop("Runner Exit [%s]" % datetime.now())
        













        