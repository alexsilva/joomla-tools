# coding: utf-8
import xml.parsers.expat
import shutil
import re
import os

## ------------------------------------------------------------------------------
class Model(object):
    """ gera o modelo de projeto dos arquivos na pasta joomla 3.x """
    
    def __init__(self, path):
        self.path = path
        
        self.parse = xml.parsers.expat.ParserCreate()
        self.parse.StartElementHandler = self.element
        
        self.instances = {}
        self.rel = {"dirs": {}, "files":{}}
        
    def read(self):
        """ lê a analiza o arquivo xml """
        with open(self.path) as _file:   
            self.parse.Parse(_file.read())
        
    def element(self, name, attrs):
        """ converte os emelentos xml para instância de python """
        self.instances[name] = type(str(name), (), attrs)
    
    def __getitem__(self, name):
        return self.instances[name]
    
    def __dir__(self):
        return self.instances.keys()
    
    def resolve(self):
        """ resolve os caminhos relativos para absoluto """
        pattern = re.compile("\{(?P<base>.+)\}(?P<path>.+)")
        
        for name in self.instances:
            inst = self.instances[name]
            
            if not getattr(inst,"path",None) is None:
                matchobj = pattern.match( inst.path )
                
                if matchobj:
                    base = self.instances[matchobj.group("base")]
                    inst.path = os.path.join(base.path, matchobj.group("path"))
                    setattr(base, name, inst)
                    
                    if pattern.match(inst.path): self.resolve()
    
    def copy_all(self, source_dir, dest_dir, basename, in_dir):
        """ copia os arquivos da pasta joomla 3.x relacionando os arquivos com 'admin' ou 'site'"""
        for root, dirs, files in os.walk(source_dir):
            dst = os.path.join(dest_dir, in_dir + root.split(basename)[-1])
            
            for dirname in dirs:
                dirpath = os.path.join(dst, dirname)
                path = os.path.join(root, dirname)
                
                self.rel["dirs"][dirpath] = path
                
                if os.path.exists(dirpath): continue
                os.mkdir(dirpath)
                
            for filename in files:
                srcpath = os.path.join(root, filename)
                dstpath = os.path.join(dst, filename)
                
                shutil.copyfile(srcpath, dstpath)
                self.rel["files"][dstpath] = srcpath
                
    def create(self):
        """ analiza a estrutura de arquivos do projeto na pasta joomla 3.x """
        target = self.instances["target"]
        print "TARGET: ", target.name
        
        for name in self.instances:
            inst = self.instances[name]
            
            if not getattr(inst,"path",None) is None:
                if not os.path.exists(inst.path): continue
                
                tname =  target.name
                tdir = os.path.join(inst.path, tname)
                
                if not os.path.exists(tdir):
                    tname = target.name.split("com_")[-1]
                    tdir = os.path.join(inst.path, tname)
                    
                if not os.path.exists(tdir): continue
                ndir = os.path.join(os.getcwd(), target.name)
                
                # diretorio base para todos os arquivos
                d = os.path.join(ndir, name)
                if not os.path.exists(d): os.makedirs(d)
                
                self.copy_all(tdir, ndir, tname, name)
                print name, inst.path
    
    def clean(self, leveldir=2):
        """ remove arquivos remonomeados ou removidos do projeto """
        source = os.path.join(os.getcwd(), self.instances["target"].name)
        index = 1
        for root, dirs, files in os.walk(source):
            if index > leveldir:
                for dirname in dirs:
                    dirpath = os.path.join(root, dirname)
                    
                    relpath = self.rel["dirs"].get(dirpath,"")
                    if os.path.exists(relpath): continue
                    
                    shutil.rmtree(dirpath)
                
            for filename in files:
                path = os.path.join(root, filename)
                
                relfile = self.rel["files"].get(path,"")
                if os.path.exists(relfile): continue
                
                os.remove(path)
            index += 1
            
## ------------------------------------------------------------------------------
model = Model("struct.xml")

# analiza o xml
model.read()

# resolução de nomes relativos
model.resolve()

# cria a estrutura do componente
model.create()

# remove arquivos inexistentes
model.clean()















