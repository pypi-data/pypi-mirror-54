import os


CHUNKSIZE = 8 << 20  # 8 MB


class OSDestination:
    """Generator yielding `store()/delete()`-able files in a local directory"""
    def __init__(self, dirpath):
        os.makedirs(dirpath, exist_ok=True)
        self.dirpath = dirpath
        self.check_perms()

    def __iter__(self):
        for dirpath, _, filenames in os.walk(self.dirpath):
            for filepath in (f'{dirpath}/{filename}' for filename in filenames):
                yield self.file(os.path.relpath(filepath, self.dirpath))

    def file(self, relpath):
        return OSFile(self, relpath)

    def cleanup(self):
        """Remove any empty directories within the local directory"""
        for dirpath, dirnames, filenames in os.walk(self.dirpath):
            if not dirnames and not filenames:
                os.rmdir(dirpath)

    def check_perms(self):
        if not os.access(self.dirpath, os.W_OK):
            raise PermissionError('{} is not writable'.format(self.dirpath))


class OSFile:
    """Store read()-ables / delete files locally"""
    __slots__ = ('name', 'size', 'modified', 'filepath')

    def __init__(self, osdst, relpath):
        self.name = relpath
        self.filepath = f'{osdst.dirpath}/{relpath}'

    def stat(self):
        try:
            stat = os.stat(self.filepath)
        except FileNotFoundError:
            return False
        self.size, self.modified = stat.st_size, stat.st_mtime
        return True

    def store(self, src):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'wb') as dst:
            data = src.read(CHUNKSIZE)
            while data:
                dst.write(data)
                data = src.read(CHUNKSIZE)

    def delete(self):
        os.remove(self.filepath)
