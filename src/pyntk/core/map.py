##
# This file is part of Netsukuku
# (c) Copyright 2007 Andrea Lo Pumo aka AlpT <alpt@freaknet.org>
#
# This source code is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This source code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# Please refer to the GNU Public License for more details.
#
# You should have received a copy of the GNU Public License along with
# this source code; if not, write to:
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
##
#
# Implementation of the map. See {-topodoc-}
# 

import sys
sys.path.append("..")
from lib.event import Event
from random import randint

class Map:

    def __init__(self, levels, gsize, dataclass, me=None):
	"""Initialise the map
	
	If me = None, then self.me is set to a random nip (ntk ip)
	"""
	
	self.levels = levels	# Number of levels
	self.gsize  = gsize	# How many nodes are contained in a gnode
	self.dataclass = dataclass
	self.me	    = me	# Ourself. self.me[lvl] is the ID of our
				# (g)node of level lvl
	# Choose a random nip
	if me == None: self.me = self.nip_rand()

	# The member self.node[l][i] is a node of level l and its ID is i
	self.node = [[None for i in xrange(gsize)] for i in xrange(levels)]
	# Number of nodes of each level
	self.node_nb = [ 0 for i in xrange(levels) ]

	self.events = Event( [ 'NEW_NODE', 'DEL_NODE' ] )

    def node_get(self, lvl, id):
	"""Returns from the map a node of level `lvl' and id `id'.

	A class instance of type `self.dataclass' will always be returned: if
	it doesn't exist, it is created"""
	
	if self.node[lvl][id] == None:
		self.node[lvl][id]=self.dataclass(lvl, id)
	return self.node[lvl][id]

    def node_add(self, lvl, id):
        if self.node[lvl][id] is None:
		node=self.node_get(lvl, id)
		self.node_nb[lvl]+=1
		self.events.send('NEW_NODE', (lvl, id))

    def node_del(self, lvl, id):
        if self.node[lvl][id] is not None:
		self.node_nb[lvl]-=1
	    	self.events.send('DEL_NODE', (lvl, id))
	self.node[lvl][id]=None

    def free_nodes_nb(self, lvl):
    	"""Returns the number of free nodes of level `lvl'"""
    	return self.maproute.gsize-self.maproute.node_nb[lvl]

    def free_nodes_list(self, lvl):
        """Returns the list of free nodes of level `lvl'"""\
        return [nid for n in self.node[lvl] 
			for nid in self.gsize
			    if self.node[lvl][nid] != None]

    def is_in_level(self, nip, lvl):
	"""Does the node nip belongs to our gnode of level `lvl'?"""
	return nip[:-lvl-1] == self.me[:-lvl-1]

    def ip_to_nip(self, ip):
        """Converts the given ip to a nip (Netsukuku IP)
	
	A nip is a list [a_0, a_1, ..., a_{n-1}], where n = self.levels
	and such that a_{n-1}*g^{n-1}+a_{n-2}*g^(n-2)+...+a_0 = ip, 
	where g = self.gsize"""

	g=self.gsize
	return [int(ip/g**l) - (int(ip/g**(l+1)) * g) for l in xrange(self.levels)]

    def nip_to_ip(self, nip):
        """The reverse of ip_to_nip"""

	g=self.gsize
        return sum([nip[l] * g**l for l in xrange(self.levels)])

    def nip_cmp(self, nipA, nipB):
        """Returns the first level where nipA and nipB differs. The search
	start from the end of the nip """

	for lvl in reversed(xrange(self.levels)):
		if nipA[lvl] != nipB[lvl]:
			return lvl

	return self.levels+1

    def nip_rand(self):
        return [randint(0, self.gsize-1) for i in xrange(self.levels)]
