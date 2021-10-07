# write your code here
import sys
import os
import hashlib


args = sys.argv
print(sys.argv)
if len(args) < 2:
    print("Directory is not specified")
    sys.exit()
else:
    file_ext = ''
    file_ext = input('Enter file format:')
    sort = input('\nSize sorting options:\n1. Descending\n2. Ascending\n\nEnter a sorting option:')
    while sort not in ['1', '2']:
        print('\nWrong option\n')
        sort = input('Enter a sorting option:')
    files_dict = dict()
    for root, dirs, files in os.walk(sys.argv[1]):
        for name in files:
            #print(os.path.join(root, name))
            #print(os.path.splitext(os.path.join(root, name))[1])
            #print(os.path.getsize(os.path.join(root, name)))
            if file_ext in os.path.splitext(os.path.join(root, name))[1]:
                if str(os.path.getsize(os.path.join(root, name))) in files_dict.keys():
                    l = files_dict.get(f"{os.path.getsize(os.path.join(root, name))}")
                    l.append(os.path.join(root, name))
                    files_dict[f'{os.path.getsize(os.path.join(root, name))}'] = l
                else:
                    l = list()
                    l.append(os.path.join(root, name))
                    files_dict[f'{os.path.getsize(os.path.join(root, name))}'] = l
    f_dict = dict(filter(lambda elem: len(elem[1]) > 1, files_dict.items()))
    reverse = True if sort == '1' else False
    for i in sorted(f_dict, reverse=reverse):
        print(f'\n{i} bytes')
        for j in f_dict[i]:
            print(j)

db_check = input("\nCheck for duplicates?")
while db_check not in ['yes', 'no']:
    print('Wrong option')
    db_check = input("\nCheck for duplicates?\n")

if db_check != 'yes':
    sys.exit()
else:
    n = 1
    hash_dict = dict()
    for i in sorted(f_dict, reverse=reverse):
        h_dict = dict()
        hash_dict[i] = list()
        for j in f_dict[i]:
            hash = hashlib.md5(open(j, 'rb').read()).hexdigest()
            if hash in h_dict.keys():
                l = h_dict.get(hash)
                l.append(j)
                h_dict[hash] = l
            else:
                l = list()
                l.append(j)
                h_dict[hash] = l
        t_hdict = dict(filter(lambda elem: len(elem[1]) > 1, h_dict.items()))
        hash_dict[i].append(t_hdict)

n = 1

for i in sorted(hash_dict, reverse=reverse):
    print(f'\n{i} bytes')
    for j in hash_dict[i]:
        for x in j:
            print(f'Hash: {x}')
            for y in j[x]:
                print(f'{n}. {y}')
                n += 1
n_list = [x for x in range(1, n+1)]

db_check = input("\nDelete files?")
while db_check not in ['yes', 'no']:
    print('Wrong option')
    db_check = input("\nDelete files?\n")

if db_check != 'yes':
    sys.exit()
else:
    file_numbers = input("\nEnter file numbers to delete:")
    while len(file_numbers) == 0 or not file_numbers.replace(' ', '').isnumeric():
        print('\nWrong format')
        file_numbers = input("\nEnter file numbers to delete:")
    flag = 0
    file_ints = list(map(int, list(file_numbers.split())))
    if set(file_ints).issubset(set(n_list)):
        flag = 1
    while flag == 0:
        print('\nWrong format')
        file_numbers = input("\nEnter file numbers to delete:")
        file_ints = list(map(int, list(file_numbers.split())))
        if set(file_ints).issubset(set(n_list)):
            flag = 1

    saved_space = 0
    for z in sorted(file_ints):
        n = 1
        #print(f'z: {z}')
        for i in sorted(hash_dict, reverse=reverse):
            #print(f'\n{i} bytes')
            for j in hash_dict[i]:
                for x in j:
                    #print(f'Hash: {x}')
                    for y in j[x]:
                        if z == n:
                            #print(f"Removing: z: {z}, n: {n}, y: {y}")
                            os.remove(y)
                            saved_space += int(i)
                        n += 1
print(f'Total freed up space: {saved_space} bytes')







