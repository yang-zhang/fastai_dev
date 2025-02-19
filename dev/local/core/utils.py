#AUTOGENERATED! DO NOT EDIT! File to edit: dev/01a_utils.ipynb (unless otherwise specified).

__all__ = ['ifnone', 'get_class', 'mk_class', 'wrap_class', 'store_attr', 'attrdict', 'properties', 'camel2snake',
           'class2attr', 'hasattrs', 'tuplify', 'detuplify', 'replicate', 'uniqueify', 'setify', 'is_listy', 'range_of',
           'groupby', 'merge', 'first', 'shufflish', 'IterLen', 'ReindexCollection', 'lt', 'gt', 'le', 'ge', 'eq', 'ne',
           'add', 'sub', 'mul', 'truediv', 'Inf', 'true', 'stop', 'gen', 'chunked', 'retain_type', 'retain_types',
           'show_title', 'ShowTitle', 'Int', 'Float', 'Str', 'num_methods', 'rnum_methods', 'inum_methods', 'Tuple',
           'TupleTitled', 'trace', 'compose', 'maps', 'partialler', 'mapped', 'instantiate', 'Self', 'Self', 'bunzip',
           'join_path_file', 'sort_by_run', 'subplots', 'show_image', 'show_titled_image', 'ArrayBase',
           'ArrayImageBase', 'ArrayImage', 'ArrayImageBW', 'ArrayMask', 'PrettyString', 'display_df', 'round_multiple',
           'even_mults', 'num_cpus', 'add_props']

#Cell
from ..test import *
from .foundation import *
from .imports import *

#Cell
def ifnone(a, b):
    "`b` if `a` is None else `a`"
    return b if a is None else a

#Cell
def get_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    "Dynamically create a class, optionally inheriting from `sup`, containing `fld_names`"
    attrs = {}
    for f in fld_names: attrs[f] = None
    for f in L(funcs): attrs[f.__name__] = f
    for k,v in flds.items(): attrs[k] = v
    sup = ifnone(sup, ())
    if not isinstance(sup, tuple): sup=(sup,)

    def _init(self, *args, **kwargs):
        for i,v in enumerate(args): setattr(self, list(attrs.keys())[i], v)
        for k,v in kwargs.items(): setattr(self,k,v)

    def _repr(self):
        return '\n'.join(f'{o}: {getattr(self,o)}' for o in set(dir(self))
                         if not o.startswith('_') and not isinstance(getattr(self,o), types.MethodType))

    if not sup: attrs['__repr__'] = _repr
    attrs['__init__'] = _init
    res = type(nm, sup, attrs)
    if doc is not None: res.__doc__ = doc
    return res

#Cell
def mk_class(nm, *fld_names, sup=None, doc=None, funcs=None, mod=None, **flds):
    "Create a class using `get_class` and add to the caller's module"
    if mod is None: mod = inspect.currentframe().f_back.f_locals
    res = get_class(nm, *fld_names, sup=sup, doc=doc, funcs=funcs, **flds)
    mod[nm] = res

#Cell
def wrap_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    "Decorator: makes function a method of a new class `nm` passing parameters to `mk_class`"
    def _inner(f):
        mk_class(nm, *fld_names, sup=sup, doc=doc, funcs=L(funcs)+f, mod=f.__globals__, **flds)
        return f
    return _inner

#Cell
def store_attr(self, nms):
    "Store params named in comma-separated `nms` from calling context into attrs in `self`"
    mod = inspect.currentframe().f_back.f_locals
    for n in re.split(', *', nms): setattr(self,n,mod[n])

#Cell
def attrdict(o, *ks):
    "Dict from each `k` in `ks` to `getattr(o,k)`"
    return {k:getattr(o,k) for k in ks}

#Cell
def properties(cls, *ps):
    "Change attrs in `cls` with names in `ps` to properties"
    for p in ps: setattr(cls,p,property(getattr(cls,p)))

#Cell
_camel_re1 = re.compile('(.)([A-Z][a-z]+)')
_camel_re2 = re.compile('([a-z0-9])([A-Z])')

def camel2snake(name):
    s1   = re.sub(_camel_re1, r'\1_\2', name)
    return re.sub(_camel_re2, r'\1_\2', s1).lower()

test_eq(camel2snake('ClassAreCamel'), 'class_are_camel')

#Cell
def class2attr(self, cls_name):
    return camel2snake(re.sub(rf'{cls_name}$', '', self.__class__.__name__) or cls_name.lower())

#Cell
def hasattrs(o,attrs):
    for attr in attrs:
        if not hasattr(o,attr): return False
    return True

#Cell
def tuplify(o, use_list=False, match=None):
    "Make `o` a tuple"
    return tuple(L(o, use_list=use_list, match=match))

#Cell
def detuplify(x):
    "If `x` is a tuple with one thing, extract it"
    return None if len(x)==0 else x[0] if len(x)==1 else x

#Cell
def replicate(item,match):
    "Create tuple of `item` copied `len(match)` times"
    return (item,)*len(match)

#Cell
def uniqueify(x, sort=False, bidir=False, start=None):
    "Return the unique elements in `x`, optionally `sort`-ed, optionally return the reverse correspondance."
    res = L(x).unique()
    if start is not None: res = start+res
    if sort: res.sort()
    if bidir: return res, res.val2idx()
    return res

#Cell
def setify(o): return o if isinstance(o,set) else set(L(o))

#Cell
def is_listy(x):
    "`isinstance(x, (tuple,list,L))`"
    return isinstance(x, (tuple,list,L,slice,Generator))

#Cell
def range_of(x):
    "All indices of collection `x` (i.e. `list(range(len(x)))`)"
    return list(range(len(x)))

#Cell
def groupby(x, key):
    "Like `itertools.groupby` but doesn't need to be sorted, and isn't lazy"
    res = {}
    for o in x: res.setdefault(key(o), []).append(o)
    return res

#Cell
def merge(*ds):
    "Merge all dictionaries in `ds`"
    return {k:v for d in ds if d is not None for k,v in d.items()}

#Cell
def first(x):
    "First element of `x`; i.e. a shortcut for `next(iter(x))`"
    return next(iter(x))

#Cell
def shufflish(x, pct=0.04):
    "Randomly relocate items of `x` up to `pct` of `len(x)` from their starting location"
    n = len(x)
    return L(x[i] for i in sorted(range_of(x), key=lambda o: o+n*(1+random.random()*pct)))

#Cell
class IterLen:
    "Base class to add iteration to anything supporting `len` and `__getitem__`"
    def __iter__(self): return (self[i] for i in range_of(self))

#Cell
@docs
class ReindexCollection(GetAttr, IterLen):
    "Reindexes collection `coll` with indices `idxs` and optional LRU cache of size `cache`"
    _default='coll'
    def __init__(self, coll, idxs=None, cache=None):
        self.coll,self.idxs,self.cache = coll,ifnone(idxs,L.range(coll)),cache
        def _get(self, i): return self.coll[i]
        self._get = types.MethodType(_get,self)
        if cache is not None: self._get = functools.lru_cache(maxsize=cache)(self._get)

    def __getitem__(self, i): return self._get(self.idxs[i])
    def __len__(self): return len(self.coll)
    def reindex(self, idxs): self.idxs = idxs
    def shuffle(self): random.shuffle(self.idxs)
    def cache_clear(self): self._get.cache_clear()

    _docs = dict(reindex="Replace `self.idxs` with idxs",
                shuffle="Randomly shuffle indices",
                cache_clear="Clear LRU cache")

#Cell
def _oper(op,a,b=None): return (lambda o:op(o,a)) if b is None else op(a,b)

def _mk_op(nm, mod=None):
    "Create an operator using `oper` and add to the caller's module"
    if mod is None: mod = inspect.currentframe().f_back.f_locals
    op = getattr(operator,nm)
    def _inner(a,b=None): return _oper(op, a,b)
    _inner.__name__ = _inner.__qualname__ = nm
    _inner.__doc__ = f'Same as `operator.{nm}`, or returns partial if 1 arg'
    mod[nm] = _inner

#Cell
for op in 'lt gt le ge eq ne add sub mul truediv'.split(): _mk_op(op)

#Cell
class _InfMeta(type):
    @property
    def count(self): return itertools.count()
    @property
    def zeros(self): return itertools.cycle([0])
    @property
    def ones(self):  return itertools.cycle([1])
    @property
    def nones(self): return itertools.cycle([None])

#Cell
class Inf(metaclass=_InfMeta):
    "Infinite lists"
    pass

#Cell
def true(*args, **kwargs):
    "Predicate: always `True`"
    return True

#Cell
def stop(e=StopIteration):
    "Raises exception `e` (by default `StopException`) even if in an expression"
    raise e

#Cell
def gen(func, seq, cond=true):
    "Like `(func(o) for o in seq if cond(func(o)))` but handles `StopIteration`"
    return itertools.takewhile(cond, map(func,seq))

#Cell
def chunked(it, cs, drop_last=False):
    if not isinstance(it, Iterator): it = iter(it)
    while True:
        res = list(itertools.islice(it, cs))
        if res and (len(res)==cs or not drop_last): yield res
        if len(res)<cs: return

#Cell
def retain_type(new, old=None, typ=None):
    "Cast `new` to type of `old` if it's a superclass"
    # e.g. old is TensorImage, new is Tensor - if not subclass then do nothing
    if new is None: return new
    assert old is not None or typ is not None
    if typ is None:
        if not isinstance(old, type(new)): return new
        typ = old if isinstance(old,type) else type(old)
    # Do nothing the new type is already an instance of requested type (i.e. same type)
    return typ(new) if typ!=NoneType and not isinstance(new, typ) else new

#Cell
def retain_types(new, old=None, typs=None):
    "Cast each item of `new` to type of matching item in `old` if it's a superclass"
    if not is_listy(new): return retain_type(new, old, typs)
    return type(new)(L(new, old, typs).map_zip(retain_type, cycled=True))

#Cell
@patch
def split_arr(df:pd.DataFrame, from_col):
    "Split col `from_col` (containing arrays) in `DataFrame` `df` into separate colums"
    col = df[from_col]
    n = len(col.iloc[0])
    cols = [f'{from_col}{o}' for o in range(n)]
    df[cols] = pd.DataFrame(df[from_col].values.tolist())
    df.drop(columns=from_col, inplace=True)

#Cell
def show_title(o, ax=None, ctx=None, label=None, color='black', **kwargs):
    "Set title of `ax` to `o`, or print `o` if `ax` is `None`"
    ax = ifnone(ax,ctx)
    if ax is None: print(o)
    elif hasattr(ax, 'set_title'):
        t = ax.title.get_text()
        if len(t) > 0: o = t+'\n'+str(o)
        ax.set_title(o, color=color)
    elif isinstance(ax, pd.Series):
        while label in ax: label += '_'
        ax = ax.append(pd.Series({label: o}))
    return ax

#Cell
class ShowTitle:
    "Base class that adds a simple `show`"
    _show_args = {'label': 'text'}
    def show(self, ctx=None, **kwargs): return show_title(str(self), ctx=ctx, **merge(self._show_args, kwargs))

class Int(int, ShowTitle): pass
class Float(float, ShowTitle): pass
class Str(str, ShowTitle): pass
add_docs(Int, "An `int` with `show`"); add_docs(Str, "An `str` with `show`"); add_docs(Float, "An `float` with `show`")

#Cell
num_methods = """
    __add__ __sub__ __mul__ __matmul__ __truediv__ __floordiv__ __mod__ __divmod__ __pow__
    __lshift__ __rshift__ __and__ __xor__ __or__ __neg__ __pos__ __abs__
""".split()
rnum_methods = """
    __radd__ __rsub__ __rmul__ __rmatmul__ __rtruediv__ __rfloordiv__ __rmod__ __rdivmod__
    __rpow__ __rlshift__ __rrshift__ __rand__ __rxor__ __ror__
""".split()
inum_methods = """
    __iadd__ __isub__ __imul__ __imatmul__ __itruediv__
    __ifloordiv__ __imod__ __ipow__ __ilshift__ __irshift__ __iand__ __ixor__ __ior__
""".split()

#Cell
class Tuple(tuple):
    "A `tuple` with elementwise ops and more friendly __init__ behavior"
    def __new__(cls, x=None, *rest):
        if x is None: x = ()
        if not isinstance(x,tuple):
            if len(rest): x = (x,)
            else:
                try: x = tuple(iter(x))
                except TypeError: x = (x,)
        return super().__new__(cls, x+rest if rest else x)

    def _op(self,op,*args):
        if not isinstance(self,Tuple): self = Tuple(self)
        return type(self)(map(op,self,*map(cycle, args)))

    def mul(self,*args):
        "`*` is already defined in `tuple` for replicating, so use `mul` instead"
        return Tuple._op(self, operator.mul,*args)

    def add(self,*args):
        "`+` is already defined in `tuple` for concat, so use `add` instead"
        return Tuple._op(self, operator.add,*args)

def _get_op(op):
    if isinstance(op,str): op = getattr(operator,op)
    def _f(self,*args): return self._op(op,*args)
    return _f

for n in num_methods:
    if not hasattr(Tuple, n) and hasattr(operator,n): setattr(Tuple,n,_get_op(n))

for n in 'eq ne lt le gt ge'.split(): setattr(Tuple,n,_get_op(n))
setattr(Tuple,'__invert__',_get_op('__not__'))
setattr(Tuple,'max',_get_op(max))
setattr(Tuple,'min',_get_op(min))

#Cell
class TupleTitled(Tuple, ShowTitle):
    "A `Tuple` with `show`"
    pass

#Cell
def trace(f):
    "Add `set_trace` to an existing function `f`"
    def _inner(*args,**kwargs):
        set_trace()
        return f(*args,**kwargs)
    return _inner

#Cell
def compose(*funcs, order=None):
    "Create a function that composes all functions in `funcs`, passing along remaining `*args` and `**kwargs` to all"
    funcs = L(funcs)
    if len(funcs)==0: return noop
    if len(funcs)==1: return funcs[0]
    if order is not None: funcs = funcs.sorted(order)
    def _inner(x, *args, **kwargs):
        for f in L(funcs): x = f(x, *args, **kwargs)
        return x
    return _inner

#Cell
def maps(*args, retain=noop):
    "Like `map`, except funcs are composed first"
    f = compose(*args[:-1])
    def _f(b): return retain(f(b), b)
    return map(_f, args[-1])

#Cell
def partialler(f, *args, order=None, **kwargs):
    "Like `functools.partial` but also copies over docstring"
    fnew = partial(f,*args,**kwargs)
    fnew.__doc__ = f.__doc__
    if order is not None: fnew.order=order
    elif hasattr(f,'order'): fnew.order=f.order
    return fnew

#Cell
def mapped(f, it):
    "map `f` over `it`, unless it's not listy, in which case return `f(it)`"
    return L(it).map(f) if is_listy(it) else f(it)

#Cell
def instantiate(t):
    "Instantiate `t` if it's a type, otherwise do nothing"
    return t() if isinstance(t, type) else t

#Cell
class _Self:
    "An alternative to `lambda` for calling methods on passed object."
    def __init__(self): self.nms,self.args,self.kwargs,self.ready = [],[],[],True
    def __repr__(self): return f'self: {self.nms}({self.args}, {self.kwargs})'

    def __call__(self, *args, **kwargs):
        if self.ready:
            x = args[0]
            for n,a,k in zip(self.nms,self.args,self.kwargs):
                x = getattr(x,n)
                if callable(x) and a is not None: x = x(*a, **k)
            return x
        else:
            self.args.append(args)
            self.kwargs.append(kwargs)
            self.ready = True
            return self

    def __getattr__(self,k):
        if not self.ready:
            self.args.append(None)
            self.kwargs.append(None)
        self.nms.append(k)
        self.ready = False
        return self

class _SelfCls:
    def __getattr__(self,k): return getattr(_Self(),k)

Self = _SelfCls()

#Cell
@patch
def readlines(self:Path, hint=-1):
    "Read the content of `fname`"
    with self.open() as f: return f.readlines(hint)

#Cell
@patch
def read(self:Path, size=-1):
    "Read the content of `fname`"
    with self.open() as f: return f.read(size)

#Cell
@patch
def write(self:Path, txt):
    "Write `txt` to `self`, creating directories as needed"
    self.parent.mkdir(parents=True,exist_ok=True)
    with self.open('w') as f: f.write(txt)

#Cell
@patch
def save(fn:Path, o):
    "Save a pickle file, to a file name or opened file"
    if not isinstance(fn, io.IOBase): fn = open(fn,'wb')
    try: pickle.dump(o, fn)
    finally: fn.close()

#Cell
@patch
def load(fn:Path):
    "Load a pickle file from a file name or opened file"
    if not isinstance(fn, io.IOBase): fn = open(fn,'rb')
    try: return pickle.load(fn)
    finally: fn.close()

#Cell
#NB: Please don't move this to a different line or module, since it's used in testing `get_source_link`
@patch
def ls(self:Path, n_max=None, file_type=None, file_exts=None):
    "Contents of path as a list"
    extns=L(file_exts)
    if file_type: extns += L(k for k,v in mimetypes.types_map.items() if v.startswith(file_type+'/'))
    has_extns = len(extns)==0
    res = (o for o in self.iterdir() if has_extns or o.suffix in extns)
    if n_max is not None: res = itertools.islice(res, n_max)
    return L(res)

#Cell
def bunzip(fn):
    "bunzip `fn`, raising exception if output already exists"
    fn = Path(fn)
    assert fn.exists(), f"{fn} doesn't exist"
    out_fn = fn.with_suffix('')
    assert not out_fn.exists(), f"{out_fn} already exists"
    with bz2.BZ2File(fn, 'rb') as src, out_fn.open('wb') as dst:
        for d in iter(lambda: src.read(1024*1024), b''): dst.write(d)

#Cell
def join_path_file(file, path, ext=''):
    "Return `path/file` if file is a string or a `Path`, file otherwise"
    if not isinstance(file, (str, Path)): return file
    path.mkdir(parents=True, exist_ok=True)
    return path/f'{file}{ext}'

#Cell
def _is_instance(f, gs):
    tst = [g if type(g) in [type, 'function'] else g.__class__ for g in gs]
    for g in tst:
        if isinstance(f, g) or f==g: return True
    return False

def _is_first(f, gs):
    for o in L(getattr(f, 'run_after', None)):
        if _is_instance(o, gs): return False
    for g in gs:
        if _is_instance(f, L(getattr(g, 'run_before', None))): return False
    return True

def sort_by_run(fs):
    end = L(fs).attrgot('toward_end')
    inp,res = L(fs)[~end] + L(fs)[end], L()
    while len(inp):
        for i,o in enumerate(inp):
            if _is_first(o, inp):
                res.append(inp.pop(i))
                break
        else: raise Exception("Impossible to sort")
    return res

#Cell
@delegates(plt.subplots, keep=True)
def subplots(nrows=1, ncols=1, figsize=None, imsize=4, **kwargs):
    if figsize is None: figsize=(imsize*ncols,imsize*nrows)
    fig,ax = plt.subplots(nrows, ncols, figsize=figsize, **kwargs)
    if nrows*ncols==1: ax = array([ax])
    return fig,ax

#Cell
def show_image(im, ax=None, figsize=None, title=None, ctx=None, **kwargs):
    "Show a PIL or PyTorch image on `ax`."
    ax = ifnone(ax,ctx)
    if ax is None: _,ax = plt.subplots(figsize=figsize)
    # Handle pytorch axis order
    if hasattrs(im, ('data','cpu','permute')):
        im = im.data.cpu()
        if im.shape[0]<5: im=im.permute(1,2,0)
    elif not isinstance(im,np.ndarray): im=array(im)
    # Handle 1-channel images
    if im.shape[-1]==1: im=im[...,0]
    ax.imshow(im, **kwargs)
    if title is not None: ax.set_title(title)
    ax.axis('off')
    return ax

#Cell
def show_titled_image(o, **kwargs):
    "Call `show_image` destructuring `o` to `(img,title)`"
    show_image(o[0], title=str(o[1]), **kwargs)

#Cell
class ArrayBase(ndarray):
    def __new__(cls, x, *args, **kwargs):
        if isinstance(x,tuple): super().__new__(cls, x, *args, **kwargs)
        if args or kwargs: raise RuntimeError('Unknown array init args')
        if not isinstance(x,ndarray): x = array(x)
        return x.view(cls)

#Cell
class ArrayImageBase(ArrayBase):
    _show_args = {'cmap':'viridis'}
    def show(self, ctx=None, **kwargs):
        return show_image(self, ctx=ctx, **{**self._show_args, **kwargs})

#Cell
class ArrayImage(ArrayImageBase): pass

#Cell
class ArrayImageBW(ArrayImage): _show_args = {'cmap':'Greys'}

#Cell
class ArrayMask(ArrayImageBase): _show_args = {'alpha':0.5, 'cmap':'tab20', 'interpolation':'nearest'}

#Cell
class PrettyString(str):
    "Little hack to get strings to show properly in Jupyter."
    def __repr__(self): return self

#Cell
def display_df(df):
    "Display `df` in a notebook or defaults to print"
    try: from IPython.display import display, HTML
    except: return print(df)
    display(HTML(df.to_html()))

#Cell
def round_multiple(x, mult, round_down=False):
    "Round `x` to nearest multiple of `mult`"
    def _f(x_): return (int if round_down else round)(x_/mult)*mult
    res = L(x).map(_f)
    return res if is_listy(x) else res[0]

#Cell
def even_mults(start, stop, n):
    "Build log-stepped array from `start` to `stop` in `n` steps."
    if n==1: return stop
    mult = stop/start
    step = mult**(1/(n-1))
    return np.array([start*(step**i) for i in range(n)])

#Cell
def num_cpus():
    "Get number of cpus"
    try:                   return len(os.sched_getaffinity(0))
    except AttributeError: return os.cpu_count()

defaults.cpus = num_cpus()

#Cell
def add_props(f, n=2):
    "Create properties passing each of `range(n)` to f"
    return (property(partial(f,i)) for i in range(n))