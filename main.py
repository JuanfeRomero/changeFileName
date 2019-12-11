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
    extension = input('please insert the extension of the files you wish to replace in format ".extension", if you wish to change all files in folder, leave this blank')
    extension = extension.lower()
    new_name = input('please insert the new name for your files')
    counter = 0
    if not extension:
        for filename in os.listdir(file_path):
            dst = new_name + str(counter)
            src = file_path + filename
            dst = file_path + dst
            os.rename(src, dst)
            counter += 1
    if extension:
        for filename in os.listdir(file_path):
            filename = filename.lower()
            if filename == ("\Z" + extension):
                dst = new_name + str(counter)
                src = file_path + filename
                dst = file_path + dst + extension
                os.rename(src, dst)
                counter += 1


if __name__ == '__main__':
    main()
