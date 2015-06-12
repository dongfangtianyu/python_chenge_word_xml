# -*- coding: cp936 -*-  
from distutils.core import setup  
import py2exe  
  
includes = ["encodings", "encodings.*"]

options = {"py2exe":
            {"compressed": 1, #压缩
             "optimize": 2,
             "ascii": 1,
             "includes":includes,
             "bundle_files": 1 #所有文件打包成一个exe文件
            }}
setup(
    console=["main.py"],
    options=options,
#     zipfile=None,
#     data_files=[("in", ["tr.xml", "dome-0.xml"],), ],
#     version="2015.5.19.01",
#     description="this is a py2exe test",
#     name="HelloGuys."
)
# setup(console=["main.py"])