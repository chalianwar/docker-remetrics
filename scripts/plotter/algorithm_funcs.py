
from draw_pic import *

def calculate_repeates(l):
    logging.info("first file_sha256s list: %s", l[0])
    l_dict = pd.DataFrame(l, columns=["x"]).groupby('x').size().to_dict()
    return l_dict


