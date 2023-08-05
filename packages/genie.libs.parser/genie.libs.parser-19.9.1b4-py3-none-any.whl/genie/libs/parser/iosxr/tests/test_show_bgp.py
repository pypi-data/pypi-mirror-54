
# Python
import unittest
from unittest.mock import Mock
import xml.etree.ElementTree as ET

# ATS
from ats.topology import Device
from ats.topology import loader

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError

# iosxr show_bgp
from genie.libs.parser.iosxr.show_bgp import ShowPlacementProgramAll,\
                                  ShowBgpInstanceAfGroupConfiguration,\
                                  ShowBgpInstanceSessionGroupConfiguration,\
                                  ShowBgpInstanceProcessDetail,\
                                  ShowBgpInstanceNeighborsDetail,\
                                  ShowBgpInstanceNeighborsAdvertisedRoutes,\
                                  ShowBgpInstanceNeighborsReceivedRoutes,\
                                  ShowBgpInstanceNeighborsRoutes,\
                                  ShowBgpInstanceSummary,\
                                  ShowBgpInstanceAllAll, ShowBgpInstances,\
                                  ShowBgpL2vpnEvpn, ShowBgpL2vpnEvpnNeighbors, \
                                  ShowBgpVrfDbVrfAll, \
                                  ShowBgpL2vpnEvpnAdvertised, \
                                  ShowBgpSessions, \
                                  ShowBgpInstanceAllSessions


# ==================================
# Unit test for 'show bgp instances'
# ==================================

class test_show_bgp_instances(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        "instance": {
            "test1": {
                 "num_vrfs": 0,
                 "instance_id": 1,
                 "placed_grp": "bgp2_1",
                 "bgp_id": 333
            },
            "default": {
                 "num_vrfs": 2,
                 "instance_id": 3,
                 "address_families": [
                      "ipv4 unicast",
                      "vpnv4 unicast",
                      "ipv6 unicast",
                      "vpnv6 unicast"
                 ],
                 "placed_grp": "bgp4_1",
                 "bgp_id": 100
            },
            "test": {
                 "num_vrfs": 0,
                 "instance_id": 0,
                 "placed_grp": "v4_routing",
                 "bgp_id": 333
            },
            "test2": {
                 "num_vrfs": 0,
                 "instance_id": 2,
                 "placed_grp": "bgp3_1",
                 "bgp_id": 333
            }
        }
    }
    
    golden_output = {'execute.return_value': '''
        ID  Placed-Grp  Name              AS        VRFs    Address Families
        --------------------------------------------------------------------------------
        0   v4_routing  test              333       0       none
        1   bgp2_1      test1             333       0       none
        2   bgp3_1      test2             333       0       none
        3   bgp4_1      default           100       2       IPv4 Unicast, VPNv4 Unicast,
                                                            IPv6 Unicast, VPNv6 Unicast
      '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstances(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstances(device=self.device)
        parsed_output = obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output)


# ==========================================
# Unit test for 'show placement program all'
# ==========================================

class test_show_placement_program_all(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'program': 
            {'rcp_fs':
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'central-services',
                        'jid': '1168',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'ospf': 
                {'instance':
                    {'1':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'v4-routing',
                        'jid': '1018',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'bgp': 
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'v4-routing',
                        'jid': '1018',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'statsd_manager_g': 
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'netmgmt',
                        'jid': '1141',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'pim': 
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'mcast-routing',
                        'jid': '1158',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'ipv6_local': 
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'v6-routing',
                        'jid': '1156',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}}
            }
        }
    
    golden_output = {'execute.return_value': '''
            
            Display program related information. This is the program information corresponding to this LR as
            perceived by the placement daemon.
            ------------------------------------------------------------------------------------------------------------------------------------------
                               Process Information
            ------------------------------------------------------------------------------------------------------------------------------------------
            Program                                 Group               jid  Active         Active-state             Standby        Standby-state  
            ------------------------------------------------------------------------------------------------------------------------------------------
            rcp_fs                                  central-services    1168 0/0/CPU0       RUNNING                  NONE           NOT_SPAWNED    
            ospf(1)                                 v4-routing          1018 0/0/CPU0       RUNNING                  NONE           NOT_SPAWNED    
            bgp(default)                            v4-routing          1018 0/0/CPU0       RUNNING                  NONE           NOT_SPAWNED
            statsd_manager_g                        netmgmt             1141 0/0/CPU0       RUNNING                  NONE           NOT_SPAWNED    
            pim                                     mcast-routing       1158 0/0/CPU0       RUNNING                  NONE           NOT_SPAWNED    
            ipv6_local                              v6-routing          1156 0/0/CPU0       RUNNING                  NONE           NOT_SPAWNED    
      '''}


    golden_parsed_output1 = {
        'program': 
            {'auto_ip_ring': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                       'active_state': 'RUNNING',
                                                       'group': 'central-services',
                                                       'jid': '1156',
                                                       'standby': '0/RSP0/CPU0',
                                                       'standby_state': 'RUNNING'}}},
             'bfd': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                              'active_state': 'RUNNING',
                                              'group': 'central-services',
                                              'jid': '1158',
                                              'standby': '0/RSP0/CPU0',
                                              'standby_state': 'RUNNING'}}},
             'bgp': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                              'active_state': 'RUNNING',
                                              'group': 'v4-routing',
                                              'jid': '1051',
                                              'standby': '0/RSP0/CPU0',
                                              'standby_state': 'RUNNING'},
                                  'test': {'active': '0/RSP1/CPU0',
                                           'active_state': 'RUNNING',
                                           'group': 'Group_10_bgp2',
                                           'jid': '1052',
                                           'standby': '0/RSP0/CPU0',
                                           'standby_state': 'RUNNING'},
                                  'test1': {'active': '0/RSP1/CPU0',
                                            'active_state': 'RUNNING',
                                            'group': 'Group_5_bgp3',
                                            'jid': '1053',
                                            'standby': '0/RSP0/CPU0',
                                            'standby_state': 'RUNNING'},
                                  'test2': {'active': '0/RSP1/CPU0',
                                            'active_state': 'RUNNING',
                                            'group': 'Group_5_bgp4',
                                            'jid': '1054',
                                            'standby': '0/RSP0/CPU0',
                                            'standby_state': 'RUNNING'}}},
             'bgp_epe': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                  'active_state': 'RUNNING',
                                                  'group': 'v4-routing',
                                                  'jid': '1159',
                                                  'standby': '0/RSP0/CPU0',
                                                  'standby_state': 'RUNNING'}}},
             'bpm': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                              'active_state': 'RUNNING',
                                              'group': 'v4-routing',
                                              'jid': '1066',
                                              'standby': '0/RSP0/CPU0',
                                              'standby_state': 'RUNNING'}}},
             'bundlemgr_distrib': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                            'active_state': 'RUNNING',
                                                            'group': 'central-services',
                                                            'jid': '1157',
                                                            'standby': '0/RSP0/CPU0',
                                                            'standby_state': 'RUNNING'}}},
             'domain_services': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                          'active_state': 'RUNNING',
                                                          'group': 'central-services',
                                                          'jid': '1160',
                                                          'standby': '0/RSP0/CPU0',
                                                          'standby_state': 'RUNNING'}}},
             'es_acl_mgr': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                     'active_state': 'RUNNING',
                                                     'group': 'central-services',
                                                     'jid': '1169',
                                                     'standby': '0/RSP0/CPU0',
                                                     'standby_state': 'RUNNING'}}},
             'eth_gl_cfg': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                     'active_state': 'RUNNING',
                                                     'group': 'central-services',
                                                     'jid': '1151',
                                                     'standby': '0/RSP0/CPU0',
                                                     'standby_state': 'RUNNING'}}},
             'ethernet_stats_controller_edm': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                                        'active_state': 'RUNNING',
                                                                        'group': 'central-services',
                                                                        'jid': '1161',
                                                                        'standby': '0/RSP0/CPU0',
                                                                        'standby_state': 'RUNNING'}}},
             'ftp_fs': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                 'active_state': 'RUNNING',
                                                 'group': 'central-services',
                                                 'jid': '1162',
                                                 'standby': '0/RSP0/CPU0',
                                                 'standby_state': 'RUNNING'}}},
             'icpe_satmgr': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                      'active_state': 'RUNNING',
                                                      'group': 'central-services',
                                                      'jid': '1163',
                                                      'standby': '0/RSP0/CPU0',
                                                      'standby_state': 'RUNNING'}}},
             'igmp': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                               'active_state': 'RUNNING',
                                               'group': 'mcast-routing',
                                               'jid': '1208',
                                               'standby': '0/RSP0/CPU0',
                                               'standby_state': 'RUNNING'}}},
             'intf_mgbl': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                    'active_state': 'RUNNING',
                                                    'group': 'central-services',
                                                    'jid': '1143',
                                                    'standby': '0/RSP0/CPU0',
                                                    'standby_state': 'RUNNING'}}},
             'ipv4_connected': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                         'active_state': 'RUNNING',
                                                         'group': 'v4-routing',
                                                         'jid': '1152',
                                                         'standby': '0/RSP0/CPU0',
                                                         'standby_state': 'RUNNING'}}},
             'ipv4_local': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                     'active_state': 'RUNNING',
                                                     'group': 'v4-routing',
                                                     'jid': '1153',
                                                     'standby': '0/RSP0/CPU0',
                                                     'standby_state': 'RUNNING'}}},
             'ipv4_mfwd_ma': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                       'active_state': 'RUNNING',
                                                       'group': 'mcast-routing',
                                                       'jid': '1204',
                                                       'standby': '0/RSP0/CPU0',
                                                       'standby_state': 'RUNNING'}}},
             'ipv4_mpa': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                   'active_state': 'RUNNING',
                                                   'group': 'central-services',
                                                   'jid': '1149',
                                                   'standby': '0/RSP0/CPU0',
                                                   'standby_state': 'RUNNING'}}},
             'ipv4_rib': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                   'active_state': 'RUNNING',
                                                   'group': 'v4-routing',
                                                   'jid': '1146',
                                                   'standby': '0/RSP0/CPU0',
                                                   'standby_state': 'RUNNING'}}},
             'ipv4_rump': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                    'active_state': 'RUNNING',
                                                    'group': 'v4-routing',
                                                    'jid': '1167',
                                                    'standby': '0/RSP0/CPU0',
                                                    'standby_state': 'RUNNING'}}},
             'ipv4_static': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                      'active_state': 'RUNNING',
                                                      'group': 'v4-routing',
                                                      'jid': '1043',
                                                      'standby': '0/RSP0/CPU0',
                                                      'standby_state': 'RUNNING'}}},
             'ipv6_connected': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                         'active_state': 'RUNNING',
                                                         'group': 'v6-routing',
                                                         'jid': '1154',
                                                         'standby': '0/RSP0/CPU0',
                                                         'standby_state': 'RUNNING'}}},
             'ipv6_local': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                     'active_state': 'RUNNING',
                                                     'group': 'v6-routing',
                                                     'jid': '1155',
                                                     'standby': '0/RSP0/CPU0',
                                                     'standby_state': 'RUNNING'}}},
             'ipv6_mfwd_ma': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                       'active_state': 'RUNNING',
                                                       'group': 'mcast-routing',
                                                       'jid': '1205',
                                                       'standby': '0/RSP0/CPU0',
                                                       'standby_state': 'RUNNING'}}},
             'ipv6_mpa': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                   'active_state': 'RUNNING',
                                                   'group': 'central-services',
                                                   'jid': '1150',
                                                   'standby': '0/RSP0/CPU0',
                                                   'standby_state': 'RUNNING'}}},
             'ipv6_rib': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                   'active_state': 'RUNNING',
                                                   'group': 'v6-routing',
                                                   'jid': '1147',
                                                   'standby': '0/RSP0/CPU0',
                                                   'standby_state': 'RUNNING'}}},
             'ipv6_rump': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                    'active_state': 'RUNNING',
                                                    'group': 'v6-routing',
                                                    'jid': '1168',
                                                    'standby': '0/RSP0/CPU0',
                                                    'standby_state': 'RUNNING'}}},
             'l2tp_mgr': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                   'active_state': 'RUNNING',
                                                   'group': 'v4-routing',
                                                   'jid': '1176',
                                                   'standby': '0/RSP0/CPU0',
                                                   'standby_state': 'RUNNING'}}},
             'l2vpn_mgr': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                    'active_state': 'RUNNING',
                                                    'group': 'v4-routing',
                                                    'jid': '1175',
                                                    'standby': '0/RSP0/CPU0',
                                                    'standby_state': 'RUNNING'}}},
             'mld': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                              'active_state': 'RUNNING',
                                              'group': 'mcast-routing',
                                              'jid': '1209',
                                              'standby': '0/RSP0/CPU0',
                                              'standby_state': 'RUNNING'}}},
             'mpls_ldp': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                   'active_state': 'RUNNING',
                                                   'group': 'v4-routing',
                                                   'jid': '1199',
                                                   'standby': '0/RSP0/CPU0',
                                                   'standby_state': 'RUNNING'}}},
             'mpls_static': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                      'active_state': 'RUNNING',
                                                      'group': 'v4-routing',
                                                      'jid': '1142',
                                                      'standby': '0/RSP0/CPU0',
                                                      'standby_state': 'RUNNING'}}},
             'mrib': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                               'active_state': 'RUNNING',
                                               'group': 'mcast-routing',
                                               'jid': '1206',
                                               'standby': '0/RSP0/CPU0',
                                               'standby_state': 'RUNNING'}}},
             'mrib6': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                'active_state': 'RUNNING',
                                                'group': 'mcast-routing',
                                                'jid': '1207',
                                                'standby': '0/RSP0/CPU0',
                                                'standby_state': 'RUNNING'}}},
             'netconf': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                  'active_state': 'RUNNING',
                                                  'group': 'central-services',
                                                  'jid': '1189',
                                                  'standby': '0/RSP0/CPU0',
                                                  'standby_state': 'RUNNING'}}},
             'nfmgr': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                'active_state': 'RUNNING',
                                                'group': 'central-services',
                                                'jid': '1145',
                                                'standby': '0/RSP0/CPU0',
                                                'standby_state': 'RUNNING'}}},
             'ospf': {'instance': {'1': {'active': '0/RSP1/CPU0',
                                         'active_state': 'RUNNING',
                                         'group': 'v4-routing',
                                         'jid': '1018',
                                         'standby': '0/RSP0/CPU0',
                                         'standby_state': 'RUNNING'}}},
             'ospf_uv': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                  'active_state': 'RUNNING',
                                                  'group': 'v4-routing',
                                                  'jid': '1114',
                                                  'standby': '0/RSP0/CPU0',
                                                  'standby_state': 'RUNNING'}}},
             'pbr_ma': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                 'active_state': 'RUNNING',
                                                 'group': 'central-services',
                                                 'jid': '1171',
                                                 'standby': '0/RSP0/CPU0',
                                                 'standby_state': 'RUNNING'}}},
             'pim': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                              'active_state': 'RUNNING',
                                              'group': 'mcast-routing',
                                              'jid': '1210',
                                              'standby': '0/RSP0/CPU0',
                                              'standby_state': 'RUNNING'}}},
             'pim6': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                               'active_state': 'RUNNING',
                                               'group': 'mcast-routing',
                                               'jid': '1211',
                                               'standby': '0/RSP0/CPU0',
                                               'standby_state': 'RUNNING'}}},
             'policy_repository': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                            'active_state': 'RUNNING',
                                                            'group': 'v4-routing',
                                                            'jid': '1148',
                                                            'standby': '0/RSP0/CPU0',
                                                            'standby_state': 'RUNNING'}}},
             'python_process_manager': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                                 'active_state': 'RUNNING',
                                                                 'group': 'central-services',
                                                                 'jid': '1164',
                                                                 'standby': '0/RSP0/CPU0',
                                                                 'standby_state': 'RUNNING'}}},
             'qos_ma': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                 'active_state': 'RUNNING',
                                                 'group': 'central-services',
                                                 'jid': '1172',
                                                 'standby': '0/RSP0/CPU0',
                                                 'standby_state': 'RUNNING'}}},
             'rcp_fs': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                 'active_state': 'RUNNING',
                                                 'group': 'central-services',
                                                 'jid': '1165',
                                                 'standby': '0/RSP0/CPU0',
                                                 'standby_state': 'RUNNING'}}},
             'rt_check_mgr': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                       'active_state': 'RUNNING',
                                                       'group': 'v4-routing',
                                                       'jid': '1170',
                                                       'standby': '0/RSP0/CPU0',
                                                       'standby_state': 'RUNNING'}}},
             'schema_server': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                        'active_state': 'RUNNING',
                                                        'group': 'central-services',
                                                        'jid': '1177',
                                                        'standby': '0/RSP0/CPU0',
                                                        'standby_state': 'RUNNING'}}},
             'snmppingd': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                    'active_state': 'RUNNING',
                                                    'group': 'central-services',
                                                    'jid': '1195',
                                                    'standby': '0/RSP0/CPU0',
                                                    'standby_state': 'RUNNING'}}},
             'spa_cfg_hlpr': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                       'active_state': 'RUNNING',
                                                       'group': 'central-services',
                                                       'jid': '1130',
                                                       'standby': '0/RSP0/CPU0',
                                                       'standby_state': 'RUNNING'}}},
             'ssh_conf_verifier': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                            'active_state': 'RUNNING',
                                                            'group': 'central-services',
                                                            'jid': '1183',
                                                            'standby': '0/RSP0/CPU0',
                                                            'standby_state': 'RUNNING'}}},
             'ssh_server': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                     'active_state': 'RUNNING',
                                                     'group': 'central-services',
                                                     'jid': '1184',
                                                     'standby': '0/RSP0/CPU0',
                                                     'standby_state': 'RUNNING'}}},
             'statsd_manager_g': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                           'active_state': 'RUNNING',
                                                           'group': 'netmgmt',
                                                           'jid': '1144',
                                                           'standby': '0/RSP0/CPU0',
                                                           'standby_state': 'RUNNING'}}},
             'telemetry_encoder': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                            'active_state': 'RUNNING',
                                                            'group': 'central-services',
                                                            'jid': '1194',
                                                            'standby': '0/RSP0/CPU0',
                                                            'standby_state': 'RUNNING'}}},
             'tty_verifyd': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                      'active_state': 'RUNNING',
                                                      'group': 'central-services',
                                                      'jid': '1166',
                                                      'standby': '0/RSP0/CPU0',
                                                      'standby_state': 'RUNNING'}}},
             'vservice_mgr': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                       'active_state': 'RUNNING',
                                                       'group': 'central-services',
                                                       'jid': '1173',
                                                       'standby': '0/RSP0/CPU0',
                                                       'standby_state': 'RUNNING'}}},
             'wanphy_proc': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                      'active_state': 'RUNNING',
                                                      'group': 'central-services',
                                                      'jid': '1178',
                                                      'standby': '0/RSP0/CPU0',
                                                      'standby_state': 'RUNNING'}}},
             'xtc_agent': {'instance': {'default': {'active': '0/RSP1/CPU0',
                                                    'active_state': 'RUNNING',
                                                    'group': 'central-services',
                                                    'jid': '1174',
                                                    'standby': '0/RSP0/CPU0',
                                                    'standby_state': 'RUNNING'}}}}}

    golden_output1 = {'execute.return_value': '''

        Mon Jul 17 18:58:33.074 PDT
        Display program related information. This is the program information corresponding to this LR as
        perceived by the placement daemon.
        ------------------------------------------------------------------------------------------------------------------------------------------
                           Process Information
        ------------------------------------------------------------------------------------------------------------------------------------------
        Program                                 Group               jid  Active         Active-state             Standby        Standby-state  
        ------------------------------------------------------------------------------------------------------------------------------------------
        schema_server                           central-services    1177 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        vservice_mgr                            central-services    1173 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv4_mpa                                central-services    1149 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        qos_ma                                  central-services    1172 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        icpe_satmgr                             central-services    1163 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        eth_gl_cfg                              central-services    1151 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        rcp_fs                                  central-services    1165 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ssh_server                              central-services    1184 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        es_acl_mgr                              central-services    1169 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        snmppingd                               central-services    1195 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        xtc_agent                               central-services    1174 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ftp_fs                                  central-services    1162 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv6_mpa                                central-services    1150 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        telemetry_encoder                       central-services    1194 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        bfd                                     central-services    1158 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ethernet_stats_controller_edm           central-services    1161 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        tty_verifyd                             central-services    1166 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        spa_cfg_hlpr                            central-services    1130 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        auto_ip_ring                            central-services    1156 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        nfmgr                                   central-services    1145 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        bundlemgr_distrib                       central-services    1157 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        netconf                                 central-services    1189 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        intf_mgbl                               central-services    1143 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        domain_services                         central-services    1160 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        python_process_manager                  central-services    1164 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        wanphy_proc                             central-services    1178 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ssh_conf_verifier                       central-services    1183 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        pbr_ma                                  central-services    1171 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        rt_check_mgr                            v4-routing          1170 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv4_rib                                v4-routing          1146 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        l2vpn_mgr                               v4-routing          1175 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv4_connected                          v4-routing          1152 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ospf(1)                                 v4-routing          1018 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        l2tp_mgr                                v4-routing          1176 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        bgp_epe                                 v4-routing          1159 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ospf_uv                                 v4-routing          1114 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        bpm                                     v4-routing          1066 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv4_rump                               v4-routing          1167 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv4_static                             v4-routing          1043 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        mpls_ldp                                v4-routing          1199 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        bgp(default)                            v4-routing          1051 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        policy_repository                       v4-routing          1148 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        mpls_static                             v4-routing          1142 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv4_local                              v4-routing          1153 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        statsd_manager_g                        netmgmt             1144 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        igmp                                    mcast-routing       1208 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        mrib                                    mcast-routing       1206 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv4_mfwd_ma                            mcast-routing       1204 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        pim6                                    mcast-routing       1211 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv6_mfwd_ma                            mcast-routing       1205 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        mld                                     mcast-routing       1209 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        pim                                     mcast-routing       1210 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        mrib6                                   mcast-routing       1207 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv6_rib                                v6-routing          1147 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv6_connected                          v6-routing          1154 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv6_local                              v6-routing          1155 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ipv6_rump                               v6-routing          1168 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        bgp(test)                               Group_10_bgp2       1052 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        bgp(test1)                              Group_5_bgp3        1053 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        bgp(test2)                              Group_5_bgp4        1054 0/RSP1/CPU0    RUNNING                  0/RSP0/CPU0    RUNNING        
        ------------------------------------------------------------------------------------------------------------------------------------------
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        placement_program_all_obj = ShowPlacementProgramAll(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = placement_program_all_obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        placement_program_all_obj = ShowPlacementProgramAll(device=self.device)
        parsed_output = placement_program_all_obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        placement_program_all_obj = ShowPlacementProgramAll(device=self.device)
        parsed_output = placement_program_all_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)


# ======================================================================
# Unit test for 'show bgp instance <WORD> af-group <WORD> configuration'
# ======================================================================

class test_show_bgp_instance_af_group_configuration(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    golden_parsed_output = {
        "instance": {
            "default": {
                "pp_name": {
                    "af_group": {
                        "address_family": "ipv4 unicast",
                        "default_originate": True,
                        "default_originate_route_map": "allpass",
                        "maximum_prefix_max_prefix_no": 429,
                        "maximum_prefix_threshold": 75,
                        "maximum_prefix_restart": 35,
                        "next_hop_self": True,
                        "route_map_name_in": "allpass",
                        "route_map_name_out": "allpass",
                        "route_reflector_client": True,
                        "send_community": "both",
                        "send_comm_ebgp": True,
                        "send_ext_comm_ebgp": True,
                        "soo": "100:1",
                        "soft_reconfiguration": "inbound always",
                        "allowas_in_as_number": 10,
                        "allowas_in": True,
                        "as_override": True
                    }
                }
            }
        }

    }

    golden_output = {'execute.return_value': '''

    Fri Jul 14 16:30:21.081 EDT
    Building configuration...    
    router bgp 100 af-group af_group address-family ipv4 unicast 

        Wed Jul 12 15:42:07.027 EDT
    af-group af_group address-family IPv4 Unicast
      default-originate policy allpass            []
      maximum-prefix 429 75 35                    []
      next-hop-self                               []
      policy allpass in                           []
      policy allpass out                          []
      route-reflector-client                      []
      send-community-ebgp                         []
      send-extended-community-ebgp                []
      site-of-origin 100:1                        []
      soft-reconfiguration inbound always         []
      allowas-in 10                               []
      as-override                                 []

        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceAfGroupConfiguration(device=self.device1)
        self.maxDiff = None
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstanceAfGroupConfiguration(device=self.device)
        parsed_output = obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output)


# ===========================================================================
# Unit test for 'show bgp instance <WORD> session-group <WORD> configuration'
# ===========================================================================

class test_show_bgp_instance_session_group_configuration(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
        "instance": {
            "default": {
                "peer_session": {
                    "SG": {
                        "remote_as": 333,
                        "fall_over_bfd": True,
                        "password_text": "094F471A1A0A464058",
                        "holdtime": 30,
                        "transport_connection_mode": "active-only",
                        "ebgp_multihop_max_hop": 254,
                        "local_replace_as": True,
                        "ps_minimum_holdtime": 3,
                        "keepalive_interval": 10,
                        "shutdown": True,
                        "local_dual_as": True,
                        "local_no_prepend": True,
                        "ebgp_multihop_enable": True,
                        "suppress_four_byte_as_capability": True,
                        "local_as_as_no": 200,
                        "description": "SG_group",
                        "update_source": 'loopback0',
                        "disable_connected_check": True}}}}}

    golden_output = {'execute.return_value': '''
        Fri Jul 14 17:50:40.461 EDT
        Building configuration...
        router bgp 100 session-group SG 

        Thu Jul 13 12:28:48.673 EDT
        session-group SG
         remote-as 333                              []
         description SG_group                       []
         ebgp-multihop 254                          []
         local-as 200 no-prepend replace-as dual-as []
         password encrypted 094F471A1A0A464058      []
         shutdown                                   []
         timers 10 30 3                             []
         update-source Loopback0                    []
         suppress-4byteas                           []
         session-open-mode active-only              []
         bfd fast-detect                            []
         ignore-connected                           []
        '''}

    golden_parsed_output1 = {
        'instance': 
            {'default': 
                {'peer_session': 
                    {'SG': 
                        {'description': 'LALALALLA',
                        'ebgp_multihop_enable': True,
                        'ebgp_multihop_max_hop': 255,
                        'fall_over_bfd': True,
                        'local_as_as_no': 10,
                        'local_no_prepend': True}}},
            'test': 
                {'peer_session': 
                    {'LALALALLA': 
                        {'description': 'LALALALLA',
                        'ebgp_multihop_enable': True,
                        'ebgp_multihop_max_hop': 255,
                        'fall_over_bfd': True,
                        'local_as_as_no': 10,
                        'local_no_prepend': True},
                    'abcd': 
                        {'description': 'LALALALLA',
                        'ebgp_multihop_enable': True,
                        'ebgp_multihop_max_hop': 255,
                        'fall_over_bfd': True,
                        'local_as_as_no': 10,
                        'local_no_prepend': True},
                    'efddd': 
                        {'description': 'LALALALLA',
                        'ebgp_multihop_enable': True,
                        'ebgp_multihop_max_hop': 255,
                        'fall_over_bfd': True,
                        'local_as_as_no': 10,
                        'local_no_prepend': True}}}}}

    golden_output1 = {'execute.return_value': '''
        router bgp 333 instance test session-group abcd
        router bgp 333 instance test session-group abcd bfd fast-detect
        router bgp 333 instance test session-group abcd description LALALALLA
        router bgp 333 instance test session-group efddd
        router bgp 333 instance test session-group efddd bfd fast-detect
        router bgp 333 instance test session-group efddd ebgp-multihop 255
        router bgp 333 instance test session-group efddd local-as 10 no-prepend
        router bgp 333 instance test neighbor 10.4.1.1 use session-group LALALALLA
        router bgp 100 session-group SG
        router bgp 100 session-group SG description SG

        RP/0/RSP1/CPU0:PE1#show bgp instance default session-group SG configuration
        Thu Jul 20 09:02:18.537 PDT
        session-group SG
         description SG  []

        RP/0/RSP1/CPU0:PE1#show bgp instance test session-group abcd configuration 
        Thu Jul 20 09:02:48.738 PDT
        session-group abcd
         description LALALALLA []
         bfd fast-detect       []

        RP/0/RSP1/CPU0:PE1#show bgp instance test session-group efddd configuration 
        Thu Jul 20 09:03:10.702 PDT
        session-group efddd
         ebgp-multihop 255      []
         local-as 10 no-prepend []
         bfd fast-detect        []
        
        RP/0/RSP1/CPU0:PE1#show bgp instance test session-group LALALALLA configuration 
        Thu Jul 20 09:03:41.151 PDT
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceSessionGroupConfiguration(device=self.device1)
        self.maxDiff = None
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstanceSessionGroupConfiguration(device=self.device)
        parsed_output = obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowBgpInstanceSessionGroupConfiguration(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)


# ============================================================
# Unit test for 'show bgp instance all vrf all process detail'
# ============================================================

class test_show_bgp_instance_all_vrf_all_process_detail(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output1 = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'VRF1': 
                        {'active_cluster_id': '10',
                        'always_compare_med': False,
                        'as_number': 100,
                        'as_system_number_format': 'ASPLAIN',
                        'att': {'as_paths': {'memory_used': 0,
                                            'number': 0},
                               'attributes': {'memory_used': 152,
                                              'number': 1},
                               'communities': {'memory_used': 0,
                                               'number': 0},
                               'extended_communities': {'memory_used': 0,
                                                        'number': 0},
                               'nexthop_entries': {'memory_used': 7600,
                                                   'number': 19},
                               'pe_distinguisher_labels': {'memory_used': 0,
                                                           'number': 0},
                               'pmsi_tunnel_attr': {'memory_used': 0,
                                                    'number': 0},
                               'ppmp_attr': {'memory_used': 0,
                                             'number': 0},
                               'ribrnh_tunnel_attr': {'memory_used': 0,
                                                      'number': 0},
                               'route_reflector_entries': {'memory_used': 0,
                                                           'number': 0},
                               'tunnel_encap_attr': {'memory_used': 0,
                                                     'number': 0}},
                        'bestpath_compare_routerid': False,
                        'bestpath_cost_community_ignore': False,
                        'bestpath_med_missing_at_worst': False,
                        'bgp_speaker_process': 0,
                        'bmp_pool_summary': {'100': {'alloc': 0,
                                                    'free': 0},
                                            '10000': {'alloc': 0,
                                                      'free': 0},
                                            '1200': {'alloc': 0,
                                                     'free': 0},
                                            '200': {'alloc': 0,
                                                    'free': 0},
                                            '20000': {'alloc': 0,
                                                      'free': 0},
                                            '2200': {'alloc': 0,
                                                     'free': 0},
                                            '300': {'alloc': 0,
                                                    'free': 0},
                                            '3300': {'alloc': 0,
                                                     'free': 0},
                                            '400': {'alloc': 0,
                                                    'free': 0},
                                            '4000': {'alloc': 0,
                                                     'free': 0},
                                            '4500': {'alloc': 0,
                                                     'free': 0},
                                            '500': {'alloc': 0,
                                                    'free': 0},
                                            '5500': {'alloc': 0,
                                                     'free': 0},
                                            '600': {'alloc': 0,
                                                    'free': 0},
                                            '6500': {'alloc': 0,
                                                     'free': 0},
                                            '700': {'alloc': 0,
                                                    'free': 0},
                                            '7500': {'alloc': 0,
                                                     'free': 0},
                                            '800': {'alloc': 0,
                                                    'free': 0},
                                            '8500': {'alloc': 0,
                                                     'free': 0},
                                            '900': {'alloc': 0,
                                                    'free': 0}},
                        'current_limit_for_bmp_buffer_size': 307,
                        'current_utilization_of_bmp_buffer_limit': 0,
                        'default_cluster_id': '10',
                        'default_keepalive': 60,
                        'default_local_preference': 100,
                        'default_value_for_bmp_buffer_size': 307,
                        'enforce_first_as': True,
                        'fast_external_fallover': True,
                        'generic_scan_interval': 60,
                        'max_limit_for_bmp_buffer_size': 409,
                        'message_logging_pool_summary': {'100': {'alloc': 0,
                                                                'free': 0},
                                                        '200': {'alloc': 0,
                                                                'free': 0},
                                                        '2200': {'alloc': 0,
                                                                 'free': 0},
                                                        '4500': {'alloc': 0,
                                                                 'free': 0},
                                                        '500': {'alloc': 0,
                                                                'free': 0}},
                        'log_neighbor_changes': True,
                        'node': 'node0_0_CPU0',
                        'non_stop_routing': True,
                        'operation_mode': 'standalone',
                        'platform_rlimit_max': 2147483648,
                        'pool': {'1200': {'alloc': 0,
                                         'free': 0},
                                '200': {'alloc': 0,
                                        'free': 0},
                                '20000': {'alloc': 0,
                                          'free': 0},
                                '2200': {'alloc': 0,
                                         'free': 0},
                                '300': {'alloc': 1,
                                        'free': 0},
                                '3300': {'alloc': 0,
                                         'free': 0},
                                '400': {'alloc': 0,
                                        'free': 0},
                                '4000': {'alloc': 0,
                                         'free': 0},
                                '4500': {'alloc': 0,
                                         'free': 0},
                                '500': {'alloc': 0,
                                        'free': 0},
                                '5000': {'alloc': 0,
                                         'free': 0},
                                '600': {'alloc': 0,
                                        'free': 0},
                                '700': {'alloc': 0,
                                        'free': 0},
                                '800': {'alloc': 0,
                                        'free': 0},
                                '900': {'alloc': 0,
                                        'free': 0}},
                        'received_notifications': 0,
                        'received_updates': 0,
                        'restart_count': 1,
                        'route_distinguisher': '100:2',
                        'router_id': '10.64.4.4',
                        'sent_notifications': 0,
                        'sent_updates': 0,
                        'update_delay': 120,
                        'vrf_info': {'default': {'cfg': 1,
                                                'nbrs_estab': 0,
                                                'total': 1},
                                    'non-default': {'cfg': 2,
                                                    'nbrs_estab': 0,
                                                    'total': 3}}},
                    'a': 
                        {'active_cluster_id': '10',
                        'address_family': {'ipv4 unicast': {'attribute_download': 'Disabled',
                                                             'bgp_table_version': '1',
                                                             'chunk_elememt_size': '3',
                                                             'client_to_client_reflection': False,
                                                             'current_vrf': 'a',
                                                             'dampening': False,
                                                             'dynamic_med': True,
                                                             'dynamic_med_int': '10 '
                                                                                'minutes',
                                                             'dynamic_med_periodic_timer': 'Not '
                                                                                           'Running',
                                                             'dynamic_med_timer': 'Not '
                                                                                  'Running',
                                                             'label_retention_timer_value': '5 '
                                                                                            'mins',
                                                             'main_table_version': '1',
                                                             'nexthop_resolution_minimum_prefix_length': '0 '
                                                                                                         '(not '
                                                                                                         'configured)',
                                                             'num_of_scan_segments': '0',
                                                             'permanent_network': 'unconfigured',
                                                             'prefix_scanned_per_segment': '100000',
                                                             'prefixes_path': {'prefixes': {'mem_used': 0,
                                                                                            'number': 0}},
                                                             'remote_local': {'prefixes': {'allocated': 0,
                                                                                           'freed': 0}},
                                                             'rib_has_not_converged': 'version '
                                                                                      '0',
                                                             'rib_table_prefix_limit_reached': 'no',
                                                             'rib_table_prefix_limit_ver': '0',
                                                             'scan_interval': '60',
                                                             'soft_reconfig_entries': '0',
                                                             'state': 'read '
                                                                      'only '
                                                                      'mode',
                                                             'table_bit_field_size': '1 ',
                                                             'table_state': 'inactive',
                                                             'table_version_acked_by_rib': '0',
                                                             'table_version_synced_to_rib': '1',
                                                             'total_prefixes_scanned': '0'}},
                        'always_compare_med': False,
                        'as_number': 100,
                        'as_system_number_format': 'ASPLAIN',
                        'att': {'as_paths': {'memory_used': 0,
                                             'number': 0},
                                'attributes': {'memory_used': 152,
                                               'number': 1},
                                'bmp_paths': {'memory_used': 0,
                                              'number': 0},
                                'bmp_prefixes': {'memory_used': 0,
                                                 'number': 0},
                                'communities': {'memory_used': 0,
                                                'number': 0},
                                'extended_communities': {'memory_used': 0,
                                                         'number': 0},
                                'nexthop_entries': {'memory_used': 7600,
                                                    'number': 19},
                                'paths': {'memory_used': 0,
                                          'number': 0},
                                'pe_distinguisher_labels': {'memory_used': 0,
                                                            'number': 0},
                                'pmsi_tunnel_attr': {'memory_used': 0,
                                                     'number': 0},
                                'ppmp_attr': {'memory_used': 0,
                                              'number': 0},
                                'ribrnh_tunnel_attr': {'memory_used': 0,
                                                       'number': 0},
                                'route_reflector_entries': {'memory_used': 0,
                                                            'number': 0},
                                'tunnel_encap_attr': {'memory_used': 0,
                                                      'number': 0}},
                        'bestpath_compare_routerid': False,
                        'bestpath_cost_community_ignore': False,
                        'bestpath_med_missing_at_worst': False,
                        'bgp_speaker_process': 0,
                        'bmp_pool_summary': {'100': {'alloc': 0,
                                                     'free': 0},
                                             '10000': {'alloc': 0,
                                                       'free': 0},
                                             '1200': {'alloc': 0,
                                                      'free': 0},
                                             '200': {'alloc': 0,
                                                     'free': 0},
                                             '20000': {'alloc': 0,
                                                       'free': 0},
                                             '2200': {'alloc': 0,
                                                      'free': 0},
                                             '300': {'alloc': 0,
                                                     'free': 0},
                                             '3300': {'alloc': 0,
                                                      'free': 0},
                                             '400': {'alloc': 0,
                                                     'free': 0},
                                             '4000': {'alloc': 0,
                                                      'free': 0},
                                             '4500': {'alloc': 0,
                                                      'free': 0},
                                             '500': {'alloc': 0,
                                                     'free': 0},
                                             '5500': {'alloc': 0,
                                                      'free': 0},
                                             '600': {'alloc': 0,
                                                     'free': 0},
                                             '6500': {'alloc': 0,
                                                      'free': 0},
                                             '700': {'alloc': 0,
                                                     'free': 0},
                                             '7500': {'alloc': 0,
                                                      'free': 0},
                                             '800': {'alloc': 0,
                                                     'free': 0},
                                             '8500': {'alloc': 0,
                                                      'free': 0},
                                             '900': {'alloc': 0,
                                                     'free': 0}},
                        'current_limit_for_bmp_buffer_size': 307,
                        'current_utilization_of_bmp_buffer_limit': 0,
                        'default_cluster_id': '10',
                        'default_keepalive': 60,
                        'default_local_preference': 100,
                        'default_value_for_bmp_buffer_size': 307,
                        'enforce_first_as': True,
                        'fast_external_fallover': True,
                        'generic_scan_interval': 60,
                        'max_limit_for_bmp_buffer_size': 409,
                        'message_logging_pool_summary': {'100': {'alloc': 0,
                                                                 'free': 0},
                                                         '200': {'alloc': 0,
                                                                 'free': 0},
                                                         '2200': {'alloc': 0,
                                                                  'free': 0},
                                                         '4500': {'alloc': 0,
                                                                  'free': 0},
                                                         '500': {'alloc': 0,
                                                                 'free': 0}},
                        'log_neighbor_changes': True,
                        'node': 'node0_0_CPU0',
                        'non_stop_routing': True,
                        'operation_mode': 'standalone',
                        'platform_rlimit_max': 2147483648,
                        'pool': {'1200': {'alloc': 0,
                                          'free': 0},
                                 '200': {'alloc': 0,
                                         'free': 0},
                                 '20000': {'alloc': 0,
                                           'free': 0},
                                 '2200': {'alloc': 0,
                                          'free': 0},
                                 '300': {'alloc': 1,
                                         'free': 0},
                                 '3300': {'alloc': 0,
                                          'free': 0},
                                 '400': {'alloc': 0,
                                         'free': 0},
                                 '4000': {'alloc': 0,
                                          'free': 0},
                                 '4500': {'alloc': 0,
                                          'free': 0},
                                 '500': {'alloc': 0,
                                         'free': 0},
                                 '5000': {'alloc': 0,
                                          'free': 0},
                                 '600': {'alloc': 0,
                                         'free': 0},
                                 '700': {'alloc': 0,
                                         'free': 0},
                                 '800': {'alloc': 0,
                                         'free': 0},
                                 '900': {'alloc': 0,
                                         'free': 0}},
                        'received_notifications': 0,
                        'received_updates': 0,
                        'restart_count': 1,
                        'route_distinguisher': '100:1',
                        'router_id': '10.64.4.4',
                        'sent_notifications': 0,
                        'sent_updates': 0,
                        'update_delay': 120,
                        'vrf_info': {'default': {'cfg': 1,
                                                 'nbrs_estab': 0,
                                                 'total': 1},
                                     'non-default': {'cfg': 2,
                                                     'nbrs_estab': 0,
                                                     'total': 3}}},
                    'vrf1': 
                        {'active_cluster_id': '10',
                        'always_compare_med': False,
                        'as_number': 100,
                        'as_system_number_format': 'ASPLAIN',
                        'att': {'as_paths': {'memory_used': 0,
                                            'number': 0},
                               'attributes': {'memory_used': 152,
                                              'number': 1},
                               'communities': {'memory_used': 0,
                                               'number': 0},
                               'extended_communities': {'memory_used': 0,
                                                        'number': 0},
                               'nexthop_entries': {'memory_used': 7600,
                                                   'number': 19},
                               'pe_distinguisher_labels': {'memory_used': 0,
                                                           'number': 0},
                               'pmsi_tunnel_attr': {'memory_used': 0,
                                                    'number': 0},
                               'ppmp_attr': {'memory_used': 0,
                                             'number': 0},
                               'ribrnh_tunnel_attr': {'memory_used': 0,
                                                      'number': 0},
                               'route_reflector_entries': {'memory_used': 0,
                                                           'number': 0},
                               'tunnel_encap_attr': {'memory_used': 0,
                                                     'number': 0}},
                        'bestpath_compare_routerid': False,
                        'bestpath_cost_community_ignore': False,
                        'bestpath_med_missing_at_worst': False,
                        'bgp_speaker_process': 0,
                        'bmp_pool_summary': {'100': {'alloc': 0,
                                                    'free': 0},
                                            '10000': {'alloc': 0,
                                                      'free': 0},
                                            '1200': {'alloc': 0,
                                                     'free': 0},
                                            '200': {'alloc': 0,
                                                    'free': 0},
                                            '20000': {'alloc': 0,
                                                      'free': 0},
                                            '2200': {'alloc': 0,
                                                     'free': 0},
                                            '300': {'alloc': 0,
                                                    'free': 0},
                                            '3300': {'alloc': 0,
                                                     'free': 0},
                                            '400': {'alloc': 0,
                                                    'free': 0},
                                            '4000': {'alloc': 0,
                                                     'free': 0},
                                            '4500': {'alloc': 0,
                                                     'free': 0},
                                            '500': {'alloc': 0,
                                                    'free': 0},
                                            '5500': {'alloc': 0,
                                                     'free': 0},
                                            '600': {'alloc': 0,
                                                    'free': 0},
                                            '6500': {'alloc': 0,
                                                     'free': 0},
                                            '700': {'alloc': 0,
                                                    'free': 0},
                                            '7500': {'alloc': 0,
                                                     'free': 0},
                                            '800': {'alloc': 0,
                                                    'free': 0},
                                            '8500': {'alloc': 0,
                                                     'free': 0},
                                            '900': {'alloc': 0,
                                                    'free': 0}},
                        'current_limit_for_bmp_buffer_size': 307,
                        'current_utilization_of_bmp_buffer_limit': 0,
                        'default_cluster_id': '10',
                        'default_keepalive': 60,
                        'default_local_preference': 100,
                        'default_value_for_bmp_buffer_size': 307,
                        'enforce_first_as': True,
                        'fast_external_fallover': True,
                        'generic_scan_interval': 60,
                        'max_limit_for_bmp_buffer_size': 409,
                        'message_logging_pool_summary': {'100': {'alloc': 0,
                                                                'free': 0},
                                                        '200': {'alloc': 0,
                                                                'free': 0},
                                                        '2200': {'alloc': 0,
                                                                 'free': 0},
                                                        '4500': {'alloc': 0,
                                                                 'free': 0},
                                                        '500': {'alloc': 0,
                                                                'free': 0}},
                        'log_neighbor_changes': True,
                        'node': 'node0_0_CPU0',
                        'non_stop_routing': True,
                        'operation_mode': 'standalone',
                        'platform_rlimit_max': 2147483648,
                        'pool': {'1200': {'alloc': 0,
                                         'free': 0},
                                '200': {'alloc': 0,
                                        'free': 0},
                                '20000': {'alloc': 0,
                                          'free': 0},
                                '2200': {'alloc': 0,
                                         'free': 0},
                                '300': {'alloc': 1,
                                        'free': 0},
                                '3300': {'alloc': 0,
                                         'free': 0},
                                '400': {'alloc': 0,
                                        'free': 0},
                                '4000': {'alloc': 0,
                                         'free': 0},
                                '4500': {'alloc': 0,
                                         'free': 0},
                                '500': {'alloc': 0,
                                        'free': 0},
                                '5000': {'alloc': 0,
                                         'free': 0},
                                '600': {'alloc': 0,
                                        'free': 0},
                                '700': {'alloc': 0,
                                        'free': 0},
                                '800': {'alloc': 0,
                                        'free': 0},
                                '900': {'alloc': 0,
                                        'free': 0}},
                        'received_notifications': 0,
                        'received_updates': 0,
                        'restart_count': 1,
                        'route_distinguisher': '100:3',
                        'router_id': '10.64.4.4',
                        'sent_notifications': 0,
                        'sent_updates': 0,
                        'update_delay': 120,
                        'vrf_info': {'default': {'cfg': 1,
                                                'nbrs_estab': 0,
                                                'total': 1},
                                    'non-default': {'cfg': 2,
                                                    'nbrs_estab': 0,
                                                    'total': 3}}}}},
            'test': {}}}

    golden_output1 = {'execute.return_value': '''

        Wed Jul 12 16:37:22.420 EDT

        BGP instance 0: 'default'
        =========================

        VRF: a
        ------

        BGP Process Information: VRF a (Inactive)
        BGP Route Distinguisher: 100:1

        BGP is operating in standalone mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.64.4.4
        Default Cluster ID: 10 (manually configured)
        Active Cluster IDs:  10
        Fast external fallover enabled
        Platform RLIMIT max: 2147483648 bytes
        Maximum limit for BMP buffer size: 409 MB
        Default value for BMP buffer size: 307 MB
        Current limit for BMP buffer size: 307 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 0, Node: node0_0_CPU0
        Restart count: 1
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/1
        Non-Default VRFs:          3               0/2
        This VRF:                                  0/2

                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               

                                   Number          Memory Used
        Attributes:                1               152             
        AS Paths:                  0               0               
        Communities:               0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           19              7600            

                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             

        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             

        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             

        VRF a Address family: IPv4 Unicast (Table inactive)
        Dampening is not enabled
        Client reflection is not enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 0
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 1
        Table version synced to RIB: 1
        Table version acked by RIB: 0
        IGP notification: IGPs notified
        RIB has not converged: version 0
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured

        State: Read Only mode.
        BGP Table Version: 1
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3

                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  

        Label Thread       Total triggers: 0

        Import Thread      Total triggers: 0

        RIB Thread         Total triggers: 0

        Update Thread      Total triggers: 0

                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             

                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0             


        VRF: VRF1
        ---------

        BGP Process Information: VRF VRF1 (Inactive)
        BGP Route Distinguisher: 100:2

        BGP is operating in standalone mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.64.4.4
        Default Cluster ID: 10 (manually configured)
        Active Cluster IDs:  10
        Fast external fallover enabled
        Platform RLIMIT max: 2147483648 bytes
        Maximum limit for BMP buffer size: 409 MB
        Default value for BMP buffer size: 307 MB
        Current limit for BMP buffer size: 307 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 0, Node: node0_0_CPU0
        Restart count: 1
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/1
        Non-Default VRFs:          3               0/2
        This VRF:                                  0/0

                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               

                                   Number          Memory Used
        Attributes:                1               152             
        AS Paths:                  0               0               
        Communities:               0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           19              7600            

                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             

        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             

        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             

        VRF: vrf1
        ---------

        BGP Process Information: VRF vrf1 (Inactive)
        BGP Route Distinguisher: 100:3

        BGP is operating in standalone mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.64.4.4
        Default Cluster ID: 10 (manually configured)
        Active Cluster IDs:  10
        Fast external fallover enabled
        Platform RLIMIT max: 2147483648 bytes
        Maximum limit for BMP buffer size: 409 MB
        Default value for BMP buffer size: 307 MB
        Current limit for BMP buffer size: 307 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 0, Node: node0_0_CPU0
        Restart count: 1
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/1
        Non-Default VRFs:          3               0/2
        This VRF:                                  0/0

                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               

                                   Number          Memory Used
        Attributes:                1               152             
        AS Paths:                  0               0               
        Communities:               0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           19              7600            

                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             

        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             

        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             


        BGP instance 1: 'test'
        ======================
        % None of the requested address families are configured for instance 'test'(28591)
        '''}

    golden_parsed_output2 = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'VRF1': 
                        {'active_cluster_id': '10.4.1.1',
                        'address_family': 
                            {'ipv6 unicast': 
                                {'attribute_download': 'Disabled',
                                'bgp_table_version': '3',
                                'chunk_elememt_size': '3',
                                'client_to_client_reflection': False,
                                'current_vrf': 'vrf1',
                                'dampening': False,
                                'dynamic_med': True,
                                'dynamic_med_int': '10 '
                                                   'minutes',
                                'dynamic_med_periodic_timer': 'Not '
                                                              'Running',
                                'dynamic_med_timer': 'Not '
                                                     'Running',
                                'label_retention_timer_value': '5 '
                                                               'mins',
                                'main_table_version': '3',
                                'nexthop_resolution_minimum_prefix_length': '0 '
                                                                            '(not '
                                                                            'configured)',
                                'num_of_scan_segments': '1',
                                'permanent_network': 'unconfigured',
                                'prefix_scanned_per_segment': '100000',
                                'prefixes_path': {'prefixes': {'mem_used': 0,
                                                               'number': 0}},
                                'remote_local': {'prefixes': {'allocated': 0,
                                                              'freed': 0}},
                                'rib_table_prefix_limit_reached': 'no',
                                'rib_table_prefix_limit_ver': '0',
                                'scan_interval': '60',
                                'soft_reconfig_entries': '0',
                                'state': 'normal '
                                         'mode',
                                'table_bit_field_size': '1 ',
                                'table_state': 'None',
                                'table_version_acked_by_rib': '3',
                                'table_version_synced_to_rib': '3',
                                'thread': {'import thread': {'triggers': {'Aug 10 15:55:35.385': {'tbl_ver': 3,
                                                                                                  'trig_tid': 3,
                                                                                                  'ver': 3}}},
                                           'label thread': {'triggers': {'Aug 10 15:55:35.385': {'tbl_ver': 3,
                                                                                                 'trig_tid': 3,
                                                                                                 'ver': 3}}},
                                           'rib thread': {'triggers': {'Aug 10 15:55:32.391': {'tbl_ver': 3,
                                                                                               'trig_tid': 8,
                                                                                               'ver': 3}}},
                                           'update thread': {'triggers': {'Aug 10 15:55:35.385': {'tbl_ver': 3,
                                                                                                  'trig_tid': 8,
                                                                                                  'ver': 3}}}},
                                'total_prefixes_scanned': '0'}},
                        'always_compare_med': False,
                        'as_number': 100,
                        'as_system_number_format': 'ASPLAIN',
                        'att': {'as_paths': {'memory_used': 0,
                                            'number': 0},
                               'attributes': {'memory_used': 0,
                                              'number': 0},
                               'bmp_paths': {'memory_used': 0,
                                             'number': 0},
                               'bmp_prefixes': {'memory_used': 0,
                                                'number': 0},
                               'communities': {'memory_used': 0,
                                               'number': 0},
                               'extended_communities': {'memory_used': 0,
                                                        'number': 0},
                               'large_communities': {'memory_used': 0,
                                                     'number': 0},
                               'nexthop_entries': {'memory_used': 10800,
                                                   'number': 27},
                               'paths': {'memory_used': 0,
                                         'number': 0},
                               'pe_distinguisher_labels': {'memory_used': 0,
                                                           'number': 0},
                               'pmsi_tunnel_attr': {'memory_used': 0,
                                                    'number': 0},
                               'ppmp_attr': {'memory_used': 0,
                                             'number': 0},
                               'ribrnh_tunnel_attr': {'memory_used': 0,
                                                      'number': 0},
                               'route_reflector_entries': {'memory_used': 0,
                                                           'number': 0},
                               'tunnel_encap_attr': {'memory_used': 0,
                                                     'number': 0}},
                        'bestpath_compare_routerid': False,
                        'bestpath_cost_community_ignore': False,
                        'bestpath_med_missing_at_worst': False,
                        'bgp_speaker_process': 0,
                        'bmp_pool_summary': {'100': {'alloc': 0,
                                                    'free': 0},
                                            '10000': {'alloc': 0,
                                                      'free': 0},
                                            '1200': {'alloc': 0,
                                                     'free': 0},
                                            '200': {'alloc': 0,
                                                    'free': 0},
                                            '20000': {'alloc': 0,
                                                      'free': 0},
                                            '2200': {'alloc': 0,
                                                     'free': 0},
                                            '300': {'alloc': 0,
                                                    'free': 0},
                                            '3300': {'alloc': 0,
                                                     'free': 0},
                                            '400': {'alloc': 0,
                                                    'free': 0},
                                            '4000': {'alloc': 0,
                                                     'free': 0},
                                            '4500': {'alloc': 0,
                                                     'free': 0},
                                            '500': {'alloc': 0,
                                                    'free': 0},
                                            '5500': {'alloc': 0,
                                                     'free': 0},
                                            '600': {'alloc': 0,
                                                    'free': 0},
                                            '6500': {'alloc': 0,
                                                     'free': 0},
                                            '700': {'alloc': 0,
                                                    'free': 0},
                                            '7500': {'alloc': 0,
                                                     'free': 0},
                                            '800': {'alloc': 0,
                                                    'free': 0},
                                            '8500': {'alloc': 0,
                                                     'free': 0},
                                            '900': {'alloc': 0,
                                                    'free': 0}},
                        'current_limit_for_bmp_buffer_size': 326,
                        'current_utilization_of_bmp_buffer_limit': 0,
                        'default_cluster_id': '10.4.1.1',
                        'default_keepalive': 60,
                        'default_local_preference': 100,
                        'default_value_for_bmp_buffer_size': 326,
                        'enforce_first_as': True,
                        'fast_external_fallover': True,
                        'generic_scan_interval': 60,
                        'log_neighbor_changes': True,
                        'max_limit_for_bmp_buffer_size': 435,
                        'message_logging_pool_summary': {'100': {'alloc': 0,
                                                                'free': 0},
                                                        '200': {'alloc': 0,
                                                                'free': 0},
                                                        '2200': {'alloc': 0,
                                                                 'free': 0},
                                                        '4500': {'alloc': 0,
                                                                 'free': 0},
                                                        '500': {'alloc': 0,
                                                                'free': 0}},
                        'node': 'node0_RSP1_CPU0',
                        'non_stop_routing': True,
                        'operation_mode': 'standalone',
                        'platform_rlimit_max': 2281701376,
                        'pool': {'1200': {'alloc': 0,
                                         'free': 0},
                                '200': {'alloc': 0,
                                        'free': 0},
                                '20000': {'alloc': 0,
                                          'free': 0},
                                '2200': {'alloc': 0,
                                         'free': 0},
                                '300': {'alloc': 1,
                                        'free': 0},
                                '3300': {'alloc': 0,
                                         'free': 0},
                                '400': {'alloc': 0,
                                        'free': 0},
                                '4000': {'alloc': 0,
                                         'free': 0},
                                '4500': {'alloc': 0,
                                         'free': 0},
                                '500': {'alloc': 0,
                                        'free': 0},
                                '5000': {'alloc': 0,
                                         'free': 0},
                                '600': {'alloc': 0,
                                        'free': 0},
                                '700': {'alloc': 0,
                                        'free': 0},
                                '800': {'alloc': 0,
                                        'free': 0},
                                '900': {'alloc': 0,
                                        'free': 0}},
                        'received_notifications': 0,
                        'received_updates': 0,
                        'restart_count': 7,
                        'route_distinguisher': '200:1',
                        'router_id': '10.229.11.11',
                        'sent_notifications': 0,
                        'sent_updates': 0,
                        'update_delay': 120,
                        'vrf_info': 
                            {'default': 
                                {'cfg': 3,
                                'nbrs_estab': 0,
                                'total': 1},
                            'non-default': 
                                {'cfg': 4,
                                'nbrs_estab': 0,
                                'total': 2}}},
                    'VRF2': 
                        {'active_cluster_id': '10.4.1.1',
                        'address_family': 
                            {'ipv6 unicast': 
                                {'attribute_download': 'Disabled',
                                'bgp_table_version': '3',
                                'chunk_elememt_size': '3',
                                'client_to_client_reflection': False,
                                'current_vrf': 'vrf2',
                                'dampening': False,
                                'dynamic_med': True,
                                'dynamic_med_int': '10 '
                                                   'minutes',
                                'dynamic_med_periodic_timer': 'Not '
                                                              'Running',
                                'dynamic_med_timer': 'Not '
                                                     'Running',
                                'label_retention_timer_value': '5 '
                                                               'mins',
                                'main_table_version': '3',
                                'nexthop_resolution_minimum_prefix_length': '0 '
                                                                            '(not '
                                                                            'configured)',
                                'num_of_scan_segments': '1',
                                'permanent_network': 'unconfigured',
                                'prefix_scanned_per_segment': '100000',
                                'prefixes_path': {'prefixes': {'mem_used': 0,
                                                               'number': 0}},
                                'remote_local': {'prefixes': {'allocated': 0,
                                                              'freed': 0}},
                                'rib_table_prefix_limit_reached': 'no',
                                'rib_table_prefix_limit_ver': '0',
                                'scan_interval': '60',
                                'soft_reconfig_entries': '0',
                                'state': 'normal '
                                         'mode',
                                'table_bit_field_size': '1 ',
                                'table_state': 'None',
                                'table_version_acked_by_rib': '3',
                                'table_version_synced_to_rib': '3',
                                'thread': {'import thread': {'triggers': {'Aug 10 15:55:35.385': {'tbl_ver': 3,
                                                                                                  'trig_tid': 3,
                                                                                                  'ver': 3}}},
                                           'label thread': {'triggers': {'Aug 10 15:55:35.385': {'tbl_ver': 3,
                                                                                                 'trig_tid': 3,
                                                                                                 'ver': 3}}},
                                           'rib thread': {'triggers': {'Aug 10 15:55:32.391': {'tbl_ver': 3,
                                                                                               'trig_tid': 8,
                                                                                               'ver': 3}}},
                                           'update thread': {'triggers': {'Aug 10 15:55:35.385': {'tbl_ver': 3,
                                                                                                  'trig_tid': 8,
                                                                                                  'ver': 3}}}},
                                'total_prefixes_scanned': '0'}},
                        'always_compare_med': False,
                        'as_number': 100,
                        'as_system_number_format': 'ASPLAIN',
                        'att': {'as_paths': {'memory_used': 0,
                                            'number': 0},
                               'attributes': {'memory_used': 0,
                                              'number': 0},
                               'bmp_paths': {'memory_used': 0,
                                             'number': 0},
                               'bmp_prefixes': {'memory_used': 0,
                                                'number': 0},
                               'communities': {'memory_used': 0,
                                               'number': 0},
                               'extended_communities': {'memory_used': 0,
                                                        'number': 0},
                               'large_communities': {'memory_used': 0,
                                                     'number': 0},
                               'nexthop_entries': {'memory_used': 10800,
                                                   'number': 27},
                               'paths': {'memory_used': 0,
                                         'number': 0},
                               'pe_distinguisher_labels': {'memory_used': 0,
                                                           'number': 0},
                               'pmsi_tunnel_attr': {'memory_used': 0,
                                                    'number': 0},
                               'ppmp_attr': {'memory_used': 0,
                                             'number': 0},
                               'ribrnh_tunnel_attr': {'memory_used': 0,
                                                      'number': 0},
                               'route_reflector_entries': {'memory_used': 0,
                                                           'number': 0},
                               'tunnel_encap_attr': {'memory_used': 0,
                                                     'number': 0}},
                        'bestpath_compare_routerid': False,
                        'bestpath_cost_community_ignore': False,
                        'bestpath_med_missing_at_worst': False,
                        'bgp_speaker_process': 0,
                        'bmp_pool_summary': {'100': {'alloc': 0,
                                                    'free': 0},
                                            '10000': {'alloc': 0,
                                                      'free': 0},
                                            '1200': {'alloc': 0,
                                                     'free': 0},
                                            '200': {'alloc': 0,
                                                    'free': 0},
                                            '20000': {'alloc': 0,
                                                      'free': 0},
                                            '2200': {'alloc': 0,
                                                     'free': 0},
                                            '300': {'alloc': 0,
                                                    'free': 0},
                                            '3300': {'alloc': 0,
                                                     'free': 0},
                                            '400': {'alloc': 0,
                                                    'free': 0},
                                            '4000': {'alloc': 0,
                                                     'free': 0},
                                            '4500': {'alloc': 0,
                                                     'free': 0},
                                            '500': {'alloc': 0,
                                                    'free': 0},
                                            '5500': {'alloc': 0,
                                                     'free': 0},
                                            '600': {'alloc': 0,
                                                    'free': 0},
                                            '6500': {'alloc': 0,
                                                     'free': 0},
                                            '700': {'alloc': 0,
                                                    'free': 0},
                                            '7500': {'alloc': 0,
                                                     'free': 0},
                                            '800': {'alloc': 0,
                                                    'free': 0},
                                            '8500': {'alloc': 0,
                                                     'free': 0},
                                            '900': {'alloc': 0,
                                                    'free': 0}},
                        'current_limit_for_bmp_buffer_size': 326,
                        'current_utilization_of_bmp_buffer_limit': 0,
                        'default_cluster_id': '10.4.1.1',
                        'default_keepalive': 60,
                        'default_local_preference': 100,
                        'default_value_for_bmp_buffer_size': 326,
                        'enforce_first_as': True,
                        'fast_external_fallover': True,
                        'generic_scan_interval': 60,
                        'log_neighbor_changes': True,
                        'max_limit_for_bmp_buffer_size': 435,
                        'message_logging_pool_summary': {'100': {'alloc': 0,
                                                                'free': 0},
                                                        '200': {'alloc': 0,
                                                                'free': 0},
                                                        '2200': {'alloc': 0,
                                                                 'free': 0},
                                                        '4500': {'alloc': 0,
                                                                 'free': 0},
                                                        '500': {'alloc': 0,
                                                                'free': 0}},
                        'node': 'node0_RSP1_CPU0',
                        'non_stop_routing': True,
                        'operation_mode': 'standalone',
                        'platform_rlimit_max': 2281701376,
                        'pool': {'1200': {'alloc': 0,
                                         'free': 0},
                                '200': {'alloc': 0,
                                        'free': 0},
                                '20000': {'alloc': 0,
                                          'free': 0},
                                '2200': {'alloc': 0,
                                         'free': 0},
                                '300': {'alloc': 1,
                                        'free': 0},
                                '3300': {'alloc': 0,
                                         'free': 0},
                                '400': {'alloc': 0,
                                        'free': 0},
                                '4000': {'alloc': 0,
                                         'free': 0},
                                '4500': {'alloc': 0,
                                         'free': 0},
                                '500': {'alloc': 0,
                                        'free': 0},
                                '5000': {'alloc': 0,
                                         'free': 0},
                                '600': {'alloc': 0,
                                        'free': 0},
                                '700': {'alloc': 0,
                                        'free': 0},
                                '800': {'alloc': 0,
                                        'free': 0},
                                '900': {'alloc': 0,
                                        'free': 0}},
                        'received_notifications': 0,
                        'received_updates': 0,
                        'restart_count': 7,
                        'route_distinguisher': '200:2',
                        'router_id': '10.229.11.11',
                        'sent_notifications': 0,
                        'sent_updates': 0,
                        'update_delay': 120,
                        'vrf_info': 
                            {'default': 
                                {'cfg': 3,
                                'nbrs_estab': 0,
                                'total': 1},
                            'non-default': 
                                {'cfg': 4,
                                'nbrs_estab': 0,
                                'total': 2}}}}},
            'test': {},
            'test1': {},
            'test2': {}}}

    golden_output2 = {'execute.return_value': '''
        RP/0/RSP1/CPU0:PE1#show bgp instance all vrf all ipv6 unicast process detail 
        Fri Aug 11 11:09:29.206 PDT

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        BGP Process Information: VRF VRF1
        BGP Route Distinguisher: 200:1

        BGP is operating in STANDALONE mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.229.11.11 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2281701376 bytes
        Maximum limit for BMP buffer size: 435 MB
        Default value for BMP buffer size: 326 MB
        Current limit for BMP buffer size: 326 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 0, Node: node0_RSP1_CPU0
        Restart count: 7
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/3
        Non-Default VRFs:          2               0/4
        This VRF:                                  0/2

                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               

                                   Number          Memory Used
        Attributes:                0               0               
        AS Paths:                  0               0               
        Communities:               0               0               
        Large Communities:         0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           27              10800           
                  
                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             
                  
        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             
                  
        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             
                  
        VRF VRF1 Address family: IPv6 Unicast
        Dampening is not enabled
        Client reflection is not enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 3
        Table version synced to RIB: 3
        Table version acked by RIB: 3
        RIB has converged: version 2
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 3
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Aug 10 15:55:35.385   3           3           3         
                           Aug 10 15:55:32.391   3           3           19        
                           Aug 10 15:55:32.385   0           3           4         
                           Total triggers: 3
                  
        Import Thread      Aug 10 15:55:35.385   3           3           3         
                           Aug 10 15:55:32.391   3           3           19        
                           Aug 10 15:55:32.385   0           3           19        
                           Total triggers: 3
                  
        RIB Thread         Aug 10 15:55:32.391   3           3           8         
                           Aug 10 15:55:32.385   1           3           8         
                           Aug 10 15:55:32.385   1           3           6         
                           Total triggers: 3
                  
        Update Thread      Aug 10 15:55:35.385   3           3           8         
                           Aug 10 15:55:32.391   3           3           8         
                           Aug 10 15:55:32.391   3           3           19        
                           Total triggers: 3
                  
                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
                  
                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0             
                  
                  
        VRF: VRF2 
        --------- 
                  
        BGP Process Information: VRF VRF2
        BGP Route Distinguisher: 200:2
                  
        BGP is operating in STANDALONE mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.229.11.11 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2281701376 bytes
        Maximum limit for BMP buffer size: 435 MB
        Default value for BMP buffer size: 326 MB
        Current limit for BMP buffer size: 326 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60
                  
        BGP Speaker process: 0, Node: node0_RSP1_CPU0
        Restart count: 7
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/3
        Non-Default VRFs:          2               0/4
        This VRF:                                  0/2
                  
                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               
                  
                                   Number          Memory Used
        Attributes:                0               0               
        AS Paths:                  0               0               
        Communities:               0               0               
        Large Communities:         0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           27              10800           
                  
                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             
                  
        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             
                  
        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             
                  
        VRF VRF2 Address family: IPv6 Unicast
        Dampening is not enabled
        Client reflection is not enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 3
        Table version synced to RIB: 3
        Table version acked by RIB: 3
        RIB has converged: version 2
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 3
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Aug 10 15:55:35.385   3           3           3         
                           Aug 10 15:55:32.391   3           3           19        
                           Aug 10 15:55:32.385   0           3           4         
                           Total triggers: 3
                  
        Import Thread      Aug 10 15:55:35.385   3           3           3         
                           Aug 10 15:55:32.391   3           3           19        
                           Aug 10 15:55:32.385   0           3           19        
                           Total triggers: 3
                  
        RIB Thread         Aug 10 15:55:32.391   3           3           8         
                           Aug 10 15:55:32.385   1           3           8         
                           Aug 10 15:55:32.385   1           3           6         
                           Total triggers: 3
                  
        Update Thread      Aug 10 15:55:35.385   3           3           8         
                           Aug 10 15:55:32.391   3           3           8         
                           Aug 10 15:55:32.391   3           3           19        
                           Total triggers: 3
                  
                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
                  
                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0             
                  
                  
                  
        BGP instance 1: 'test'
        ======================
        % None of the requested address families are configured for instance 'test'(29193)
                  
        BGP instance 2: 'test1'
        =======================
        % None of the requested address families are configured for instance 'test1'(29193)
                  
        BGP instance 3: 'test2'
        =======================
        % None of the requested address families are configured for instance 'test2'(29193)
        RP/0/RSP1/CPU0:PE1#
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowBgpInstanceProcessDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='vrf')

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowBgpInstanceProcessDetail(device=self.device)
        parsed_output = obj.parse(vrf_type='vrf')
        self.assertEqual(parsed_output,self.golden_parsed_output1)

    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowBgpInstanceProcessDetail(device=self.device)
        parsed_output = obj.parse(vrf_type='vrf', address_family='ipv6 unicast')
        self.assertEqual(parsed_output,self.golden_parsed_output2)


# ============================================================
# Unit test for 'show bgp instance all all all process detail'
# ============================================================

class test_show_bgp_instance_all_all_all_process_detail(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output1 = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'default': 
                        {'active_cluster_id': '10.4.1.1',
                        'address_family': 
                            {'vpnv4 unicast': 
                                {'attribute_download': 'Disabled',
                                'bgp_table_version': '43',
                                'chunk_elememt_size': '3',
                                'client_to_client_reflection': True,
                                'dampening': False,
                                'dynamic_med': True,
                                'dynamic_med_int': '10 '
                                                  'minutes',
                                'dynamic_med_periodic_timer': 'Not '
                                                             'Running',
                                'dynamic_med_timer': 'Not '
                                                    'Running',
                                'label_retention_timer_value': '5 '
                                                              'mins',
                                'main_table_version': '43',
                                'nexthop_resolution_minimum_prefix_length': '0 '
                                                                           '(not '
                                                                           'configured)',
                                'num_of_scan_segments': '1',
                                'permanent_network': 'unconfigured',
                                'prefix_scanned_per_segment': '100000',
                                'prefixes_path': {'remote prefixes': {'mem_used': 920,
                                                                     'number': 10}},
                                'remote_local': {'remote prefixes': {'allocated': 10,
                                                                    'freed': 0}},
                                'rib_has_not_converged': 'version '
                                                        '0',
                                'rib_table_prefix_limit_reached': 'no',
                                'rib_table_prefix_limit_ver': '0',
                                'scan_interval': '60',
                                'soft_reconfig_entries': '0',
                                'state': 'normal '
                                        'mode',
                                'table_bit_field_size': '1 ',
                                'table_version_acked_by_rib': '0',
                                'table_version_synced_to_rib': '43',
                                'thread': {'import thread': {'triggers': {'Jun 28 19:10:16.427': {'tbl_ver': 43,
                                                                                                 'trig_tid': 3,
                                                                                                 'ver': 43}}},
                                          'label thread': {'triggers': {'Jun 28 19:10:16.427': {'tbl_ver': 43,
                                                                                                'trig_tid': 3,
                                                                                                'ver': 43}}},
                                          'rib thread': {'triggers': {'Jun 28 18:29:29.595': {'tbl_ver': 43,
                                                                                              'trig_tid': 8,
                                                                                              'ver': 33}}},
                                          'update thread': {'triggers': {'Jun 28 19:10:16.427': {'tbl_ver': 43,
                                                                                                 'trig_tid': 8,
                                                                                                 'ver': 43}}}},
                                'total_prefixes_scanned': '40'},
                            'vpnv6 unicast': 
                                {'attribute_download': 'Disabled',
                                'bgp_table_version': '43',
                                'chunk_elememt_size': '3',
                                'client_to_client_reflection': True,
                                'dampening': False,
                                'dynamic_med': False,
                                'dynamic_med_int': '10 '
                                                  'minutes',
                                'dynamic_med_periodic_timer': 'Not '
                                                             'Running',
                                'dynamic_med_timer': 'Not '
                                                    'Running',
                                'label_retention_timer_value': '5 '
                                                              'mins',
                                'main_table_version': '43',
                                'nexthop_resolution_minimum_prefix_length': '0 '
                                                                           '(not '
                                                                           'configured)',
                                'num_of_scan_segments': '1',
                                'permanent_network': 'unconfigured',
                                'prefix_scanned_per_segment': '100000',
                                'prefixes_path': {'remote prefixes': {'mem_used': 1040,
                                                                     'number': 10}},
                                'remote_local': {'remote prefixes': {'allocated': 10,
                                                                    'freed': 0}},
                                'rib_has_not_converged': 'version '
                                                        '0',
                                'rib_table_prefix_limit_reached': 'no',
                                'rib_table_prefix_limit_ver': '0',
                                'scan_interval': '60',
                                'soft_reconfig_entries': '0',
                                'state': 'normal '
                                        'mode',
                                'table_bit_field_size': '1 ',
                                'table_version_acked_by_rib': '0',
                                'table_version_synced_to_rib': '43',
                                'thread': {'import thread': {'triggers': {'Jun 28 19:10:16.427': {'tbl_ver': 43,
                                                                                                 'trig_tid': 3,
                                                                                                 'ver': 43}}},
                                          'label thread': {'triggers': {'Jun 28 19:10:16.427': {'tbl_ver': 43,
                                                                                                'trig_tid': 3,
                                                                                                'ver': 43}}},
                                          'rib thread': {'triggers': {'Jun 28 18:29:34.604': {'tbl_ver': 43,
                                                                                              'trig_tid': 8,
                                                                                              'ver': 33}}},
                                          'update thread': {'triggers': {'Jun 28 19:10:16.427': {'tbl_ver': 43,
                                                                                                 'trig_tid': 8,
                                                                                                 'ver': 43}}}},
                                'total_prefixes_scanned': '40'}},
                        'as_number': 100,
                        'as_system_number_format': 'ASPLAIN',
                        'att': {'as_paths': {'memory_used': 480,
                                           'number': 6},
                              'attributes': {'memory_used': 912,
                                             'number': 6},
                              'communities': {'memory_used': 0,
                                              'number': 0},
                              'extended_communities': {'memory_used': 480,
                                                       'number': 6},
                              'imported_paths': {'memory_used': 2200,
                                                 'number': 25},
                              'local_paths': {'memory_used': 2640,
                                              'number': 30},
                              'local_prefixes': {'memory_used': 3210,
                                                 'number': 30},
                              'local_rds': {'memory_used': 160,
                                            'number': 2},
                              'nexthop_entries': {'memory_used': 12800,
                                                  'number': 32},
                              'pe_distinguisher_labels': {'memory_used': 0,
                                                          'number': 0},
                              'pmsi_tunnel_attr': {'memory_used': 0,
                                                   'number': 0},
                              'ppmp_attr': {'memory_used': 0,
                                            'number': 0},
                              'remote_paths': {'memory_used': 1760,
                                               'number': 20},
                              'remote_rds': {'memory_used': 160,
                                             'number': 2},
                              'ribrnh_tunnel_attr': {'memory_used': 0,
                                                     'number': 0},
                              'route_reflector_entries': {'memory_used': 320,
                                                          'number': 4},
                              'total_paths': {'memory_used': 4400,
                                              'number': 50},
                              'total_prefixes': {'memory_used': 4280,
                                                 'number': 40},
                              'total_rds': {'memory_used': 320,
                                            'number': 4},
                              'tunnel_encap_attr': {'memory_used': 0,
                                                    'number': 0}},
                        'bgp_speaker_process': 0,
                        'bmp_pool_summary': {'100': {'alloc': 0,
                                                   'free': 0},
                                           '10000': {'alloc': 0,
                                                     'free': 0},
                                           '1200': {'alloc': 0,
                                                    'free': 0},
                                           '200': {'alloc': 0,
                                                   'free': 0},
                                           '20000': {'alloc': 0,
                                                     'free': 0},
                                           '2200': {'alloc': 0,
                                                    'free': 0},
                                           '300': {'alloc': 0,
                                                   'free': 0},
                                           '3300': {'alloc': 0,
                                                    'free': 0},
                                           '400': {'alloc': 0,
                                                   'free': 0},
                                           '4000': {'alloc': 0,
                                                    'free': 0},
                                           '4500': {'alloc': 0,
                                                    'free': 0},
                                           '500': {'alloc': 0,
                                                   'free': 0},
                                           '5500': {'alloc': 0,
                                                    'free': 0},
                                           '600': {'alloc': 0,
                                                   'free': 0},
                                           '6500': {'alloc': 0,
                                                    'free': 0},
                                           '700': {'alloc': 0,
                                                   'free': 0},
                                           '7500': {'alloc': 0,
                                                    'free': 0},
                                           '800': {'alloc': 0,
                                                   'free': 0},
                                           '8500': {'alloc': 0,
                                                    'free': 0},
                                           '900': {'alloc': 0,
                                                   'free': 0}},
                        'current_limit_for_bmp_buffer_size': 307,
                        'current_utilization_of_bmp_buffer_limit': 0,
                        'default_cluster_id': '10.4.1.1',
                        'default_keepalive': 60,
                        'default_local_preference': 100,
                        'default_value_for_bmp_buffer_size': 307,
                        'enforce_first_as': True,
                        'fast_external_fallover': True,
                        'generic_scan_interval': 60,
                        'max_limit_for_bmp_buffer_size': 409,
                        'message_logging_pool_summary': {'100': {'alloc': 19,
                                                               'free': 10},
                                                       '200': {'alloc': 11,
                                                               'free': 1},
                                                       '2200': {'alloc': 0,
                                                                'free': 0},
                                                       '4500': {'alloc': 0,
                                                                'free': 0},
                                                       '500': {'alloc': 19,
                                                               'free': 12}},
                        'log_neighbor_changes': True,
                        'node': 'node0_0_CPU0',
                        'non_stop_routing': True,
                        'operation_mode': 'standalone',
                        'platform_rlimit_max': 2147483648,
                        'pool': {'1200': {'alloc': 0,
                                        'free': 0},
                               '200': {'alloc': 0,
                                       'free': 0},
                               '20000': {'alloc': 0,
                                         'free': 0},
                               '2200': {'alloc': 0,
                                        'free': 0},
                               '300': {'alloc': 311,
                                       'free': 310},
                               '3300': {'alloc': 0,
                                        'free': 0},
                               '400': {'alloc': 6,
                                       'free': 6},
                               '4000': {'alloc': 0,
                                        'free': 0},
                               '4500': {'alloc': 0,
                                        'free': 0},
                               '500': {'alloc': 20,
                                       'free': 20},
                               '5000': {'alloc': 0,
                                        'free': 0},
                               '600': {'alloc': 12,
                                       'free': 12},
                               '700': {'alloc': 2,
                                       'free': 2},
                               '800': {'alloc': 0,
                                       'free': 0},
                               '900': {'alloc': 0,
                                       'free': 0}},
                        'received_notifications': 0,
                        'received_updates': 24,
                        'restart_count': 1,
                        'router_id': '10.4.1.1',
                        'sent_notifications': 1,
                        'sent_updates': 14,
                        'update_delay': 120,
                        'vrf_info': {'default': {'cfg': 2,
                                               'nbrs_estab': 2,
                                               'total': 1},
                                   'non-default': {'cfg': 4,
                                                   'nbrs_estab': 4,
                                                   'total': 2}}}}}}}

    golden_output1 = {'execute.return_value': '''
        Wed Jun 28 19:11:16.033 UTC

        BGP instance 0: 'default'
        =========================

        BGP Process Information: 
        BGP is operating in standalone mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.4.1.1 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2147483648 bytes
        Maximum limit for BMP buffer size: 409 MB
        Default value for BMP buffer size: 307 MB
        Current limit for BMP buffer size: 307 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 0, Node: node0_0_CPU0
        Restart count: 1
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               2/2
        Non-Default VRFs:          2               4/4

                                   Sent            Received
        Updates:                   14              24              
        Notifications:             1               0               

                                   Number          Memory Used
        Attributes:                6               912             
        AS Paths:                  6               480             
        Communities:               0               0               
        Extended communities:      6               480             
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   4               320             
        Nexthop Entries:           32              12800           

                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  311             310           
        Pool 400:                  6               6             
        Pool 500:                  20              20            
        Pool 600:                  12              12            
        Pool 700:                  2               2             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             

        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  19              10            
        Pool 200:                  11              1             
        Pool 500:                  19              12            
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             

        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             

        Address family: VPNv4 Unicast
        Dampening is not enabled
        Client reflection is enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 40
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 43
        Table version synced to RIB: 43
        Table version acked by RIB: 0
        RIB has not converged: version 0
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured

        State: Normal mode.
        BGP Table Version: 43
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3

                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  

        Label Thread       Jun 28 19:10:16.427   43          43          3         
                           Jun 28 19:10:16.417   43          43          3         
                           Jun 28 19:09:29.680   43          43          3         
                           Jun 28 19:09:29.670   43          43          3         
                           Jun 28 18:29:34.604   43          43          3         
                           Jun 28 18:29:29.595   33          43          4         
                           Jun 28 18:29:29.595   33          38          3         
                           Jun 28 18:24:52.694   33          33          3         
                           Total triggers: 15

        Import Thread      Jun 28 19:10:16.427   43          43          3         
                           Jun 28 19:10:16.417   43          43          3         
                           Jun 28 19:09:29.680   43          43          3         
                           Jun 28 19:09:29.670   43          43          3         
                           Jun 28 18:29:34.604   43          43          3         
                           Jun 28 18:29:29.595   43          43          8         
                           Jun 28 18:29:29.595   38          43          4         
                           Jun 28 18:29:29.595   33          38          3         
                           Total triggers: 16

        RIB Thread         Jun 28 18:29:29.595   33          43          8         
                           Jun 28 18:29:29.595   33          43          4         
                           Jun 28 18:24:26.135   13          33          4         
                           Jun 28 18:24:26.135   13          33          8         
                           Jun 28 18:24:26.135   13          33          4         
                           Jun 28 18:24:21.656   11          13          4         
                           Jun 28 18:21:26.418   1           11          8         
                           Jun 28 18:21:26.418   1           11          6         
                           Total triggers: 8

        Update Thread      Jun 28 19:10:16.427   43          43          8         
                           Jun 28 19:10:16.417   43          43          8         
                           Jun 28 19:09:29.680   43          43          8         
                           Jun 28 19:09:29.670   43          43          8         
                           Jun 28 18:29:34.604   43          43          8         
                           Jun 28 18:29:29.605   43          43          18        
                           Jun 28 18:29:29.595   33          43          8         
                           Jun 28 18:24:52.694   33          33          8         
                           Total triggers: 17

                              Allocated       Freed         
        Remote Prefixes:      10              0             
        Remote Paths:         20              0             
        Remote Path-elems:    10              0             

        Local Prefixes:       30              0             
        Local Paths:          30              0             

                              Number          Mem Used      
        Remote Prefixes:      10              920           
        Remote Paths:         20              1760          
        Remote Path-elems:    10              630           
        Remote RDs:           2               160           

        Local Prefixes:       30              2850          
        Local Paths:          30              2640          
        Local RDs:            2               160           

        Total Prefixes:       40              3800          
        Total Paths:          50              4400          
        Total Path-elems:     40              4400          
        Imported Paths:       25              2200          
        Total RDs:            4               320           


        Address family: VPNv6 Unicast
        Dampening is not enabled
        Client reflection is enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 40
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 43
        Table version synced to RIB: 43
        Table version acked by RIB: 0
        RIB has not converged: version 0
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured

        State: Normal mode.
        BGP Table Version: 43
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3

                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  

        Label Thread       Jun 28 19:10:16.427   43          43          3         
                           Jun 28 19:10:16.417   43          43          3         
                           Jun 28 19:09:29.680   43          43          3         
                           Jun 28 19:09:29.670   43          43          3         
                           Jun 28 18:29:34.604   33          43          4         
                           Jun 28 18:29:34.604   33          38          3         
                           Jun 28 18:29:29.595   33          33          3         
                           Jun 28 18:24:52.694   33          33          3         
                           Total triggers: 15

        Import Thread      Jun 28 19:10:16.427   43          43          3         
                           Jun 28 19:10:16.417   43          43          3         
                           Jun 28 19:09:29.680   43          43          3         
                           Jun 28 19:09:29.670   43          43          3         
                           Jun 28 18:29:34.604   43          43          8         
                           Jun 28 18:29:34.604   38          43          4         
                           Jun 28 18:29:34.604   33          38          3         
                           Jun 28 18:29:29.595   33          33          3         
                           Total triggers: 16

        RIB Thread         Jun 28 18:29:34.604   33          43          8         
                           Jun 28 18:29:34.604   33          43          4         
                           Jun 28 18:24:26.135   13          33          4         
                           Jun 28 18:24:26.135   13          33          4         
                           Jun 28 18:24:21.656   11          13          8         
                           Jun 28 18:21:26.428   1           11          8         
                           Jun 28 18:21:26.418   1           11          6         
                           Total triggers: 7

        Update Thread      Jun 28 19:10:16.427   43          43          8         
                           Jun 28 19:10:16.417   43          43          8         
                           Jun 28 19:09:29.680   43          43          8         
                           Jun 28 19:09:29.670   43          43          8         
                           Jun 28 18:29:34.604   43          43          19        
                           Jun 28 18:29:34.604   33          43          8         
                           Jun 28 18:29:29.595   33          33          8         
                           Jun 28 18:24:52.694   33          33          8         
                           Total triggers: 17

                              Allocated       Freed         
        Remote Prefixes:      10              0             
        Remote Paths:         20              0             
        Remote Path-elems:    10              0             

        Local Prefixes:       30              0             
        Local Paths:          30              0             

                              Number          Mem Used      
        Remote Prefixes:      10              1040          
        Remote Paths:         20              1760          
        Remote Path-elems:    10              630           
        Remote RDs:           2               160           

        Local Prefixes:       30              3210          
        Local Paths:          30              2640          
        Local RDs:            2               160           

        Total Prefixes:       40              4280          
        Total Paths:          50              4400          
        Total Path-elems:     40              4400          
        Imported Paths:       25              2200          
        Total RDs:            4               320
        '''}

    golden_parsed_output2 = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'default': 
                        {'active_cluster_id': '10.4.1.1',
                        'address_family': 
                            {'vpnv4 unicast': 
                                {'attribute_download': 'Disabled',
                                'bgp_table_version': '7',
                                'chunk_elememt_size': '3',
                                'client_to_client_reflection': True,
                                'dampening': False,
                                'dynamic_med': True,
                                'dynamic_med_int': '10 '
                                                  'minutes',
                                'dynamic_med_periodic_timer': 'Not '
                                                             'Running',
                                'dynamic_med_timer': 'Not '
                                                    'Running',
                                'label_retention_timer_value': '5 '
                                                              'mins',
                                'main_table_version': '7',
                                'nexthop_resolution_minimum_prefix_length': '0 '
                                                                           '(not '
                                                                           'configured)',
                                'num_of_scan_segments': '1',
                                'permanent_network': 'unconfigured',
                                'prefix_scanned_per_segment': '100000',
                                'prefixes_path': {'remote prefixes': {'mem_used': 0,
                                                                     'number': 0}},
                                'remote_local': {'remote prefixes': {'allocated': 0,
                                                                    'freed': 0}},
                                'rib_has_not_converged': 'version '
                                                        '0',
                                'rib_table_prefix_limit_reached': 'no',
                                'rib_table_prefix_limit_ver': '0',
                                'scan_interval': '60',
                                'soft_reconfig_entries': '0',
                                'state': 'normal '
                                        'mode',
                                'table_bit_field_size': '1 ',
                                'table_version_acked_by_rib': '0',
                                'table_version_synced_to_rib': '7',
                                'total_prefixes_scanned': '0'},
                            'vpnv6 unicast': 
                                {'attribute_download': 'Disabled',
                                'bgp_table_version': '7',
                                'chunk_elememt_size': '3',
                                'client_to_client_reflection': True,
                                'dampening': False,
                                'dynamic_med': False,
                                'dynamic_med_int': '10 '
                                                  'minutes',
                                'dynamic_med_periodic_timer': 'Not '
                                                             'Running',
                                'dynamic_med_timer': 'Not '
                                                    'Running',
                                'label_retention_timer_value': '5 '
                                                              'mins',
                                'main_table_version': '7',
                                'nexthop_resolution_minimum_prefix_length': '0 '
                                                                           '(not '
                                                                           'configured)',
                                'num_of_scan_segments': '1',
                                'permanent_network': 'unconfigured',
                                'prefix_scanned_per_segment': '100000',
                                'prefixes_path': {'remote prefixes': {'mem_used': 0,
                                                                     'number': 0}},
                                'remote_local': {'remote prefixes': {'allocated': 0,
                                                                    'freed': 0}},
                                'rib_has_not_converged': 'version '
                                                        '0',
                                'rib_table_prefix_limit_reached': 'no',
                                'rib_table_prefix_limit_ver': '0',
                                'scan_interval': '60',
                                'soft_reconfig_entries': '0',
                                'state': 'normal '
                                        'mode',
                                'table_bit_field_size': '1 ',
                                'table_version_acked_by_rib': '0',
                                'table_version_synced_to_rib': '7',
                                'total_prefixes_scanned': '0'}},
                        'as_number': 100,
                        'as_system_number_format': 'ASPLAIN',
                        'att': {'as_paths': {'memory_used': 0,
                                           'number': 0},
                              'attributes': {'memory_used': 0,
                                             'number': 0},
                              'communities': {'memory_used': 0,
                                              'number': 0},
                              'extended_communities': {'memory_used': 0,
                                                       'number': 0},
                              'imported_paths': {'memory_used': 0,
                                                 'number': 0},
                              'large_communities': {'memory_used': 0,
                                                    'number': 0},
                              'local_paths': {'memory_used': 0,
                                              'number': 0},
                              'local_prefixes': {'memory_used': 0,
                                                 'number': 0},
                              'local_rds': {'memory_used': 160,
                                            'number': 2},
                              'nexthop_entries': {'memory_used': 10400,
                                                  'number': 26},
                              'pe_distinguisher_labels': {'memory_used': 0,
                                                          'number': 0},
                              'pmsi_tunnel_attr': {'memory_used': 0,
                                                   'number': 0},
                              'ppmp_attr': {'memory_used': 0,
                                            'number': 0},
                              'remote_paths': {'memory_used': 0,
                                               'number': 0},
                              'remote_rds': {'memory_used': 0,
                                             'number': 0},
                              'ribrnh_tunnel_attr': {'memory_used': 0,
                                                     'number': 0},
                              'route_reflector_entries': {'memory_used': 0,
                                                          'number': 0},
                              'total_paths': {'memory_used': 0,
                                              'number': 0},
                              'total_prefixes': {'memory_used': 0,
                                                 'number': 0},
                              'total_rds': {'memory_used': 160,
                                            'number': 2},
                              'tunnel_encap_attr': {'memory_used': 0,
                                                    'number': 0}},
                        'bgp_speaker_process': 0,
                        'bmp_pool_summary': {'100': {'alloc': 0,
                                                   'free': 0},
                                           '10000': {'alloc': 0,
                                                     'free': 0},
                                           '1200': {'alloc': 0,
                                                    'free': 0},
                                           '200': {'alloc': 0,
                                                   'free': 0},
                                           '20000': {'alloc': 0,
                                                     'free': 0},
                                           '2200': {'alloc': 0,
                                                    'free': 0},
                                           '300': {'alloc': 0,
                                                   'free': 0},
                                           '3300': {'alloc': 0,
                                                    'free': 0},
                                           '400': {'alloc': 0,
                                                   'free': 0},
                                           '4000': {'alloc': 0,
                                                    'free': 0},
                                           '4500': {'alloc': 0,
                                                    'free': 0},
                                           '500': {'alloc': 0,
                                                   'free': 0},
                                           '5500': {'alloc': 0,
                                                    'free': 0},
                                           '600': {'alloc': 0,
                                                   'free': 0},
                                           '6500': {'alloc': 0,
                                                    'free': 0},
                                           '700': {'alloc': 0,
                                                   'free': 0},
                                           '7500': {'alloc': 0,
                                                    'free': 0},
                                           '800': {'alloc': 0,
                                                   'free': 0},
                                           '8500': {'alloc': 0,
                                                    'free': 0},
                                           '900': {'alloc': 0,
                                                   'free': 0}},
                        'current_limit_for_bmp_buffer_size': 326,
                        'current_utilization_of_bmp_buffer_limit': 0,
                        'default_cluster_id': '10.4.1.1',
                        'default_keepalive': 60,
                        'default_local_preference': 100,
                        'default_value_for_bmp_buffer_size': 326,
                        'enforce_first_as': True,
                        'fast_external_fallover': True,
                        'generic_scan_interval': 60,
                        'max_limit_for_bmp_buffer_size': 435,
                        'message_logging_pool_summary': {'100': {'alloc': 0,
                                                               'free': 0},
                                                       '200': {'alloc': 0,
                                                               'free': 0},
                                                       '2200': {'alloc': 0,
                                                                'free': 0},
                                                       '4500': {'alloc': 0,
                                                                'free': 0},
                                                       '500': {'alloc': 0,
                                                               'free': 0}},
                        'log_neighbor_changes': True,
                        'node': 'node0_RSP1_CPU0',
                        'non_stop_routing': True,
                        'operation_mode': 'standalone',
                        'platform_rlimit_max': 2281701376,
                        'pool': {'1200': {'alloc': 0,
                                        'free': 0},
                               '200': {'alloc': 0,
                                       'free': 0},
                               '20000': {'alloc': 0,
                                         'free': 0},
                               '2200': {'alloc': 0,
                                        'free': 0},
                               '300': {'alloc': 1,
                                       'free': 0},
                               '3300': {'alloc': 0,
                                        'free': 0},
                               '400': {'alloc': 0,
                                       'free': 0},
                               '4000': {'alloc': 0,
                                        'free': 0},
                               '4500': {'alloc': 0,
                                        'free': 0},
                               '500': {'alloc': 0,
                                       'free': 0},
                               '5000': {'alloc': 0,
                                        'free': 0},
                               '600': {'alloc': 0,
                                       'free': 0},
                               '700': {'alloc': 0,
                                       'free': 0},
                               '800': {'alloc': 0,
                                       'free': 0},
                               '900': {'alloc': 0,
                                       'free': 0}},
                        'received_notifications': 0,
                        'received_updates': 0,
                        'restart_count': 1,
                        'router_id': '10.4.1.1',
                        'sent_notifications': 0,
                        'sent_updates': 0,
                        'update_delay': 120,
                        'vrf_info': {'default': {'cfg': 2,
                                               'nbrs_estab': 0,
                                               'total': 1},
                                   'non-default': {'cfg': 4,
                                                   'nbrs_estab': 0,
                                                   'total': 2}}}}},
            'test': {'vrf': {'default': {}}},
            'test1': {'vrf': {'default': {}}},
            'test2': {'vrf': {'default': {}}}}}
        
    golden_output2 = {'execute.return_value': '''
        BGP instance 0: 'default'
        =========================

        BGP Process Information: 
        BGP is operating in standalone mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.4.1.1 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2281701376 bytes
        Maximum limit for BMP buffer size: 435 MB
        Default value for BMP buffer size: 326 MB
        Current limit for BMP buffer size: 326 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 0, Node: node0_RSP1_CPU0
        Restart count: 1
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/2
        Non-Default VRFs:          2               0/4

                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               

                                   Number          Memory Used
        Attributes:                0               0               
        AS Paths:                  0               0               
        Communities:               0               0               
        Large Communities:         0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           26              10400           

                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             

        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             

        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             

        Address family: VPNv4 Unicast
        Dampening is not enabled
        Client reflection is enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 7
        Table version synced to RIB: 7
        Table version acked by RIB: 0
        RIB has not converged: version 0
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured

        State: Normal mode.
        BGP Table Version: 7
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
        Maximum supported label-stack depth:
           For IPv4 Nexthop: 0
           For IPv6 Nexthop: 0

                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  

        Label Thread       Jul  6 11:42:04.367   7           7           3         
                           Jul  6 11:42:01.371   5           6           9         
                           Jul  6 11:42:01.370   5           5           18        
                           Jul  6 11:42:01.367   0           5           4         
                           Total triggers: 4

        Import Thread      Jul  6 11:42:04.367   7           7           3         
                           Jul  6 11:42:01.371   5           6           9         
                           Jul  6 11:42:01.370   5           5           18        
                           Jul  6 11:42:01.366   0           5           18        
                           Total triggers: 4

        RIB Thread         Jul  6 11:42:01.371   5           7           8         
                           Jul  6 11:42:01.370   5           5           8         
                           Jul  6 11:42:01.367   1           5           8         
                           Jul  6 11:42:01.366   1           5           6         
                           Total triggers: 4

        Update Thread      Jul  6 11:42:04.367   7           7           8         
                           Jul  6 11:42:01.371   7           7           18        
                           Jul  6 11:42:01.371   5           7           9         
                           Jul  6 11:42:01.370   5           5           8         
                           Jul  6 11:42:01.370   5           5           18        
                           Total triggers: 5

                              Allocated       Freed         
        Remote Prefixes:      0               0             
        Remote Paths:         0               0             
        Remote Path-elems:    0               0             

        Local Prefixes:       0               0             
        Local Paths:          0               0             

                              Number          Mem Used      
        Remote Prefixes:      0               0             
        Remote Paths:         0               0             
        Remote Path-elems:    0               0             
        Remote RDs:           0               0             

        Local Prefixes:       0               0             
        Local Paths:          0               0             
        Local RDs:            2               160           

        Total Prefixes:       0               0             
        Total Paths:          0               0             
        Total Path-elems:     0               0             
        Imported Paths:       0               0             
        Total RDs:            2               160           


        Address family: VPNv6 Unicast
        Dampening is not enabled
        Client reflection is enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 7
        Table version synced to RIB: 7
        Table version acked by RIB: 0
        RIB has not converged: version 0
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured

        State: Normal mode.
        BGP Table Version: 7
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
        Maximum supported label-stack depth:
           For IPv4 Nexthop: 0
           For IPv6 Nexthop: 0

                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  

        Label Thread       Jul  6 11:42:04.367   7           7           3         
                           Jul  6 11:42:01.373   5           6           9         
                           Jul  6 11:42:01.371   5           5           19        
                           Jul  6 11:42:01.367   0           5           4         
                           Total triggers: 4

        Import Thread      Jul  6 11:42:04.367   7           7           3         
                           Jul  6 11:42:01.373   5           6           9         
                           Jul  6 11:42:01.371   5           5           19        
                           Jul  6 11:42:01.367   0           5           19        
                           Total triggers: 4

        RIB Thread         Jul  6 11:42:01.373   5           7           4         
                           Jul  6 11:42:01.371   5           5           8         
                           Jul  6 11:42:01.367   1           5           8         
                           Jul  6 11:42:01.367   1           5           6         
                           Total triggers: 4

        Update Thread      Jul  6 11:42:04.367   7           7           8         
                           Jul  6 11:42:01.373   7           7           19        
                           Jul  6 11:42:01.373   5           7           8         
                           Jul  6 11:42:01.373   5           7           9         
                           Jul  6 11:42:01.371   5           5           8         
                           Jul  6 11:42:01.371   5           5           19        
                           Total triggers: 6

                              Allocated       Freed         
        Remote Prefixes:      0               0             
        Remote Paths:         0               0             
        Remote Path-elems:    0               0             

        Local Prefixes:       0               0             
        Local Paths:          0               0             

                              Number          Mem Used      
        Remote Prefixes:      0               0             
        Remote Paths:         0               0             
        Remote Path-elems:    0               0             
        Remote RDs:           0               0             

        Local Prefixes:       0               0             
        Local Paths:          0               0             
        Local RDs:            2               160           

        Total Prefixes:       0               0             
        Total Paths:          0               0             
        Total Path-elems:     0               0             
        Imported Paths:       0               0             
        Total RDs:            2               160           



        BGP instance 1: 'test'
        ======================
        % None of the requested address families are configured for instance 'test'(29193)

        BGP instance 2: 'test1'
        =======================
        % None of the requested address families are configured for instance 'test1'(29193)

        BGP instance 3: 'test2'
        =======================
        % None of the requested address families are configured for instance 'test2'(29193)
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowBgpInstanceProcessDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='all')
    
    def test_golden1(self):
        self.device = Mock(**self.golden_output1)
        obj = ShowBgpInstanceProcessDetail(device=self.device)
        parsed_output = obj.parse(vrf_type='all')
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output1)

    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowBgpInstanceProcessDetail(device=self.device)
        parsed_output = obj.parse(vrf_type='all')
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output2)


# ==============================================================
# Unit test for 'show bgp instance all all all neighbors detail'
# ==============================================================

class test_show_bgp_instance_all_all_all_neighbors_detail(unittest.TestCase):

    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        "instance": {
          "default": {
               "vrf": {
                    "default": {
                         "neighbor": {
                              "10.36.3.3": {
                                   "last_ka_start_before_reset": "00:00:00",
                                   "bgp_session_transport": {
                                        "connection": {
                                             "connections_established": 1,
                                             "connections_dropped": 0,
                                             "last_reset": "00:00:00",
                                             "state": "established"
                                        },
                                        "transport": {
                                             "if_handle": "0x00000000",
                                             "foreign_port": "179",
                                             "local_port": "54707",
                                             "foreign_host": "10.36.3.3",
                                             "local_host": "10.4.1.1"
                                        }
                                   },
                                   "inbound_message": "3",
                                   "second_last_write": "00:01:23",
                                   "outbound_message": "3",
                                   "precedence": "internet",
                                   "message_stats_output_queue": 0,
                                   "last_ka_start_before_second_last": "00:00:00",
                                   "last_write_thread_event_before_reset": "00:00:00",
                                   "tcp_initial_sync_done": "---",
                                   "keepalive_interval": 60,
                                   "nsr_state": "None",
                                   "tcp_initial_sync": "---",
                                   "last_ka_expiry_before_second_last": "00:00:00",
                                   "address_family": {
                                        "vpnv4 unicast": {
                                             "last_ack_version": 43,
                                             "prefix_suppressed": 0,
                                             "cummulative_no_prefixes_denied": 0,
                                             "filter_group": "0.2",
                                             "best_paths": 0,
                                             "neighbor_version": 43,
                                             "maximum_prefix_warning_only": True,
                                             "outstanding_version_objects_max": 1,
                                             "maximum_prefix_max_prefix_no": 2097152,
                                             "additional_paths_operation": "None",
                                             "last_synced_ack_version": 0,
                                             "update_group": "0.2",
                                             "exact_no_prefixes_denied": 0,
                                             "accepted_prefixes": 10,
                                             "eor_status": "was not received during read-only mode",
                                             "prefix_withdrawn": 0,
                                             "maximum_prefix_threshold": "75%",
                                             "route_refresh_request_received": 0,
                                             "outstanding_version_objects_current": 0,
                                             "maximum_prefix_restart": 0,
                                             "prefix_advertised": 5,
                                             "route_refresh_request_sent": 0,
                                             "send_multicast_attributes": True,
                                             "refresh_request_status": "No Refresh request being processed"
                                        },
                                        "vpnv6 unicast": {
                                             "last_ack_version": 43,
                                             "prefix_suppressed": 0,
                                             "cummulative_no_prefixes_denied": 0,
                                             "filter_group": "0.2",
                                             "best_paths": 0,
                                             "neighbor_version": 43,
                                             "maximum_prefix_warning_only": True,
                                             "outstanding_version_objects_max": 1,
                                             "maximum_prefix_max_prefix_no": 1048576,
                                             "additional_paths_operation": "None",
                                             "last_synced_ack_version": 0,
                                             "update_group": "0.2",
                                             "exact_no_prefixes_denied": 0,
                                             "accepted_prefixes": 10,
                                             "eor_status": "was not received during read-only mode",
                                             "prefix_withdrawn": 0,
                                             "maximum_prefix_threshold": "75%",
                                             "route_refresh_request_received": 0,
                                             "outstanding_version_objects_current": 0,
                                             "maximum_prefix_restart": 0,
                                             "prefix_advertised": 5,
                                             "route_refresh_request_sent": 0,
                                             "send_multicast_attributes": True,
                                             "refresh_request_status": "No Refresh request being processed"
                                        }
                                   },
                                   "last_write_pulse_rcvd": "Jun 28 19:03:52.763 ",
                                   "local_as_replace_as": False,
                                   "remote_as": 100,
                                   "minimum_time_between_adv_runs": 0,
                                   "last_write_before_reset": "00:00:00",
                                   "up_time": "00:39:07",
                                   "last_write_written": 0,
                                   "second_attempted": 19,
                                   "last_read_before_reset": "00:00:00",
                                   "router_id": "10.36.3.3",
                                   "link_state": "internal link",
                                   "local_as_no_prepend": False,
                                   "second_last_write_before_written": 0,
                                   "bgp_negotiated_capabilities": {
                                        "vpnv6_unicast": "advertised received",
                                        "vpnv4_unicast": "advertised received",
                                        "route_refresh": "advertised received",
                                        "four_octets_asn": "advertised received"
                                   },
                                   "attempted": 19,
                                   "written": 19,
                                   "last_write_attempted": 0,
                                   "holdtime": 180,
                                   "last_write": "00:00:23",
                                   "local_as_dual_as": False,
                                   "last_write_thread_event_second_last": "00:00:00",
                                   "non_stop_routing": True,
                                   "bgp_neighbor_counters": {
                                        "messages": {
                                             "received": {
                                                  "notifications": 0,
                                                  "updates": 6,
                                                  "keepalives": 41,
                                                  "opens": 1
                                             },
                                             "sent": {
                                                  "notifications": 0,
                                                  "updates": 4,
                                                  "keepalives": 40,
                                                  "opens": 1
                                             }
                                        }
                                   },
                                   "multiprotocol_capability": "received",
                                   "last_full_not_set_pulse_count": 88,
                                   "last_write_pulse_rcvd_before_reset": "00:00:00",
                                   "min_acceptable_hold_time": 3,
                                   "second_last_write_before_reset": "00:00:00",
                                   "second_last_write_before_attempted": 0,
                                   "last_read": "00:00:06",
                                   "local_as_as_no": 100,
                                   "last_ka_expiry_before_reset": "00:00:00",
                                   "last_ka_error_ka_not_sent": "00:00:00",
                                   "session_state": "established",
                                   "second_written": 19,
                                   "message_stats_input_queue": 0,
                                   "last_ka_error_before_reset": "00:00:00"
                              },
                              "10.16.2.2": {
                                   "last_ka_start_before_reset": "00:00:00",
                                   "bgp_session_transport": {
                                        "connection": {
                                             "connections_established": 1,
                                             "connections_dropped": 0,
                                             "last_reset": "00:00:00",
                                             "state": "established"
                                        },
                                        "transport": {
                                             "if_handle": "0x00000000",
                                             "foreign_port": "179",
                                             "local_port": "46663",
                                             "foreign_host": "10.16.2.2",
                                             "local_host": "10.4.1.1"
                                        }
                                   },
                                   "inbound_message": "3",
                                   "second_last_write": "00:01:23",
                                   "outbound_message": "3",
                                   "precedence": "internet",
                                   "message_stats_output_queue": 0,
                                   "last_ka_start_before_second_last": "00:00:00",
                                   "last_write_thread_event_before_reset": "00:00:00",
                                   "tcp_initial_sync_done": "---",
                                   "keepalive_interval": 60,
                                   "nsr_state": "None",
                                   "tcp_initial_sync": "---",
                                   "last_ka_expiry_before_second_last": "00:00:00",
                                   "address_family": {
                                        "vpnv4 unicast": {
                                             "last_ack_version": 43,
                                             "prefix_suppressed": 0,
                                             "cummulative_no_prefixes_denied": 0,
                                             "filter_group": "0.2",
                                             "best_paths": 10,
                                             "neighbor_version": 43,
                                             "maximum_prefix_warning_only": True,
                                             "outstanding_version_objects_max": 1,
                                             "maximum_prefix_max_prefix_no": 2097152,
                                             "additional_paths_operation": "None",
                                             "last_synced_ack_version": 0,
                                             "update_group": "0.2",
                                             "exact_no_prefixes_denied": 0,
                                             "accepted_prefixes": 10,
                                             "eor_status": "was received during read-only mode",
                                             "prefix_withdrawn": 0,
                                             "maximum_prefix_threshold": "75%",
                                             "route_refresh_request_received": 0,
                                             "outstanding_version_objects_current": 0,
                                             "maximum_prefix_restart": 0,
                                             "prefix_advertised": 5,
                                             "route_refresh_request_sent": 0,
                                             "send_multicast_attributes": True,
                                             "refresh_request_status": "No Refresh request being processed"
                                        },
                                        "vpnv6 unicast": {
                                             "last_ack_version": 43,
                                             "prefix_suppressed": 0,
                                             "cummulative_no_prefixes_denied": 0,
                                             "filter_group": "0.2",
                                             "best_paths": 10,
                                             "neighbor_version": 43,
                                             "maximum_prefix_warning_only": True,
                                             "outstanding_version_objects_max": 1,
                                             "maximum_prefix_max_prefix_no": 1048576,
                                             "additional_paths_operation": "None",
                                             "last_synced_ack_version": 0,
                                             "update_group": "0.2",
                                             "exact_no_prefixes_denied": 0,
                                             "accepted_prefixes": 10,
                                             "eor_status": "was received during read-only mode",
                                             "prefix_withdrawn": 0,
                                             "maximum_prefix_threshold": "75%",
                                             "route_refresh_request_received": 0,
                                             "outstanding_version_objects_current": 0,
                                             "maximum_prefix_restart": 0,
                                             "prefix_advertised": 5,
                                             "route_refresh_request_sent": 0,
                                             "send_multicast_attributes": True,
                                             "refresh_request_status": "No Refresh request being processed"
                                        }
                                   },
                                   "last_write_pulse_rcvd": "Jun 28 19:03:35.294 ",
                                   "local_as_replace_as": False,
                                   "remote_as": 100,
                                   "minimum_time_between_adv_runs": 0,
                                   "last_write_before_reset": "00:00:00",
                                   "up_time": "00:42:33",
                                   "last_write_written": 0,
                                   "second_attempted": 19,
                                   "last_read_before_reset": "00:00:00",
                                   "router_id": "10.16.2.2",
                                   "link_state": "internal link",
                                   "local_as_no_prepend": False,
                                   "second_last_write_before_written": 0,
                                   "bgp_negotiated_capabilities": {
                                        "vpnv6_unicast": "advertised received",
                                        "vpnv4_unicast": "advertised received",
                                        "route_refresh": "advertised received",
                                        "four_octets_asn": "advertised received"
                                   },
                                   "attempted": 19,
                                   "written": 19,
                                   "last_write_attempted": 0,
                                   "holdtime": 180,
                                   "last_write": "00:00:23",
                                   "local_as_dual_as": False,
                                   "last_write_thread_event_second_last": "00:00:00",
                                   "non_stop_routing": True,
                                   "bgp_neighbor_counters": {
                                        "messages": {
                                             "received": {
                                                  "notifications": 0,
                                                  "updates": 6,
                                                  "keepalives": 44,
                                                  "opens": 1
                                             },
                                             "sent": {
                                                  "notifications": 0,
                                                  "updates": 4,
                                                  "keepalives": 43,
                                                  "opens": 1
                                             }
                                        }
                                   },
                                   "multiprotocol_capability": "received",
                                   "last_full_not_set_pulse_count": 93,
                                   "last_write_pulse_rcvd_before_reset": "00:00:00",
                                   "min_acceptable_hold_time": 3,
                                   "second_last_write_before_reset": "00:00:00",
                                   "second_last_write_before_attempted": 0,
                                   "last_read": "00:00:32",
                                   "local_as_as_no": 100,
                                   "last_ka_expiry_before_reset": "00:00:00",
                                   "last_ka_error_ka_not_sent": "00:00:00",
                                   "session_state": "established",
                                   "second_written": 19,
                                   "message_stats_input_queue": 0,
                                   "last_ka_error_before_reset": "00:00:00"
                              }
                         }
                    }
               }
          }
     }

        }

    golden_output = {'execute.return_value': '''
           
        BGP instance 0: 'default'
        =========================

        BGP neighbor is 10.16.2.2
         Remote AS 100, local AS 100, internal link
         Remote router ID 10.16.2.2
          BGP state = Established, up for 00:42:33
          NSR State: None
          Last read 00:00:32, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:23, attempted 19, written 19
          Second last write 00:01:23, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Jun 28 19:03:35.294 last full not set pulse count 93
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Multi-protocol capability received
          Neighbor capabilities:            Adv         Rcvd
            Route refresh:                  Yes         Yes
            4-byte AS:                      Yes         Yes
            Address family VPNv4 Unicast:   Yes         Yes
            Address family VPNv6 Unicast:   Yes         Yes
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           Jun 28 18:21:24.198        1  Jun 28 18:21:24.208        1
            Notification:   ---                        0  ---                        0
            Update:         Jun 28 18:29:34.624        4  Jun 28 18:21:26.218        6
            Keepalive:      Jun 28 19:03:35.164       43  Jun 28 19:03:26.445       44
            Route_Refresh:  ---                        0  ---                        0
            Total:                                    48                            51
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: VPNv4 Unicast
          BGP neighbor version 43
          Update group: 0.2 Filter-group: 0.2  No Refresh request being processed
            Graceful Restart capability received
              Remote Restart time is 120 seconds
              Neighbor did not preserve the forwarding state during latest restart
          Route refresh request: received 0, sent 0
          10 accepted prefixes, 10 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 5, suppressed 0, withdrawn 0
          Maximum prefixes allowed 2097152
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 43, Last synced ack version 0
          Outstanding version objects: current 0, max 1
          Additional-paths operation: None
          Send Multicast Attributes

         For Address Family: VPNv6 Unicast
          BGP neighbor version 43
          Update group: 0.2 Filter-group: 0.2  No Refresh request being processed
            Graceful Restart capability received
              Remote Restart time is 120 seconds
              Neighbor did not preserve the forwarding state during latest restart
          Route refresh request: received 0, sent 0
          10 accepted prefixes, 10 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 5, suppressed 0, withdrawn 0
          Maximum prefixes allowed 1048576
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 43, Last synced ack version 0
          Outstanding version objects: current 0, max 1
          Additional-paths operation: None
          Send Multicast Attributes

          Connections established 1; dropped 0
          Local host: 10.4.1.1, Local port: 46663, IF Handle: 0x00000000
          Foreign host: 10.16.2.2, Foreign port: 179
          Last reset 00:00:00

        BGP neighbor is 10.36.3.3
         Remote AS 100, local AS 100, internal link
         Remote router ID 10.36.3.3
          BGP state = Established, up for 00:39:07
          NSR State: None
          Last read 00:00:06, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:23, attempted 19, written 19
          Second last write 00:01:23, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Jun 28 19:03:52.763 last full not set pulse count 88
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Multi-protocol capability received
          Neighbor capabilities:            Adv         Rcvd
            Route refresh:                  Yes         Yes
            4-byte AS:                      Yes         Yes
            Address family VPNv4 Unicast:   Yes         Yes
            Address family VPNv6 Unicast:   Yes         Yes
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           Jun 28 18:24:51.194        1  Jun 28 18:24:51.204        1
            Notification:   ---                        0  ---                        0
            Update:         Jun 28 18:29:34.624        4  Jun 28 18:24:52.664        6
            Keepalive:      Jun 28 19:03:35.164       40  Jun 28 19:03:52.763       41
            Route_Refresh:  ---                        0  ---                        0
            Total:                                    45                            48
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: VPNv4 Unicast
          BGP neighbor version 43
          Update group: 0.2 Filter-group: 0.2  No Refresh request being processed
            Graceful Restart capability received
              Remote Restart time is 120 seconds
              Neighbor did not preserve the forwarding state during latest restart
          Route refresh request: received 0, sent 0
          10 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 5, suppressed 0, withdrawn 0
          Maximum prefixes allowed 2097152
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was not received during read-only mode
          Last ack version 43, Last synced ack version 0
          Outstanding version objects: current 0, max 1
          Additional-paths operation: None
          Send Multicast Attributes

         For Address Family: VPNv6 Unicast
          BGP neighbor version 43
          Update group: 0.2 Filter-group: 0.2  No Refresh request being processed
            Graceful Restart capability received
              Remote Restart time is 120 seconds
              Neighbor did not preserve the forwarding state during latest restart
          Route refresh request: received 0, sent 0
          10 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 5, suppressed 0, withdrawn 0
          Maximum prefixes allowed 1048576
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was not received during read-only mode
          Last ack version 43, Last synced ack version 0
          Outstanding version objects: current 0, max 1
          Additional-paths operation: None
          Send Multicast Attributes

          Connections established 1; dropped 0
          Local host: 10.4.1.1, Local port: 54707, IF Handle: 0x00000000
          Foreign host: 10.36.3.3, Foreign port: 179
          Last reset 00:00:00
            '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        bgp_instance_neighbors_detail_obj = ShowBgpInstanceNeighborsDetail(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = bgp_instance_neighbors_detail_obj.parse(vrf_type='all')

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        bgp_instance_neighbors_detail_obj = ShowBgpInstanceNeighborsDetail(device=self.device)
        parsed_output = bgp_instance_neighbors_detail_obj.parse(vrf_type='all')
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output)


# ==============================================================
# Unit test for 'show bgp instance all vrf all neighbors detail'
# ==============================================================

class test_show_bgp_instance_all_vrf_all_neighbors_detail(unittest.TestCase):

    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        "instance": {
            "default": {
                "vrf": {
                    "VRF1": {
                        "neighbor": {
                            "2001:db8:1:5::5": {
                                "remove_private_as": False,
                                "shutdown": False,
                                "suppress_four_byte_as_capability": False,
                                "router_id": "10.1.5.1",
                                "local_as_as_no": 100,
                                "local_as_dual_as": False,
                                "local_as_no_prepend": False,
                                "local_as_replace_as": False,
                                "bgp_negotiated_capabilities": {
                                    "ipv6_unicast": "advertised received",
                                    "four_octets_asn": "advertised ",
                                    "route_refresh": "advertised "
                                },
                                "last_write_pulse_rcvd": "Jun 28 19:17:44.716 ",
                                "tcp_initial_sync": "---",
                                "last_full_not_set_pulse_count": 112,
                                "bgp_session_transport": {
                                    "connection": {
                                        "state": "established",
                                       "last_reset": "00:00:00",
                                        "connections_established": 1,
                                        "connections_dropped": 0
                                    },
                                    "transport": {
                                        "foreign_host": "2001:db8:1:5::5",
                                        "local_port": "179",
                                        "if_handle": "0x00000060",
                                        "local_host": "2001:db8:1:5::1",
                                        "foreign_port": "11014",
                                    }
                                },
                                "inbound_message": "3",
                                "keepalive_interval": 60,
                                "minimum_time_between_adv_runs": 0,
                                "last_write": "00:00:38",
                                "enforcing_first_as": "enabled",
                                "second_attempted": 19,
                                "last_ka_start_before_second_last": "00:00:00",
                                "message_stats_input_queue": 0,
                                "address_family": {
                                    "ipv6 unicast": {
                                        "outstanding_version_objects_current": 0,
                                        "outstanding_version_objects_max": 1,
                                        "cummulative_no_by_orf_policy": 0,
                                        "route_map_name_in": "all-pass",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 43,
                                        "best_paths": 0,
                                        "cummulative_no_prefixes_denied": 5,
                                        "maximum_prefix_max_prefix_no": 524288,
                                        "cummulative_no_no_policy": 5,
                                        "eor_status": "was not received during read-only mode",
                                        "maximum_prefix_warning_only": True,
                                        "cummulative_no_by_policy": 0,
                                        "refresh_request_status": "No Refresh request being processed",
                                        "maximum_prefix_restart": 0,
                                        "additional_routes_local_label": "Unicast SAFI",
                                        "route_refresh_request_received": 0,
                                        "maximum_prefix_threshold": "75%",
                                        "update_group": "0.2",
                                        "neighbor_version": 43,
                                        "filter_group": "0.2",
                                        "exact_no_prefixes_denied": 0,
                                        "prefix_advertised": 10,
                                        "additional_paths_operation": "None",
                                        "prefix_withdrawn": 0,
                                        "prefix_suppressed": 0,
                                        "route_refresh_request_sent": 0,
                                        "accepted_prefixes": 0,
                                        "cummulative_no_failed_rt_match": 0,
                                        "route_map_name_out": "all-pass"
                                    }
                                },
                                "second_last_write_before_written": 0,
                                "last_ka_error_ka_not_sent": "00:00:00",
                                "last_write_written": 0,
                                "written": 19,
                                "precedence": "internet",
                                "nsr_state": "None",
                                "second_last_write_before_attempted": 0,
                                "last_read_before_reset": "00:00:00",
                                "multiprotocol_capability": "received",
                                "second_written": 19,
                                "link_state": "external link",
                                "holdtime": 180,
                                "last_write_pulse_rcvd_before_reset": "00:00:00",
                                "last_ka_error_before_reset": "00:00:00",
                                "second_last_write": "00:01:38",
                                "non_stop_routing": True,
                                "attempted": 19,
                                "second_last_write_before_reset": "00:00:00",
                                "last_ka_expiry_before_second_last": "00:00:00",
                                "last_write_before_reset": "00:00:00",
                                "outbound_message": "3",
                                "last_write_attempted": 0,
                                "message_stats_output_queue": 0,
                                "remote_as": 200,
                                "last_write_thread_event_second_last": "00:00:00",
                                "last_write_thread_event_before_reset": "00:00:00",
                                "last_ka_start_before_reset": "00:00:00",
                                "min_acceptable_hold_time": 3,
                                "tcp_initial_sync_done": "---",
                                "last_read": "00:00:42",
                                "last_ka_expiry_before_reset": "00:00:00",
                                "session_state": "established",
                                "up_time": "00:53:45",
                                "bgp_neighbor_counters": {
                                    "messages": {
                                        "received": {
                                            "opens": 1,
                                            "keepalives": 54,
                                            "notifications": 0,
                                            "updates": 1,
                                        },
                                        "sent": {
                                            "opens": 1,
                                            "keepalives": 55,
                                            "notifications": 0,
                                            "updates": 3,
                                        }
                                    }
                                }
                            },
                            "10.1.5.5": {
                                "remove_private_as": False,
                                "shutdown": False,
                                "suppress_four_byte_as_capability": False,
                                "router_id": "10.1.5.5",
                                "local_as_as_no": 100,
                                "local_as_dual_as": False,
                                "local_as_no_prepend": False,
                                "local_as_replace_as": False,
                                "bgp_negotiated_capabilities": {
                                    "ipv4_unicast": "advertised received",
                                    "four_octets_asn": "advertised ",
                                    "route_refresh": "advertised "
                                },
                                "last_write_pulse_rcvd": "Jun 28 19:17:44.716 ",
                                "tcp_initial_sync": "---",
                                "last_full_not_set_pulse_count": 113,
                                "bgp_session_transport": {
                                    "connection": {
                                        "state": "established",
                                        "last_reset": "00:00:00",
                                        "connections_established": 1,
                                        "connections_dropped": 0
                                    },
                                    "transport": {
                                        "foreign_host": "10.1.5.5",
                                        "local_port": "179",
                                        "if_handle": "0x00000060",
                                        "local_host": "10.1.5.1",
                                        "foreign_port": "11052",
                                    }
                                },
                                "inbound_message": "3",
                                "keepalive_interval": 60,
                                "minimum_time_between_adv_runs": 0,
                                "last_write": "00:00:38",
                                "enforcing_first_as": "enabled",
                                "second_attempted": 19,
                                "last_ka_start_before_second_last": "00:00:00",
                                "message_stats_input_queue": 0,
                                "address_family": {
                                    "ipv4 unicast": {
                                        "outstanding_version_objects_current": 0,
                                        "outstanding_version_objects_max": 1,
                                        "cummulative_no_by_orf_policy": 0,
                                        "route_map_name_in": "all-pass",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 43,
                                        "best_paths": 0,
                                        "cummulative_no_prefixes_denied": 5,
                                        "maximum_prefix_max_prefix_no": 1048576,
                                        "cummulative_no_no_policy": 5,
                                        "eor_status": "was not received during read-only mode",
                                        "maximum_prefix_warning_only": True,
                                        "cummulative_no_by_policy": 0,
                                        "refresh_request_status": "No Refresh request being processed",
                                        "maximum_prefix_restart": 0,
                                        "additional_routes_local_label": "Unicast SAFI",
                                        "route_refresh_request_received": 0,
                                        "maximum_prefix_threshold": "75%",
                                        "update_group": "0.2",
                                        "neighbor_version": 43,
                                        "filter_group": "0.2",
                                        "exact_no_prefixes_denied": 0,
                                        "prefix_advertised": 10,
                                        "additional_paths_operation": "None",
                                        "prefix_withdrawn": 0,
                                        "prefix_suppressed": 0,
                                        "route_refresh_request_sent": 0,
                                        "accepted_prefixes": 0,
                                        "cummulative_no_failed_rt_match": 0,
                                        "route_map_name_out": "all-pass"
                                    }
                                },
                                "second_last_write_before_written": 0,
                                "last_ka_error_ka_not_sent": "00:00:00",
                                "last_write_written": 0,
                                "written": 19,
                                "precedence": "internet",
                                "nsr_state": "None",
                                "second_last_write_before_attempted": 0,
                                "last_read_before_reset": "00:00:00",
                                "multiprotocol_capability": "not received",
                                "second_written": 19,
                                "link_state": "external link",
                                "holdtime": 180,
                                "last_write_pulse_rcvd_before_reset": "00:00:00",
                                "last_ka_error_before_reset": "00:00:00",
                                "second_last_write": "00:01:38",
                                "non_stop_routing": True,
                                "attempted": 19,
                                "second_last_write_before_reset": "00:00:00",
                                "last_ka_expiry_before_second_last": "00:00:00",
                                "last_write_before_reset": "00:00:00",
                                "outbound_message": "3",
                                "last_write_attempted": 0,
                                "message_stats_output_queue": 0,
                                "remote_as": 200,
                                "last_write_thread_event_second_last": "00:00:00",
                                "last_write_thread_event_before_reset": "00:00:00",
                                "last_ka_start_before_reset": "00:00:00",
                                "min_acceptable_hold_time": 3,
                                "tcp_initial_sync_done": "---",
                                "last_read": "00:00:51",
                                "last_ka_expiry_before_reset": "00:00:00",
                                "session_state": "established",
                                "up_time": "00:53:54",
                                "bgp_neighbor_counters": {
                                    "messages": {
                                        "received": {
                                            "opens": 1,
                                            "keepalives": 54,
                                            "notifications": 0,
                                            "updates": 1,
                                        },
                                        "sent": {
                                            "opens": 1,
                                            "keepalives": 55,
                                            "notifications": 0,
                                            "updates": 2,
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "VRF2": {
                        "neighbor": {
                            "2001:db8:20:1:5::5": {
                                "remove_private_as": False,
                                "shutdown": False,
                                "suppress_four_byte_as_capability": False,
                                "router_id": "10.186.5.1",
                                "local_as_as_no": 100,
                                "local_as_dual_as": False,
                                "local_as_no_prepend": False,
                                "local_as_replace_as": False,
                                "bgp_negotiated_capabilities": {
                                    "ipv6_unicast": "advertised received",
                                    "four_octets_asn": "advertised ",
                                    "route_refresh": "advertised "
                                },
                                "last_write_pulse_rcvd": "Jun 28 19:17:40.237 ",
                                "tcp_initial_sync": "---",
                                "last_full_not_set_pulse_count": 102,
                                "bgp_session_transport": {
                                    "connection": {
                                        "state": "established",
                                        "last_reset": "00:00:00",
                                        "connections_established": 1,
                                        "connections_dropped": 0
                                    },
                                    "transport": {
                                        "foreign_host": "2001:db8:20:1:5::5",
                                        "local_port": "179",
                                        "if_handle": "0x00000080",
                                        "local_host": "2001:db8:20:1:5::1",
                                        "foreign_port": "11013",
                                    }
                                },
                                "inbound_message": "3",
                                "keepalive_interval": 60,
                                "minimum_time_between_adv_runs": 0,
                                "last_write": "00:00:43",
                                "enforcing_first_as": "enabled",
                                "second_attempted": 19,
                                "last_ka_start_before_second_last": "00:00:00",
                                "message_stats_input_queue": 0,
                                "address_family": {
                                    "ipv6 unicast": {
                                        "outstanding_version_objects_current": 0,
                                        "outstanding_version_objects_max": 1,
                                        "additional_routes_local_label": "Unicast SAFI",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 43,
                                        "best_paths": 5,
                                        "cummulative_no_prefixes_denied": 0,
                                        "maximum_prefix_max_prefix_no": 524288,
                                        "eor_status": "was not received during read-only mode",
                                        "maximum_prefix_warning_only": True,
                                        "additional_paths_operation": "None",
                                        "maximum_prefix_restart": 0,
                                        "route_map_name_in": "all-pass",
                                        "route_refresh_request_received": 0,
                                        "accepted_prefixes": 5,
                                        "update_group": "0.1",
                                        "neighbor_version": 43,
                                        "filter_group": "0.1",
                                        "exact_no_prefixes_denied": 0,
                                        "prefix_advertised": 10,
                                        "prefix_withdrawn": 0,
                                        "prefix_suppressed": 0,
                                        "route_refresh_request_sent": 0,
                                        "maximum_prefix_threshold": "75%",
                                        "route_map_name_out": "all-pass",
                                        "refresh_request_status": "No Refresh request being processed"
                                    }
                                },
                                "second_last_write_before_written": 0,
                                "last_ka_error_ka_not_sent": "00:00:00",
                                "last_write_written": 0,
                                "written": 19,
                                "precedence": "internet",
                                "nsr_state": "None",
                                "second_last_write_before_attempted": 0,
                                "last_read_before_reset": "00:00:00",
                                "multiprotocol_capability": "received",
                                "second_written": 19,
                                "link_state": "external link",
                                "holdtime": 180,
                                "last_write_pulse_rcvd_before_reset": "00:00:00",
                                "last_ka_error_before_reset": "00:00:00",
                                "second_last_write": "00:01:43",
                                "non_stop_routing": True,
                                "attempted": 19,
                                "second_last_write_before_reset": "00:00:00",
                                "last_ka_expiry_before_second_last": "00:00:00",
                                "last_write_before_reset": "00:00:00",
                                "outbound_message": "3",
                                "last_write_attempted": 0,
                                "message_stats_output_queue": 0,
                                "remote_as": 200,
                                "last_write_thread_event_second_last": "00:00:00",
                                "last_write_thread_event_before_reset": "00:00:00",
                                "last_ka_start_before_reset": "00:00:00",
                                "min_acceptable_hold_time": 3,
                                "tcp_initial_sync_done": "---",
                                "last_read": "00:00:46",
                                "last_ka_expiry_before_reset": "00:00:00",
                                "session_state": "established",
                                "up_time": "00:48:49",
                                "bgp_neighbor_counters": {
                                    "messages": {
                                        "received": {
                                            "opens": 1,
                                            "keepalives": 49,
                                            "notifications": 0,
                                            "updates": 1,
                                        },
                                        "sent": {
                                            "opens": 1,
                                            "keepalives": 49,
                                            "notifications": 0,
                                            "updates": 3,
                                        }
                                    }
                                }
                            },
                            "10.186.5.5": {
                                "remove_private_as": False,
                                "shutdown": False,
                                "suppress_four_byte_as_capability": False,
                                "router_id": "10.186.5.5",
                                "local_as_as_no": 100,
                                "local_as_dual_as": False,
                                "local_as_no_prepend": False,
                                "local_as_replace_as": False,
                                "bgp_negotiated_capabilities": {
                                    "ipv4_unicast": "advertised received",
                                    "four_octets_asn": "advertised ",
                                    "route_refresh": "advertised "
                                },
                                "last_write_pulse_rcvd": "Jun 28 19:17:40.237 ",
                                "tcp_initial_sync": "---",
                                "last_full_not_set_pulse_count": 102,
                                "bgp_session_transport": {
                                    "connection": {
                                        "state": "established",
                                        "last_reset": "00:00:00",
                                        "connections_established": 1,
                                        "connections_dropped": 0
                                    },
                                    "transport": {
                                        "foreign_host": "10.186.5.5",
                                        "local_port": "179",
                                        "if_handle": "0x00000080",
                                        "local_host": "10.186.5.1",
                                        "foreign_port": "11099",
                                    }
                                },
                                "inbound_message": "3",
                                "keepalive_interval": 60,
                                "minimum_time_between_adv_runs": 0,
                                "last_write": "00:00:43",
                                "enforcing_first_as": "enabled",
                                "second_attempted": 19,
                                "last_ka_start_before_second_last": "00:00:00",
                                "message_stats_input_queue": 0,
                                "address_family": {
                                    "ipv4 unicast": {
                                        "outstanding_version_objects_current": 0,
                                        "outstanding_version_objects_max": 1,
                                        "additional_routes_local_label": "Unicast SAFI",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 43,
                                        "best_paths": 5,
                                        "cummulative_no_prefixes_denied": 0,
                                        "maximum_prefix_max_prefix_no": 495,
                                        "eor_status": "was not received during read-only mode",
                                        "maximum_prefix_warning_only": True,
                                        "additional_paths_operation": "None",
                                        "maximum_prefix_restart": 0,
                                        "route_map_name_in": "all-pass",
                                        "route_refresh_request_received": 0,
                                        "accepted_prefixes": 5,
                                        "update_group": "0.1",
                                        "neighbor_version": 43,
                                        "filter_group": "0.1",
                                        "exact_no_prefixes_denied": 0,
                                        "prefix_advertised": 10,
                                        "prefix_withdrawn": 0,
                                        "prefix_suppressed": 0,
                                        "route_refresh_request_sent": 0,
                                        "maximum_prefix_threshold": "75%",
                                        "route_map_name_out": "all-pass",
                                        "refresh_request_status": "No Refresh request being processed"
                                    }
                                },
                                "second_last_write_before_written": 0,
                                "last_ka_error_ka_not_sent": "00:00:00",
                                "last_write_written": 0,
                                "written": 19,
                                "precedence": "internet",
                                "nsr_state": "None",
                                "second_last_write_before_attempted": 0,
                                "last_read_before_reset": "00:00:00",
                                "multiprotocol_capability": "not received",
                                "second_written": 19,
                                "link_state": "external link",
                                "holdtime": 180,
                                "last_write_pulse_rcvd_before_reset": "00:00:00",
                                "last_ka_error_before_reset": "00:00:00",
                                "second_last_write": "00:01:43",
                                "non_stop_routing": True,
                                "attempted": 19,
                                "second_last_write_before_reset": "00:00:00",
                                "last_ka_expiry_before_second_last": "00:00:00",
                                "last_write_before_reset": "00:00:00",
                                "outbound_message": "3",
                                "last_write_attempted": 0,
                                "message_stats_output_queue": 0,
                                "remote_as": 200,
                                "last_write_thread_event_second_last": "00:00:00",
                                "last_write_thread_event_before_reset": "00:00:00",
                                "last_ka_start_before_reset": "00:00:00",
                                "min_acceptable_hold_time": 3,
                                "tcp_initial_sync_done": "---",
                                "last_read": "00:00:51",
                                "last_ka_expiry_before_reset": "00:00:00",
                                "session_state": "established",
                                "up_time": "00:48:54",
                                "bgp_neighbor_counters": {
                                    "messages": {
                                         "received": {
                                              "opens": 1,
                                              "keepalives": 49,
                                              "notifications": 0,
                                              "updates": 1,
                                         },
                                         "sent": {
                                              "opens": 1,
                                              "keepalives": 50,
                                              "notifications": 0,
                                              "updates": 2}}}}}}}}}}

    golden_output = {'execute.return_value': '''
        Wed Jun 28 19:18:23.304 UTC

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        BGP neighbor is 10.1.5.5, vrf VRF1
         Remote AS 200, local AS 100, external link
         Remote router ID 10.1.5.5
          BGP state = Established, up for 00:53:54
          NSR State: None
          Last read 00:00:51, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:38, attempted 19, written 19
          Second last write 00:01:38, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Jun 28 19:17:44.716 last full not set pulse count 113
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability not received
          Neighbor capabilities:            Adv         Rcvd
            Route refresh:                  Yes         No
            4-byte AS:                      Yes         No
            Address family IPv4 Unicast:    Yes         Yes
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           Jun 28 18:24:28.875        1  Jun 28 18:24:28.875        1
            Notification:   ---                        0  ---                        0
            Update:         Jun 28 18:28:43.838        2  Jun 28 18:24:29.135        1
            Keepalive:      Jun 28 19:17:44.616       55  Jun 28 19:17:31.987       54
            Route_Refresh:  ---                        0  ---                        0
            Total:                                    58                            56
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: IPv4 Unicast
          BGP neighbor version 43
          Update group: 0.2 Filter-group: 0.2  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 5. 
            No policy: 5, Failed RT match: 0
            By ORF policy: 0, By policy: 0
          Prefix advertised 10, suppressed 0, withdrawn 0
          Maximum prefixes allowed 1048576
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 43, Last synced ack version 0
          Outstanding version objects: current 0, max 1
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI

          Connections established 1; dropped 0
          Local host: 10.1.5.1, Local port: 179, IF Handle: 0x00000060
          Foreign host: 10.1.5.5, Foreign port: 11052
          Last reset 00:00:00

        BGP neighbor is 2001:db8:1:5::5, vrf VRF1
         Remote AS 200, local AS 100, external link
         Remote router ID 10.1.5.1
          BGP state = Established, up for 00:53:45
          NSR State: None
          Last read 00:00:42, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:38, attempted 19, written 19
          Second last write 00:01:38, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Jun 28 19:17:44.716 last full not set pulse count 112
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability received
          Neighbor capabilities:            Adv         Rcvd
            Route refresh:                  Yes         No
            4-byte AS:                      Yes         No
            Address family IPv6 Unicast:    Yes         Yes
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           Jun 28 18:24:37.875        1  Jun 28 18:24:37.875        1
            Notification:   ---                        0  ---                        0
            Update:         Jun 28 18:28:43.838        3  Jun 28 18:24:38.135        1
            Keepalive:      Jun 28 19:17:44.616       55  Jun 28 19:17:41.026       54
            Route_Refresh:  ---                        0  ---                        0
            Total:                                    59                            56
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: IPv6 Unicast
          BGP neighbor version 43
          Update group: 0.2 Filter-group: 0.2  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 5. 
            No policy: 5, Failed RT match: 0
            By ORF policy: 0, By policy: 0
          Prefix advertised 10, suppressed 0, withdrawn 0
          Maximum prefixes allowed 524288
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 43, Last synced ack version 0
          Outstanding version objects: current 0, max 1
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI

          Connections established 1; dropped 0
          Local host: 2001:db8:1:5::1, Local port: 179, IF Handle: 0x00000060
          Foreign host: 2001:db8:1:5::5, Foreign port: 11014
          Last reset 00:00:00

        VRF: VRF2
        ---------

        BGP neighbor is 10.186.5.5, vrf VRF2
         Remote AS 200, local AS 100, external link
         Remote router ID 10.186.5.5
          BGP state = Established, up for 00:48:54
          NSR State: None
          Last read 00:00:51, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:43, attempted 19, written 19
          Second last write 00:01:43, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Jun 28 19:17:40.237 last full not set pulse count 102
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability not received
          Neighbor capabilities:            Adv         Rcvd
            Route refresh:                  Yes         No
            4-byte AS:                      Yes         No
            Address family IPv4 Unicast:    Yes         Yes
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           Jun 28 18:29:29.345        1  Jun 28 18:29:29.345        1
            Notification:   ---                        0  ---                        0
            Update:         Jun 28 18:29:39.374        2  Jun 28 18:29:29.595        1
            Keepalive:      Jun 28 19:17:40.137       50  Jun 28 19:17:31.987       49
            Route_Refresh:  ---                        0  ---                        0
            Total:                                    53                            51
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: IPv4 Unicast
          BGP neighbor version 43
          Update group: 0.1 Filter-group: 0.1  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          5 accepted prefixes, 5 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 10, suppressed 0, withdrawn 0
          Maximum prefixes allowed 495
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 43, Last synced ack version 0
          Outstanding version objects: current 0, max 1
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI

          Connections established 1; dropped 0
          Local host: 10.186.5.1, Local port: 179, IF Handle: 0x00000080
          Foreign host: 10.186.5.5, Foreign port: 11099
          Last reset 00:00:00

        BGP neighbor is 2001:db8:20:1:5::5, vrf VRF2
         Remote AS 200, local AS 100, external link
         Remote router ID 10.186.5.1
          BGP state = Established, up for 00:48:49
          NSR State: None
          Last read 00:00:46, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:43, attempted 19, written 19
          Second last write 00:01:43, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Jun 28 19:17:40.237 last full not set pulse count 102
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability received
          Neighbor capabilities:            Adv         Rcvd
            Route refresh:                  Yes         No
            4-byte AS:                      Yes         No
            Address family IPv6 Unicast:    Yes         Yes
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           Jun 28 18:29:34.344        1  Jun 28 18:29:34.344        1
            Notification:   ---                        0  ---                        0
            Update:         Jun 28 18:29:39.374        3  Jun 28 18:29:34.604        1
            Keepalive:      Jun 28 19:17:40.137       49  Jun 28 19:17:37.007       49
            Route_Refresh:  ---                        0  ---                        0
            Total:                                    53                            51
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: IPv6 Unicast
          BGP neighbor version 43
          Update group: 0.1 Filter-group: 0.1  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          5 accepted prefixes, 5 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 10, suppressed 0, withdrawn 0
          Maximum prefixes allowed 524288
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 43, Last synced ack version 0
          Outstanding version objects: current 0, max 1
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI

          Connections established 1; dropped 0
          Local host: 2001:db8:20:1:5::1, Local port: 179, IF Handle: 0x00000080
          Foreign host: 2001:db8:20:1:5::5, Foreign port: 11013
          Last reset 00:00:00
        '''}

    golden_parsed_output2 = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'VRF1': 
                        {'neighbor': 
                            {'2001:db8:1:5::5': 
                                {'address_family': 
                                    {'ipv6 unicast': 
                                        {'accepted_prefixes': 0,
                                        'additional_paths_operation': 'None',
                                        'additional_routes_local_label': 'Unicast '
                                                                      'SAFI',
                                        'best_paths': 0,
                                        'cummulative_no_prefixes_denied': 0,
                                        'eor_status': 'was '
                                                   'not '
                                                   'received '
                                                   'during '
                                                   'read-only '
                                                   'mode',
                                        'exact_no_prefixes_denied': 0,
                                        'filter_group': '0.0',
                                        'last_ack_version': 1,
                                        'last_synced_ack_version': 0,
                                        'maximum_prefix_max_prefix_no': 524288,
                                        'maximum_prefix_restart': 0,
                                        'maximum_prefix_threshold': '75%',
                                        'maximum_prefix_warning_only': True,
                                        'neighbor_version': 0,
                                        'outstanding_version_objects_current': 0,
                                        'outstanding_version_objects_max': 0,
                                        'prefix_advertised': 0,
                                        'prefix_suppressed': 0,
                                        'prefix_withdrawn': 0,
                                        'refresh_request_status': 'No '
                                                               'Refresh '
                                                               'request '
                                                               'being '
                                                               'processed',
                                        'route_map_name_in': 'all-pass',
                                        'route_map_name_out': 'all-pass',
                                        'route_refresh_request_received': 0,
                                        'route_refresh_request_sent': 0,
                                        'update_group': '0.1'}},
                                'attempted': 0,
                                'remove_private_as': False,
                                'shutdown': False,
                                'suppress_four_byte_as_capability': False,
                                'bgp_neighbor_counters': {'messages': {'received': {'keepalives': 0,
                                                                                    'notifications': 0,
                                                                                    'opens': 0,
                                                                                    'updates': 0},
                                                                       'sent': {'keepalives': 0,
                                                                                'notifications': 0,
                                                                                'opens': 0,
                                                                                'updates': 0}}},
                                'bgp_session_transport': {'connection': {'connections_dropped': 0,
                                                                         'connections_established': 0,
                                                                         'last_reset': '00:00:00',
                                                                         'state': 'established'},
                                                          'transport': {'foreign_host': '2001:db8:1:5::5',
                                                                        'foreign_port': '0',
                                                                        'if_handle': '0x00000000',
                                                                        'local_host': '::',
                                                                        'local_port': '0'}},
                                'holdtime': 180,
                                'enforcing_first_as': 'enabled',
                                'inbound_message': '3',
                                'keepalive_interval': 60,
                                'last_full_not_set_pulse_count': 0,
                                'last_ka_error_before_reset': '00:00:00',
                                'last_ka_error_ka_not_sent': '00:00:00',
                                'last_ka_expiry_before_reset': '00:00:00',
                                'last_ka_expiry_before_second_last': '00:00:00',
                                'last_ka_start_before_reset': '00:00:00',
                                'last_ka_start_before_second_last': '00:00:00',
                                'last_read': '00:00:00',
                                'last_read_before_reset': '00:00:00',
                                'last_write': '00:00:00',
                                'last_write_attempted': 0,
                                'last_write_before_reset': '00:00:00',
                                'last_write_pulse_rcvd': 'not '
                                                         'set ',
                                'last_write_pulse_rcvd_before_reset': '00:00:00',
                                'last_write_thread_event_before_reset': '00:00:00',
                                'last_write_thread_event_second_last': '00:00:00',
                                'last_write_written': 0,
                                'link_state': 'external '
                                              'link',
                                'local_as_as_no': 100,
                                'local_as_dual_as': False,
                                'local_as_no_prepend': False,
                                'local_as_replace_as': False,
                                'message_stats_input_queue': 0,
                                'message_stats_output_queue': 0,
                                'min_acceptable_hold_time': 3,
                                'minimum_time_between_adv_runs': 0,
                                'multiprotocol_capability': 'not '
                                                            'received',
                                'non_stop_routing': True,
                                'nsr_state': 'None',
                                'outbound_message': '3',
                                'precedence': 'internet',
                                'remote_as': 200,
                                'router_id': '0.0.0.0',
                                'second_attempted': 0,
                                'second_last_write': '00:00:00',
                                'second_last_write_before_attempted': 0,
                                'second_last_write_before_reset': '00:00:00',
                                'second_last_write_before_written': 0,
                                'second_written': 0,
                                'session_state': 'idle',
                                'session_state_reason': ' '
                                                        '(No '
                                                        'best '
                                                        'local '
                                                        'address '
                                                        'found)',
                                'tcp_initial_sync': '---',
                                'tcp_initial_sync_done': '---',
                                'written': 0}}},
            'VRF2': 
                {'neighbor': 
                    {'2001:db8:20:1:5::5': 
                        {'address_family': 
                            {'ipv6 unicast': 
                                {'accepted_prefixes': 0,
                                'additional_paths_operation': 'None',
                                'additional_routes_local_label': 'Unicast '
                                                                 'SAFI',
                                'best_paths': 0,
                                'cummulative_no_prefixes_denied': 0,
                                'eor_status': 'was '
                                              'not '
                                              'received '
                                              'during '
                                              'read-only '
                                              'mode',
                                'exact_no_prefixes_denied': 0,
                                'filter_group': '0.0',
                                'last_ack_version': 1,
                                'last_synced_ack_version': 0,
                                'maximum_prefix_max_prefix_no': 524288,
                                'maximum_prefix_restart': 0,
                                'maximum_prefix_threshold': '75%',
                                'maximum_prefix_warning_only': True,
                                'neighbor_version': 0,
                                'outstanding_version_objects_current': 0,
                                'outstanding_version_objects_max': 0,
                                'prefix_advertised': 0,
                                'prefix_suppressed': 0,
                                'prefix_withdrawn': 0,
                                'refresh_request_status': 'No '
                                                          'Refresh '
                                                          'request '
                                                          'being '
                                                          'processed',
                                'route_map_name_in': 'all-pass',
                                'route_map_name_out': 'all-pass',
                                'route_refresh_request_received': 0,
                                'route_refresh_request_sent': 0,
                                'update_group': '0.1'}},
                        'remove_private_as': False,
                        'shutdown': False,
                        'suppress_four_byte_as_capability': False,
                        'attempted': 0,
                        'bgp_neighbor_counters': {'messages': {'received': {'keepalives': 0,
                                                                           'notifications': 0,
                                                                           'opens': 0,
                                                                           'updates': 0},
                                                              'sent': {'keepalives': 0,
                                                                       'notifications': 0,
                                                                       'opens': 0,
                                                                       'updates': 0}}},
                        'bgp_session_transport': {'connection': {'connections_dropped': 0,
                                                                'connections_established': 0,
                                                                'last_reset': '00:00:00',
                                                                'state': 'established'},
                                                 'transport': {'foreign_host': '2001:db8:20:1:5::5',
                                                               'foreign_port': '0',
                                                               'if_handle': '0x00000000',
                                                               'local_host': '::',
                                                               'local_port': '0'}},
                        'holdtime': 180,
                        'enforcing_first_as': 'enabled',
                        'inbound_message': '3',
                        'keepalive_interval': 60,
                        'last_full_not_set_pulse_count': 0,
                        'last_ka_error_before_reset': '00:00:00',
                        'last_ka_error_ka_not_sent': '00:00:00',
                        'last_ka_expiry_before_reset': '00:00:00',
                        'last_ka_expiry_before_second_last': '00:00:00',
                        'last_ka_start_before_reset': '00:00:00',
                        'last_ka_start_before_second_last': '00:00:00',
                        'last_read': '00:00:00',
                        'last_read_before_reset': '00:00:00',
                        'last_write': '00:00:00',
                        'last_write_attempted': 0,
                        'last_write_before_reset': '00:00:00',
                        'last_write_pulse_rcvd': 'not '
                                                'set ',
                        'last_write_pulse_rcvd_before_reset': '00:00:00',
                        'last_write_thread_event_before_reset': '00:00:00',
                        'last_write_thread_event_second_last': '00:00:00',
                        'last_write_written': 0,
                        'link_state': 'external '
                                     'link',
                        'local_as_as_no': 100,
                        'local_as_dual_as': False,
                        'local_as_no_prepend': False,
                        'local_as_replace_as': False,
                        'message_stats_input_queue': 0,
                        'message_stats_output_queue': 0,
                        'min_acceptable_hold_time': 3,
                        'minimum_time_between_adv_runs': 0,
                        'multiprotocol_capability': 'not '
                                                   'received',
                        'non_stop_routing': True,
                        'nsr_state': 'None',
                        'outbound_message': '3',
                        'precedence': 'internet',
                        'remote_as': 200,
                        'router_id': '0.0.0.0',
                        'second_attempted': 0,
                        'second_last_write': '00:00:00',
                        'second_last_write_before_attempted': 0,
                        'second_last_write_before_reset': '00:00:00',
                        'second_last_write_before_written': 0,
                        'second_written': 0,
                        'session_state': 'idle',
                        'session_state_reason': ' '
                                               '(No '
                                               'best '
                                               'local '
                                               'address '
                                               'found)',
                        'tcp_initial_sync': '---',
                        'tcp_initial_sync_done': '---',
                        'written': 0}}}}},
            'test': {},
            'test1': {},
            'test2': {}}}

    golden_output2 = {'execute.return_value': '''
        RP/0/RSP1/CPU0:PE1#show bgp instance all vrf all ipv6 unicast neighbors detail 
        Fri Aug 11 13:15:07.809 PDT

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        BGP neighbor is 2001:db8:1:5::5, vrf VRF1
         Remote AS 200, local AS 100, external link
         Remote router ID 0.0.0.0
          BGP state = Idle (No best local address found)
          NSR State: None
          Last read 00:00:00, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:00, attempted 0, written 0
          Second last write 00:00:00, attempted 0, written 0
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  not set last full not set pulse count 0
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, not armed for read, not armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability not received
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           ---                        0  ---                        0
            Notification:   ---                        0  ---                        0
            Update:         ---                        0  ---                        0
            Keepalive:      ---                        0  ---                        0
            Route_Refresh:  ---                        0  ---                        0
            Total:                                     0                             0
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: IPv6 Unicast
          BGP neighbor version 0
          Update group: 0.1 Filter-group: 0.0  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 0, suppressed 0, withdrawn 0
          Maximum prefixes allowed 524288
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 1, Last synced ack version 0
          Outstanding version objects: current 0, max 0
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI
                  
          Connections established 0; dropped 0
          Local host: ::, Local port: 0, IF Handle: 0x00000000
          Foreign host: 2001:db8:1:5::5, Foreign port: 0
          Last reset 00:00:00
          External BGP neighbor not directly connected.
                  
        VRF: VRF2 
        --------- 
                  
        BGP neighbor is 2001:db8:20:1:5::5, vrf VRF2
         Remote AS 200, local AS 100, external link
         Remote router ID 0.0.0.0
          BGP state = Idle (No best local address found)
          NSR State: None
          Last read 00:00:00, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:00, attempted 0, written 0
          Second last write 00:00:00, attempted 0, written 0
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  not set last full not set pulse count 0
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, not armed for read, not armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability not received
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           ---                        0  ---                        0
            Notification:   ---                        0  ---                        0
            Update:         ---                        0  ---                        0
            Keepalive:      ---                        0  ---                        0
            Route_Refresh:  ---                        0  ---                        0
            Total:                                     0                             0
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered
                  
         For Address Family: IPv6 Unicast
          BGP neighbor version 0
          Update group: 0.1 Filter-group: 0.0  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 0, suppressed 0, withdrawn 0
          Maximum prefixes allowed 524288
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 1, Last synced ack version 0
          Outstanding version objects: current 0, max 0
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI
                  
          Connections established 0; dropped 0
          Local host: ::, Local port: 0, IF Handle: 0x00000000
          Foreign host: 2001:db8:20:1:5::5, Foreign port: 0
          Last reset 00:00:00
          External BGP neighbor not directly connected.
                  
        BGP instance 1: 'test'
        ======================
                  
        BGP instance 2: 'test1'
        =======================
                  
        BGP instance 3: 'test2'
        =======================
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceNeighborsDetail(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='vrf')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstanceNeighborsDetail(device=self.device)
        parsed_output = obj.parse(vrf_type='vrf')
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowBgpInstanceNeighborsDetail(device=self.device)
        parsed_output = obj.parse(vrf_type='vrf', address_family='ipv6 unicast')
        self.assertEqual(parsed_output,self.golden_parsed_output2)


# ================================================================================
# Unit test for 'show bgp instance all vrf all neighbors <WORD> advertised-routes'
# ================================================================================

class test_show_bgp_instance_all_vrf_all_neighbors_advertised_routes(unittest.TestCase):
        
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}
    golden_parsed_output =  {
        'instance': 
            {'default': 
                {'vrf': 
                    {'VRF1': {},
                    'VRF2': 
                        {'address_family': 
                            {'vpnv4 unicast RD 200:2': 
                                {'advertised': 
                                    {'10.169.1.0/24': 
                                        {'index': 
                                            {1: 
                                                {'froms': '10.16.2.2',
                                                'next_hop': '10.186.5.1',
                                                'origin_code': 'e',
                                                'path': '100 '
                                                        '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}'}}},
                                    '10.169.4.0/24': 
                                        {'index': 
                                            {1: 
                                                {'froms': '10.16.2.2',
                                                'next_hop': '10.186.5.1',
                                                'origin_code': 'e',
                                                'path': '100 '
                                                        '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}'}}},
                                    '10.169.5.0/24': 
                                        {'index': 
                                            {1: 
                                                {'froms': '10.16.2.2',
                                                'next_hop': '10.186.5.1',
                                                'origin_code': 'e',
                                                'path': '100 '
                                                        '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}'}}},
                                    '10.9.2.0/24': 
                                        {'index': 
                                            {1: 
                                                {'froms': '10.16.2.2',
                                                'next_hop': '10.186.5.1',
                                                'origin_code': 'e',
                                                'path': '100 '
                                                        '400 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}'}}}},
                                'default_vrf': 'VRF2',
                                'processed_paths': '4',
                                'processed_prefixes': '4',
                                'route_distinguisher': '200:2'}}}}}}}

    golden_output = {'execute.return_value': '''

        Neighbor not found

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        VRF: VRF2
        ---------
        Network            Next Hop        From            AS Path
        Route Distinguisher: 200:2 (default for vrf VRF2)
        10.169.1.0/24        10.186.5.1        10.16.2.2         100 300 33299 51178 47751 {27016}e
        10.169.4.0/24        10.186.5.1        10.16.2.2         100 300 33299 51178 47751 {27016}e
        10.169.5.0/24        10.186.5.1        10.16.2.2         100 300 33299 51178 47751 {27016}e
        10.9.2.0/24        10.186.5.1        10.16.2.2         100 400 33299 51178 47751 {27016}e

        Processed 4 prefixes, 4 paths
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceNeighborsAdvertisedRoutes(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='vrf', neighbor='10.186.5.5')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstanceNeighborsAdvertisedRoutes(device=self.device)
        parsed_output = obj.parse(vrf_type='vrf', neighbor='10.186.5.5')
        self.assertEqual(parsed_output,self.golden_parsed_output)


# ================================================================================
# Unit test for 'show bgp instance all all all neighbors <WORD> advertised-routes'
# ================================================================================

class test_show_bgp_instance_all_all_all_neighbors_advertised_routes(unittest.TestCase):
        
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output =  {
        'instance': 
            {'default': 
                {'vrf': 
                    {'default': 
                        {'address_family': 
                            {'vpnv4 unicast RD 200:2': 
                                {'advertised': 
                                    {'10.1.1.0/24': 
                                        {'index': 
                                            {1: 
                                                {'froms': '10.186.5.5',
                                                'next_hop': '10.4.1.1',
                                                'origin_code': 'e',
                                                'path': '200 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}'}}},
                                    '10.1.2.0/24': 
                                        {'index': 
                                            {1: 
                                                {'froms': '10.186.5.5',
                                                'next_hop': '10.4.1.1',
                                                'origin_code': 'e',
                                                'path': '200 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}'}}}},
                                'default_vrf': 'default',
                                'processed_paths': '2',
                                'processed_prefixes': '2',
                                'route_distinguisher': '200:2'},
                            'vpnv6 unicast RD 200:2': 
                                {'advertised': 
                                    {'615:11:11:1::/64': 
                                        {'index': 
                                            {1: 
                                                {'froms': '2001:db8:20:1:5::5',
                                                'next_hop': '10.4.1.1',
                                                'origin_code': 'e',
                                                'path': '200 '
                                                '33299 '
                                                '51178 '
                                                '47751 '
                                                '{27016}'}}},
                                    '615:11:11::/64': 
                                        {'index': 
                                            {1: 
                                                {'froms': '2001:db8:20:1:5::5',
                                                'next_hop': '10.4.1.1',
                                                'origin_code': 'e',
                                                'path': '200 '
                                                '33299 '
                                                '51178 '
                                                '47751 '
                                                '{27017}'}}}},
                                'default_vrf': 'default',
                                'processed_paths': '2',
                                'processed_prefixes': '2',
                                'route_distinguisher': '200:2'}}}}}}}

    golden_output = {'execute.return_value': '''

        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        Network            Next Hop        From            AS  Path
        Route Distinguisher: 200:2
        10.1.1.0/24        10.4.1.1         10.186.5.5        200 33299 51178 47751 {27016}e
        10.1.2.0/24        10.4.1.1         10.186.5.5        200 33299 51178 47751 {27016}e

        Processed 2 prefixes, 2 paths

        Address Family: VPNv6 Unicast
        -----------------------------

        Network            Next Hop        From            AS  Path
        Route Distinguisher: 200:2
        615:11:11::/64     10.4.1.1         2001:db8:20:1:5::5
                                                           200 33299 51178 47751 {27017}e
        615:11:11:1::/64   10.4.1.1         2001:db8:20:1:5::5
                                                           200 33299 51178 47751 {27016}e

        Processed 2 prefixes, 2 paths
        '''}
    
    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceNeighborsAdvertisedRoutes(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='all', neighbor='10.36.3.3')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstanceNeighborsAdvertisedRoutes(device=self.device)
        parsed_output = obj.parse(vrf_type='all', neighbor='10.36.3.3')
        self.assertEqual(parsed_output,self.golden_parsed_output)


# ==============================================================================
# Unit test for 'show bgp instance all vrf all neighbors <WORD> received routes'
# ==============================================================================

class test_show_bgp_instance_all_vrf_all_neighbors_received_routes(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'VRF2': 
                        {'address_family': 
                            {'vpnv4 unicast RD 200:2': 
                                {'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'processed_paths': 2,
                                'processed_prefixes': 2,
                                'rd_version': 63,
                                'received': 
                                    {'10.1.1.0/24': 
                                        {'index': 
                                            {1: 
                                                {'metric': '2219',
                                                'next_hop': '10.186.5.5',
                                                'origin_codes': 'e',
                                                'path': '200 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*',
                                                'weight': '0'}}},
                                    '10.1.2.0/24': 
                                        {'index': 
                                            {1: 
                                                {'metric': '2219',
                                                'next_hop': '10.186.5.5',
                                                'origin_codes': 'e',
                                                'path': '200 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*',
                                                'weight': '0'}}}},
                                'route_distinguisher': '200:2',
                                'router_identifier': '10.229.11.11',
                                'state': 'active',
                                'table_id': '0xe0000011',
                                'table_state': 'active',
                                'routing_table_version': 63,
                                'vrf_id': '0x60000002'}}}}}}}
  
    golden_output = {'execute.return_value': '''

        % Neighbor not found

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        VRF: VRF2
        ---------
        BGP VRF VRF2, state: Active
        BGP Route Distinguisher: 200:2
        VRF ID: 0x60000002
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000011   RD version: 63
        BGP main routing table version 63
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:2 (default for vrf VRF2)
        *  10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *  10.1.2.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e

        Processed 2 prefixes, 2 paths
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceNeighborsReceivedRoutes(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='vrf', neighbor='10.186.5.5')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstanceNeighborsReceivedRoutes(device=self.device)
        parsed_output = obj.parse(vrf_type='vrf', neighbor='10.186.5.5')
        self.assertEqual(parsed_output,self.golden_parsed_output)


# ==============================================================================
# Unit test for 'show bgp instance all all all neighbors <WORD> received routes'
# ==============================================================================

class test_show_bgp_instance_all_all_all_neighbors_received_routes(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'default': 
                        {'address_family': 
                            {'vpnv4 unicast RD 300:1': 
                                {'generic_scan_interval': 60,
                                'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'rd_version': 0,
                                'received': 
                                    {'10.169.1.0/24': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}}},
                                'router_identifier': '10.4.1.1',
                                'scan_interval': 60,
                                'table_id': '0x0',
                                'table_state': 'active',
                                'routing_table_version': 43},
                            'vpnv4 unicast RD 400:1': 
                                {'generic_scan_interval': 60,
                                'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'processed_paths': 10,
                                'processed_prefixes': 10,
                                'rd_version': 0,
                                'received': 
                                    {'10.9.2.0/24': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '400 '
                                                      '33299 '
                                                      '51178 '
                                                      '47751 '
                                                      '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}}},
                                'router_identifier': '10.4.1.1',
                                'scan_interval': 60,
                                'table_id': '0x0',
                                'table_state': 'active',
                                'routing_table_version': 43},
                            'vpnv6 unicast RD 300:1': 
                                {'generic_scan_interval': 60,
                                'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'rd_version': 0,
                                'received': 
                                    {'646:11:11:4::/64': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                               'status_codes': '*i',
                                               'weight': '0'}}},
                                    '646:11:11::/64': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}}},
                                'router_identifier': '10.4.1.1',
                                'scan_interval': 60,
                                'table_id': '0x0',
                                'table_state': 'active',
                                'routing_table_version': 43},
                            'vpnv6 unicast RD 400:1': 
                                {'generic_scan_interval': 60,
                                'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'processed_paths': 10,
                                'processed_prefixes': 10,
                                'rd_version': 0,
                                'received': 
                                    {'646:22:22:1::/64': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '400 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}},
                                    '646:22:22::/64': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '400 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}}},
                                'router_identifier': '10.4.1.1',
                                'scan_interval': 60,
                                'table_id': '0x0',
                                'table_state': 'active',
                                'routing_table_version': 43}}}}}}}

    golden_output = {'execute.return_value': '''
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1
        * i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        * i10.9.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e

        Processed 10 prefixes, 10 paths

        Address Family: VPNv6 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1
        * i646:11:11::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i646:11:11:4::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        * i646:22:22::/64     10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i646:22:22:1::/64   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e

        Processed 10 prefixes, 10 paths
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceNeighborsReceivedRoutes(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='all', neighbor='10.186.5.5')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstanceNeighborsReceivedRoutes(device=self.device)
        parsed_output = obj.parse(vrf_type='all', neighbor='10.186.5.5')
        self.assertEqual(parsed_output,self.golden_parsed_output)


# =====================================================================
# Unit test for 'show bgp instance all vrf all neighbors <WORD> routes'
# =====================================================================

class test_show_bgp_instance_all_vrf_all_neighbors_routes(unittest.TestCase):
    
    dev = Device(name='Device')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'VRF2': 
                        {'address_family': 
                            {'vpnv4 unicast RD 200:2': 
                                {'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'processed_paths': 2,
                                'processed_prefixes': 2,
                                'rd_version': 63,
                                'route_distinguisher': '200:2',
                                'router_identifier': '10.229.11.11',
                                'routes':
                                    {'10.1.1.0/24': 
                                        {'index': 
                                            {1: 
                                                {'metric': '2219',
                                                'next_hop': '10.186.5.5',
                                                'origin_codes': 'e',
                                                'path': '200 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*>',
                                                'weight': '0'}}},
                                    '10.1.2.0/24': 
                                        {'index': 
                                            {1: 
                                                {'metric': '2219',
                                                'next_hop': '10.186.5.5',
                                                'origin_codes': 'e',
                                                'path': '200 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*>',
                                                'weight': '0'}}}},
                                'state': 'active',
                                'table_id': '0xe0000011',
                                'table_state': 'active',
                                'routing_table_version': 63,
                                'vrf_id': '0x60000002'}}}}}}}

    golden_output = {'execute.return_value': '''
    
        Neighbor not found

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        VRF: VRF2
        ---------
        BGP VRF VRF2, state: Active
        BGP Route Distinguisher: 200:2
        VRF ID: 0x60000002
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000011   RD version: 63
        BGP main routing table version 63
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:2 (default for vrf VRF2)
        *> 10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.2.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        
        Processed 2 prefixes, 2 paths
        '''}

    def test_empty(self):
        self.dev1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceNeighborsRoutes(device=self.dev1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='vrf', neighbor='10.186.5.5')

    def test_golden(self):
        self.maxDiff = None
        self.dev = Mock(**self.golden_output)
        obj = ShowBgpInstanceNeighborsRoutes(device=self.dev)
        parsed_output = obj.parse(vrf_type='vrf', neighbor='10.186.5.5')
        self.assertEqual(parsed_output,self.golden_parsed_output)


# =====================================================================
# Unit test for 'show bgp instance all all all neighbors <WORD> routes'
# =====================================================================

class test_show_bgp_instance_all_all_all_neighbors_routes(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'default': 
                        {'address_family': 
                            {'vpnv4 unicast RD 300:1': 
                                {'generic_scan_interval': 60,
                                'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'rd_version': 0,
                                'router_identifier': '10.4.1.1',
                                'routes': 
                                    {'10.169.1.0/24': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}}},
                                'scan_interval': 60,
                                'table_id': '0x0',
                                'table_state': 'active',
                                'routing_table_version': 43},
                            'vpnv4 unicast RD 400:1': 
                                {'generic_scan_interval': 60,
                                'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'processed_paths': 2,
                                'processed_prefixes': 2,
                                'rd_version': 0,
                                'router_identifier': '10.4.1.1',
                                'routes':
                                    {'10.9.2.0/24': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '400 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}}},
                                'scan_interval': 60,
                                'table_id': '0x0',
                                'table_state': 'active',
                                'routing_table_version': 43},
                            'vpnv6 unicast RD 300:1': 
                                {'generic_scan_interval': 60,
                                'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'rd_version': 0,
                                'router_identifier': '10.4.1.1',
                                'routes': 
                                    {'646:11:11:1::/64': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}},
                                    '646:11:11::/64': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '300 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}}},
                                'scan_interval': 60,
                                'table_id': '0x0',
                                'table_state': 'active',
                                'routing_table_version': 43},
                            'vpnv6 unicast RD 400:1': 
                                {'generic_scan_interval': 60,
                                'local_as': 100,
                                'non_stop_routing': True,
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': '11',
                                'nsr_issu_sync_group_versions': '0/0',
                                'processed_paths': 3,
                                'processed_prefixes': 3,
                                'rd_version': 0,
                                'router_identifier': '10.4.1.1',
                                'routes':
                                    {'646:22:22::/64': 
                                        {'index': 
                                            {1: 
                                                {'locprf': '100',
                                                'metric': '2219',
                                                'next_hop': '10.64.4.4',
                                                'origin_codes': 'e',
                                                'path': '400 '
                                                       '33299 '
                                                       '51178 '
                                                       '47751 '
                                                       '{27016}',
                                                'status_codes': '*i',
                                                'weight': '0'}}}},
                                'scan_interval': 60,
                                'table_id': '0x0',
                                'table_state': 'active',
                                'routing_table_version': 43}}}}}}}

    golden_output = {'execute.return_value': '''
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1
        * i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        
        Route Distinguisher: 400:1
        * i10.9.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        

        Processed 2 prefixes, 2 paths

        Address Family: VPNv6 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1
        * i646:11:11::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i646:11:11:1::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        * i646:22:22::/64     10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        

        Processed 3 prefixes, 3 paths


        '''}

    
    golden_parsed_output_1 = {
        "instance": {
            "default": {
                 "vrf": {
                      "default": {
                           "address_family": {
                                "ipv4 unicast": {
                                     "non_stop_routing": True,
                                     "generic_scan_interval": 60,
                                     "routing_table_version": 376,
                                     "processed_prefixes": 1,
                                     "nsr_initial_initsync_version": "2",
                                     "table_state": "active",
                                     "nsr_initial_init_ver_status": "reached",
                                     "routes": {
                                          "192.168.0.4/32": {
                                               "index": {
                                                    1: {
                                                         "origin_codes": "i",
                                                         "status_codes": "*>i",
                                                         "next_hop": "192.168.0.4"
                                                    }
                                               }
                                          }
                                     },
                                     "local_as": 1,
                                     "processed_paths": 1,
                                     "scan_interval": 60,
                                     "router_identifier": "192.168.0.1",
                                     "nsr_issu_sync_group_versions": "0/0",
                                     "table_id": "0xe0000000",
                                     "rd_version": 376
                                }
                           }
                      }
                 }
            }
        }
    }

    golden_output_1 = {'execute.return_value': '''
        show bgp instance all all all  neighbors 192.168.0.4 routes
    
        Mon Jan 22 14:32:03.615 UTC

        BGP instance 0: 'default'
        =========================

        Address Family: IPv4 Unicast
        ----------------------------

        BGP router identifier 192.168.0.1, local AS number 1
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000000   RD version: 376
        BGP main routing table version 376
        BGP NSR Initial initsync version 2 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        *>i192.168.0.4/32     192.168.0.4                   100      0 i

        Processed 1 prefixes, 1 paths
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        obj = ShowBgpInstanceNeighborsRoutes(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(vrf_type='all', neighbor='10.36.3.3')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj = ShowBgpInstanceNeighborsRoutes(device=self.device)
        parsed_output = obj.parse(vrf_type='all', neighbor='10.36.3.3')
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_1(self):
        self.maxDiff = None
        self.dev = Mock(**self.golden_output_1)
        obj = ShowBgpInstanceNeighborsRoutes(device=self.dev)
        parsed_output = obj.parse(vrf_type='all', neighbor='192.168.0.4')
        self.assertEqual(parsed_output,self.golden_parsed_output_1)

# =====================================================
# Unit test for 'show bgp instance all all all summary'
# =====================================================

class test_show_bgp_instance_all_all_all_summary(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {'instance': {'default': {'vrf': {'default': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 43,
                                                                                   'generic_scan_interval': 60,
                                                                                   'local_as': 100,
                                                                                   'non_stop_routing': 'enabled',
                                                                                   'nsr_initial_init_ver_status': 'reached',
                                                                                   'nsr_initial_initsync_version': 11,
                                                                                   'nsr_issu_sync_group_versions': '0/0',
                                                                                   'operation_mode': 'standalone',
                                                                                   'process': {'Speaker': {'brib_rib': 43,
                                                                                                           'importver': 43,
                                                                                                           'labelver': 43,
                                                                                                           'rcvtblver': 43,
                                                                                                           'sendtblver': 43,
                                                                                                           'standbyver': 0}},
                                                                                   'rd_version': 0,
                                                                                   'router_id': '10.4.1.1',
                                                                                   'table_id': '0x0',
                                                                                   'table_state': 'active'},
                                                                 'vpnv6 unicast': {'bgp_table_version': 43,
                                                                                   'generic_scan_interval': 60,
                                                                                   'local_as': 100,
                                                                                   'non_stop_routing': 'enabled',
                                                                                   'nsr_initial_init_ver_status': 'reached',
                                                                                   'nsr_initial_initsync_version': 11,
                                                                                   'nsr_issu_sync_group_versions': '0/0',
                                                                                   'operation_mode': 'standalone',
                                                                                   'process': {'Speaker': {'brib_rib': 43,
                                                                                                           'importver': 43,
                                                                                                           'labelver': 43,
                                                                                                           'rcvtblver': 43,
                                                                                                           'sendtblver': 43,
                                                                                                           'standbyver': 0}},
                                                                                   'rd_version': 0,
                                                                                   'router_id': '10.4.1.1',
                                                                                   'table_id': '0x0',
                                                                                   'table_state': 'active'}},
                                              'neighbor': {'10.16.2.2': {'address_family': {'vpnv4 unicast': {'input_queue': 0,
                                                                                                            'msg_rcvd': 59,
                                                                                                            'msg_sent': 56,
                                                                                                            'output_queue': 0,
                                                                                                            'spk': 0,
                                                                                                            'state_pfxrcd': '10',
                                                                                                            'tbl_ver': 43,
                                                                                                            'up_down': '00:50:38'},
                                                                                          'vpnv6 unicast': {'input_queue': 0,
                                                                                                            'msg_rcvd': 59,
                                                                                                            'msg_sent': 56,
                                                                                                            'output_queue': 0,
                                                                                                            'spk': 0,
                                                                                                            'state_pfxrcd': '10',
                                                                                                            'tbl_ver': 43,
                                                                                                            'up_down': '00:50:38'}},
                                                                       'remote_as': 100},
                                                           '10.36.3.3': {'address_family': {'vpnv4 unicast': {'input_queue': 0,
                                                                                                            'msg_rcvd': 68,
                                                                                                            'msg_sent': 58,
                                                                                                            'output_queue': 0,
                                                                                                            'spk': 0,
                                                                                                            'state_pfxrcd': '10',
                                                                                                            'tbl_ver': 43,
                                                                                                            'up_down': '00:47:11'},
                                                                                          'vpnv6 unicast': {'input_queue': 0,
                                                                                                            'msg_rcvd': 68,
                                                                                                            'msg_sent': 58,
                                                                                                            'output_queue': 0,
                                                                                                            'spk': 0,
                                                                                                            'state_pfxrcd': '10',
                                                                                                            'tbl_ver': 43,
                                                                                                            'up_down': '00:47:11'}},
                                                                       'remote_as': 100}}}}}}}

    golden_output = {'execute.return_value': '''
    
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        BGP is operating in standalone mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker              43         43         43         43          43           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        10.16.2.2           0   100      59      56       43    0    0 00:50:38         10
        10.36.3.3           0   100      68      58       43    0    0 00:47:11         10


        Address Family: VPNv6 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        BGP is operating in standalone mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker              43         43         43         43          43           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        10.16.2.2           0   100      59      56       43    0    0 00:50:38         10
        10.36.3.3           0   100      68      58       43    0    0 00:47:11         10
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        bgp_instance_summary_obj = ShowBgpInstanceSummary(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = bgp_instance_summary_obj.parse(vrf_type='all')

    def test_golden(self):
       self.device = Mock(**self.golden_output)
       bgp_instance_summary_obj = ShowBgpInstanceSummary(device=self.device)
       parsed_output = bgp_instance_summary_obj.parse(vrf_type='all')
       self.maxDiff = None
       self.assertEqual(parsed_output,self.golden_parsed_output)


# =====================================================
# Unit test for 'show bgp instance all vrf all summary'
# =====================================================

class test_show_bgp_instance_all_vrf_all_summary(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'instance': {'default': {'vrf': {'VRF1': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 63,
                                                                                'bgp_vrf': 'vrf1',
                                                                                'local_as': 100,
                                                                                'non_stop_routing': 'enabled',
                                                                                'nsr_initial_init_ver_status': 'reached',
                                                                                'nsr_initial_initsync_version': 11,
                                                                                'nsr_issu_sync_group_versions': '0/0',
                                                                                'operation_mode': 'standalone',
                                                                                'process': {'Speaker': {'brib_rib': 63,
                                                                                                        'importver': 63,
                                                                                                        'labelver': 63,
                                                                                                        'rcvtblver': 63,
                                                                                                        'sendtblver': 63,
                                                                                                        'standbyver': 0}},
                                                                                'rd_version': 63,
                                                                                'route_distinguisher': '200:1',
                                                                                'router_id': '10.229.11.11',
                                                                                'table_id': '0xe0000010',
                                                                                'table_state': 'active',
                                                                                'vrf_id': '0x60000001',
                                                                                'vrf_state': 'active'}},
                                           'neighbor': {'10.1.5.5': {'address_family': {'vpnv4 unicast': {'input_queue': 0,
                                                                                                          'msg_rcvd': 60,
                                                                                                          'msg_sent': 62,
                                                                                                          'output_queue': 0,
                                                                                                          'route_distinguisher': '200:1',
                                                                                                          'spk': 0,
                                                                                                          'state_pfxrcd': '0',
                                                                                                          'tbl_ver': 63,
                                                                                                          'up_down': '00:57:32'}},
                                                                     'remote_as': 200}}},
                                  'VRF2': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 63,
                                                                                'bgp_vrf': 'vrf2',
                                                                                'local_as': 100,
                                                                                'non_stop_routing': 'enabled',
                                                                                'nsr_initial_init_ver_status': 'reached',
                                                                                'nsr_initial_initsync_version': 11,
                                                                                'nsr_issu_sync_group_versions': '0/0',
                                                                                'operation_mode': 'standalone',
                                                                                'process': {'Speaker': {'brib_rib': 63,
                                                                                                        'importver': 63,
                                                                                                        'labelver': 63,
                                                                                                        'rcvtblver': 63,
                                                                                                        'sendtblver': 63,
                                                                                                        'standbyver': 0}},
                                                                                'rd_version': 63,
                                                                                'route_distinguisher': '200:2',
                                                                                'router_id': '10.229.11.11',
                                                                                'table_id': '0xe0000011',
                                                                                'table_state': 'active',
                                                                                'vrf_id': '0x60000002',
                                                                                'vrf_state': 'active'}},
                                           'neighbor': {'10.186.5.5': {'address_family': {'vpnv4 unicast': {'input_queue': 0,
                                                                                                          'msg_rcvd': 58,
                                                                                                          'msg_sent': 62,
                                                                                                          'output_queue': 0,
                                                                                                          'route_distinguisher': '200:2',
                                                                                                          'spk': 0,
                                                                                                          'state_pfxrcd': '5',
                                                                                                          'tbl_ver': 63,
                                                                                                          'up_down': '00:01:12'}},
                                                                     'remote_as': 200}}}}}}}

    golden_output = {'execute.return_value': '''
        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------
        BGP VRF VRF1, state: Active
        BGP Route Distinguisher: 200:1
        VRF ID: 0x60000001
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000010   RD version: 63
        BGP main routing table version 63
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        BGP is operating in standalone mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker              63         63         63         63          63           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        10.1.5.5          0   200      60      62       63    0    0 00:57:32          0


        VRF: VRF2
        ---------
        BGP VRF VRF2, state: Active
        BGP Route Distinguisher: 200:2
        VRF ID: 0x60000002
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000011   RD version: 63
        BGP main routing table version 63
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        BGP is operating in standalone mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker              63         63         63         63          63           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        10.186.5.5          0   200      58      62       63    0    0 00:01:12          5
        '''}

    golden_parsed_output2 = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'VRF1': 
                        {'address_family': 
                            {'vpnv6 unicast': 
                                {'bgp_table_version': 3,
                                'bgp_vrf': 'vrf1',
                                'local_as': 100,
                                'non_stop_routing': 'enabled',
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': 3,
                                'nsr_issu_sync_group_versions': '0/0',
                                'operation_mode': 'standalone',
                                'process': {'Speaker': {'brib_rib': 3,
                                                        'importver': 3,
                                                        'labelver': 3,
                                                        'rcvtblver': 3,
                                                        'sendtblver': 3,
                                                        'standbyver': 0}},
                                'rd_version': 2,
                                'route_distinguisher': '200:1',
                                'router_id': '10.229.11.11',
                                'table_id': '0xe0800011',
                                'table_state': 'active',
                                'vrf_id': '0x60000002',
                                'vrf_state': 'active'}},
                        'neighbor': 
                            {'2001:db8:1:5::5': 
                                {'address_family': 
                                    {'vpnv6 unicast': 
                                        {'input_queue': 0,
                                         'msg_rcvd': 0,
                                         'msg_sent': 0,
                                         'output_queue': 0,
                                         'route_distinguisher': '200:1',
                                         'spk': 3,
                                         'state_pfxrcd': 'Idle',
                                         'tbl_ver': 0,
                                         'up_down': '00:00:00'}},
                                'remote_as': 200}}},
                    'VRF2': 
                        {'address_family': 
                            {'vpnv6 unicast': 
                                {'bgp_table_version': 3,
                                'bgp_vrf': 'vrf2',
                                'local_as': 100,
                                'non_stop_routing': 'enabled',
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_initial_initsync_version': 3,
                                'nsr_issu_sync_group_versions': '0/0',
                                'operation_mode': 'standalone',
                                'process': {'Speaker': {'brib_rib': 3,
                                                        'importver': 3,
                                                        'labelver': 3,
                                                        'rcvtblver': 3,
                                                        'sendtblver': 3,
                                                        'standbyver': 0}},
                                'rd_version': 3,
                                'route_distinguisher': '200:2',
                                'router_id': '10.229.11.11',
                                'table_id': '0xe0800012',
                                'table_state': 'active',
                                'vrf_id': '0x60000003',
                                'vrf_state': 'active'}},
                        'neighbor': 
                            {'2001:db8:20:1:5::5': 
                                {'address_family': 
                                    {'vpnv6 unicast': 
                                        {'input_queue': 0,
                                        'msg_rcvd': 0,
                                        'msg_sent': 0,
                                        'output_queue': 0,
                                        'route_distinguisher': '200:2',
                                        'spk': 3,
                                        'state_pfxrcd': 'Idle',
                                        'tbl_ver': 0,
                                        'up_down': '00:00:00'}},
                                'remote_as': 200}}}}},
            'test': {},
            'test1': {},
            'test2': {}}}

    golden_output2 = {'execute.return_value': '''
        RP/0/RSP1/CPU0:PE1#show bgp instance all vrf all ipv6 unicast summary
        Tue Aug 15 14:07:59.536 PDT

        BGP instance 0: 'test'
        ======================
        % None of the requested address families are configured for instance 'test'(29261)

        BGP instance 1: 'test1'
        =======================
        % None of the requested address families are configured for instance 'test1'(29261)

        BGP instance 2: 'test2'
        =======================
        % None of the requested address families are configured for instance 'test2'(29261)

        BGP instance 3: 'default'
        =========================

        VRF: VRF1
        ---------
        BGP VRF VRF1, state: Active
        BGP Route Distinguisher: 200:1
        VRF ID: 0x60000002
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0800011   RD version: 2
        BGP main routing table version 3
        BGP NSR Initial initsync version 3 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        BGP is operating in STANDALONE mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker               3          3          3          3           3           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        2001:db8:1:5::5   3   200       0       0        0    0    0 00:00:00 Idle


        VRF: VRF2
        ---------
        BGP VRF VRF2, state: Active
        BGP Route Distinguisher: 200:2
        VRF ID: 0x60000003
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0800012   RD version: 3
        BGP main routing table version 3
        BGP NSR Initial initsync version 3 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        BGP is operating in STANDALONE mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker               3          3          3          3           3           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        2001:db8:20:1:5::5
                          3   200       0       0        0    0    0 00:00:00 Idle
        '''}

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        bgp_instance_summary_obj = ShowBgpInstanceSummary(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = bgp_instance_summary_obj.parse(vrf_type='vrf')

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        bgp_instance_summary_obj = ShowBgpInstanceSummary(device=self.device)
        parsed_output = bgp_instance_summary_obj.parse(vrf_type='vrf')
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        bgp_instance_summary_obj = ShowBgpInstanceSummary(device=self.device)
        parsed_output = bgp_instance_summary_obj.parse(vrf_type='vrf', address_family='ipv6 unicast')
        self.assertEqual(parsed_output,self.golden_parsed_output2)

# =============================================
# Unit test for 'show bgp instance all all all'
# =============================================

class test_show_bgp_instance_all_all_all(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {'instance': {'default': {'vrf': {'default': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 43,
                                                                                   'generic_scan_interval': '60',
                                                                                   'instance_number': '0',
                                                                                   'local_as': 100,
                                                                                   'non_stop_routing': True,
                                                                                   'nsr_initial_init_ver_status': 'reached',
                                                                                   'nsr_initial_initsync_version': '11',
                                                                                   'nsr_issu_sync_group_versions': '0/0',
                                                                                   'rd_version': 0,
                                                                                   'router_identifier': '10.4.1.1',
                                                                                   'scan_interval': 60,
                                                                                   'table_id': '0x0',
                                                                                   'table_state': 'active'},
                                                                 'vpnv4 unicast RD 200:1': {'default_vrf': 'vrf1',
                                                                                            'prefix': {'10.1.1.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                     'next_hop': '10.186.5.5',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '200 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*>',
                                                                                                                                     'weight': '0'}}},
                                                                                                       '10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                     'metric': '2219',
                                                                                                                                     'next_hop': '10.64.4.4',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '300 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*>i',
                                                                                                                                     'weight': '0'}}}},
                                                                                            'route_distinguisher': '200:1'},
                                                                 'vpnv4 unicast RD 200:2': {'default_vrf': 'vrf2',
                                                                                            'prefix': {'10.1.1.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                     'next_hop': '10.186.5.5',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '200 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*>',
                                                                                                                                     'weight': '0'}}},
                                                                                                       '10.169.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                     'metric': '2219',
                                                                                                                                     'next_hop': '10.64.4.4',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '300 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*>i',
                                                                                                                                     'weight': '0'}}}},
                                                                                            'route_distinguisher': '200:2'},
                                                                 'vpnv4 unicast RD 300:1': {'default_vrf': 'none',
                                                                                            'prefix': {'10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                     'metric': '2219',
                                                                                                                                     'next_hop': '10.64.4.4',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '300 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*>i',
                                                                                                                                     'weight': '0'},
                                                                                                                                 2: {'locprf': '100',
                                                                                                                                     'metric': '2219',
                                                                                                                                     'next_hop': '10.64.4.4',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '300 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*i',
                                                                                                                                     'weight': '0'}}}},
                                                                                            'route_distinguisher': '300:1'},
                                                                 'vpnv4 unicast RD 400:1': {'default_vrf': 'none',
                                                                                            'prefix': {'10.9.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                     'metric': '2219',
                                                                                                                                     'next_hop': '10.64.4.4',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '400 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*>i',
                                                                                                                                     'weight': '0'},
                                                                                                                                 2: {'locprf': '100',
                                                                                                                                     'metric': '2219',
                                                                                                                                     'next_hop': '10.64.4.4',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '400 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*i',
                                                                                                                                     'weight': '0'}}},
                                                                                                       '10.9.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                     'metric': '2219',
                                                                                                                                     'next_hop': '10.64.4.4',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '400 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*>i',
                                                                                                                                     'weight': '0'},
                                                                                                                                 2: {'locprf': '100',
                                                                                                                                     'metric': '2219',
                                                                                                                                     'next_hop': '10.64.4.4',
                                                                                                                                     'origin_codes': 'e',
                                                                                                                                     'path': '400 '
                                                                                                                                             '33299 '
                                                                                                                                             '51178 '
                                                                                                                                             '47751 '
                                                                                                                                             '{27016}',
                                                                                                                                     'status_codes': '*i',
                                                                                                                                     'weight': '0'}}}},
                                                                                            'processed_paths': 50,
                                                                                            'processed_prefix': 40,
                                                                                            'route_distinguisher': '400:1'},
                                                                 'vpnv6 unicast': {'bgp_table_version': 43,
                                                                                   'generic_scan_interval': '60',
                                                                                   'instance_number': '0',
                                                                                   'local_as': 100,
                                                                                   'non_stop_routing': True,
                                                                                   'nsr_initial_init_ver_status': 'reached',
                                                                                   'nsr_initial_initsync_version': '11',
                                                                                   'nsr_issu_sync_group_versions': '0/0',
                                                                                   'rd_version': 0,
                                                                                   'router_identifier': '10.4.1.1',
                                                                                   'scan_interval': 60,
                                                                                   'table_id': '0x0',
                                                                                   'table_state': 'active'},
                                                                 'vpnv6 unicast RD 200:1': {'default_vrf': 'vrf1',
                                                                                            'prefix': {'615:11:11:3::/64': {'index': {1: {'metric': '2219',
                                                                                                                                          'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '200 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '615:11:11:4::/64': {'index': {1: {'metric': '2219',
                                                                                                                                          'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '200 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '646:11:11:1::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '646:11:11:2::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '646:11:11::/64': {'index': {1: {'locprf': '100',
                                                                                                                                        'metric': '2219',
                                                                                                                                        'next_hop': '10.64.4.4',
                                                                                                                                        'origin_codes': 'e',
                                                                                                                                        'path': '300 '
                                                                                                                                                '33299 '
                                                                                                                                                '51178 '
                                                                                                                                                '47751 '
                                                                                                                                                '{27016}',
                                                                                                                                        'status_codes': '*>i',
                                                                                                                                        'weight': '0'}}}},
                                                                                            'route_distinguisher': '200:1'},
                                                                 'vpnv6 unicast RD 200:2': {'default_vrf': 'vrf2',
                                                                                            'prefix': {'615:11:11:1::/64': {'index': {1: {'metric': '2219',
                                                                                                                                          'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '200 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '615:11:11::/64': {'index': {1: {'metric': '2219',
                                                                                                                                        'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                        'origin_codes': 'e',
                                                                                                                                        'path': '200 '
                                                                                                                                                '33299 '
                                                                                                                                                '51178 '
                                                                                                                                                '47751 '
                                                                                                                                                '{27016}',
                                                                                                                                        'status_codes': '*>',
                                                                                                                                        'weight': '0'}}},
                                                                                                       '646:11:11:1::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '646:11:11:2::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '646:11:11::/64': {'index': {1: {'locprf': '100',
                                                                                                                                        'metric': '2219',
                                                                                                                                        'next_hop': '10.64.4.4',
                                                                                                                                        'origin_codes': 'e',
                                                                                                                                        'path': '300 '
                                                                                                                                                '33299 '
                                                                                                                                                '51178 '
                                                                                                                                                '47751 '
                                                                                                                                                '{27016}',
                                                                                                                                        'status_codes': '*>i',
                                                                                                                                        'weight': '0'}}}},
                                                                                            'route_distinguisher': '200:2'},
                                                                 'vpnv6 unicast RD 300:1': {'default_vrf': 'none',
                                                                                            'prefix': {'646:11:11:1::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'},
                                                                                                                                      2: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*i',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '646:11:11::/64': {'index': {1: {'locprf': '100',
                                                                                                                                        'metric': '2219',
                                                                                                                                        'next_hop': '10.64.4.4',
                                                                                                                                        'origin_codes': 'e',
                                                                                                                                        'path': '300 '
                                                                                                                                                '33299 '
                                                                                                                                                '51178 '
                                                                                                                                                '47751 '
                                                                                                                                                '{27016}',
                                                                                                                                        'status_codes': '*>i',
                                                                                                                                        'weight': '0'},
                                                                                                                                    2: {'locprf': '100',
                                                                                                                                        'metric': '2219',
                                                                                                                                        'next_hop': '10.64.4.4',
                                                                                                                                        'origin_codes': 'e',
                                                                                                                                        'path': '300 '
                                                                                                                                                '33299 '
                                                                                                                                                '51178 '
                                                                                                                                                '47751 '
                                                                                                                                                '{27016}',
                                                                                                                                        'status_codes': '*i',
                                                                                                                                        'weight': '0'}}}},
                                                                                            'route_distinguisher': '300:1'},
                                                                 'vpnv6 unicast RD 400:1': {'default_vrf': 'none',
                                                                                            'prefix': {'646:22:22:1::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '400 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'},
                                                                                                                                      2: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '400 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*i',
                                                                                                                                          'weight': '0'}}},
                                                                                                       '646:22:22::/64': {'index': {1: {'locprf': '100',
                                                                                                                                        'metric': '2219',
                                                                                                                                        'next_hop': '10.64.4.4',
                                                                                                                                        'origin_codes': 'e',
                                                                                                                                        'path': '400 '
                                                                                                                                                '33299 '
                                                                                                                                                '51178 '
                                                                                                                                                '47751 '
                                                                                                                                                '{27016}',
                                                                                                                                        'status_codes': '*>i',
                                                                                                                                        'weight': '0'},
                                                                                                                                    2: {'locprf': '100',
                                                                                                                                        'metric': '2219',
                                                                                                                                        'next_hop': '10.64.4.4',
                                                                                                                                        'origin_codes': 'e',
                                                                                                                                        'path': '400 '
                                                                                                                                                '33299 '
                                                                                                                                                '51178 '
                                                                                                                                                '47751 '
                                                                                                                                                '{27016}',
                                                                                                                                        'status_codes': '*i',
                                                                                                                                        'weight': '0'}}}},
                                                                                            'processed_paths': 50,
                                                                                            'processed_prefix': 40,
                                                                                            'route_distinguisher': '400:1'}}}}}}}
                                                

    golden_output = {'execute.return_value': '''
    
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:1 (default for vrf VRF1)
        *> 10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 200:2 (default for vrf VRF2)
        *> 10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *>i10.169.5.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 300:1
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        *>i10.9.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.3.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        
        Processed 40 prefixes, 50 paths

        Address Family: VPNv6 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:1 (default for vrf VRF1)
        *> 615:11:11:3::/64   2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 615:11:11:4::/64   2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *>i646:11:11::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i646:11:11:1::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i646:11:11:2::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 200:2 (default for vrf VRF2)
        *> 615:11:11::/64     2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 615:11:11:1::/64   2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *>i646:11:11::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i646:11:11:1::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i646:11:11:2::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 300:1
        *>i646:11:11::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i646:11:11:1::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        *>i646:22:22::/64     10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i646:22:22:1::/64   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
    
        Processed 40 prefixes, 50 paths

        '''}
    
    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        bgp_instance_all_all_obj = ShowBgpInstanceAllAll(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = bgp_instance_all_all_obj.parse(vrf_type='all')

    def test_golden_all(self):
       self.device = Mock(**self.golden_output)
       bgp_instance_all_all_obj = ShowBgpInstanceAllAll(device=self.device)
       parsed_output = bgp_instance_all_all_obj.parse(vrf_type='all')
       self.maxDiff = None
       self.assertEqual(parsed_output,self.golden_parsed_output)


# =============================================
# Unit test for 'show bgp instance all vrf all'
# =============================================

class test_show_bgp_instance_all_vrf_all(unittest.TestCase):
    
    device = Device(name='aDevice')
    device0 = Device(name='bDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {'instance': {'default': {'vrf': {'VRF1': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 43,
                                                                                'bgp_vrf': 'vrf1',
                                                                                'local_as': 100,
                                                                                'non_stop_routing': True,
                                                                                'nsr_initial_init_ver_status': 'reached',
                                                                                'nsr_initial_initsync_version': '11',
                                                                                'nsr_issu_sync_group_versions': '0/0',
                                                                                'rd_version': 43,
                                                                                'router_identifier': '10.229.11.11',
                                                                                'table_id': '0xe0000010',
                                                                                'table_state': 'active',
                                                                                'vrf_id': '0x60000001',
                                                                                'vrf_state': 'active'},
                                                              'vpnv4 unicast RD 200:1': {'default_vrf': 'vrf1',
                                                                                         'prefix': {'10.1.1.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.1.2.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.1.3.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.1.4.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.1.5.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.6.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}}},
                                                                                         'processed_paths': 15,
                                                                                         'processed_prefix': 15,
                                                                                         'route_distinguisher': '200:1'}}},
                                  'VRF2': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 43,
                                                                                'bgp_vrf': 'vrf2',
                                                                                'local_as': 100,
                                                                                'non_stop_routing': True,
                                                                                'nsr_initial_init_ver_status': 'reached',
                                                                                'nsr_initial_initsync_version': '11',
                                                                                'nsr_issu_sync_group_versions': '0/0',
                                                                                'rd_version': 43,
                                                                                'router_identifier': '10.229.11.11',
                                                                                'table_id': '0xe0000011',
                                                                                'table_state': 'active',
                                                                                'vrf_id': '0x60000002',
                                                                                'vrf_state': 'active'},
                                                              'vpnv4 unicast RD 200:2': {'default_vrf': 'vrf2',
                                                                                         'prefix': {'10.1.1.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.1.2.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.1.3.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.1.4.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.1.5.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                  'next_hop': '10.186.5.5',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '200 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.169.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '300 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}},
                                                                                                    '10.9.6.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                  'metric': '2219',
                                                                                                                                  'next_hop': '10.64.4.4',
                                                                                                                                  'origin_codes': 'e',
                                                                                                                                  'path': '400 '
                                                                                                                                          '33299 '
                                                                                                                                          '51178 '
                                                                                                                                          '47751 '
                                                                                                                                          '{27016}',
                                                                                                                                  'status_codes': '*>i',
                                                                                                                                  'weight': '0'}}}},
                                                                                         'processed_paths': 15,
                                                                                         'processed_prefix': 15,
                                                                                         'route_distinguisher': '200:2'}}}}}}}


    golden_output = {'execute.return_value': '''
        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------
        BGP VRF VRF1, state: Active
        BGP Route Distinguisher: 200:1
        VRF ID: 0x60000001
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000010   RD version: 43
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:1 (default for vrf VRF1)
        *> 10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.2.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.3.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.4.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.5.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.2.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.3.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.4.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.5.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.9.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.3.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.4.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.5.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.6.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e

        Processed 15 prefixes, 15 paths

        VRF: VRF2
        ---------
        BGP VRF VRF2, state: Active
        BGP Route Distinguisher: 200:2
        VRF ID: 0x60000002
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000011   RD version: 43
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:2 (default for vrf VRF2)
        *> 10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.2.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.3.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.4.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.5.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.2.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.3.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.4.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.5.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.9.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.3.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.4.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.5.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.9.6.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e

        Processed 15 prefixes, 15 paths
        '''}

    golden_output2 = {'execute.return_value': '''
        RP/0/RP0/CPU0:ML26#
        +++ ML26: executing command 'show bgp instance all all all' +++
        show bgp instance all all all

        BGP instance 0: 'default'
        =========================

        Address Family: IPv6 Labeled-unicast
        ------------------------------------

        BGP router identifier 192.168.87.47, local AS number 123123
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0800000   RD version: 41
        BGP main routing table version 41
        BGP NSR Initial initsync version 9 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

    '''}

    golden_parsed_output2 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'address_family': {
                            'ipv6 labeled-unicast': {
                                'instance_number': '0',
                                'router_identifier': '192.168.87.47',
                                'local_as': 123123,
                                'generic_scan_interval': '60',
                                'non_stop_routing': True,
                                'table_state': 'active',
                                'table_id': '0xe0800000',
                                'rd_version': 41,
                                'bgp_table_version': 41,
                                'nsr_initial_initsync_version': '9',
                                'nsr_initial_init_ver_status': 'reached',
                                'nsr_issu_sync_group_versions': '0/0',
                                'scan_interval': 60,
                            },
                        },
                    },
                },
            },
        },
    }

    def test_empty(self):
        self.device1 = Mock(**self.empty_output)
        bgp_instance_all_all_obj = ShowBgpInstanceAllAll(device=self.device1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = bgp_instance_all_all_obj.parse(vrf_type='vrf')

    def test_golden_vrf(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        bgp_instance_all_all_obj = ShowBgpInstanceAllAll(device=self.device)
        parsed_output = bgp_instance_all_all_obj.parse(vrf_type='vrf')
        self.assertEqual(parsed_output,self.golden_parsed_output)
    
    def test_golden_all(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        bgp_instance_all_all_obj = ShowBgpInstanceAllAll(device=self.device)
        parsed_output = bgp_instance_all_all_obj.parse(instance='all')
        self.assertEqual(parsed_output,self.golden_parsed_output2)


# =============================================
# Unit test for 'show bgp l2vpn evpn'
# =============================================
class test_show_bgp_l2vpn_evpn(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        "vrf": {
            "default": {
                "address_family": {
                    "l2vpn evpn": {
                        "bgp_table_version": 33445,
                        "local_router_id": "10.16.2.1"
                    },
                    "l2vpn evpn RD 10.16.2.1:12345": {
                        "bgp_table_version": 33445,
                        "default_vrf": "L2",
                        "local_router_id": "10.16.2.1",
                        "prefixes": {
                            "[2]:[0]:[0]:[48]:[0001.0010.0001]:[32]:[10.1.1.2]/272": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1000::abcd:5678:1",
                                        "path_type": "l",
                                        "status_codes": "*>",
                                        "weight": 33445
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[0010.0010.0001]:[32]:[10.1.1.4]/272": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1000::abcd:5678:1",
                                        "path_type": "l",
                                        "status_codes": "*>",
                                        "weight": 33445
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[0011.0100.0001]:[128]:[2000:1:ab:10::1:2]/368": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1000::abcd:5678:1",
                                        "path_type": "l",
                                        "status_codes": "*>",
                                        "weight": 33445
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[0011.0100.0002]:[128]:[2000:1:ab:10::1:3]/368": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1000::abcd:5678:1",
                                        "path_type": "l",
                                        "status_codes": "*>",
                                        "weight": 33445
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[0014.0100.0001]:[128]:[2000:1:ab:10::4:2]/368": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1000::abcd:5678:1",
                                        "path_type": "l",
                                        "status_codes": "*>",
                                        "weight": 33445
                                    }
                                }
                            },
                            "[3]:[0]:[128]:[2000:1000::abcd:5678:1]/184": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1000::abcd:5678:1",
                                        "path_type": "l",
                                        "status_codes": "*>",
                                        "weight": 33445
                                    }
                                }
                            }
                        },
                        "route_distinguisher": "10.16.2.1:12345"
                    },
                    "l2vpn evpn RD 10.16.2.1:33333": {
                        "bgp_table_version": 33445,
                        "default_vrf": "L2",
                        "local_router_id": "10.16.2.1",
                        "prefixes": {
                            "[2]:[0]:[0]:[48]:[0020.0100.0007]:[32]:[10.2.2.2]/272": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*>",
                                        "weight": 0
                                    },
                                    2: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*",
                                        "weight": 0
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[0020.0100.0008]:[32]:[10.2.2.3]/272": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*>",
                                        "weight": 0
                                    },
                                    2: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*",
                                        "weight": 0
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[0020.0100.0009]:[32]:[10.2.2.4]/272": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*>",
                                        "weight": 0
                                    },
                                    2: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*",
                                        "weight": 0
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[0020.0100.000a]:[32]:[10.2.2.5]/272": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*>",
                                        "weight": 0
                                    },
                                    2: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*",
                                        "weight": 0
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[0020.0100.000b]:[32]:[10.2.2.6]/272": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*>",
                                        "weight": 0
                                    },
                                    2: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:3",
                                        "path_type": "i",
                                        "status_codes": "*",
                                        "weight": 0
                                    }
                                }
                            },
                            "[2]:[0]:[0]:[48]:[1000.0100.0007]:[32]:[10.2.1.2]/272": {
                                "index": {
                                    1: {
                                        "localprf": 100,
                                        "next_hop": "2000:1015::abcd:5678:1",
                                        "path_type": "l",
                                        "status_codes": "*>",
                                        "weight": 33445
                                    }
                                }
                            }
                        },
                        "route_distinguisher": "10.16.2.1:33333"
                    }
                }
            }
        }
    }

    golden_output = {'execute.return_value': '''
         show bgp l2vpn evpn

        BGP routing table information for VRF default, address family L2VPN EVPN

        BGP table version is 33445, Local Router ID is 10.16.2.1

        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best

        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected

        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup, 2 - best2



           Network            Next Hop            Metric     LocPrf     Weight Path

        Route Distinguisher: 10.16.2.1:12345    (L2VNI 10001)

        *>l[2]:[0]:[0]:[48]:[0001.0010.0001]:[32]:[10.1.1.2]/272

                              2000:1000::abcd:5678:1

                                                                100      33445 i

        *>l[2]:[0]:[0]:[48]:[0010.0010.0001]:[32]:[10.1.1.4]/272

                              2000:1000::abcd:5678:1

                                                                100      33445 i

        *>l[2]:[0]:[0]:[48]:[0011.0100.0001]:[128]:[2000:1:ab:10::1:2]/368

                              2000:1000::abcd:5678:1

                                                                100      33445 i

        *>l[2]:[0]:[0]:[48]:[0011.0100.0002]:[128]:[2000:1:ab:10::1:3]/368

                              2000:1000::abcd:5678:1

                                                                100      33445 i

        *>l[2]:[0]:[0]:[48]:[0014.0100.0001]:[128]:[2000:1:ab:10::4:2]/368

                              2000:1000::abcd:5678:1

                                                                100      33445 i

        *>l[3]:[0]:[128]:[2000:1000::abcd:5678:1]/184

                              2000:1000::abcd:5678:1

                                                                100      33445 i



        Route Distinguisher: 10.16.2.1:33333    (L2VNI 20002)

        *>l[2]:[0]:[0]:[48]:[1000.0100.0007]:[32]:[10.2.1.2]/272

                              2000:1015::abcd:5678:1

                                                                100      33445 i

        *>i[2]:[0]:[0]:[48]:[0020.0100.0007]:[32]:[10.2.2.2]/272

                              2000:1015::abcd:5678:3

                                                                100          0 i

        * i                   2000:1015::abcd:5678:3

                                                                100          0 i

        *>i[2]:[0]:[0]:[48]:[0020.0100.0008]:[32]:[10.2.2.3]/272

                              2000:1015::abcd:5678:3

                                                                100          0 i

        * i                   2000:1015::abcd:5678:3

                                                                100          0 i

        *>i[2]:[0]:[0]:[48]:[0020.0100.0009]:[32]:[10.2.2.4]/272

                              2000:1015::abcd:5678:3

                                                                100          0 i

        * i                   2000:1015::abcd:5678:3

                                                                100          0 i

        *>i[2]:[0]:[0]:[48]:[0020.0100.000a]:[32]:[10.2.2.5]/272

                              2000:1015::abcd:5678:3

                                                                100          0 i

        * i                   2000:1015::abcd:5678:3

                                                                100          0 i

        *>i[2]:[0]:[0]:[48]:[0020.0100.000b]:[32]:[10.2.2.6]/272

                              2000:1015::abcd:5678:3

                                                                100          0 i

        * i                   2000:1015::abcd:5678:3

                                                                100          0 i
    '''}

    golden_output2 = {'execute.return_value': '''
        +++ Router2: executing command 'show bgp l2vpn evpn' +++
        show bgp l2vpn evpn

        Fri Sep  6 10:39:01.396 EST
        BGP router identifier 192.168.99.25, local AS number 65001
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 2
        BGP NSR Initial initsync version 2 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                    i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
        Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 192.168.99.25:100 (default for vrf Mansion-100)
        *> [3][0][32][192.168.99.25]/80
                            0.0.0.0                                0 i

        Processed 1 prefixes, 1 paths
        RP/0/RP0/CPU0:Router2#

    '''}


    golden_parsed_output2 = {
        'vrf': {
            'default': {
                'address_family': {
                    'l2vpn evpn': {
                        'router_identifier': '192.168.99.25',
                        'local_as': 65001,
                        'generic_scan_interval': '60',
                        'non_stop_routing': 'enabled',
                        'table_state': 'active',
                        'table_id': '0x0',
                        'rd_version': 0,
                        'bgp_table_version': 2,
                        'nsr_initial_initsync_version': '2',
                        'nsr_initial_init_ver_status': 'reached',
                        'nsr_issu_sync_group_versions': '0/0',
                        'scan_interval': 60,
                    },
                    'l2vpn evpn RD 192.168.99.25:100': {
                        'bgp_table_version': 2,
                        'local_router_id': '',
                        'route_distinguisher': '192.168.99.25:100',
                        'prefixes': {
                            '[3][0][32][192.168.99.25]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                        'processed_prefix': 1,
                        'processed_paths': 1,
                    },
                },
            },
        },
    }

    
    golden_parsed_output3 = {
        'vrf': {
            'default': {
                'address_family': {
                    'l2vpn evpn': {
                        'router_identifier': '172.16.2.88',
                        'local_as': 64577,
                        'generic_scan_interval': '60',
                        'non_stop_routing': 'enabled',
                        'table_state': 'active',
                        'table_id': '0x0',
                        'rd_version': 0,
                        'bgp_table_version': 730,
                        'nsr_initial_initsync_version': '65',
                        'nsr_initial_init_ver_status': 'reached',
                        'nsr_issu_sync_group_versions': '0/0',
                        'scan_interval': 60,
                    },
                    'l2vpn evpn RD 172.16.2.88:1000': {
                        'bgp_table_version': 730,
                        'local_router_id': '',
                        'route_distinguisher': '172.16.2.88:1000',
                        'prefixes': {
                            '[2][0][48][0012.0100.0001][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0002][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0003][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0004][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0005][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0006][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0007][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0008][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0009][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000a][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000b][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000c][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000d][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000e][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000f][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0010][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0011][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0012][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0013][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0014][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0015][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0016][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0017][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0018][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0019][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001a][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001b][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001c][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001d][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001e][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001f][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0020][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0021][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0022][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0023][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0024][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0025][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0026][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0027][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0028][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0029][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002a][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002b][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002c][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002d][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002e][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002f][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0030][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0031][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0032][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0001][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0002][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0003][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0004][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0005][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0006][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0007][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0008][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0009][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.000a][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.000b][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.000c][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.000d][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.000e][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.000f][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0010][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0011][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0012][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0013][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0014][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0015][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0016][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0017][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0018][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0019][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.001a][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.001b][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.001c][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.001d][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.001e][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.001f][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0020][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0021][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0022][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0023][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0024][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0025][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0026][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0027][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0028][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0029][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.002a][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.002b][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.002c][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.002d][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.002e][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.002f][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0030][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0031][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0200.0032][0]/104': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[3][0][32][172.16.2.88]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[3][0][32][172.16.2.89]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[3][0][32][172.16.2.90]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.90',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 172.16.2.89:1': {
                        'bgp_table_version': 730,
                        'local_router_id': '',
                        'route_distinguisher': '172.16.2.89:1',
                        'prefixes': {
                            '[5][0][22][10.249.248.0]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'localprf': 0,
                                        'weight': 100,
                                        'path': '0',
                                        'origin_codes': '?',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 172.16.2.89:1000': {
                        'bgp_table_version': 730,
                        'local_router_id': '',
                        'route_distinguisher': '172.16.2.89:1000',
                        'prefixes': {
                            '[2][0][48][0012.0100.0001][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0002][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0003][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0004][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0005][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0006][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0007][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0008][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0009][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000a][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000b][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000c][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000d][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000e][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.000f][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0010][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0011][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0012][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0013][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0014][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0015][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0016][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0017][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0018][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0019][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001a][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001b][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001c][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001d][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001e][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.001f][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0020][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0021][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0022][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0023][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0024][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0025][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0026][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0027][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0028][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0029][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002a][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002b][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002c][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002d][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002e][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.002f][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0030][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0031][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[2][0][48][0012.0100.0032][0]/104': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[3][0][32][172.16.2.89]/80': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.89',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 172.16.2.90:1': {
                        'bgp_table_version': 730,
                        'local_router_id': '',
                        'route_distinguisher': '172.16.2.90:1',
                        'prefixes': {
                            '[5][0][22][10.249.248.0]/80': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.90',
                                        'localprf': 0,
                                        'weight': 100,
                                        'path': '0',
                                        'origin_codes': '?',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 172.16.2.90:1000': {
                        'bgp_table_version': 730,
                        'local_router_id': '',
                        'route_distinguisher': '172.16.2.90:1000',
                        'prefixes': {
                            '[3][0][32][172.16.2.90]/80': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '172.16.2.90',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 172.18.0.209:162': {
                        'bgp_table_version': 730,
                        'local_router_id': '',
                        'route_distinguisher': '172.18.0.209:162',
                        'prefixes': {
                            '[5][0][24][10.120.1.0]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*',
                                        'next_hop': '172.18.0.209',
                                        'localprf': 100,
                                        'weight': 0,
                                        'path': '65505',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[5][0][30][10.120.0.4]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*',
                                        'next_hop': '172.18.0.209',
                                        'localprf': 0,
                                        'weight': 100,
                                        'path': '0',
                                        'origin_codes': '?',
                                    },
                                },
                            },
                            '[5][0][32][10.0.120.1]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*',
                                        'next_hop': '172.18.0.209',
                                        'localprf': 100,
                                        'weight': 0,
                                        'path': '65505',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 172.19.3.1:161': {
                        'bgp_table_version': 730,
                        'local_router_id': '',
                        'route_distinguisher': '172.19.3.1:161',
                        'prefixes': {
                            '[5][0][24][10.120.1.0]/80': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '10.154.219.79',
                                        'localprf': 100,
                                        'weight': 0,
                                        'path': '65505',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[5][0][30][10.120.0.0]/80': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '10.154.219.79',
                                        'localprf': 0,
                                        'weight': 100,
                                        'path': '0',
                                        'origin_codes': '?',
                                    },
                                },
                            },
                            '[5][0][32][10.0.120.1]/80': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '10.154.219.79',
                                        'localprf': 100,
                                        'weight': 0,
                                        'path': '65505',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                        'processed_prefix': 163,
                        'processed_paths': 166,
                    },
                },
            },
        },
    }

    golden_output3 = {'execute.return_value': '''
        +++ tor1-tatooine: executing command 'show bgp l2vpn evpn' +++
        show bgp l2vpn evpn

        Thu Sep 26 12:40:06.520 EDT
        BGP router identifier 172.16.2.88, local AS number 64577
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 730
        BGP NSR Initial initsync version 65 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                    i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
        Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 172.16.2.88:1000 (default for vrf EVPN-Multicast-BTV)
        *>i[2][0][48][0012.0100.0001][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0002][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0003][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0004][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0005][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0006][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0007][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0008][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0009][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000a][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000b][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000c][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000d][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000e][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000f][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0010][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0011][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0012][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0013][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0014][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0015][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0016][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0017][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0018][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0019][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001a][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001b][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001c][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001d][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001e][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001f][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0020][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0021][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0022][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0023][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0024][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0025][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0026][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0027][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0028][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0029][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002a][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002b][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002c][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002d][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002e][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002f][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0030][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0031][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0032][0]/104
                            172.16.2.89                   100      0 i
        *> [2][0][48][0012.0200.0001][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0002][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0003][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0004][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0005][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0006][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0007][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0008][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0009][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.000a][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.000b][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.000c][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.000d][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.000e][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.000f][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0010][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0011][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0012][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0013][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0014][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0015][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0016][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0017][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0018][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0019][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.001a][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.001b][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.001c][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.001d][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.001e][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.001f][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0020][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0021][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0022][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0023][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0024][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0025][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0026][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0027][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0028][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0029][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.002a][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.002b][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.002c][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.002d][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.002e][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.002f][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0030][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0031][0]/104
                            0.0.0.0                                0 i
        *> [2][0][48][0012.0200.0032][0]/104
                            0.0.0.0                                0 i
        *> [3][0][32][172.16.2.88]/80
                            0.0.0.0                                0 i
        *>i[3][0][32][172.16.2.89]/80
                            172.16.2.89                   100      0 i
        *>i[3][0][32][172.16.2.90]/80
                            172.16.2.90                   100      0 i
        Route Distinguisher: 172.16.2.89:1
        *>i[5][0][22][10.249.248.0]/80
                            172.16.2.89              0    100      0 ?
        Route Distinguisher: 172.16.2.89:1000
        *>i[2][0][48][0012.0100.0001][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0002][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0003][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0004][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0005][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0006][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0007][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0008][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0009][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000a][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000b][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000c][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000d][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000e][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.000f][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0010][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0011][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0012][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0013][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0014][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0015][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0016][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0017][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0018][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0019][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001a][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001b][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001c][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001d][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001e][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.001f][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0020][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0021][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0022][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0023][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0024][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0025][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0026][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0027][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0028][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0029][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002a][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002b][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002c][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002d][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002e][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.002f][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0030][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0031][0]/104
                            172.16.2.89                   100      0 i
        *>i[2][0][48][0012.0100.0032][0]/104
                            172.16.2.89                   100      0 i
        *>i[3][0][32][172.16.2.89]/80
                            172.16.2.89                   100      0 i
        Route Distinguisher: 172.16.2.90:1
        *>i[5][0][22][10.249.248.0]/80
                            172.16.2.90              0    100      0 ?
        Route Distinguisher: 172.16.2.90:1000
        *>i[3][0][32][172.16.2.90]/80
                            172.16.2.90                   100      0 i
        Route Distinguisher: 172.18.0.209:162
        * i[5][0][24][10.120.1.0]/80
                            172.18.0.209                  100      0 65505 i
        *>i                   10.154.219.86                  100      0 65505 i
        * i[5][0][30][10.120.0.4]/80
                            172.18.0.209             0    100      0 ?
        *>i                   10.154.219.86             0    100      0 ?
        * i[5][0][32][10.0.120.1]/80
                            172.18.0.209                  100      0 65505 i
        *>i                   10.154.219.86                  100      0 65505 i
        Route Distinguisher: 172.19.3.1:161
        *>i[5][0][24][10.120.1.0]/80
                            10.154.219.79                  100      0 65505 i
        *>i[5][0][30][10.120.0.0]/80
                            10.154.219.79             0    100      0 ?
        *>i[5][0][32][10.0.120.1]/80
                            10.154.219.79                  100      0 65505 i

        Processed 163 prefixes, 166 paths
        RP/0/RP0/CPU0:tor1-tatooine#



    '''}
    
    golden_output4 = {'execute.return_value': '''
        +++ genie-router: executing command 'show bgp l2vpn evpn' +++
        show bgp l2vpn evpn

        Fri Sep 27 17:01:51.580 EDT
        BGP router identifier 10.154.219.88, local AS number 64577
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 7
        BGP NSR Initial initsync version 3 (Reached)
        BGP NSR/ISSU Sync-Group versions 7/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                    i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
        Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 10.154.219.82:10100
        *>i[1][0000.0000.0000.0000.0000][30100]/120
                            10.154.219.82                  100      0 i
        Route Distinguisher: 10.154.219.82:10200
        *>i[1][0000.0000.0000.0000.0000][30200]/120
                            10.154.219.82                  100      0 i
        Route Distinguisher: 10.154.219.88:10100 (default for vrf VPWS:10100)
        *> [1][0000.0000.0000.0000.0000][20100]/120
                            0.0.0.0                                0 i
        *>i[1][0000.0000.0000.0000.0000][30100]/120
                            10.154.219.82                  100      0 i
        Route Distinguisher: 10.154.219.88:10200 (default for vrf VPWS:10200)
        *> [1][0000.0000.0000.0000.0000][20200]/120
                            0.0.0.0                                0 i
        *>i[1][0000.0000.0000.0000.0000][30200]/120
                            10.154.219.82                  100      0 i

        Processed 6 prefixes, 6 paths
        RP/0/RP0/CPU0:genie-router#
    '''}

    golden_parsed_output4 = {
        'vrf': {
            'default': {
                'address_family': {
                    'l2vpn evpn': {
                        'router_identifier': '10.154.219.88',
                        'local_as': 64577,
                        'generic_scan_interval': '60',
                        'non_stop_routing': 'enabled',
                        'table_state': 'active',
                        'table_id': '0x0',
                        'rd_version': 0,
                        'bgp_table_version': 7,
                        'nsr_initial_initsync_version': '3',
                        'nsr_initial_init_ver_status': 'reached',
                        'nsr_issu_sync_group_versions': '7/0',
                        'scan_interval': 60,
                    },
                    'l2vpn evpn RD 10.154.219.82:10100': {
                        'bgp_table_version': 7,
                        'local_router_id': '',
                        'route_distinguisher': '10.154.219.82:10100',
                        'prefixes': {
                            '[1][0000.0000.0000.0000.0000][30100]/120': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '10.154.219.82',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 10.154.219.82:10200': {
                        'bgp_table_version': 7,
                        'local_router_id': '',
                        'route_distinguisher': '10.154.219.82:10200',
                        'prefixes': {
                            '[1][0000.0000.0000.0000.0000][30200]/120': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '10.154.219.82',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 10.154.219.88:10100': {
                        'bgp_table_version': 7,
                        'local_router_id': '',
                        'route_distinguisher': '10.154.219.88:10100',
                        'prefixes': {
                            '[1][0000.0000.0000.0000.0000][20100]/120': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[1][0000.0000.0000.0000.0000][30100]/120': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '10.154.219.82',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                    },
                    'l2vpn evpn RD 10.154.219.88:10200': {
                        'bgp_table_version': 7,
                        'local_router_id': '',
                        'route_distinguisher': '10.154.219.88:10200',
                        'prefixes': {
                            '[1][0000.0000.0000.0000.0000][20200]/120': {
                                'index': {
                                    1: {
                                        'status_codes': '*>',
                                        'next_hop': '0.0.0.0',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                            '[1][0000.0000.0000.0000.0000][30200]/120': {
                                'index': {
                                    2: {
                                        'status_codes': '*>',
                                        'next_hop': '10.154.219.82',
                                        'origin_codes': 'i',
                                    },
                                },
                            },
                        },
                        'processed_prefix': 6,
                        'processed_paths': 6,
                    },
                },
            },
        },
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowBgpL2vpnEvpn(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowBgpL2vpnEvpn(device=self.device)
        parsed_output = obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output)
    
    def test_golden2(self):
        self.device = Mock(**self.golden_output2)
        obj = ShowBgpL2vpnEvpn(device=self.device)
        parsed_output = obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output2)
    
    def test_golden3(self):
        self.device = Mock(**self.golden_output3)
        obj = ShowBgpL2vpnEvpn(device=self.device)
        parsed_output = obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output3)
    
    def test_golden4(self):
        self.device = Mock(**self.golden_output4)
        obj = ShowBgpL2vpnEvpn(device=self.device)
        parsed_output = obj.parse()
        self.maxDiff = None
        self.assertEqual(parsed_output,self.golden_parsed_output4)

# =============================================
# Unit test for 'show bgp l2vpn evpn neighbors'
# =============================================

class test_show_bgp_l2vpn_evpn_all(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        "instance": {
            "all": {
                "vrf": {
                    "default": {
                        "neighbor": {
                            "192.168.99.11": {
                                "remote_as": 65001,
                                "link_state": "internal link",
                                "local_as_as_no": 65001,
                                "local_as_no_prepend": False,
                                "local_as_replace_as": False,
                                "local_as_dual_as": False,
                                "router_id": "192.168.99.11",
                                "session_state": "established",
                                "up_time": "2w5d",
                                "nsr_state": "None",
                                "last_read": "00:00:18",
                                "last_read_before_reset": "00:00:00",
                                "holdtime": 180,
                                "keepalive_interval": 60,
                                "min_acceptable_hold_time": 3,
                                "last_write": "00:00:18",
                                "attempted": 19,
                                "written": 19,
                                "second_last_write": "00:01:18",
                                "second_attempted": 19,
                                "second_written": 19,
                                "last_write_before_reset": "00:00:00",
                                "last_write_attempted": 0,
                                "last_write_written": 0,
                                "second_last_write_before_reset": "00:00:00",
                                "second_last_write_before_attempted": 0,
                                "second_last_write_before_written": 0,
                                "last_write_pulse_rcvd": "Aug 13 23:27:04.895 ",
                                "last_full_not_set_pulse_count": 57338,
                                "last_write_pulse_rcvd_before_reset": "00:00:00",
                                "last_write_thread_event_before_reset": "00:00:00",
                                "last_write_thread_event_second_last": "00:00:00",
                                "last_ka_expiry_before_reset": "00:00:00",
                                "last_ka_expiry_before_second_last": "00:00:00",
                                "last_ka_error_before_reset": "00:00:00",
                                "last_ka_error_ka_not_sent": "00:00:00",
                                "last_ka_start_before_reset": "00:00:00",
                                "last_ka_start_before_second_last": "00:00:00",
                                "precedence": "internet",
                                "non_stop_routing": True,
                                "multiprotocol_capability": "received",
                                "minimum_time_between_adv_runs": 0,
                                "inbound_message": "3",
                                "outbound_message": "3",
                                "address_family": {
                                    "ipv4 unicast": {
                                        "neighbor_version": 177,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 0,
                                        "accepted_prefixes": 26,
                                        "best_paths": 11,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 0,
                                        "prefix_advertised": 6,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 2,
                                        "maximum_prefix_max_prefix_no": 1048576,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 177,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True,
                                        "additional_routes_local_label": "Unicast SAFI"
                                    },
                                    "ipv6 labeled-unicast": {
                                        "neighbor_version": 141,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 0,
                                        "accepted_prefixes": 25,
                                        "best_paths": 1,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 0,
                                        "prefix_advertised": 4,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 1,
                                        "maximum_prefix_max_prefix_no": 131072,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 141,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True
                                    },
                                    "l2vpn evpn": {
                                        "neighbor_version": 367,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 2,
                                        "accepted_prefixes": 83,
                                        "best_paths": 83,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 6,
                                        "cummulative_no_no_policy": 0,
                                        "cummulative_no_failed_rt_match": 45,
                                        "cummulative_no_by_orf_policy": 0,
                                        "cummulative_no_by_policy": 0,
                                        "prefix_advertised": 40,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 12,
                                        "maximum_prefix_max_prefix_no": 2097152,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 367,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True
                                    }
                                },
                                "bgp_session_transport": {
                                    "connection": {
                                        "state": "established",
                                        "connections_established": 1,
                                        "connections_dropped": 0,
                                        "last_reset": "00:00:00"
                                    },
                                    "transport": {
                                        "local_host": "192.168.99.25",
                                        "local_port": "18078",
                                        "if_handle": "0x00000000",
                                        "foreign_host": "192.168.99.11",
                                        "foreign_port": "179"
                                    }
                                }
                            },
                            "192.168.99.12": {
                                "remote_as": 65001,
                                "link_state": "internal link",
                                "local_as_as_no": 65001,
                                "local_as_no_prepend": False,
                                "local_as_replace_as": False,
                                "local_as_dual_as": False,
                                "router_id": "192.168.99.12",
                                "session_state": "established",
                                "up_time": "2w5d",
                                "nsr_state": "None",
                                "last_read": "00:00:18",
                                "last_read_before_reset": "00:00:00",
                                "holdtime": 180,
                                "keepalive_interval": 60,
                                "min_acceptable_hold_time": 3,
                                "last_write": "00:00:18",
                                "attempted": 19,
                                "written": 19,
                                "second_last_write": "00:01:18",
                                "second_attempted": 19,
                                "second_written": 19,
                                "last_write_before_reset": "00:00:00",
                                "last_write_attempted": 0,
                                "last_write_written": 0,
                                "second_last_write_before_reset": "00:00:00",
                                "second_last_write_before_attempted": 0,
                                "second_last_write_before_written": 0,
                                "last_write_pulse_rcvd": "Aug 13 23:27:05.090 ",
                                "last_full_not_set_pulse_count": 57565,
                                "last_write_pulse_rcvd_before_reset": "00:00:00",
                                "last_write_thread_event_before_reset": "00:00:00",
                                "last_write_thread_event_second_last": "00:00:00",
                                "last_ka_expiry_before_reset": "00:00:00",
                                "last_ka_expiry_before_second_last": "00:00:00",
                                "last_ka_error_before_reset": "00:00:00",
                                "last_ka_error_ka_not_sent": "00:00:00",
                                "last_ka_start_before_reset": "00:00:00",
                                "last_ka_start_before_second_last": "00:00:00",
                                "precedence": "internet",
                                "non_stop_routing": True,
                                "multiprotocol_capability": "received",
                                "minimum_time_between_adv_runs": 0,
                                "inbound_message": "3",
                                "outbound_message": "3",
                                "address_family": {
                                    "ipv4 unicast": {
                                        "neighbor_version": 177,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 0,
                                        "accepted_prefixes": 26,
                                        "best_paths": 13,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 0,
                                        "prefix_advertised": 6,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 2,
                                        "maximum_prefix_max_prefix_no": 1048576,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 177,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True,
                                        "additional_routes_local_label": "Unicast SAFI"
                                    },
                                    "ipv6 labeled-unicast": {
                                        "neighbor_version": 141,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 0,
                                        "accepted_prefixes": 25,
                                        "best_paths": 23,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 0,
                                        "prefix_advertised": 4,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 1,
                                        "maximum_prefix_max_prefix_no": 131072,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 141,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True
                                    },
                                    "l2vpn evpn": {
                                        "neighbor_version": 367,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 2,
                                        "accepted_prefixes": 83,
                                        "best_paths": 0,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 6,
                                        "cummulative_no_no_policy": 0,
                                        "cummulative_no_failed_rt_match": 42,
                                        "cummulative_no_by_orf_policy": 0,
                                        "cummulative_no_by_policy": 0,
                                        "prefix_advertised": 40,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 12,
                                        "maximum_prefix_max_prefix_no": 2097152,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 367,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True
                                    }
                                },
                                "bgp_session_transport": {
                                    "connection": {
                                        "state": "established",
                                        "connections_established": 1,
                                        "connections_dropped": 0,
                                        "last_reset": "00:00:00"
                                    },
                                    "transport": {
                                        "local_host": "192.168.99.25",
                                        "local_port": "179",
                                        "if_handle": "0x00000000",
                                        "foreign_host": "192.168.99.12",
                                        "foreign_port": "34287"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    golden_output = {'execute.return_value': '''
        #show bgp l2vpn evpn neighbors
        Tue Aug 13 23:27:23.263 EST

        BGP neighbor is 192.168.99.11
         Remote AS 65001, local AS 65001, internal link
         Remote router ID 192.168.99.11
          BGP state = Established, up for 2w5d
          NSR State: None
          Last read 00:00:18, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:18, attempted 19, written 19
          Second last write 00:01:18, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Aug 13 23:27:04.895 last full not set pulse count 57338
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Multi-protocol capability received
          Neighbor capabilities:
            Route refresh: advertised (old + new) and received (old + new)
            4-byte AS: advertised and received
            Address family IPv4 Unicast: advertised and received
            Address family IPv6 Labeled-unicast: advertised and received
            Address family L2VPN EVPN: advertised and received
          Received 29295 messages, 0 notifications, 0 in queue
          Sent 28818 messages, 0 notifications, 0 in queue
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: IPv4 Unicast
          BGP neighbor version 177
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
            Extended Nexthop Encoding: advertised and received
          Route refresh request: received 0, sent 0
          26 accepted prefixes, 11 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0.
          Prefix advertised 6, suppressed 0, withdrawn 2
          Maximum prefixes allowed 1048576
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 177, Last synced ack version 0
          Outstanding version objects: current 0, max 1, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes
          Advertise routes with local-label via Unicast SAFI

         For Address Family: IPv6 Labeled-unicast
          BGP neighbor version 141
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
          Route refresh request: received 0, sent 0
          25 accepted prefixes, 1 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0.
          Prefix advertised 4, suppressed 0, withdrawn 1
          Maximum prefixes allowed 131072
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 141, Last synced ack version 0
          Outstanding version objects: current 0, max 1, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes

         For Address Family: L2VPN EVPN
          BGP neighbor version 367
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
          Route refresh request: received 0, sent 2
          83 accepted prefixes, 83 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 6.
            No policy: 0, Failed RT match: 45
            By ORF policy: 0, By policy: 0
          Prefix advertised 40, suppressed 0, withdrawn 12
          Maximum prefixes allowed 2097152
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 367, Last synced ack version 0
          Outstanding version objects: current 0, max 2, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes

          Connections established 1; dropped 0
          Local host: 192.168.99.25, Local port: 18078, IF Handle: 0x00000000
          Foreign host: 192.168.99.11, Foreign port: 179
          Last reset 00:00:00

        BGP neighbor is 192.168.99.12
         Remote AS 65001, local AS 65001, internal link
         Remote router ID 192.168.99.12
          BGP state = Established, up for 2w5d
          NSR State: None
          Last read 00:00:18, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:18, attempted 19, written 19
          Second last write 00:01:18, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Aug 13 23:27:05.090 last full not set pulse count 57565
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Multi-protocol capability received
          Neighbor capabilities:
            Route refresh: advertised (old + new) and received (old + new)
            4-byte AS: advertised and received
            Address family IPv4 Unicast: advertised and received
            Address family IPv6 Labeled-unicast: advertised and received
            Address family L2VPN EVPN: advertised and received
          Received 29291 messages, 0 notifications, 0 in queue
          Sent 28818 messages, 0 notifications, 0 in queue
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: IPv4 Unicast
          BGP neighbor version 177
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
            Extended Nexthop Encoding: advertised and received
          Route refresh request: received 0, sent 0
          26 accepted prefixes, 13 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0.
          Prefix advertised 6, suppressed 0, withdrawn 2
          Maximum prefixes allowed 1048576
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 177, Last synced ack version 0
          Outstanding version objects: current 0, max 1, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes
          Advertise routes with local-label via Unicast SAFI

         For Address Family: IPv6 Labeled-unicast
          BGP neighbor version 141
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
          Route refresh request: received 0, sent 0
          25 accepted prefixes, 23 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0.
          Prefix advertised 4, suppressed 0, withdrawn 1
          Maximum prefixes allowed 131072
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 141, Last synced ack version 0
          Outstanding version objects: current 0, max 1, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes

         For Address Family: L2VPN EVPN
          BGP neighbor version 367
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
          Route refresh request: received 0, sent 2
          83 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 6.
            No policy: 0, Failed RT match: 42
            By ORF policy: 0, By policy: 0
          Prefix advertised 40, suppressed 0, withdrawn 12
          Maximum prefixes allowed 2097152
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 367, Last synced ack version 0
          Outstanding version objects: current 0, max 2, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes

          Connections established 1; dropped 0
          Local host: 192.168.99.25, Local port: 179, IF Handle: 0x00000000
          Foreign host: 192.168.99.12, Foreign port: 34287
          Last reset 00:00:00
    '''}

    golden_parsed_output_neighbor = {
        "instance": {
            "all": {
                "vrf": {
                    "default": {
                        "neighbor": {
                            "192.168.99.11": {
                                "remote_as": 65001,
                                "link_state": "internal link",
                                "local_as_as_no": 65001,
                                "local_as_no_prepend": False,
                                "local_as_replace_as": False,
                                "local_as_dual_as": False,
                                "router_id": "192.168.99.11",
                                "session_state": "established",
                                "up_time": "2w5d",
                                "nsr_state": "None",
                                "last_read": "00:00:09",
                                "last_read_before_reset": "00:00:00",
                                "holdtime": 180,
                                "keepalive_interval": 60,
                                "min_acceptable_hold_time": 3,
                                "last_write": "00:00:09",
                                "attempted": 19,
                                "written": 19,
                                "second_last_write": "00:01:09",
                                "second_attempted": 19,
                                "second_written": 19,
                                "last_write_before_reset": "00:00:00",
                                "last_write_attempted": 0,
                                "last_write_written": 0,
                                "second_last_write_before_reset": "00:00:00",
                                "second_last_write_before_attempted": 0,
                                "second_last_write_before_written": 0,
                                "last_write_pulse_rcvd": "Aug 13 04:20:04.721 ",
                                "last_full_not_set_pulse_count": 55044,
                                "last_write_pulse_rcvd_before_reset": "00:00:00",
                                "last_write_thread_event_before_reset": "00:00:00",
                                "last_write_thread_event_second_last": "00:00:00",
                                "last_ka_expiry_before_reset": "00:00:00",
                                "last_ka_expiry_before_second_last": "00:00:00",
                                "last_ka_error_before_reset": "00:00:00",
                                "last_ka_error_ka_not_sent": "00:00:00",
                                "last_ka_start_before_reset": "00:00:00",
                                "last_ka_start_before_second_last": "00:00:00",
                                "precedence": "internet",
                                "non_stop_routing": True,
                                "multiprotocol_capability": "received",
                                "minimum_time_between_adv_runs": 0,
                                "inbound_message": "3",
                                "outbound_message": "3",
                                "address_family": {
                                    "ipv4 unicast": {
                                        "neighbor_version": 177,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 0,
                                        "accepted_prefixes": 26,
                                        "best_paths": 11,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 0,
                                        "prefix_advertised": 6,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 2,
                                        "maximum_prefix_max_prefix_no": 1048576,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 177,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True,
                                        "additional_routes_local_label": "Unicast SAFI"
                                    },
                                    "ipv6 labeled-unicast": {
                                        "neighbor_version": 141,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 0,
                                        "accepted_prefixes": 25,
                                        "best_paths": 1,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 0,
                                        "prefix_advertised": 4,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 1,
                                        "maximum_prefix_max_prefix_no": 131072,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 141,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True
                                    },
                                    "l2vpn evpn": {
                                        "neighbor_version": 367,
                                        "update_group": "0.2",
                                        "filter_group": "0.1",
                                        "refresh_request_status": "No Refresh request being processed",
                                        "route_refresh_request_received": 0,
                                        "route_refresh_request_sent": 2,
                                        "accepted_prefixes": 83,
                                        "best_paths": 83,
                                        "exact_no_prefixes_denied": 0,
                                        "cummulative_no_prefixes_denied": 6,
                                        "cummulative_no_no_policy": 0,
                                        "cummulative_no_failed_rt_match": 45,
                                        "cummulative_no_by_orf_policy": 0,
                                        "cummulative_no_by_policy": 0,
                                        "prefix_advertised": 40,
                                        "prefix_suppressed": 0,
                                        "prefix_withdrawn": 12,
                                        "maximum_prefix_max_prefix_no": 2097152,
                                        "maximum_prefix_warning_only": True,
                                        "maximum_prefix_threshold": "75%",
                                        "maximum_prefix_restart": 0,
                                        "eor_status": "was received during read-only mode",
                                        "last_synced_ack_version": 0,
                                        "last_ack_version": 367,
                                        "additional_paths_operation": "None",
                                        "send_multicast_attributes": True
                                    }
                                },
                                "bgp_session_transport": {
                                    "connection": {
                                        "state": "established",
                                        "connections_established": 1,
                                        "connections_dropped": 0,
                                        "last_reset": "00:00:00"
                                    },
                                    "transport": {
                                        "local_host": "192.168.99.25",
                                        "local_port": "18078",
                                        "if_handle": "0x00000000",
                                        "foreign_host": "192.168.99.11",
                                        "foreign_port": "179"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    golden_output_neighbor = {'execute.return_value': '''
        #show bgp l2vpn evpn neighbors 192.168.99.11
        Tue Aug 13 04:20:13.553 EST

        BGP neighbor is 192.168.99.11
         Remote AS 65001, local AS 65001, internal link
         Remote router ID 192.168.99.11
          BGP state = Established, up for 2w5d
          NSR State: None
          Last read 00:00:09, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:09, attempted 19, written 19
          Second last write 00:01:09, attempted 19, written 19
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  Aug 13 04:20:04.721 last full not set pulse count 55044
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, armed for read, armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Multi-protocol capability received
          Neighbor capabilities:
            Route refresh: advertised (old + new) and received (old + new)
            4-byte AS: advertised and received
            Address family IPv4 Unicast: advertised and received
            Address family IPv6 Labeled-unicast: advertised and received
            Address family L2VPN EVPN: advertised and received
          Received 28148 messages, 0 notifications, 0 in queue
          Sent 27671 messages, 0 notifications, 0 in queue
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered

         For Address Family: IPv4 Unicast
          BGP neighbor version 177
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
            Extended Nexthop Encoding: advertised and received
          Route refresh request: received 0, sent 0
          26 accepted prefixes, 11 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0.
          Prefix advertised 6, suppressed 0, withdrawn 2
          Maximum prefixes allowed 1048576
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 177, Last synced ack version 0
          Outstanding version objects: current 0, max 1, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes
          Advertise routes with local-label via Unicast SAFI

         For Address Family: IPv6 Labeled-unicast
          BGP neighbor version 141
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
          Route refresh request: received 0, sent 0
          25 accepted prefixes, 1 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0.
          Prefix advertised 4, suppressed 0, withdrawn 1
          Maximum prefixes allowed 131072
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 141, Last synced ack version 0
          Outstanding version objects: current 0, max 1, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes

         For Address Family: L2VPN EVPN
          BGP neighbor version 367
          Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
          Route refresh request: received 0, sent 2
          83 accepted prefixes, 83 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 6.
            No policy: 0, Failed RT match: 45
            By ORF policy: 0, By policy: 0
          Prefix advertised 40, suppressed 0, withdrawn 12
          Maximum prefixes allowed 2097152
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was received during read-only mode
          Last ack version 367, Last synced ack version 0
          Outstanding version objects: current 0, max 2, refresh 0
          Additional-paths operation: None
          Send Multicast Attributes

          Connections established 1; dropped 0
          Local host: 192.168.99.25, Local port: 18078, IF Handle: 0x00000000
          Foreign host: 192.168.99.11, Foreign port: 179
          Last reset 00:00:00
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowBgpL2vpnEvpnNeighbors(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowBgpL2vpnEvpnNeighbors(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_neighbor(self):
        self.device = Mock(**self.golden_output_neighbor)
        obj = ShowBgpL2vpnEvpnNeighbors(device=self.device)
        parsed_output = obj.parse(neighbor='192.168.99.11')
        self.assertEqual(parsed_output,self.golden_parsed_output_neighbor)


# ========================================
#  Unit test for 'show bgp vrf-db vrf all'
# ========================================
class TestShowBgpVrfDbVrfAll(unittest.TestCase):
    '''Unit test for 'show bgp vrf-db vrf all' '''

    maxDiff = None
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'vrf':
            {'BTV-nPVR-MULTICAST-IAAS':
                {'afs': ['v4u'],
                'id': '0x60000004',
                'rd': '172.16.2.88:1',
                'ref': 4},
            'ES:GLOBAL':
                {'afs': ['L2evpn'],
                'id': '-',
                'rd': '172.16.2.88:0',
                'ref': 2},
            'EVPN-Multicast-BTV':
                {'afs': ['L2evpn'],
                'id': '-',
                'rd': '172.16.2.88:1000',
                'ref': 2},
            'NOVI-TST':
                {'afs': ['v4u'],
                'id': '0x60000001',
                'rd': '172.16.2.88:0',
                'ref': 4},
            'VPWS:10293':
                {'afs': ['L2evpn'],
                'id': '-',
                'rd': '172.16.2.88:10293',
                'ref': 2},
            'VPWS:2000':
                {'afs': ['L2evpn'],
                'id': '-',
                'rd': '172.16.2.88:2000',
                'ref': 2},
            'VPWS:2078':
                {'afs': ['L2evpn'],
                'id': '-',
                'rd': '172.16.2.88:2078',
                'ref': 2},
            'default':
                {'afs': ['v4u', 'Vv4u', 'v6u', 'Vv6u', 'L2evpn'],
                'id': '0x60000000',
                'rd': '0:0:0',
                'ref': 8},
            'test_ipv6_overlay':
                {'afs': ['v4u', 'v6u'],
                'id': '0x0',
                'rd': '0:0:0',
                'ref': 2}}}

    golden_output1 = {'execute.return_value': '''
        +++ PE1: executing command 'show bgp vrf-db vrf all' +++
        show bgp vrf-db vrf all

        Fri Jun 12 16:57:48.790 EDT
        VRF                              ID          RD              REF AFs
        default                          0x60000000  0:0:0           8   v4u, Vv4u, v6u, 
                                                                         Vv6u, L2evpn
        NOVI-TST                         0x60000001  172.16.2.88:0   4   v4u
        test_ipv6_overlay                0x0         0:0:0           2   v4u, v6u
        BTV-nPVR-MULTICAST-IAAS          0x60000004  172.16.2.88:1   4   v4u
        ES:GLOBAL                        -           172.16.2.88:0   2   L2evpn
        VPWS:2000                        -           172.16.2.88:2000 2   L2evpn
        VPWS:2078                        -           172.16.2.88:2078 2   L2evpn
        VPWS:10293                       -           172.16.2.88:10293 2   L2evpn
        EVPN-Multicast-BTV               -           172.16.2.88:1000 2   L2evpn
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowBgpVrfDbVrfAll(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.device = Mock(**self.golden_output1)
        obj = ShowBgpVrfDbVrfAll(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)


# ===============================================
#  Unit test for 'show bgp l2vpn evpn advertised'
# ===============================================
class TestShowBgpL2vpnEvpnAdvertised(unittest.TestCase):
    '''Unit test for 'show bgp l2vpn evpn advertised' '''

    maxDiff = None
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'neighbor': 
            {'10.100.5.5': 
                {'address_family': 
                    {'l2vpn evpn RD 10.196.7.7:3':
                        {'advertised': 
                            {'[1][0009.0807.0605.0403.0201][0]/120': 
                                {'index': 
                                    {1: 
                                        {'neighbor': 'Local',
                                        'neighbor_router_id': '10.196.7.7',
                                        'flags': ['valid', 'redistributed', 'best', 'import-candidate'],
                                        'rx_path_id': 0,
                                        'local_path_id': 0,
                                        'version': 12,
                                        'inbound_attributes': 
                                            {'community_attributes': 'EXTCOMM',
                                            'nexthop': '0.0.0.0',
                                            'aspath': "",
                                            'origin': 'IGP',
                                            'extended_community': []},
                                        'outbound_attributes': 
                                            {'community_attributes': 'ORG AS EXTCOMM',
                                            'nexthop': '10.196.7.7',
                                            'aspath': "",
                                            'origin': 'IGP',
                                            'extended_community': ['SoO:0.0.0.0:0', 'RT:100:7']}}}}}}}}}}

    golden_output1 = {'execute.return_value': '''
        RP/0/RP0/CPU0:leafZ#sh bgp l2vpn evpn advertised
        Mon Jul 11 19:22:38.235 UTC

        Route Distinguisher: 10.196.7.7:3
         [1][0009.0807.0605.0403.0201][0]/120 is advertised to 10.100.5.5
         Path info:
           neighbor: Local           neighbor router id: 10.196.7.7
           valid  redistributed  best  import-candidate  
           Received Path ID 0, Local Path ID 0, version 12
           Attributes after inbound policy was applied:
            next hop: 0.0.0.0
            EXTCOMM 
            origin: IGP  
            aspath: 
            extended community: 
           Attributes after outbound policy was applied:
            next hop: 10.196.7.7
            ORG AS EXTCOMM 
            origin: IGP  
            aspath: 
            extended community: SoO:0.0.0.0:0 RT:100:7
        '''}


    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowBgpL2vpnEvpnAdvertised(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.device = Mock(**self.golden_output1)
        obj = ShowBgpL2vpnEvpnAdvertised(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)


# ==================================
#  Unit test for 'show bgp sessions'
# ==================================
class TestShowBgpSessions(unittest.TestCase):
    dev = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    golden_parsed_output = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'neighbors': {
                            '10.4.1.1': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '10.36.3.3': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '2001:1:1:1::1': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '2001:3:3:3::3': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                        },
                    },
                    'VRF1': {
                        'neighbors': {
                            '10.4.1.1': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '10.36.3.3': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '2001:1:1:1::1': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '2001:3:3:3::3': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                        },
                    },
                },
            }
        }
    }
        
    golden_output = {'execute.return_value': '''\
        show bgp sessions
        Fri Sep 13 19:10:54.578 UTC

        Neighbor        VRF                   Spk    AS   InQ  OutQ  NBRState     NSRState
        10.4.1.1         default                 0 65000     0     0  Established  None
        10.36.3.3         default                 0 65000     0     0  Established  None
        2001:1:1:1::1   default                 0 65000     0     0  Established  None
        2001:3:3:3::3   default                 0 65000     0     0  Established  None
        10.4.1.1         VRF1                    0 65000     0     0  Established  None
        10.36.3.3         VRF1                    0 65000     0     0  Established  None
        2001:1:1:1::1   VRF1                    0 65000     0     0  Established  None
        2001:3:3:3::3   VRF1                    0 65000     0     0  Established  None
        '''}

    def test_empty(self):
	    self.dev = Mock(**self.empty_output)
	    obj = ShowBgpSessions(device=self.dev)
	    with self.assertRaises(SchemaEmptyParserError):
	        parsed_output = obj.parse()

    def test_golden(self):
        self.dev = Mock(**self.golden_output)
        obj = ShowBgpSessions(device=self.dev)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)


# ===============================================
#  Unit test for 'show bgp instance all sessions'
# ===============================================
class TestShowBgpInstanceAllSessions(unittest.TestCase):
    dev = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'neighbors': {
                            '10.4.1.1': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '10.36.3.3': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '2001:1:1:1::1': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '2001:3:3:3::3': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                        },
                    },
                    'VRF1': {
                        'neighbors': {
                            '10.4.1.1': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '10.36.3.3': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '2001:1:1:1::1': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                            '2001:3:3:3::3': {
                                'spk': 0,
                                'as_number': 65000,
                                'in_q': 0,
                                'out_q': 0,
                                'nbr_state': 'Established',
                                'nsr_state': 'None',
                            },
                        },
                    },
                },
            },
        },
    }
        
    golden_output = {'execute.return_value': '''\
        show bgp instance all sessions
        Sat Sep 14 09:39:17.056 UTC

        BGP instance 0: 'default'
        =========================

        Neighbor        VRF                   Spk    AS   InQ  OutQ  NBRState     NSRState
        10.4.1.1         default                 0 65000     0     0  Established  None
        10.36.3.3         default                 0 65000     0     0  Established  None
        2001:1:1:1::1   default                 0 65000     0     0  Established  None
        2001:3:3:3::3   default                 0 65000     0     0  Established  None
        10.4.1.1         VRF1                    0 65000     0     0  Established  None
        10.36.3.3         VRF1                    0 65000     0     0  Established  None
        2001:1:1:1::1   VRF1                    0 65000     0     0  Established  None
        2001:3:3:3::3   VRF1                    0 65000     0     0  Established  None
        '''}

    def test_empty(self):
	    self.dev = Mock(**self.empty_output)
	    obj = ShowBgpInstanceAllSessions(device=self.dev)
	    with self.assertRaises(SchemaEmptyParserError):
	        parsed_output = obj.parse()

    def test_golden(self):
        self.dev = Mock(**self.golden_output)
        obj = ShowBgpInstanceAllSessions(device=self.dev)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)

if __name__ == '__main__':
    unittest.main()
