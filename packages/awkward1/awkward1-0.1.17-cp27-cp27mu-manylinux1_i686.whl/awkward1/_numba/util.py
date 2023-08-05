# BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

import sys

import numpy
import numba
import llvmlite.ir.types

from .._numba import cpu

py27 = (sys.version_info[0] < 3)

RefType = numba.int64

index8tpe = numba.types.Array(numba.int8, 1, "C")
index32tpe = numba.types.Array(numba.int32, 1, "C")
index64tpe = numba.types.Array(numba.int64, 1, "C")
def indextpe(bitwidth):
    if bitwidth == 8:
        return index8tpe
    elif bitwidth == 32:
        return index32tpe
    elif bitwidth == 64:
        return index64tpe
    else:
        raise AssertionError(bitwidth)

if not py27:
    exec("""
def debug(context, builder, *args):
    assert len(args) % 2 == 0
    tpes, vals = args[0::2], args[1::2]
    context.get_function(print, numba.none(*tpes))(builder, tuple(vals))
""", globals())

def cast(context, builder, fromtpe, totpe, val):
    if isinstance(fromtpe, llvmlite.ir.types.IntType):
        if fromtpe.width == 8:
            fromtpe = numba.int8
        elif fromtpe.width == 16:
            fromtpe = numba.int16
        elif fromtpe.width == 32:
            fromtpe = numba.int32
        elif fromtpe.width == 64:
            fromtpe = numba.int64
        else:
            raise AssertionError("unrecognized bitwidth")
    if fromtpe.bitwidth < totpe.bitwidth:
        return builder.sext(val, context.get_value_type(totpe))
    elif fromtpe.bitwidth > totpe.bitwidth:
        return builder.trunc(val, context.get_value_type(totpe))
    else:
        return val

def arrayptr(context, builder, tpe, val):
    return numba.targets.arrayobj.make_array(tpe)(context, builder, val).data

def arraylen(context, builder, tpe, val, totpe=None):
    if isinstance(tpe, numba.types.Array):
        out = numba.targets.arrayobj.array_len(context, builder, numba.intp(tpe), (val,))
    else:
        out = tpe.lower_len(context, builder, numba.intp(tpe), (val,))
    if totpe is None:
        return out
    else:
        return cast(context, builder, numba.intp, totpe, out)

def call(context, builder, fcn, args, errormessage=None):
    fcntpe = context.get_function_pointer_type(fcn.numbatpe)
    fcnval = context.add_dynamic_addr(builder, fcn.numbatpe.get_pointer(fcn), info=fcn.name)
    fcnptr = builder.bitcast(fcnval, fcntpe)

    err = context.call_function_pointer(builder, fcnptr, args)

    if fcn.restype is cpu.Error:
        assert errormessage is not None, "this function can return an error"
        proxyerr = numba.cgutils.create_struct_proxy(cpu.Error.numbatpe)(context, builder, value=err)
        with builder.if_then(builder.icmp_signed("!=", proxyerr.str, context.get_constant(numba.intp, 0)), likely=False):
            context.call_conv.return_user_exc(builder, ValueError, (errormessage,))

            # pyapi = context.get_python_api(builder)
            # exc = pyapi.serialize_object(ValueError(errormessage))
            # excptr = context.call_conv._get_excinfo_argument(builder.function)
            # if excptr.name == "excinfo" and excptr.type == llvmlite.llvmpy.core.Type.pointer(llvmlite.llvmpy.core.Type.pointer(llvmlite.llvmpy.core.Type.struct([llvmlite.llvmpy.core.Type.pointer(llvmlite.llvmpy.core.Type.int(8)), llvmlite.llvmpy.core.Type.int(32)]))):
            #     builder.store(exc, excptr)
            #     builder.ret(numba.targets.callconv.RETCODE_USEREXC)
            # elif excptr.name == "py_args" and excptr.type == llvmlite.llvmpy.core.Type.pointer(llvmlite.llvmpy.core.Type.int(8)):
            #     pyapi.raise_object(exc)
            #     builder.ret(llvmlite.llvmpy.core.Constant.null(context.get_value_type(numba.types.pyobject)))
            # else:
            #     raise AssertionError("unrecognized exception calling convention: {}".format(excptr))

def newindex8(context, builder, lentpe, lenval):
    return numba.targets.arrayobj.numpy_empty_nd(context, builder, index8tpe(lentpe), (lenval,))
def newindex32(context, builder, lentpe, lenval):
    return numba.targets.arrayobj.numpy_empty_nd(context, builder, index32tpe(lentpe), (lenval,))
def newindex64(context, builder, lentpe, lenval):
    return numba.targets.arrayobj.numpy_empty_nd(context, builder, index64tpe(lentpe), (lenval,))
def newindex(bitwidth, context, builder, lentpe, lenval):
    if bitwidth == 8:
        return newindex8(context, builder, lentpe, lenval)
    elif bitwidth == 32:
        return newindex32(context, builder, lentpe, lenval)
    elif bitwidth == 64:
        return newindex64(context, builder, lentpe, lenval)
    else:
        raise AssertionError(bitwidth)

@numba.jit(nopython=True)
def shapeat(shapeat, array, at, ndim):
    redat = at - (ndim - array.ndim)
    if redat < 0:
        return 1
    elif shapeat == 1:
        return array.shape[redat]
    elif shapeat == array.shape[redat] or array.shape[redat] == 1:
        return shapeat
    else:
        raise ValueError("cannot broadcast arrays to the same shape")

@numba.generated_jit(nopython=True)
def broadcast_to(array, shape):
    if isinstance(array, numba.types.Array):
        def impl(array, shape):
            out = numpy.empty(shape, array.dtype)
            out[:] = array
            return out
        return impl
    elif isinstance(array, numba.types.Integer):
        def impl(array, shape):
            return numpy.full(shape, array, numpy.int64)
        return impl
    else:
        return lambda array, shape: array

@numba.generated_jit(nopython=True)
def broadcast_arrays(arrays):
    if not isinstance(arrays, numba.types.BaseTuple) or not any(isinstance(x, numba.types.Array) for x in arrays.types):
        return lambda arrays: arrays

    else:
        ndim = max(t.ndim if isinstance(t, numba.types.Array) else 1 for t in arrays.types)
        def getshape(i, at):
            if i == -1:
                return "1"
            elif isinstance(arrays.types[i], numba.types.Array):
                return "shapeat({}, arrays[{}], {}, {})".format(getshape(i - 1, at), i, at, ndim)
            else:
                return getshape(i - 1, at)
        g = {"shapeat": shapeat, "broadcast_to": broadcast_to}
        exec("""
def impl(arrays):
    shape = ({})
    return ({})
""".format(" ".join(getshape(len(arrays.types) - 1, at) + "," for at in range(ndim)),
           " ".join("broadcast_to(arrays[{}], shape),".format(at) if isinstance(arrays.types[at], (numba.types.Array, numba.types.Integer)) else "arrays[{}],".format(at) for at in range(len(arrays.types)))), g)
        return g["impl"]

def typing_broadcast_arrays(arrays):
    if not isinstance(arrays, numba.types.BaseTuple) or not any(isinstance(x, numba.types.Array) for x in arrays.types):
        return arrays
    else:
        return numba.types.Tuple([numba.types.Array(numba.int64, 1, "C") if isinstance(t, numba.types.Integer) else t for t in arrays.types])

@numba.generated_jit(nopython=True)
def regularize_slice(arrays):
    if not isinstance(arrays, numba.types.BaseTuple) and isinstance(arrays, (numba.types.ArrayCompatible, numba.types.List)) and isinstance(arrays.dtype, numba.types.Boolean):
        return lambda arrays: numpy.nonzero(arrays)

    elif not isinstance(arrays, numba.types.BaseTuple) or not any(isinstance(t, (numba.types.ArrayCompatible, numba.types.List)) for t in arrays.types):
        return lambda arrays: arrays

    else:
        code = "def impl(arrays):\n"
        indexes = []   # all entries have trailing commas to ensure output is a tuple
        for i, t in enumerate(arrays.types):
            if isinstance(t, (numba.types.ArrayCompatible, numba.types.List)) and isinstance(t.dtype, numba.types.Boolean):
                code += "    x{} = numpy.nonzero(arrays[{}])\n".format(i, i)
                indexes.extend(["x{}[{}],".format(i, j) for j in range(arrays.types[i].ndim)])
            elif isinstance(t, (numba.types.ArrayCompatible, numba.types.List)) and isinstance(t.dtype, numba.types.Integer):
                indexes.append("numpy.asarray(arrays[{}], numpy.int64),".format(i))
            elif isinstance(t, (numba.types.ArrayCompatible, numba.types.List)):
                raise TypeError("arrays must have boolean or integer type")
            else:
                indexes.append("arrays[{}],".format(i))
        code += "    return ({})".format(" ".join(indexes))
        g = {"numpy": numpy}
        exec(code, g)
        return g["impl"]

def typing_regularize_slice(arrays):
    out = ()
    if not isinstance(arrays, numba.types.BaseTuple) and isinstance(arrays, (numba.types.ArrayCompatible, numba.types.List)) and isinstance(arrays.dtype, numba.types.Boolean):
        return numba.types.Tuple(arrays.ndims*(numba.types.Array(numba.int64, 1, "C"),))

    elif not isinstance(arrays, numba.types.BaseTuple) or not any(isinstance(t, (numba.types.ArrayCompatible, numba.types.List)) for t in arrays.types):
        return arrays

    else:
        for t in arrays.types:
            if isinstance(t, (numba.types.ArrayCompatible, numba.types.List)) and isinstance(t.dtype, numba.types.Boolean):
                out = out + t.ndims*(numba.types.Array(numba.int64, 1, "C"),)
            elif isinstance(t, (numba.types.ArrayCompatible, numba.types.List)) and isinstance(t.dtype, numba.types.Integer):
                out = out + (numba.types.Array(numba.int64, 1, "C"),)
            elif isinstance(t, (numba.types.ArrayCompatible, numba.types.List)):
                raise TypeError("arrays must have boolean or integer type")
            else:
                out = out + (t,)
        return numba.types.Tuple(out)

def preprocess_slicetuple(context, builder, wheretpe, whereval):
    wheretpe2 = typing_regularize_slice(wheretpe)
    regularize_slice.compile(wheretpe2(wheretpe))
    cres = regularize_slice.overloads[(wheretpe,)]
    whereval2 = context.call_internal(builder, cres.fndesc, wheretpe2(wheretpe), (whereval,))

    wheretpe3 = typing_broadcast_arrays(wheretpe2)
    broadcast_arrays.compile(wheretpe3(wheretpe2))
    cres2 = broadcast_arrays.overloads[(wheretpe2,)]
    whereval3 = context.call_internal(builder, cres2.fndesc, wheretpe3(wheretpe2), (whereval2,))

    return wheretpe3, whereval3

def wrap_for_slicetuple(context, builder, arraytpe, arrayval):
    import awkward1._numba.array.listarray

    length = arraylen(context, builder, arraytpe, arrayval, totpe=numba.int64)
    nexttpe = awkward1._numba.array.listarray.ListArrayType(index64tpe, index64tpe, arraytpe, numba.types.none)
    proxynext = numba.cgutils.create_struct_proxy(nexttpe)(context, builder)
    proxynext.starts = newindex64(context, builder, numba.int64, context.get_constant(numba.int64, 1))
    proxynext.stops = newindex64(context, builder, numba.int64, context.get_constant(numba.int64, 1))
    numba.targets.arrayobj.store_item(context, builder, index64tpe, context.get_constant(numba.int64, 0), arrayptr(context, builder, index64tpe, proxynext.starts))
    numba.targets.arrayobj.store_item(context, builder, index64tpe, length, arrayptr(context, builder, index64tpe, proxynext.stops))
    proxynext.content = arrayval
    nextval = proxynext._getvalue()

    return nexttpe, nextval
