import os
from glob import glob


def path_list(dir,
              pattern='*',
              path_key='a',
              sort_key='n',
              reverse=False,
              use_sort=True):
    target = os.path.join(dir, pattern)
    chech_func = __check_path(path_key)
    paths = [p for p in glob(target) if chech_func(p)]
    if use_sort:
        return sort_paths(paths, key=sort_key, reverse=reverse)
    else:
        return paths


def sort_paths(p_list, key='n', reverse=False):
    func = __sort_function(key)
    paths = [[p, func(p)] for p in p_list]
    sorted_list = sorted(paths, key=lambda paths: paths[1], reverse=reverse)
    return [l[0] for l in sorted_list]


def __sort_function(key):
    if key == 'c':
        return lambda p: os.path.getctime(p)
    elif key == 'a':
        return lambda p: os.path.getatime(p)
    elif key == 'm':
        return lambda p: os.path.getmtime(p)
    else:
        return lambda p: p


def __check_path(key):
    if key == 'd':
        return lambda p: os.path.isdir(p)
    elif key == 'f':
        return lambda p: os.path.isfile(p)
    else:
        return lambda p: os.path.exists(p)


if __name__ == '__main__':
    print(
        path_list('./', pattern='*', path_key='d', sort_key='m', reverse=True))
