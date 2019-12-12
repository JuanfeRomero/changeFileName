import os


def main():
    file_path = input("please insert the path of the files to rename")
    file_path = file_path.replace('/', '//')
    file_path = file_path + '//'
    choice = int(input(
        'type 1 if you wish to rename the files, type 2 if you wish to change the files\'s extension, 0 to finish'))
    while 0 <= choice < 3:
        if choice == 1:
            replace_name(file_path)
            break
        elif choice == 2:
            replace_format(file_path)
            break
        elif choice == 0:
            exit()


def replace_format(file_path):
    old_extension = input('please insert the extension you wish to replace in format ".yourExtension"')
    new_extension = input('please insert the new extension for your files in format ".yourNewExtension"')

    for filename in os.listdir(file_path):
        filename = filename.lower()
        dst = filename.replace(old_extension, new_extension)
        src = file_path + filename
        dst = file_path + dst
        os.rename(src, dst)


def replace_name(file_path):
    new_name = input('please insert the new name for your files')
    specific_extension = input('please select the extension you want to rename, if you wish to rename all the files (including folders) leave blank')
    counter = 0
    if specific_extension:
        for filename in os.listdir(file_path):
            filename = filename.lower()
            filename_w_path, extension = os.path.splitext((file_path+filename))
            if specific_extension == extension:
                dst = new_name + (str(counter)) + extension
                src = file_path + filename
                dst = file_path + dst
                counter += 1
                os.rename(src, dst)
    elif not specific_extension:
        for filename in os.listdir(file_path):
            filename_w_path, extension = os.path.splitext((file_path+filename))
            dst = new_name+(str(counter))+extension
            src = file_path + filename
            dst = file_path + dst
            counter += 1
            os.rename(src, dst)


if __name__ == '__main__':
    main()
