#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Common utility classes and functions."""

__author__ = "Lluís Vilanova"
__copyright__ = "Copyright 2008-2019, Lluís Vilanova"
__license__ = "GPL version 3 or later"


import re
import os
import shutil
import signal
import six
import subprocess
import tempfile
import warnings
import functools
import collections
import numpy as np
import weakref

from . import pp
from . import progress


# -----------------------------

def deprecated(func):
    """Decorator to mark routines as deprecated.

    It will result in a warning being emitted when the routine is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function '%s'" % func.__name__,
                      category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return new_func


def assert_kwargs(kwargs):
    """Raise an exception if extra keys are present."""
    if len(kwargs) > 0:
        extra = "s" if len(kwargs) > 1 else ""
        raise TypeError("Unexpected argument%s: %s" % (extra,
                                                       ", ".join(kwargs)))


def text_realign(text, from_text, to_text):
    offset = len(from_text) - len(to_text)
    if offset > 0:
        lines = text.split("\n")
        text = [lines[0]] + [line[offset:]
                             for line in lines[1:]]
        text = "\n".join(text)
    elif offset < 0:
        lines = text.split("\n")
        text = [lines[0]] + [(" " * -offset) + line
                             for line in lines[1:]]
        text = "\n".join(text)
    return text.replace(from_text, to_text, 1)


# -----------------------------

def assert_dir(path):
    """Check that given directory exists, otherwise create it."""
    if path != "" and not os.path.exists(path):
        os.makedirs(path)


def assert_path(path):
    """Check that given path exists, otherwise create directories."""
    if not path.endswith(os.sep):
        path = os.path.dirname(path)
    assert_dir(path)


def get_path(path):
    path = os.path.expanduser(path)
    return os.path.expandvars(path)


def get_file(path, mod="w"):
    """Open the given file, creating any intermediate directory."""
    dir_path = os.path.dirname(path)
    assert_dir(dir_path)
    return open(path, mod)


def get_tmp_file(mode="w", delete=True):
    """Get a temporal file."""
    return tempfile.NamedTemporaryFile(mode=mode, delete=delete)


with open(os.devnull, "w") as _null:
    _have_rsync = subprocess.call(["which", "rsync"], stdout=_null)

if _have_rsync == 0:
    def copy_path_rsync(path_from, path_to, preserve=True, dereference=False):
        """Copy contents using rsync."""
        if os.path.isdir(path_from):
            path_from = path_from + os.sep
            assert_path(path_to)
        else:
            assert_path(os.path.dirname(path_to) + os.sep)

        args = "-rptgoD"
        if preserve:
            args += "t"
        if dereference:
            args += "l"
        else:
            args += "L"
        if subprocess.call(["rsync", args, path_from, path_to]) != 0:
            raise OSError("Error copying files: %s -> %s" % (
                path_from, path_to))

    def copy_path(*args, **kwargs):
        copy_path_rsync(*args, **kwargs)

else:
    def copy_path_shutil(path_from, path_to, preserve=True, dereference=False):
        """Copy contents using Python's shutil."""
        if os.path.isdir(path_from):
            # NOTE: will fail if destination already exists
            path_from = path_from + os.sep
            assert_path(path_to)
            shutil.copytree(path_from, path_to, symlinks=not dereference)

        else:
            assert_path(os.path.dirname(path_to) + os.sep)
            if os.path.islink(path_from):
                link_to = os.readlink(path_from)
                os.symlink(link_to, path_to)
            else:
                shutil.copy(path_from, path_to)
            if preserve:
                shutil.copymode(path_from, path_to)

    def copy_path(*args, **kwargs):
        copy_path_shutil(*args, **kwargs)


def copy_path_maybe(path_from, path_to):
    """Copy files only when contents differ."""
    if not os.path.exists(path_to) or os.path.isdir(path_from):
        copy_path(path_from, path_to)
        return True
    else:
        with open(path_from) as file_from,\
                open(path_to) as file_to:
            lines_from = file_from.readlines()
            lines_to = file_to.readlines()
        if lines_from == lines_to:
            return False
        else:
            copy_path(path_from, path_to)
            return True


# -----------------------------

def str2num(string):
    """Numeric value (``int`` or ``float``) of a string, if possible."""
    # TODO: use 'numpy.lib._iotools.StringConverter.upgrade'
    try:
        return int(string)
    except:
        try:
            return float(string)
        except:
            pass
    return string

# -----------------------------

# Set to True to see which instances are not memoized
SelectiveClassMemoize_DEBUG = False


class SelectiveClassMemoize (type):
    """Metaclass for selective memoization of object instantiation.

    This is useful for immutable objects that are costly to create and/or are
    created very often.

    Then, you must selectively use `memoize_new` to memoize those
    instances for which you wish to speedup instantiation::

       MyMemoizableClass.memoize_new(common set of construction arguments)
       MyMemoizableClass.memoize_new(another set set of common arguments)

    Thus, whenever you instantiate an object for the memoized class with the
    given set of object instantiation arguments, the memoized instance will be
    returned instead.

    .. warning::

       Mutation of memoized objects is strongly discouraged.

    """

    def __call__(cls, *args, **kwargs):
        mem = getattr(cls, "__SelectiveClassMemoize_mem")
        key = "%s" % repr((args, kwargs))
        if key in mem and cls is mem[key].__class__:
            return mem[key]
        if SelectiveClassMemoize_DEBUG:
            print("Not memoized:", cls, "::", key)
        return type.__call__(cls, *args, **kwargs)

    def memoize_new(cls, *args, **kwargs):
        """Create a memoized object with given parameters."""
        if not hasattr(cls, "__SelectiveClassMemoize_mem"):
            setattr(cls, "__SelectiveClassMemoize_mem", {})
        mem = getattr(cls, "__SelectiveClassMemoize_mem")
        key = "%s" % repr((args, kwargs))
        if not key in mem:
            mem[key] = type.__call__(cls, *args, **kwargs)


# -----------------------------

def _wraps(wrapped):
    return functools.wraps(wrapped=wrapped,
                           assigned=['__doc__'])


class ViewError (Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class OrderedSet (collections.MutableSet, pp.Pretty):
    """A mutable set preserving order of insertion.

    .. todo::

       All help should come from `~collections.MutableSet` instead of
       using `_wraps`.
    """

    @_wraps(collections.Container.__init__)
    def __init__(self, iterable=None, view_able=False):
        self._view_able = view_able
        if self._view_able:
            self._list = np.array([], dtype=object)
        else:
            self._list = []
        self._set_methods(False)
        self._base = None
        self._views = {}
        self._set = set()
        if iterable is not None:
            self |= iterable

    def set_view_able(self, view_able):
        """Set whether this object can produce "views" from it.

        Objects able to produce views have lower performance when adding new
        elements to them.

        See also
        --------
        OrderedSet.view

        """
        if view_able != self._view_able:
            if view_able:
                self._list = np.array(self._list, dtype=object)
            else:
                if len(self._views) > 0:
                    raise ValueError(
                        "cannot disable 'view_able' when views already exist")
                self._list = list(self._list)
            self._view_able = view_able
            self._set_methods(False)

    def view(self, index):
        """Create a view (sub-set) of this object.

        This object also becomes a view. Modifications to the elements of a view
        will also take effect on all other views of the same object.


        Parameters
        ----------
        index : slice


        See also
        --------
        OrderedSet.set_view_able

        """
        if not self._view_able:
            raise ValueError("the object is not 'view_able'")
        if not isinstance(index, slice):
            raise TypeError("view index must be a slice")

        self._set_methods(True)

        res = OrderedSet([], True)
        res._list = self._list[index]
        for elem in res._list:
            res._set.add(elem)
        res._base = self
        res._set_methods(True)

        self._views[id(res)] = weakref.ref(res)

        return res

    def __del__(self):
        if self._base is not None:
            del self._base._views[id(self)]

    def _set_methods(self, is_view):
        if self._view_able:
            if is_view:
                self._append = self._append_array_view
                self._remove = self._remove_array_view
                self._pop = self._pop_array_view
            else:
                self._append = self._append_array
                self._remove = self._remove_array
                self._pop = self._pop_array
        else:
            assert not is_view
            self._append = self._append_list
            self._remove = self._remove_list
            self._pop = self._pop_list

    def _append_list(self, value):
        self._list.append(value)

    def _remove_list(self, value):
        if self._base is not None:
            self._base.remove(value)
        else:
            self._list.remove(value)
            for v in six.itervalues(self._views):
                v()._list.remove(value)
                v()._set.remove(value)

    def _pop_list(self, index):
        self._list.pop(index)

    def _append_array(self, value):
        self._list = np.append(self._list, value)

    def _remove_array(self, value):
        self._list = np.delete(self._list, np.where(self._list == value))

    def _pop_array(self, index):
        self._list = np.delete(self._list, index)

    def _append_array_view(self, value):
        raise ViewError("cannot append to a view")

    def _remove_array_view(self, value):
        raise ViewError("cannot remove from a view")

    def _pop_array_view(self, index):
        raise ViewError("cannot pop from a view")

    def _repr_pretty_(self, p, cycle):
        with self.pformat(p, cycle):
            p.pretty(list(self._list))

    def __repr__(self):
        return pp.Pretty.__repr__(self)

    def get_index(self, index):
        """Get item at the 'index'th position."""
        return self._list[index]

    def copy(self):
        return OrderedSet(self, self._view_able)

    def sorted(self, *args, **kwargs):
        """Same as `sort`, but returns a sorted copy."""
        res = self.copy()
        res.sort(*args, **kwargs)
        return res

    def sort(self, key=None, reverse=False):
        """Sort set in-place.

        Follows the same semantics of Python's built-in `sorted`.

        """
        if self._view_able:
            contents = list(self._list)
        else:
            contents = self._list

        contents.sort(key=key, reverse=reverse)

        if self._view_able:
            self._list[:] = contents

    # Container

    @_wraps(set.__contains__)
    def __contains__(self, key):
        return key in self._set

    # Sized

    @_wraps(set.__len__)
    def __len__(self):
        return len(self._list)

    # Iterable

    @_wraps(set.__iter__)
    def __iter__(self):
        return iter(self._list)

    # MutableSet

    def add(self, key):
        old_length = len(self._list)
        self._set.add(key)
        if len(self._set) != old_length:
            try:
                self._append(key)
            except ViewError:
                self._set.remove(key)
                raise
    add.__doc__ = collections.MutableSet.add.__doc__

    def discard(self, key):
        old_length = len(self._list)
        self._set.remove(key)
        if len(self._set) != old_length:
            try:
                self._remove(key)
            except ViewError:
                self._set.add(key)
                raise
    discard.__doc__ = collections.MutableSet.discard.__doc__
    discard.__doc__ += "\n\nThis operation has a cost of O(n)."

    @_wraps(collections.MutableSet.pop)
    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self._pop(-1) if last else self._pop(0)
        self._set.remove(key)
        return key

    # Pickling

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict["_append"]
        del odict["_remove"]
        del odict["_pop"]
        del odict["_base"]
        del odict["_views"]
        return odict

    def __setstate__(self, odict):
        self.__dict__.update(odict)
        self._base = None
        self._views = {}
        self._set_methods(False)


# -----------------------------

def find_files(template, path=None, absolute_path=False, sort=True):
    """Find files matching a given template.

    Returns an 'InstanceGroup' with all paths of existing files matching the
    given template. Each matching file path is an `Instance` with the extracted
    variables in the `template`.

    Parameters
    ----------
    template : str
        Template of file paths to find.
    path : str, optional
        On each resulting Instance, add a variable with the given name with the
        file path.
    absolute_path : bool, optional
        Make the value in `path` absolute.
    sort : bool, optional
        Sort the file paths according to the alphanumeric order of each of the
        variables in `template`, in that specific order.

    Raises
    ------
    ValueError
        The variable in `path` is already present in `template`.

    See Also
    --------
    sciexp2.common.text.extract
        Argument `template` is interpreted following the extraction syntax.

    Notes
    -----
    If `template` ends with ``/`` it will search for matching paths, and will
    search for matching files otherwise.

    Environment variables and user home directories in `template` will be expanded.

    """
    from . import text
    from .instance import InstanceGroup, Instance

    if not isinstance(template, six.string_types):
        raise ValueError("Not an expression: " + template)
    if path is not None and not isinstance(path, six.string_types):
        raise ValueError("path must be either None or a string")
    if path in text.get_variables(template):
        raise ValueError("path variable is already present in template")

    template_is_dir = template[-1] == "/" if len(template) > 0 else False
    template_is_abs = os.path.isabs(template)
    template = get_path(template) + "$"

    # get the initial directory to search
    start_dir = ""
    for part in template.split(os.sep):
        if part == "":
            continue
        if start_dir == "" and not template_is_abs:
            cur_dir = part
        else:
            cur_dir = os.sep.join([start_dir, part])
        try:
            text.translate(cur_dir, {})
        except text.VariableError:
            break
        if os.path.isdir(cur_dir):
            start_dir = cur_dir
        else:
            break

    extractor = text.Extractor(template)
    res = InstanceGroup()

    def add(env, target_path):
        # use numbers whenever possible (for later number-aware sorting)
        for key, val in six.iteritems(env):
            env[key] = str2num(val)
        if path is not None:
            if absolute_path:
                target_path = os.path.abspath(target_path)
            env[path] = target_path
        res.add(Instance(env))

    for dir_path, subdir_list, file_list in os.walk(start_dir):
        if template_is_dir:
            try:
                env = extractor.extract(dir_path + os.path.sep)
            except text.ExtractError:
                pass
            else:
                add(env, dir_path)
        else:
            for file_path in file_list:
                target_path = os.path.join(dir_path, file_path)
                try:
                    env = extractor.extract(target_path)
                except text.ExtractError:
                    pass
                else:
                    add(env, target_path)

    if sort:
        # sort result according to file sorting
        variables = text.get_variables(template)
        res.sort(variables)

    return res


# -----------------------------

def execute_with_sigint(cmd, **kwargs):
    """Execute a command and forward SIGINT to it.

    Parameters
    ----------
    cmd : list of string
        Command to execute
    kwargs : dict
        Additional arguments to subprocess.Popen.

    Returns
    -------
    Integer with the command's return code.

    """
    preexec_fn = kwargs.pop("preexec_fn", None)
    def preexec():
        os.setpgrp()
        if preexec_fn:
            preexec_fn()

    signals = [
        ("SIGINT", signal.SIGINT),
        ("SIGTERM", signal.SIGTERM),
        ("SIGKILL", signal.SIGKILL),
    ]

    state = dict(proc=None,
                 error=False,
                 signal_idx=0)

    def run():
        if state["proc"] is None:
            if not state["error"]:
                state["proc"] = subprocess.Popen(cmd, preexec_fn=preexec, **kwargs)
            else:
                return
        state["proc"].wait()

    def run_with_except(depth=0):
        try:
            run()
        except KeyboardInterrupt:
            state["error"] = True
            info = signals[state["signal_idx"]]
            progress.log(progress.LVL_NONE,
                         "WARNING: Interrupting child command with %s" % info[0])
            state["proc"].send_signal(info[1])
            if state["signal_idx"] < len(signals) - 1:
                state["signal_idx"] += 1
            run_with_except(depth + 1)
            if depth == 0:
                raise

    run_with_except()
    return state["proc"].returncode
