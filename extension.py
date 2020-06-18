# coding: utf-8
import filecmp
import os
import shutil
import threading
import time
from datetime import datetime
from xml.etree.ElementTree import ElementTree


class CaptureExceptions(object):
    def __init__(self, func):
        self.fun = func

    def __get__(self, inst, cls):
        def wraper(*args, **kwargs):
            try:
                result = self.fun(inst, *args, **kwargs)
            except Exception as err:
                inst._event.error("Error[%s] %s" % (datetime.now(), err))
                result = False
            return result

        return wraper


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


class Defs(object):
    ADMIN_FOLDER = "administrator"
    SITE_FOLDER = "."  # root joomla

    COMPONENT = "COMPONENT"
    COMPONENT_ADMIN_SIDE = "COMP_ADMIN"
    COMPONENT_SITE_SIDE = "COMP_SITE"

    PLUGIN = "PLUGIN"
    PLUGIN_ADMIN_SIDE = "PLG_ADMIN"
    PLUGIN_SITE_SIDE = "PLG_SITE"

    MODULE = "MODULE"
    MODULE_ADMIN_SIDE = "MOD_ADMIN"
    MODULE_SITE_SIDE = "MOD_SITE"


class ExtBase(object):
    prefix = ""

    def __init__(self, name, path, joomla_path, event):
        self.root = self.admin = self.site = None
        # full path of joomla
        self.joomla_path = joomla_path
        # extension name
        self.ext_name = name
        # extension path
        self.ext_path = path
        self.event = event

    @property
    def name(self):
        return self.ext_name

    @property
    def joomla(self):
        return self.joomla_path

    @property
    def path(self):
        return self.ext_path

    @property
    def fullname(self):
        return self.prefix + self.name

    def parse_xml(self):
        etree = ElementTree()
        xmpath = os.path.join(self.path, self.name + ".xml")
        return etree.parse(xmpath)

    def __getitem__(self, key):
        return self.root.find(key)

    def start(self):
        self.root = self.parse_xml()  ## refs files

        if not self.admin is None:
            self.admin.scan_files()  ## update list files

        if not self.site is None:
            self.site.scan_files()  ## update list files


class ASBase(object):

    def __init__(self, extension):
        self.extension = extension
        self.filelist = None

    def __getattr__(self, name):
        return (getattr(self.extension, name, None) if hasattr(self.extension, name) else
                super(ASBase, self).__getattr__(name))

    def get_files_in(self, folder):
        fpath = os.path.join(self.path, folder)
        content = []
        for root, dirs, files in os.walk(fpath):
            for filename in files:
                filepath = os.path.join(root, filename)
                # usando o caminho relativo para o arquivo.
                content.append(os.path.relpath(filepath, self.path))
        return content

    def scan_files(self):
        self.filelist = []
        self.filelist.extend(self.filenames)

        for folder in self.folders:
            self.filelist.extend(self.get_files_in(folder))

        self.filelist.extend(self.languages)

    def check(self):
        changes = {"changed": [], "removed": [], "new": []}

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

    @staticmethod
    def is_language(path):
        return path.startswith("language")

    def build_path(self, path, file, join=True):
        relpath = os.path.dirname(file)
        filename = os.path.basename(file)
        src = os.path.join(path, file)

        if self.extension.type == Defs.COMPONENT:
            if self.is_language(relpath):
                dst = os.path.join(self.extension.joomla, os.path.dirname(self.basename), relpath)
            else:
                dst = os.path.join(self.extension.joomla, self.basename,
                                   self.extension.fullname, relpath)

        elif self.extension.type == Defs.PLUGIN:
            if self.is_language(relpath):
                dst = os.path.join(self.extension.joomla, Defs.ADMIN_FOLDER, relpath)
            else:
                dst = os.path.join(self.extension.joomla, self.basename,
                                   self.extension.fullname, relpath)

        elif self.extension.type == Defs.MODULE:
            if self.is_language(relpath):
                dst = os.path.join(self.extension.joomla, os.path.dirname(self.basename), relpath)
            else:
                dst = os.path.join(self.extension.joomla, self.basename,
                                   self.extension.fullname, relpath)

        else:
            raise RuntimeError, "In make path: Type error!"

        if join:
            dst = os.path.join(dst, filename)
        else:
            dst = {"d": dst, "f": filename}

        return src, dst

    def send(self, changes):
        path = self.path

        for file in changes["new"]:
            src, dst = self.build_path(path, file, False)

            # contrói os diretórios necessários.
            if not os.path.exists(dst["d"]):
                os.makedirs(dst["d"])

            dst = os.path.join(dst["d"], dst["f"])
            shutil.copyfile(src, dst)

            self.event.info("[%s] New: %s" % (datetime.now(), dst))

        for file in changes["changed"]:
            src, dst = self.build_path(path, file)

            # safe check
            if os.path.exists(dst):
                dst_mtime = os.path.getmtime(dst)
            else:
                dst_mtime = 0

            if os.path.getmtime(src) > dst_mtime:
                shutil.copyfile(src, dst)
            else:
                # reverse sync
                shutil.copyfile(dst, src)
                dst = src

            self.event.changes("[%s] Updated: %s" % (datetime.now(), dst))

        for file in changes["removed"]:
            src, dst = self.build_path(path, file)
            if os.path.exists(dst):
                os.remove(dst)

            self.scan_files()  # update list files
            self.event.info("[%s] Removed: %s" % (datetime.now(), dst))


class Component(ExtBase):
    type = Defs.COMPONENT
    prefix = "com_"

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
            return [e.text for e in (files.findall("folder") if files is not None else [])]

        @property
        def filenames(self):
            files = self["files"]
            return [e.text for e in (files.findall("filename") if files is not None else [])]

        @property
        def languages(self):
            lang = self["languages"]
            return [e.text.replace("/", os.sep) for e in (lang.findall("language") if lang is not None else [])]

        @property
        def path(self):
            return os.path.join(self.extension.path, self.folder)

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
            return [e.text for e in (files.findall("folder") if files is not None else [])]

        @property
        def filenames(self):
            files = self["files"]
            return [e.text for e in (files.findall("filename") if files is not None else [])]

        @property
        def languages(self):
            lang = self["languages"]
            return [e.text.replace("/", os.sep) for e in (lang.findall("language") if lang is not None else [])]

        @property
        def path(self):
            return os.path.join(self.extension.path, self.folder)

    def __init__(self, name, path, joomla, event):
        super(Component, self).__init__(name, path, joomla, event)
        self.admin = Component.Admin(self)
        self.site = Component.Site(self)


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
            return [e.text for e in (files.findall("folder") if files is not None else [])]

        @property
        def filenames(self):
            files = self["files"]
            return [e.text for e in (files.findall("filename") if files is not None else [])]

        @property
        def languages(self):
            lang = self["languages"]
            return [e.text.replace("/", os.sep) for e in (lang.findall("language") if lang is not None else [])]

        @property
        def path(self):
            path = os.path.join(self.extension.path, self.folder)
            path = path.rstrip("/").rstrip(os.sep)
            return path

    def __init__(self, name, path, joomla, event):
        super(Plugin, self).__init__(name, path, joomla, event)
        self.site = Plugin.Site(self)


class Module(ExtBase):
    type = Defs.MODULE
    prefix = "mod_"

    class Site(ASBase):

        def __init__(self, extension):
            super(Module.Site, self).__init__(extension)

        def __getitem__(self, key):
            return self.extension[key]

        @property
        def client(self):
            return self.extension.root.get("client", "client no set")

        @property
        def basename(self):
            name = "modules"
            return name if self.client == "site" else os.path.join(Defs.ADMIN_FOLDER, name)

        @property
        def side(self):
            return Defs.MODULE_SITE_SIDE if self.client == "site" else Defs.COMPONENT_ADMIN_SIDE

        @property
        def folder(self):
            return ""

        @property
        def folders(self):
            files = self["files"]
            return [e.text for e in (files.findall("folder") if files is not None else [])]

        @property
        def filenames(self):
            files = self["files"]
            return [e.text for e in (files.findall("filename") if files is not None else [])]

        @property
        def languages(self):
            lang = self["languages"]
            return [e.text.replace("/", os.sep) for e in (lang.findall("language") if lang is not None else [])]

        @property
        def path(self):
            path = os.path.join(self.extension.path, self.folder)
            path = path.rstrip("/").rstrip(os.sep)
            return path

    def __init__(self, name, path, joomla, event):
        super(Module, self).__init__(name, path, joomla, event)
        self.site = Module.Site(self)

    @property
    def name(self):
        return (self.ext_name if self.ext_name.startswith(self.prefix)
                else self.prefix + self.ext_name)

    @property
    def fullname(self):
        return self.name


class Runner(threading.Thread):
    """ start the work check """

    def __init__(self, extension=None, event=None, scan_rate=10.0, rate=1.0):
        super(Runner, self).__init__()
        self._continue = True

        if extension is None:
            extension = []

        # event info interface
        self._event = event

        self.extension = extension

        # scan files rate
        self.scan_rate = scan_rate
        # check files rate
        self.rate = rate

        # auto scan files
        if self.start_extensions():
            self._scan_files()

        self.setDaemon(True)

    def set_rate(self, value):
        """ altera o valor da taxa de atualização """
        self.rate = value

    def set_scan_rate(self, value):
        self.scan_rate = value

    def stop(self):
        self._continue = False

    @CaptureExceptions
    def start_extensions(self):
        """ analiza os dados e cria a lista de arquivos """
        for extension in self.extension:
            extension.start()
        return True

    @CaptureExceptions
    def scan_files(self):
        self.start_extensions()
        self._event.info("[%s] Scan files" % datetime.now())
        return True

    @CaptureExceptions
    def _scan_files(self):
        self.scan_files()
        if self._continue:
            t = threading.Timer(self.scan_rate, self._scan_files)
            t.setDaemon(True)
            t.start()
        return True

    @CaptureExceptions
    def execute(self):
        for ext in self.extension:
            if ext.admin is not None:
                ext.admin.send(ext.admin.check())
            if ext.site is not None:
                ext.site.send(ext.site.check())
        return True

    def run(self):
        self._event.info("[%s] Runner started" % datetime.now())

        while self._continue and self.execute():
            time.sleep(self.rate)  # rate check

        self._event.stop("[%s] Runner exit" % datetime.now())
        self._continue = False
