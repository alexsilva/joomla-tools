import os
import zipfile

name = "com_pbevents_0.3"
path = os.path.join(os.getcwd(), name)

zip = zipfile.ZipFile(name + ".zip", "w")

for root, dirs, files in os.walk(path):
    for file in files:
        path = os.path.join(root, file)
        path = path.replace(os.getcwd() + os.sep, "")
        zip.write(path)

zip.close()
