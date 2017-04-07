import ctypes
import ioctl_def

TUNSETIFF=ioctl_def._IOW(ord('T'), 202, ctypes.c_int)
IFF_TUN=1
IFF_TAP=2

IFF_NO_PI=0x1000

IFNAMSIZ=16

class SockAddr(ctypes.Structure):
	_fields_=[("sa_family",ctypes.c_ushort),
		("sa_data",ctypes.c_char*14)]

class IfMap(ctypes.Structure):
	_fields_=[("mem_start", ctypes.c_ulong),
			  ("mem_end", ctypes.c_ulong),
			  ("base_addr", ctypes.c_ushort),
			  ("irq", ctypes.c_char),
			  ("dma", ctypes.c_char),
			  ("port", ctypes.c_char)]

class Ifs_Ifsu(ctypes.Union):
	_fields_=[("raw_hdlc", ctypes.c_void_p),
			  ("cisco", ctypes.c_void_p),
			  ("fr", ctypes.c_void_p),
			  ("fr_pvc", ctypes.c_void_p),
			  ("fr_pvc_info", ctypes.c_void_p),
			  ("sync", ctypes.c_void_p),
			  ("te1", ctypes.c_void_p)]

class IfSettings(ctypes.Structure):
	_fields_=[("type", ctypes.c_uint),
			  ("size", ctypes.c_uint),
			  ("ifs_ifsu", Ifs_Ifsu)]

class Ifr_Ifru(ctypes.Union):
	_fields_=[("ifru_addr", SockAddr),
			  ("ifru_dstaddr", SockAddr),
			  ("ifru_broadaddr", SockAddr),
			  ("ifru_netmask", SockAddr),
			  ("ifru_hwaddr", SockAddr),
			  ("ifru_flags", ctypes.c_ushort),
			  ("ifru_ivalue", ctypes.c_int),
			  ("ifru_mtu", ctypes.c_int),
			  ("ifru_map", IfMap),
			  ("ifru_slave", ctypes.c_char * IFNAMSIZ),
			  ("ifru_newname", ctypes.c_char * IFNAMSIZ),
			  ("ifru_data", ctypes.c_void_p),
			  ("ifru_settings", IfSettings)]

class Ifr_Ifrn(ctypes.Union):
	_fields_=[("ifrn_name", ctypes.c_char * IFNAMSIZ)]

class IfReq(ctypes.Structure):
	_fields_=[("ifr_ifrn", Ifr_Ifrn),
		("ifr_ifru", Ifr_Ifru)]


if __name__ == "__main__":
	ifreq = IfReq()
	print(ctypes.sizeof(ifreq.ifr_ifrn))
	print(ctypes.sizeof(ifreq.ifr_ifru))
