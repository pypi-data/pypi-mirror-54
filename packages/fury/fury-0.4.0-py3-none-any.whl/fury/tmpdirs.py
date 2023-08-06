"""Contexts for *with* statement providing temporary directories."""

from __future__ import division, print_function, absolute_import
import sys

if sys.version_info[0] >= 3:
    from tempfile import TemporaryDirectory as InTemporaryDirectory
else:
    # coming from NiBabel package.
    import os
    import shutil
    from tempfile import template, mkdtemp

    class TemporaryDirectory(object):
        r"""Create and return a temporary directory.

        This has the same
        behavior as mkdtemp but can be used as a context manager.
        Upon exiting the context, the directory and everthing contained
        in it are removed.

        Examples
        --------
        >>> import os
        >>> with TemporaryDirectory() as tmpdir:
        ...     fname = os.path.join(tmpdir, 'example_file.txt')
        ...     with open(fname, 'wt') as fobj:
        ...         _ = fobj.write('a string\\n')
        >>> os.path.exists(tmpdir)
        False

        """

        def __init__(self, suffix="", prefix=template, folder=None):
            self.name = mkdtemp(suffix, prefix, folder)
            self._closed = False

        def __enter__(self):
            return self.name

        def cleanup(self):
            if not self._closed:
                shutil.rmtree(self.name)
                self._closed = True

        def __exit__(self, exc, value, tb):
            self.cleanup()
            return False

    class InTemporaryDirectory(TemporaryDirectory):
        """Create, return, and change directory to a temporary directory.

        Examples
        --------
        >>> import os
        >>> my_cwd = os.getcwd()
        >>> with InTemporaryDirectory() as tmpdir:
        ...     _ = open('test.txt', 'wt').write('some text')
        ...     assert os.path.isfile('test.txt')
        ...     assert os.path.isfile(os.path.join(tmpdir, 'test.txt'))
        >>> os.path.exists(tmpdir)
        False
        >>> os.getcwd() == my_cwd
        True

        """
        _pwd = '.'

        def __enter__(self):
            self._pwd = os.getcwd()
            os.chdir(self.name)
            return super(InTemporaryDirectory, self).__enter__()

        def __exit__(self, exc, value, tb):
            os.chdir(self._pwd)
            return super(InTemporaryDirectory, self).__exit__(exc, value, tb)
