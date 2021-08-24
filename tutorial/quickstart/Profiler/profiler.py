import cProfile
import pstats
from functools import wraps
import io
from io import StringIO
from pstats import SortKey

import logging
logger = logging.getLogger('sample')


def profiler(output_file=None, sort_by='cumulative', lines_to_print=None, strip_dirs=False):
    """A time profiler decorator.

    Inspired by and modified the profile decorator of Giampaolo Rodola:
    http://code.activestate.com/recipes/577817-profile-decorator/

    Args:
        output_file: str or None. Default is None
            Path of the output file. If only name of the file is given, it's
            saved in the current directory.
            If it's None, the name of the decorated function is used.
        sort_by: str or SortKey enum or tuple/list of str/SortKey enum
            Sorting criteria for the Stats object.
            For a list of valid string and SortKey refer to:
            https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats
        lines_to_print: int or None
            Number of lines to print. Default (None) is for all the lines.
            This is useful in reducing the size of the printout, especially
            that sorting by 'cumulative', the time consuming operations
            are printed toward the top of the file.
        strip_dirs: bool
            Whether to remove the leading path info from file names.
            This is also useful in reducing the size of the printout

    Returns:
        Profile of the decorated function
    """

    def inner(func):
        
        @wraps(func)
        
        def wrapper(*args, **kwargs):
            
            pr = cProfile.Profile()
            
            pr.enable()
            
            retval = func(*args, **kwargs)
            
            pr.disable()
            
            s = io.StringIO()

            sortby = SortKey.TIME

            ps = pstats.Stats(pr, stream=s)

            if strip_dirs:
                ps.strip_dirs()
            
            ps.sort_stats(sortby)
            
            ps.print_stats(lines_to_print)
            
            print(s.getvalue())
            
            return retval

        return wrapper

    return inner