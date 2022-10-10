from datetime import datetime
import glob
from os import path
import os

def file_chooser(mask, not_mask=None):
    columns = {"number": 4, "name": 40, "size": 20, "date": 30}
    sep = "··"
    cols = list(columns.values())
    
    
    
    file_list = glob.glob(mask)
    if not_mask is not None:
        files_to_exclude = glob.glob(not_mask)
        file_list = [x for x in file_list if x not in files_to_exclude]

    file_list = [file_name for file_name in file_list if os.path.isfile(file_name)]
    file_list = [(os.path.basename(file_name), 
                  path.getsize(file_name),
                  path.getmtime(file_name))
                  for file_name in file_list]

    file_list = sorted(file_list, key=lambda x: x[2])

    print("#   name                                      size                     date")
    for i, (short_file_name, file_size, file_date_stamp) in enumerate(file_list[:20]):

        if len(short_file_name) >=cols[1]:
            file_name = short_file_name[:cols[1] - 3] + "..."
        else:
            file_name = short_file_name


        if file_size > 10**6:
            file_size = "{}M".format(round(file_size / 10**6, 2))
        elif file_size > 10**3:
            file_size = "{}K".format(round(file_size / 10**3, 2))

        print(str(i) +
        " " * (cols[0] - len(str(i))) + 
        str(file_name) + "·"*(cols[1] - len(file_name)) + sep +
        str(file_size) + ("·" * (cols[2] - len(str(file_size)))) +
        datetime.fromtimestamp(file_date_stamp).strftime("%m/%d/%Y  %H:%M:%S"))
 

    while True:
        txt = input("\nPick a number: ")
        if txt.isnumeric():
            break

    n = int()
    return file_list[n][0]

if __name__ == '__main__':
    file_name = file_chooser("/home/art/*")
    print("You chose", file_name)
