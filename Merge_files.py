from glob import glob

test_file_directory = "C:\\Users\\User\\Desktop\\Folder\\"

files1 = glob("*.txt")
with open(test_file_directory+"testfile.txt","r") as f:
    lines = f.readlines()[3:]

files = {}
for line in lines:
    line_list = line.split()
    filename, state = line_list[0], line_list[1]
    if state in ('ON', 'OFF'):
        files[filename] = state

for f1 in files1:
    file = f1[:-4]
    if file in files:
        with open(f1,'r') as r:
            lines = r.readlines()
        if files[file] == 'ON':
            with open('merge_file.txt','a') as a:
                a.write('\n'.join(lines[1:])+'\n')
        with open('match_file.txt','a') as a:
            a.write(f"{f1} {len(lines)}\n")