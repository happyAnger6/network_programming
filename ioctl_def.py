_IOC_NRBITS=8
_IOC_TYPEBITS=8
_IOC_SIZEBITS=14
_IOC_DIRBITS=2

_IOC_NRMASK=((1 << _IOC_NRBITS) - 1)
_IOC_TYPEMASK=((1 << _IOC_TYPEBITS) - 1)
_IOC_SIZEMASK=((1 << _IOC_SIZEBITS) - 1)
_IOC_DIRMASK=((1 << _IOC_DIRBITS) - 1)

_IOC_NRSHIFT=0
_IOC_TYPESHIFT=(_IOC_NRSHIFT + _IOC_NRBITS)
_IOC_SIZESHIFT=(_IOC_TYPESHIFT + _IOC_TYPEBITS)
_IOC_DIRSHIFT=(_IOC_SIZESHIFT + _IOC_SIZEBITS)

_IOC_NONE=0
_IOC_WRITE=1
_IOC_READ=2

def _IOC(dir, type, nr, size):
	return (((dir) << _IOC_DIRSHIFT) | \
			((type) << _IOC_TYPESHIFT) | \
			((nr) << _IOC_NRSHIFT) | \
			((size) << _IOC_SIZESHIFT))

import ctypes
def _IOC_TYPECHECK(t):
	return ctypes.sizeof(t)

def _IO(type, nr):
	return _IOC(_IOC_NONE, type, nr, 0)

def _IOR(type, nr, size):
	return _IOC(_IOC_READ, type, nr, _IOC_TYPECHECK(size))

def _IOW(type, nr, size):
	return _IOC(_IOC_WRITE, type, nr, _IOC_TYPECHECK(size))

if __name__ == "__main__":
	print(_IOC_TYPESHIFT,_IOC_SIZESHIFT,_IOC_DIRSHIFT)
	print(_IOC())
