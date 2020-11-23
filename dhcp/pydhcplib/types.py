# pydhcplib
# Copyright (C) 2008 Mathieu Ignacio -- mignacio@april.org
# Copyright (C) 2009 Stanislav Yudin -- decvar@gmail.com
#
# This file is part of pydhcplib.
# Pydhcplib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from binascii import unhexlify,hexlify


class bytelist(object):
	def __init__(self, value, lenght = 128):
		self._bytes = []
		self._value = value
		for ch in value:
			self._bytes.append(ord(ch))
		if len(self._bytes) < lenght:
			for i in xrange( 0, lenght - len(self._bytes)):
				self._bytes.append(0)
			
	# return ip string
	def str(self) :
		return self._value

	# return ip list (useful for DhcpPacket class)
	def list(self) :
		return self._bytes

# Check and convert hardware/nic/mac address type
class hwmac:
    def __init__(self,value="00:00:00:00:00:00") :
        self._hw_numlist = []
        self._hw_string = ""
        hw_type = type(value)
        if hw_type == str :
            value = value.strip()
            self._hw_string = value
            self._StringToNumlist(value)
            self._CheckNumList()
        elif hw_type == list :
            self._hw_numlist = value
            self._CheckNumList()
            self._NumlistToString()
        else : raise TypeError , 'hwmac init : Valid types are str and list'



    # Check if _hw_numlist is valid and raise error if not.
    def _CheckNumList(self) :
        if len(self._hw_numlist) != 6 : raise ValueError , "hwmac : wrong list length."
        for part in self._hw_numlist :
            if type (part) != int : raise TypeError , "hwmac : each element of list must be int"
            if part < 0 or part > 255 : raise ValueError , "hwmac : need numbers between 0 and 255."
        return True


    def _StringToNumlist(self,value):
        self._hw_string = self._hw_string.replace("-",":").replace(".",":")
        self._hw_string = self._hw_string.lower()

        for twochar in self._hw_string.split(":"):
            self._hw_numlist.append(ord(unhexlify(twochar)))
            
    # Convert NumList type ip to String type ip
    def _NumlistToString(self) :
        self._hw_string = ":".join(map(hexlify,map(chr,self._hw_numlist)))

    # Convert String type ip to NumList type ip
    # return ip string
    def str(self) :
        return self._hw_string

    # return ip list (useful for DhcpPacket class)
    def list(self) :
        return self._hw_numlist

    def __hash__(self) :
        return self._hw_string.__hash__()

    def __repr__(self) :
        return self._hw_string

    def __cmp__(self,other) :
        if self._hw_string == other : return 0
        return 1

    def __nonzero__(self) :
        if self._hw_string != "00:00:00:00:00:00" : return 1
        return 0

class ipv4:
    def __init__(self,value="0.0.0.0") :
        ip_type = type(value)
        if ip_type == str :
            if not self.CheckString(value) : raise ValueError, "ipv4 string argument is not an valid ip "
            self._ip_string = value
            self._StringToNumlist()
            self._StringToLong()
            self._NumlistToString()
        elif ip_type == list :
            if not self.CheckNumList(value) : raise ValueError, "ipv4 list argument is not an valid ip "
            self._ip_numlist = value
            self._NumlistToString()
            self._StringToLong()
        elif ip_type == int or ip_type == long:
            self._ip_long = value
            self._LongToNumlist()
            self._NumlistToString()
        elif ip_type == bool :
            self._ip_long = 0
            self._LongToNumlist()
            self._NumlistToString()
            
        else : raise TypeError , 'ipv4 init : Valid types are str, list, int or long'

    # Convert Long type ip to numlist ip
    def _LongToNumlist(self) :
        self._ip_numlist = [self._ip_long >> 24 & 0xFF]
        self._ip_numlist.append(self._ip_long >> 16 & 0xFF)
        self._ip_numlist.append(self._ip_long >> 8 & 0xFF)
        self._ip_numlist.append(self._ip_long & 0xFF)
        if not self.CheckNumList(self._ip_numlist) : raise ValueError, "ipv4 list argument is not an valid ip "
    # Convert String type ip to Long type ip
    def _StringToLong(self) :
        ip_numlist = map(int,self._ip_string.split('.'))
        self._ip_long = ip_numlist[3] + ip_numlist[2]*256 + ip_numlist[1]*256*256 + ip_numlist[0]*256*256*256
        if not self.CheckNumList(self._ip_numlist) : raise ValueError, "ipv4 list argument is not an valid ip "
    # Convert NumList type ip to String type ip
    def _NumlistToString(self) :
        self._ip_string = ".".join(map(str,self._ip_numlist))
        if not self.CheckNumList(self._ip_numlist) : raise ValueError, "ipv4 list argument is not an valid ip "
    # Convert String type ip to NumList type ip
    def _StringToNumlist(self) :
        self._ip_numlist = map(int,self._ip_string.split('.'))
        if not self.CheckNumList(self._ip_numlist) : raise ValueError, "ipv4 list argument is not an valid ip "

    """ Public methods """
    # Check if _ip_numlist is valid and raise error if not.
    # self._ip_numlist
    def CheckNumList(self,value) :
        if len(value) != 4 : return False
        for part in value :
            if part < 0 or part > 255 : return False
        return True

    # Check if _ip_numlist is valid and raise error if not.
    def CheckString(self,value) :
        tmp = value.strip().split('.')
        if len(tmp) != 4 :  return False
        for each in tmp : 
            if not each.isdigit() : return False
        return True
    
    # return ip string
    def str(self) :
        return self._ip_string

    # return ip list (useful for DhcpPacket class)
    def list(self) :
        return self._ip_numlist

    # return Long ip type (useful for SQL ip address backend)
    def int(self) :
        return self._ip_long


    """ Useful function for native python operations """

    def __hash__(self) :
        return self._ip_long.__hash__()

    def __repr__(self) :
        return self._ip_string

    def __cmp__(self,other) :
        return cmp(self._ip_long, other._ip_long);

    def __nonzero__(self) :
        if self._ip_long != 0 : return 1
        return 0

class strlist :
    def __init__(self,data="") :
        str_type = type(data)
        self._str = ""
        self._list = []
        
        if str_type == str :
            self._str = data
            for each in range(len(self._str)) :
                self._list.append(ord(self._str[each]))
        elif str_type == list :
            self._list = data
            self._str = "".join(map(chr,self._list))
        else : raise TypeError , 'strlist init : Valid types are str and  list of int'

    # return string
    def str(self) :
        return self._str

    # return list (useful for DhcpPacket class)
    def list(self) :
        return self._list

    # return int
    # FIXME
    def int(self) :
        return 0



    """ Useful function for native python operations """

    def __hash__(self) :
        return self._str.__hash__()

    def __repr__(self) :
        return self._str

    def __nonzero__(self) :
        if self._str != "" : return 1
        return 0

    def __cmp__(self,other) :
        if self._str == other : return 0
        return 1

