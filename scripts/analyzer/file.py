
from config import *
# from dir import *


def get_file_type(mode):
    if S_ISREG(mode):  # tarfile.DIRTYPE
        return 'REGTYPE'
    elif S_ISLNK(mode):  # tarfile.DIRTYPE
        return 'SYMTYPE'
    elif S_ISFIFO(mode):  # tarfile.DIRTYPE
        return 'FIFOTYPE'
    elif S_ISCHR(mode):  # tarfile.DIRTYPE
        return 'CHRTYPE'
    elif S_ISBLK(mode):  # tarfile.DIRTYPE
        return 'BLKTYPE'
    elif S_ISSOCK(mode):
        return 'SOCK'
    else:
        return 'Unknown'


def load_file(abs_filename):
    #return None
    if not os.path.isfile(abs_filename):
	return None
    sha256 = None
    f_type = None
    extension = None
    link = None
    f_size = 0

    mode = os.lstat(abs_filename).st_mode
    stat = os.lstat(abs_filename)

    # statinfo = {
    #     'st_nlink': stat.st_nlink,
    #     'st_uid': stat.st_uid,
    #     'st_gid': stat.st_gid,
    #     'st_atime': stat.st_atime,  # most recent access time
    #     'st_mtime': stat.st_mtime,  # change of content
    #     'st_ctime': stat.st_ctime  # matedata modify
    # }

    if S_ISLNK(mode):
        path = os.readlink(abs_filename)
        link = {
            'link_type': 'symlink',
            'target_path': path
        }

    elif stat.st_nlink > 1:
        link = {
            'link_type': 'hardlink',
            'num_hdlinks': stat.st_nlink
        }

    elif S_ISREG(mode):
        f_size = os.lstat(abs_filename).st_size
        if f_size > 1000000000:
            logging.warn("##################### Too large file %d > 100000000000, name: %s ################", f_size, abs_filename)

        #try:
            #sha256 = hashlib.md5(open(abs_filename, 'rb').read()).hexdigest()
        #except MemoryError as e:
            #logging.debug("##################### Memory Error #####################: %s", e)
            #logging.debug("##################### Too large file %d, name: %s ################", f_size, abs_filename)
	    #e = sys.exc_info()[0]
	    #logging.debug("###################### Error: %s #####################", e)
            read_size = 1024*1024*1024  # You can make this bigger
            sha256 = hashlib.md5()
            with open(abs_filename, 'rb') as f:
                data = f.read(read_size)
                while data:
                    sha256.update(data)
                    data = f.read(read_size)
            sha256 = sha256.hexdigest()
        else:
            try:
                sha256 = hashlib.md5(open(abs_filename, 'rb').read()).hexdigest()
            except IOError as e:
                logging.debug("###################### filename: %s, %s ####################", abs_filename, e)
        try:
	    f_type = me.from_file(abs_filename)
	except:
	    logging.debug("##################### MagicException:file %s #####################", abs_filename)
	    e = sys.exc_info()[0]
	    logging.debug("###################### Error: %s #####################", e)
        extension = os.path.splitext(abs_filename)[1]

    dir_file = {
        'filename': os.path.basename(abs_filename),
        'sha256': sha256,
        'type': f_type,
        'extension': extension
    }

    file_info = {
        'stat_size': f_size,
        'stat_type': get_file_type(mode),
        'link': link,
        # 'st_nlink': stat.st_nlink,
        'st_uid': stat.st_uid,
        'st_gid': stat.st_gid,
        'st_atime': stat.st_atime,  # most recent access time
        'st_mtime': stat.st_mtime,  # change of content
        'st_ctime': stat.st_ctime  # matedata modify
    }

    dir_file['file_info'] = file_info

    return dir_file

