import fcntl
import os

import ctypes
import struct

from if_tun import IfReq, TUNSETIFF, IFF_TUN, IFF_TAP

def tun_create(devname, flags):
	fd = -1
	if not devname:
		return -1
	fd = os.open("/dev/net/tun", os.O_RDWR)
	if fd < 0:
		print("open /dev/net/tun err!")
		return fd
	r=IfReq()
	ctypes.memset(ctypes.byref(r), 0, ctypes.sizeof(r))
	r.ifr_ifru.ifru_flags |= flags
	r.ifr_ifrn.ifrn_name = devname.encode('utf-8')
	try:
		err = fcntl.ioctl(fd, TUNSETIFF, r)
	except Exception as e:
		print("err:",e)
		os.close(fd)
		return -1
	return fd

if __name__ == "__main__":
	fd = tun_create("tap1", IFF_TAP)
	if fd < 0:
		raise OSError

	MAXSIZE=4096
	while(True):
		buf = os.read(fd,MAXSIZE)
		if not buf:
			break
		print("read size:%d" % len(buf))



