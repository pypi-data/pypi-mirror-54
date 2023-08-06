# Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from networking_generic_switch.devices import netmiko_devices


class DellNos(netmiko_devices.NetmikoSwitch):
        ADD_NETWORK = (
            'interface vlan {segmentation_id}',
            'name {network_id}',
            'exit',
        )

        DELETE_NETWORK = (
            'no interface vlan {segmentation_id}',
            'exit',
        )

        PLUG_PORT_TO_NETWORK = (
            'interface vlan {segmentation_id}',
            'untagged {port}',
            'exit',
        )

        DELETE_PORT = (
            'interface vlan {segmentation_id}',
            'no untagged {port}',
            'exit',
        )

        ADD_NETWORK_TO_TRUNK = (
            'interface vlan {segmentation_id}',
            'tagged {port}',
            'exit',
        )

        REMOVE_NETWORK_FROM_TRUNK = (
            'interface vlan {segmentation_id}',
            'no tagged {port}',
            'exit',
        )
