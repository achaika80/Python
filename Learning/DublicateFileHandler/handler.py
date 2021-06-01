# write your code here
import sys
import os

args = sys.argv

if len(args) < 2:
    print("Directory is not specified")
else:
   files_dict = dict()
   for root, dirs, files in os.walk(sys.argv[1]):
       for name in files:
           print(os.path.join(root, name))
           print(os.path.splitext(os.path.join(root, name))[1])
           print(os.path.getsize(os.path.join(root, name)))
           if str(os.path.getsize(os.path.join(root, name))) in files_dict.keys():
               l = files_dict.get(f"{os.path.getsize(os.path.join(root, name))}")
               l.append(os.path.join(root, name))
               files_dict[f'{os.path.getsize(os.path.join(root, name))}'] = l
           else:
               l = list()
               l.append(os.path.join(root, name))
               files_dict[f'{os.path.getsize(os.path.join(root, name))}'] = l
print(files_dict)








