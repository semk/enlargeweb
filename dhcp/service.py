#!/usr/bin/env python
# EnlargeWeb source code
# Licenced under GPLv3
# Stanislav Yudin

from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
from pydhcplib.types import ipv4, strlist, hwmac
from enlargeweb.model import meta
from enlargeweb.model.srv import Server, Nic, BootEntry
#from enlargeweb.lib.helpers import longFromBytesArray, ipToStr

import logging

log = logging.getLogger(__name__)

class DhcpServiceImplementation(DhcpService):
	def __init__(self, svcConfig, rangeSection):
		self.config = svcConfig
		self.range = getattr(svcConfig, rangeSection)
		broadcastAddress = self.getBroadcastAddress(self.range.address)
		self.dumpPackets = int(self.config.dhcp.dumpPackets)
		
		DhcpService.__init__(self, broadcastAddress, 
			self.config.dhcp.listenPort, 
			self.config.dhcp.emitPort)
			
	def getBroadcastAddress(self, listenAddress):
		parts = listenAddress.split('.')
		return parts[0] + '.' + parts[1] + '.' + parts[2] + '.255'
		
	def HandleDhcpDiscover(self, packet):
		if self.dumpPackets:
			log.debug('<<\n' + packet.str())
		hwAddr = self.dhcpHwAddrToStr(packet.GetOption('chaddr'))
		log.info('received DISCOVER from %s ' % hwAddr)
		
		foundNics = meta.Session.query(Nic).filter(Nic.mac == str(hwAddr)).all()
		if len(foundNics) == 1:
			nic = foundNics[0]
			host = meta.Session.query(Server).filter(Server.id == nic.node_id).one()
			#known static client
			log.info('found an address %s for client' % nic.ip_address)
			offer = DhcpPacket()
			offer.CreateDhcpOfferPacketFrom(packet)
			#client related options address
			offer.AddLine('yiaddr:%s' % str(nic.ip_address))
			offer.AddLine('router:%s' % str(self.range.router))
			offer.AddLine('subnet_mask:%s' % str(self.range.mask))
			offer.AddLine('domain_name_server:%s' % str(self.range.dns))
			offer.AddLine('name_server:%s' % str(self.range.dns))
			offer.AddLine('host_name:%s' % str(host.name))
			offer.AddLine('domain_name:%s' % str(self.range.domainName))
			#server related options
			offer.AddLine('sname:EnlargeWeb')
			offer.AddLine('siaddr:%s' % str(self.range.address))
			offer.AddLine('server_identifier:%s' % str(self.range.address))
			offer.AddLine('ip_address_lease_time:%s' % str(self.range.leaseTime))
			offer.AddLine('tftp_server_name:%s' % str(self.range.tftp))
			#boot file specified?
			boot_query = meta.Session.query(BootEntry).filter(BootEntry.mac == nic.mac)
			if boot_query.count() > 0:
				boot_entry = boot_query.one()
				log.info("Sending boot file: %s" % str(boot_entry.file))
				offer.AddLine('file:%s' % str(boot_entry.file))
			else:
				log.info("No boot entry specified")
			
			if self.dumpPackets:
				log.debug('>>\n' + offer.str())
				
			self.SendDhcpPacketTo(offer, self.listen_address, self.emit_port)
		else:
			log.warn('Failed to find client %s' % hwAddr)
			
	def HandleDhcpRequest(self, packet):
		if self.dumpPackets:
			log.debug('<<\n' + packet.str())
		
		hwAddr = self.dhcpHwAddrToStr(packet.GetOption('chaddr'))
		log.info('received REQUEST from %s' % hwAddr)
		
		foundNics = meta.Session.query(Nic).filter(Nic.mac == hwAddr).all()
		if len(foundNics) == 1:
			nic = foundNics[0]
			host = meta.Session.query(Server).filter(Server.id == nic.node_id).with_lockmode('update').one()
			#read and compare requested address
			req_addr = packet.GetOption('request_ip_address')
			if not req_addr:
				#looks like client want to update existing lease
				req_addr = packet.GetOption('ciaddr')
				log.info('Trying to update lease for %s/%s' % ( hwAddr, req_addr ))
			if not req_addr:
				#it is REQUEST but nothing requested. Igroring
				return			
			requestedAddress = ipv4(req_addr)
			log.info('Client %s requsting address %s' % ( hwAddr, requestedAddress ) )
			if requestedAddress != ipv4(str(nic.ip_address)):
				log.error('Sending NACK since address in DB is %s' % nic.ip_address)
				packet.TransformToDhcpNackPacket()
				answer = packet
			else:
				log.info('Confirming address with ACK')
				ack = DhcpPacket()
				ack.CreateDhcpAckPacketFrom(packet)
				#client related options address
				ack.AddLine('yiaddr:%s' % str(nic.ip_address))
	  			ack.AddLine('router:%s' % str(self.range.router))
				ack.AddLine('subnet_mask:%s' % str(self.range.mask))
				ack.AddLine('domain_name_server:%s' % str(self.range.dns))
				ack.AddLine('name_server:%s' % str(self.range.dns))
				ack.AddLine('host_name:%s' % str(host.name))
				ack.AddLine('domain_name:%s' % str(self.range.domainName))
				#server related options
				ack.AddLine('sname:EnlargeWeb')
				ack.AddLine('siaddr:%s' % str(self.range.address))
				ack.AddLine('server_identifier:%s' % str(self.range.address))
				ack.AddLine('ip_address_lease_time:%s' % str(self.range.leaseTime))
				ack.AddLine('tftp_server_name:%s' % str(self.range.tftp))
				#boot file specified?
				boot_query = meta.Session.query(BootEntry).filter(BootEntry.mac == nic.mac)
				if boot_query.count() > 0:
					boot_entry = boot_query.one()
					log.info("Sending boot file: %s" % str(boot_entry.file))
					ack.AddLine('file:%s' % str(boot_entry.file))
				else:
					log.info("No boot entry specified")
				answer = ack
			
			if self.dumpPackets:
				log.debug('>>\n' + answer.str())
				
			self.SendDhcpPacketTo(answer, self.listen_address, self.emit_port)
			#set host online
			host.online = True
			meta.Session.commit()
			log.info("Host %s is now ONLINE" % str(host))
		else:
			log.warn('Failed to find client %s' % hwAddr)

	def HandleDhcpDecline(self, packet):
		if self.config.dhcp.dumpPackets:
			log.debug(packet.str())

	def HandleDhcpRelease(self, packet):
		if self.config.dhcp.dumpPackets:
			log.debug(packet.str())

	def HandleDhcpInform(self, packet):
		if self.config.dhcp.dumpPackets:
			log.debug(packet.str())

	def dhcpHwAddrToStr(self, data):
		result = []
		hexsym = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
		for iterator in range(6) :
			result += [str(hexsym[data[iterator]/16]+hexsym[data[iterator]%16])]

		result = ':'.join(result)
		return result
