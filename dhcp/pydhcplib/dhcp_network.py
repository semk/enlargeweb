# pydhcplib
# Copyright (C) 2008 Mathieu Ignacio -- mignacio@april.org
#
# This file is part of pydhcplib.
# Pydhcplib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import socket
import select
import dhcp_packet
import IN
import logging

log = logging.getLogger(__name__)

class DhcpNetwork:
	def __init__(self, listen_address="0.0.0.0", listen_port=67, emit_port=68):
		log.info('starting dhcp service on %s:%s' % (listen_address, listen_port))
		self.listen_port = int(listen_port)
		self.emit_port = int(emit_port)
		self.listen_address = listen_address
		self.dhcp_socket = None

	def GetNextDhcpPacket(self,timeout=60):
		data =""


		while data == "" :
			
			data_input,data_output,data_except = select.select([self.dhcp_socket],[],[],timeout)

			if data_input != [] :
				(data, source_address) = self.dhcp_socket.recvfrom(2048)
			else:
				return None
			if data != "" :
				packet = dhcp_packet.DhcpPacket()
				packet.source_address = source_address
				packet.DecodePacket(data)

				self.HandleDhcpAll(packet)
				
				if packet.IsDhcpDiscoverPacket():
					self.HandleDhcpDiscover(packet)
				elif packet.IsDhcpRequestPacket():
					self.HandleDhcpRequest(packet)
				elif packet.IsDhcpDeclinePacket():
					self.HandleDhcpDecline(packet)
				elif packet.IsDhcpReleasePacket():
					self.HandleDhcpRelease(packet)
				elif packet.IsDhcpInformPacket():
					self.HandleDhcpInform(packet)
				elif packet.IsDhcpOfferPacket():
					self.HandleDhcpOffer(packet)
				elif packet.IsDhcpAckPacket():
					self.HandleDhcpAck(packet)
				elif packet.IsDhcpNackPacket():
					self.HandleDhcpNack(packet)
				else: self.HandleDhcpUnknown(packet)

				return packet

	def SendDhcpPacketTo(self, packet, _ip,_port):
		return self.dhcp_socket.sendto(packet.EncodePacket(),(_ip,_port))

	# Server side Handle methods
	def HandleDhcpDiscover(self, packet):
		pass

	def HandleDhcpRequest(self, packet):
		pass

	def HandleDhcpDecline(self, packet):
		pass

	def HandleDhcpRelease(self, packet):
		pass

	def HandleDhcpInform(self, packet):
		pass


	# client-side Handle methods
	def HandleDhcpOffer(self, packet):
		pass
		
	def HandleDhcpAck(self, packet):
		pass

	def HandleDhcpNack(self, packet):
		pass

	# Handle unknown options or all options
	def HandleDhcpUnknown(self, packet):
		pass

	def HandleDhcpAll(self, packet):
		pass



class DhcpService(DhcpNetwork) :
	def __init__(self, listen_address="0.0.0.0", listen_port=67, emit_port=68) :
		DhcpNetwork.__init__(self,listen_address, listen_port, emit_port)

		try :
			log.debug('creating socket: socket.AF_INET, socket.SOCK_DGRAM')
			self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		except socket.error, msg :
			log.error('socket creation error : ' + str(msg))

		try:
			log.debug('setting : socket.SOL_SOCKET,socket.SO_BROADCAST, 1')
			self.dhcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
		except socket.error, msg :
			log.error('socket error in setsockopt SO_BROADCAST : ' + str(msg))

		try :
			log.info('binding to port %s' % self.listen_port)
			self.dhcp_socket.bind(('', self.listen_port))
		except socket.error, msg :
			log.error('bind error : ' + str(msg))


