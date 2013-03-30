# coding: utf-8
from xml.etree.ElementTree import ElementTree
from datetime import datetime
import threading
import filecmp
import shutil
import time
import os

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
    
    def changes(self, value):
        pass
    
## ---------------------------------------------------------------------------
class Defs(object):
    ADMIN_FOLDER = "administrator"
    SITE_FOLDER = "." # root joomla
    
    COMPONENT = "COMPONENT"
    COMPONENT_ADMIN_SIDE = "COMP_ADMIN"
    COMPONENT_SITE_SIDE = "COMP_SITE"
    
    PLUGIN = "PLUGIN"
    PLUGIN_ADMIN_SIDE = "PLG_ADMIN"
    PLUGIN_SITE_SIDE = "PLG_SITE"
    
    MODULE = "MODULE"
    MODULE_ADMIN_SIDE = "MOD_ADMIN"
    MODULE_SITE_SIDE = "MOD_SITE"
    
## ---------------------------------------------------------------------------
class ExtBase(object):
    prefix = ""
    
    def __init__(self, name, path, joomla, event):
        self.root = self.admin = self.site = None
        # full path of joomla
        self.joomlaPath = joomla
        # extension name
        self.extName = name
        # extension path
        self.extPath = path
        self.event = event
        
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
    
    def start(self):
        self.root = self.parseXml() ## refs files
        
        if not self.admin is None:
            self.admin.scanFiles() ## update list files
            
        if not self.site is None:
            self.site.scanFiles() ## update list files
        
## ---------------------------------------------------------------------------
class ASBase(object):
    
    def __init__(self, extension):
        self.extension = extension
        self.filelist = None
        
    def __getattr__(self, name):
        return (getattr(self.extension, name, None) if hasattr(self.extension, name) else 
                        super(ASBase, self).__getattr__(name))
        
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
            src, dst = self.buildPath(self.path, file)
            
            if os.path.exists(src):
                if os.path.exists(dst):
                    if not filecmp.cmp(src, dst):
                        changes["changed"].append(file)
                else:
                    changes["new"].append(file)
            else:
                changes["removed"].append(file)
        return changes
    
    def isLanguage(self, path):
        return path.startswith("language")
    
    def buildPath(self, path, file, join=True):
        relpath = os.path.dirname(file)
        filename = os.path.basename(file)
        src = os.path.join(path, file)
        
        if self.extension.type == Defs.COMPONENT:
            if self.isLanguage(relpath):
                dst = os.path.join(self.extension.joomla, os.path.dirname(self.basename), relpath)
            else:
                dst = os.path.join(self.extension.joomla, self.basename, 
                                   self.extension.fullname, relpath)
                
        elif self.extension.type == Defs.PLUGIN:
            if self.isLanguage(relpath):
                dst = os.path.join(self.extension.joomla, Defs.ADMIN_FOLDER, relpath)
            else:
                dst = os.path.join(self.extension.joomla, self.basename, 
                                   self.extension.fullname, relpath)
                
        elif self.extension.type == Defs.MODULE:
            if self.isLanguage(relpath):
                dst = os.path.join(self.extension.joomla, os.path.dirname(self.basename), relpath)
            else:
                dst = os.path.join(self.extension.joomla, self.basename, 
                                   self.extension.fullname, relpath)
                
        else: raise RuntimeError, "In make path: Type error!"
        
        if join: dst = os.path.join(dst, filename)
        else: dst = {"d": dst, "f": filename}
        
        return src, dst
        
    def send(self, changes):
        path = self.path
        
        for file in changes["new"]:
            src, dst = self.buildPath(path, file, False)
            
            # contrói os diretórios necessários.
            if not os.path.exists(dst["d"]):
                os.makedirs(dst["d"])
            
            dst = os.path.join(dst["d"], dst["f"])
            shutil.copyfile(src, dst)
            
            self.event.info("[%s] New: %s" %(datetime.now(), dst))
            
        for file in changes["changed"]:
            src, dst = self.buildPath(path, file)
            shutil.copyfile(src, dst)
            
            self.event.changes("[%s] Updated: %s" %(datetime.now(), dst))
            
        for file in changes["removed"]:
            src, dst = self.buildPath(path, file)
            if os.path.exists(dst): os.remove(dst)
            
            self.scanFiles() ## update list files
            self.event.info("[%s] Removed: %s"%(datetime.now(), dst))
            
## ---------------------------------------------------------------------------
class Component(ExtBase):
    type = Defs.COMPONENT
    prefix = "com_"
    
    ## -----------------------------------------------------------------------
    class Admin(ASBase):
        basename = os.path.join("administrator", "components")
        side = Defs.COMPONENT_ADMIN_SIDE
        
        def __init__(self, extension):
            super(Component.Admin, self).__init__(extension)
            
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
    class Site(ASBase):
        basename = "components"
        side = Defs.COMPONENT_SITE_SIDE
        
        def __init__(self, extension):
            super(Component.Site, self).__init__(extension)
            
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
    type = Defs.PLUGIN
    
    class Site(ASBase):
        side = Defs.PLUGIN_SITE_SIDE
        
        def __init__(self, extension):
            super(Plugin.Site, self).__init__(extension)
        
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
class Module(ExtBase):
    type = Defs.MODULE
    prefix = "com_"
    
    class Site(ASBase):
        
        def __init__(self, extension):
            super(Module.Site, self).__init__(extension)
            
        def __getitem__(self, key):
            return self.extension[key]
        
        @property
        def client(self):
            return self["client"]
        
        @property
        def basename(self):
            name = "modules"
            return (name if self.client == "site" else os.path.join(Defs.ADMIN_FOLDER, name))
        
        @property
        def side(self):
            return (Defs.MODULE_SITE_SIDE if self.client == "site" else Defs.COMPONENT_ADMIN_SIDE)
        
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
        self.site = Module.Site(self)
        
## -----------------------------------------------------------------------------
class Runner(threading.Thread):
    """ start the work check """
        
    def __init__(self, extension=[], event=None, scanRate=10.0, rate=1.0):
        super(Runner,self).__init__()
        self._continue = True
        
        # event info interface
        self._event = event
        
        self.extension = extension
        
        # scan files rate
        self.scanRate = scanRate
        # check files rate
        self.rate = rate
        
        # auto scan files
        if self.startExtensions(): 
            self._scanFiles()
            
        self.setDaemon(True)
        
    def setRate(self, value):
        """ altera o valor da taxa de atualização """
        self.rate = value
    
    def setScanRate(self, value):
        self.scanRate = value
        
    def stop(self):
        self._continue = False
    
    @capture_errors
    def startExtensions(self):
        """ analiza os dados e cria a lista de arquivos """
        for extension in self.extension:
            extension.start()
        return True
    
    @capture_errors
    def scanFiles(self):
        self.startExtensions()
        self._event.info("[%s] Scan files" % datetime.now())
        return True
    
    @capture_errors
    def _scanFiles(self):
        self.scanFiles()
        if self._continue:
            t = threading.Timer(self.scanRate, self._scanFiles)
            t.setDaemon(True)
            t.start()
        return True
    
    @capture_errors
    def execute(self):
        for ext in self.extension:
            if not ext.admin is None:
                ext.admin.send(ext.admin.check())
            if not ext.site is None:
                ext.site.send(ext.site.check())
        return True
        
    def run(self):
        self._event.info("[%s] Runner started" % datetime.now())
        
        while self._continue and self.execute():
            time.sleep( self.rate ) # rate check
        
        self._event.stop("[%s] Runner exit" % datetime.now())
        self._continue = False













        