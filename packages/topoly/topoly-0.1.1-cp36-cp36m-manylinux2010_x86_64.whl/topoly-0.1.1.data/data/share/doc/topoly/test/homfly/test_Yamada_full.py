import os
import sys
if 'LD_LIBRARY_PATH' not in os.environ:                                             #|
    build_dir_name = 'build'    # set as needed                                     #|
    dir_path = os.path.dirname(os.path.realpath(__file__))                          #|
    par_dir = os.path.abspath(os.path.join(dir_path, os.pardir))                    #|
    build_dir = os.path.abspath(os.path.join(par_dir, build_dir_name))              #|
    os.environ['LD_LIBRARY_PATH'] = build_dir                                       #|
    os.environ['PYTHONPATH'] = build_dir                                            #|
    os.execv(sys.executable, [sys.executable] + sys.argv)                           #|
# until here

from topoly_preprocess import chain_read_from_string

curve = []
for k in range(3):
    arc = []
    file_name = 'structures/arc' + str(k+1)
    with open(file_name, 'r') as myfile:
        for line in myfile.readlines():
            arc.append(line.strip().split()[1:])
    curve.append(arc)



# print(yamada(curve, translate=True, debug=True))

for arc in curve:
    chain_read_from_string(arc)

# from topoly_homfly import find_link_code_to_string
# print(find_link_code_to_string(['structures/arc1'.encode('utf-8'), 'structures/arc2'.encode('utf-8'), 'structures/arc3'.encode('utf-8')], yamada=True))