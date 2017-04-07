import fcntl
import os
import sys
import select
import socket

import ctypes
import struct

from if_tun import IfReq, TUNSETIFF, IFF_TUN, IFF_TAP, IFF_NO_PI

DEF_BUF=[0xff,0xff,0xff,0xff,0xff,0xff,
		 0x2a,0x5e,0xc0,0xab,0xdc,0xae,
		 0x08,0x00,
		 0x01,0x02,0x03,0x04,0x05,0x06,
		 0x01,0x02,0x03,0x04,0x05,0x06,
		 0x01,0x02,0x03,0x04,0x05,0x06,
		 0x01,0x02,0x03,0x04,0x05,0x06,
		 0x01,0x02,0x03,0x04,0x05,0x06,
		 0xff,0xff]
BUF=bytes(DEF_BUF)

ETHER_BROAD_ADDR=[0xff,0xff,0xff,0xff,0xff,0xff]
MIN_EHTER_PKG_LEN=46

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

def get_mac(devname):
	ctlfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	if ctlfd.fileno() < 0:
		print("socket create err:%d",ctlfd)
		sys.exit(-1)
	r=IfReq()
	ctypes.memset(ctypes.byref(r), 0, ctypes.sizeof(r))
	r.ifr_ifrn.ifrn_name = devname.encode('utf-8')
	try:
		from socket_def import SIOCGIFHWADDR
		err = fcntl.ioctl(ctlfd, SIOCGIFHWADDR, r)
	except Exception as e:
		print("Get mac err:",e)
		os.close(ctlfd)
		return -1
	mac=[]
	maclen = len(r.ifr_ifru.ifru_hwaddr.sa_data)
	for i in range(0,maclen):
		mac.append(r.ifr_ifru.ifru_hwaddr.sa_data[i])
	os.close(ctlfd.fileno())
	return mac

def create_ether_packet(srcMac, dstMac, data):
	buf=[]
	buf.extend(dstMac)
	buf.extend(srcMac)
	buf.extend(data)
	total = len(buf)
	if total < MIN_EHTER_PKG_LEN:
		for i in range(total,MIN_EHTER_PKG_LEN):
			buf.append(0xff)
	return buf

def fmt_hex(buf):
	for i in range(0,len(buf)):
		#sys.stdout.write(hex(buf[i]));
		#sys.stdout.write(" ");
		print("%02x"%buf[i],end=' ')
		if (i+1)%16 == 0:
			print("")
			#sys.stdout.write('\n')
	#sys.stdout.write('\n')
	print("")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("usage: <tap_name>")
		sys.exit(-1)
	print(sys.argv[1])	
	devFd = tun_create(sys.argv[1], IFF_TAP | IFF_NO_PI)
	if devFd < 0:
		raise OSError

	try:
		epfd = select.epoll()
		epfd.register(devFd, select.EPOLLIN | select.EPOLLHUP)
		epfd.register(sys.stdin.fileno(), select.EPOLLIN | select.EPOLLHUP)
	except Exception as e:
		print("epoll init err",e)
		sys.exit(-1)

	MAXSIZE=4096
	while True:
		epoll_lst = epfd.poll()
		for fd,events in epoll_lst:
			if fd == devFd:
				buf = os.read(fd,MAXSIZE)
				print("read from dev size:%d" % len(buf))
				fmt_hex(buf)
			if fd == sys.stdin.fileno():
				buf = os.read(fd,MAXSIZE)
				print("read from stdin:%d" % len(buf))
				pkg=create_ether_packet(get_mac(sys.argv[1]), ETHER_BROAD_ADDR, buf)
				#print(pkg)
				#print("write 2 tap:%s [%s]"%(sys.argv[1],buf))
				print("send a pkg:")
				fmt_hex(pkg)
				os.write(devFd, bytes(pkg))



