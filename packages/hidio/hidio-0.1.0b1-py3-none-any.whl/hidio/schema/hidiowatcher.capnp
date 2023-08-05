# Copyright (C) 2017 by Jacob Alexander
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.

@0xc1d8b25769f376ce;

## Imports ##

using Common = import "common.capnp";



## Interfaces ##

struct HIDIOPacket {
	id @0 :UInt16;
	data @1: List(UInt8);
}

interface HIDIOWatcher extends(Common.HIDIONode) {
    struct Signal {
        union {
            devicePacket @0 :HIDIOPacket;
            hostPacket @1 :HIDIOPacket;
        }
        # TODO
    }

    interface Commands {
    }
}

