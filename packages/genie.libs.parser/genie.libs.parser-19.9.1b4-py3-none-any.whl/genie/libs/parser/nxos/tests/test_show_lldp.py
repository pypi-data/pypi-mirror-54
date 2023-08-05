# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device
from ats.topology import loader

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError, \
    SchemaMissingKeyError

# iosxe show_lisp
from genie.libs.parser.nxos.show_lldp import ShowLldpAll, ShowLldpTimers, \
    ShowLldpTlvSelect, ShowLldpNeighborsDetail, ShowLldpTraffic


# =================================
# Unit test for 'show lldp all'
# =================================
class test_show_lldp_all(unittest.TestCase):
    '''unit test for "show lldp all'''
    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'interfaces': {
            'Ethernet1/64':
                {'enabled': True,
                 'tx': True,
                 'rx': True,
                 'dcbx': True
                 },
            'mgmt0':
                {'enabled': True,
                 'tx': True,
                 'rx': True,
                 'dcbx': False
                 }
        }
    }

    golden_output = {'execute.return_value': '''
    Interface Information: Eth1/64 Enable (tx/rx/dcbx): Y/Y/Y
    Interface Information: mgmt0 Enable (tx/rx/dcbx): Y/Y/N
    '''
                     }

    def test_empty(self):
        self.maxDiff = None
        self.device = Mock(**self.empty_output)
        obj = ShowLldpAll(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowLldpAll(device=self.device)
        parsed_output = obj.parse()

        self.assertEqual(parsed_output, self.golden_parsed_output)


# =================================
# Unit test for 'show lldp timers'
# =================================
class test_show_lldp_timers(unittest.TestCase):
    '''unit test for show lldp timers'''
    empty_output = {'execute.return_value': ''}
    golden_parsed_output = {
        'hold_timer': 120,
        'reinit_timer': 2,
        'hello_timer': 30
    }
    golden_output = {'execute.return_value':
                         '''
                         LLDP Timers:

                             Holdtime in seconds: 120
                             Reinit-time in seconds: 2
                             Transmit interval in seconds: 30
                         '''
                     }

    def test_empty(self):
        self.maxDiff = None
        self.device = Mock(**self.empty_output)
        obj = ShowLldpTimers(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowLldpTimers(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


# =================================
# Unit test for 'show lldp tlv-select'
# =================================
class test_show_lldp_tlv_select(unittest.TestCase):
    '''unit test for show lldp tlv-select'''
    empty_output = {'execute.return_value': ''}
    golden_parsed_output = {
        'suppress_tlv_advertisement': {
            'port_description': False,
            'system_name': False,
            'system_description': False,
            'system_capabilities': False,
            'management_address_v4': False,
            'management_address_v6': False,
            'power_management': False,
            'port_vlan': False,
            'dcbxp': False
        }
    }
    golden_output = {'execute.return_value': '''
           management-address-v4
           management-address-v6
           port-description
           port-vlan
           power-management
           system-capabilities
           system-description
           system-name
           dcbxp
        '''}


    def test_empty(self):
        self.maxDiff = None
        self.device = Mock(**self.empty_output)
        obj = ShowLldpTlvSelect(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowLldpTlvSelect(device=self.device)
        parsed_output = obj.parse()

        self.assertEqual(parsed_output, self.golden_parsed_output)


# =================================
# Unit test for 'show lldp neighbors detail'
# =================================
class test_show_lldp_neighbors_detail(unittest.TestCase):
    '''unit test for show lldp neighbors detail'''
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'total_entries': 2,
        'interfaces': {
            'Ethernet1/1': {
                'port_id': {
                    'GigabitEthernet3': {
                        'neighbors': {
                            'R1_csr1000v.openstacklocal': {
                                'chassis_id': '001e.49f7.2c00',
                                'port_description': 'GigabitEthernet3',
                                'system_name': 'R1_csr1000v.openstacklocal',
                                'system_description': 'Cisco IOS Software [Everest], '
                                                      'Virtual XE Software ('
                                                      'X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 22-Jul-17 05:51 by',
                                'time_remaining': 114,
                                'capabilities': {
                                    'bridge': {
                                        'name': 'bridge',
                                        'system': True,
                                    },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True
                                    }
                                },
                                'management_address_v4': '10.1.3.1',
                                'management_address_v6': 'not advertised',
                                'vlan_id': 'not advertised'
                            }
                        }
                    }
                }
            },
            'Ethernet1/2': {
                'port_id': {
                    'GigabitEthernet0/0/0/1': {
                        'neighbors': {
                            'R2_xrv9000': {
                                'chassis_id': '000d.bd09.46fa',
                                'system_name': 'R2_xrv9000',
                                'system_description': '6.2.2, IOS-XRv 9000',
                                'time_remaining': 95,
                                'capabilities': {
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True
                                    }
                                },
                                'management_address_v4': '10.2.3.2',
                                'management_address_v6': 'not advertised',
                                'vlan_id': 'not advertised'
                            }
                        }
                    }
                }
            }
        }
    }
    golden_output = {'execute.return_value': '''
            Capability codes:
              (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
              (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other
            Device ID            Local Intf      Hold-time  Capability  Port ID  

            Chassis id: 001e.49f7.2c00
            Port id: Gi3
            Local Port id: Eth1/1
            Port Description: GigabitEthernet3
            System Name: R1_csr1000v.openstacklocal
            System Description: Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)
            Technical Support: http://www.cisco.com/techsupport
            Copyright (c) 1986-2017 by Cisco Systems, Inc.
            Compiled Sat 22-Jul-17 05:51 by 
            Time remaining: 114 seconds
            System Capabilities: B, R
            Enabled Capabilities: R
            Management Address: 10.1.3.1
            Management Address IPV6: not advertised
            Vlan ID: not advertised


            Chassis id: 000d.bd09.46fa
            Port id: Gi0/0/0/1
            Local Port id: Eth1/2
            Port Description: null
            System Name: R2_xrv9000
            System Description: 6.2.2, IOS-XRv 9000
            Time remaining: 95 seconds
            System Capabilities: R
            Enabled Capabilities: R
            Management Address: 10.2.3.2
            Management Address IPV6: not advertised
            Vlan ID: not advertised

            Total entries displayed: 2
        '''}

    def test_empty(self):
        self.maxDiff = None
        self.device = Mock(**self.empty_output)
        obj = ShowLldpNeighborsDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowLldpNeighborsDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertDictEqual(parsed_output, self.golden_parsed_output)


# =================================
# Unit test for 'show lldp traffic'
# =================================
class test_show_lldp_traffic(unittest.TestCase):
    '''unit test for show lldp traffic'''
    empty_output = {'execute.return_value': ''}
    golden_parsed_output = {
        'counters': {
            "total_frames_received": 209,
            "total_frames_transmitted": 349,
            "total_frames_received_in_error": 0,
            "total_frames_discarded": 0,
            'total_unrecognized_tlvs': 0,
            'total_entries_aged': 0
    }
    }
    golden_output = {'execute.return_value': '''
                    LLDP traffic statistics:

                        Total frames transmitted: 349
                        Total entries aged: 0
                        Total frames received: 209
                        Total frames received in error: 0
                        Total frames discarded: 0
                        Total unrecognized TLVs: 0
                        '''
                     }

    def test_empty(self):
        self.maxDiff = None
        self.device = Mock(**self.empty_output)
        obj = ShowLldpTraffic(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowLldpTraffic(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


if __name__ == '__main__':
    unittest.main()
