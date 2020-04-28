#!/usr/bin/env python
# coding: utf-8

# In[1]:
#
#import numpy as np
#arr = np.ones(10)
#val = arr[0]
#val = arr.__getitem__(0) # there's nothing to step into here!

# add node using dict of details for name, line etc
# colour the nodes using name (pandas, python, numpy etc)
# make it optional to drop text details

# conda install pydot, networkx

from networkx import DiGraph
from networkx.drawing.nx_pydot import to_pydot
from io import StringIO
from contextlib import contextmanager
from sys import setprofile
# https://docs.python.org/3/library/sys.html#sys.setprofile
from collections import namedtuple

class Ident(namedtuple('IdentBase', 'filename lineno name')):
    def __str__(self):
        filename = self.filename
        if 'site-packages' in filename:
            # e.g. '/home/ian/miniconda3/envs/course2/lib/python3.8/site-packages/pandas/io/formats/format.py'
            filename = filename.split('site-packages')[1]
        elif 'python3.' in filename:
            filename = filename.split('python3.')[1]
        elif 'callgraph.py' in filename:
            filename = 'callgraph.py'
        split = filename.rsplit('/')
        file_name = split[-1]
        file_path = "/".join(split[:-1])

        #return f'"{self.filename}:{self.lineno}:{self.name}"'
        #return f'"{filename}\n{self.lineno}:{self.name}"'
        return f'"{file_path}\n{file_name}\n{self.lineno}:{self.name}"'
           



@contextmanager
def callgraph(root=Ident('<context manager>', -1, '')):
    def cb(frame, event, arg):
        DO_C_CALL = True
        nonlocal current
        if DO_C_CALL and event == 'c_call':
            #print('in c_call')
            code = frame.f_code
            nxt = Ident(code.co_filename, code.co_firstlineno, code.co_name)
            g.add_edge(current, nxt)
            current = nxt
        if event == 'call':
            code = frame.f_code
            nxt = Ident(code.co_filename, code.co_firstlineno, code.co_name)
            g.add_edge(current, nxt)
            current = nxt
        if DO_C_CALL and event == 'c_return':
            #print('in c_return')
            current = next(g.predecessors(current), root)
        elif event == 'return':
            current = next(g.predecessors(current), root)
    g = DiGraph()
    g.add_node(root)
    current = root
    try:
        setprofile(cb)
        yield g
        setprofile(None)
    finally:
        pass
    
    
if False:
    import pandas as pd
    with callgraph() as cg:
        data = """
        a, b, c
        1, 10, 100
        2, 20, 200"""
        df = pd.read_csv(StringIO(data))

if True:
    import pandas as pd
    import numpy as np
    arr = np.ones(int(1e6))
    df = pd.DataFrame({'arr': arr})
    #In [6]: %timeit df.arr.mean()                                       
    #4.44 ms ± 26.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    #In [7]: %timeit df.arr.values.mean()
    #519 µs ± 1.42 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    with callgraph() as cg:
        #pd.DataFrame()
        #df.arr.mean() #25 files, 89 functions
        #df.arr.values.mean() # 19 files, 52 functions
        #arr.mean() # 5 files, 6 functions

        #df.sum() # 29 files, 97 functions
        #df['arr'].sum() # 25 files, 83 functions
        df.arr.values.sum() # 18 files, 51 functions


    filenames = {n.filename for n in cg.nodes()}  
    functions = {n.name for n in cg.nodes()}
    print(f"{len(filenames)} files, {len(functions)} functions")
        
    from matplotlib.pyplot import imshow, show, axis
    from matplotlib.image import imread
    from io import BytesIO

    png = BytesIO()
    png.write(to_pydot(cg).create_png(prog='dot'))

    with open('callgraph.png', 'wb') as f:
        f.write(png.getbuffer())


if False:
    import pandas as pd
    data = """
    a, b, c
    1, 10, 100
    2, 20, 200"""
    df = pd.read_csv(StringIO(data))
    with callgraph() as cg:
        #df.info(memory_usage='deep') # 49 files, 227 fns, more if including c fns
        df.info(memory_usage=False) # 40 files, 171 fns

if False:
    def f(): 
        g()
        
    def g():
        h()
        
    def h():
        pass

    with callgraph() as cg:
        f()


if False:
    import numpy as np
    l = np.array([1, 2, 3])
    with callgraph() as cg:
        #l.__getitem__(0) # don't register?
        #l[0] # don't register?
        l.mean() # does something small

if False:

    filenames = {n.filename for n in cg.nodes()} 
    functions = {n.name for n in cg.nodes()}
    print(f"{len(filenames)} files, {len(functions)} functions")


    from matplotlib.pyplot import imshow, show, axis
    from matplotlib.image import imread
    from io import BytesIO
    #(png := BytesIO()).write(to_pydot(cg).create_png(prog='dot')); png.seek(0)
    #axis('off'); imshow(imread(png), aspect='equal'); show()

    png = BytesIO()
    png.write(to_pydot(cg).create_png(prog='dot'))

    with open('img.png', 'wb') as f:
        f.write(png.getbuffer())


if False:
    fig, ax = plt.subplots()
    #nx.draw(cg, pos=nx.spring_layout(cg), ax=ax)  
    nx.draw(cg, pos=nx.shell_layout(cg), ax=ax)  
    plt.savefig('ian.png')
