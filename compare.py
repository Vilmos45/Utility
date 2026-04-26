import os
import hashlib

def read_clean(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().strip().replace('\r\n', '\n').replace('\r', '\n')

def file_hash(path):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def compare_dirs(dir1, dir2):
    files1 = {f for f in os.listdir(dir1) if os.path.isfile(os.path.join(dir1, f))}
    files2 = {f for f in os.listdir(dir2) if os.path.isfile(os.path.join(dir2, f))}

    only_in_1 = files1 - files2
    only_in_2 = files2 - files1
    common = files1 & files2

    print("Csak az első mappában:")
    for f in only_in_1:
        print("  ", f)

    print("\nCsak a második mappában:")
    for f in only_in_2:
        print("  ", f)

    print("\nEltérő tartalmú fájlok:")
    for f in common:
        path1 = os.path.join(dir1, f)
        path2 = os.path.join(dir2, f)

        if os.path.isfile(path1) and os.path.isfile(path2):
            if file_hash(path1) != file_hash(path2):
                if read_clean(path1) != read_clean(path2):
                    print("  ", f)

if __name__ == "__main__":
    dir1 = input("Első mappa: ").strip()
    dir2 = input("Második mappa: ").strip()

    if not os.path.isdir(dir1) or not os.path.isdir(dir2):
        print("Hibás mappaútvonal.")
    else:
        compare_dirs(dir1, dir2)