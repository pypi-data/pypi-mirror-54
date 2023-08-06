#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
"""
import json
import os
import socket
import sys
import time
import traceback
# noinspection PyProtectedMember
from ipaddress import ip_network, ip_address, _BaseAddress, _BaseNetwork
from multiprocessing import current_process, Event

import dns.zone

import logbook
import requests

from keychest_agent.config import KCConfig
from keychest_agent.logger import logger, TCPHandler
from keychest_agent.misc import TlsUtils, DNSUtils, ControlUtils
from keychest_agent.proxy import AgentProxy
from keychest_agent.threadpool import DiscoveryPool, test_ip
from keychest_agent.security import Security

__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@keychest.net'
__status__ = 'Development'


class Agent(object):

    def __init__(self, args):
        self.banned_space = []
        self.permitted_space = []  # list of pairs
        self.counter = 0
        self.config = None
        self.last_result = 0
        self.args = args
        self.config_ready = False
        self.log_dispatcher_thread = None
        self.logger_stop_event = Event()
        self.active_proxies = {}
        self.host_inventory = {}
        self.proxy_ports = []
        self.init_config()
        self.update_proxy_range()

    def update_proxy_range(self):
        proxy_range = KCConfig.config.agent_proxy_ports
        if isinstance(proxy_range, list):
            self.proxy_ports = []
            for _port in proxy_range:
                if isinstance(_port, int) and (_port > 1024) and (_port < 65536):
                    self.proxy_ports.append(_port)
        else:
            proxy_range = str(proxy_range)
            _split = proxy_range.split('-')
            if len(_split) == 1:
                self.proxy_ports = [int(proxy_range)]
            else:
                self.proxy_ports = list(range(int(_split[0]), int(_split[1]) + 1))

    def run(self):
        pass

    def restart_itself(self):
        # https://github.com/cherrypy/cherrypy/blob/0857fa81eb0ab647c7b59a019338bab057f7748b/
        # cherrypy/process/wspbus.py#L305
        # args = sys.argv[:]
        # self.log('Re-spawning %s' % ' '.join(args))
        #
        # args.insert(0, sys.executable)
        # if sys.platform == 'win32':
        #     args = ['"%s"' % arg for arg in args]
        #
        # os.chdir(_startup_cwd)
        # os.execv(sys.executable, args)
        pass

    def return_code(self, code=0):
        self.last_result = code
        return code

    def init_config(self):
        """
        Initializes configuration
        :return:
        """
        self.config = KCConfig.read_configuration()
        if self.config is None or not self.config.has_nonempty_config():
            sys.stderr.write('Configuration is empty: %s\nCreating a new one ... \n  (review and update '
                             'authentication credentials)\n' % KCConfig.get_config_file_path())
            self.config = KCConfig.default_config()
            KCConfig.write_configuration(self.config)

        self.config_ready = True

        try:
            if not os.path.exists(KCConfig.config.logdir):
                os.makedirs(KCConfig.config.logdir, mode=0o755)
            if not os.path.exists(KCConfig.config.piddir):
                os.makedirs(KCConfig.config.piddir, mode=0o755)
            if not os.path.exists(KCConfig.config.sockdir):
                os.makedirs(KCConfig.config.sockdir, mode=0o755)
            if not os.path.exists(KCConfig.config.rundir):
                os.makedirs(KCConfig.config.rundir, mode=0o755)
        except Exception as ex:
            logger.error("Can't create a config folder", cause=str(ex))

        # clean pid folder contents
        for the_file in os.listdir(KCConfig.config.piddir):
            file_path = os.path.join(KCConfig.config.piddir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as ex:
                logger.error("Can't clean pid folder", cause=str(ex))
                pass
        # let's process IP addresses into an operational form
        self.set_permitted_space()
        self.set_banned_space()
        # also update_proxy_range ....

    def set_permitted_space(self):
        permitted = KCConfig.config.permitted_space
        _step1 = permitted.split(',')

        for _range in _step1:
            # noinspection PyBroadException
            try:
                _range = _range.strip()
                _parts = _range.split(':')
                _is_range = len(_parts[0].split('/')) > 1
                if len(_parts) > 1:
                    _port = int(_parts[1])
                else:
                    _port = 0
                if _is_range:
                    _item = (ip_network(_parts[0]), _port)
                else:
                    _item = (ip_address(_parts[0]), _port)
                self.permitted_space.append(_item)
            except Exception:
                logger.error("The definition of permitted space is incorrect", query=_range)

    def set_banned_space(self):
        banned = KCConfig.config.banned_space
        _step1 = banned.split(',')

        for _range in _step1:
            if len(_range.strip()) == 0:
                continue
            # noinspection PyBroadException
            try:
                _range = _range.strip()
                _parts = _range.split(':')
                _is_range = len(_parts[0].split('/')) > 1
                if len(_parts) > 1:
                    _port = int(_parts[1])
                else:
                    _port = 0
                if _is_range:
                    _item = (ip_network(_parts[0]), _port)
                else:
                    _item = (ip_address(_parts[0]), _port)
                self.banned_space.append(_item)
            except Exception:
                logger.error("The definition of banned space is incorrect", query=_range)

    # noinspection PyUnusedLocal
    @staticmethod
    def setup_logging(level=logbook.DEBUG, true_socket=False):

        if true_socket:
            local_sock = socket.gethostbyname("localhost")
            port = KCConfig.config.internal_socket
            _handler = TCPHandler(None, flush_threshold=1, flush_time=1, ip=local_sock, port=port,
                                  extra_fields={'process': current_process().name})
        else:
            sock_file = os.path.join(os.path.join(KCConfig.config.sockdir, 'logbook.sock'))
            _handler = TCPHandler(sock_file, flush_threshold=1, flush_time=1,
                                  extra_fields={'process': current_process().name})
        # noinspection PyBroadException
        try:
            _handler.pop_application()
        except:
            pass
        _handler.push_application()

    # noinspection PyMethodMayBeStatic
    def do_registration(self):
        """
        We need to register after installation - this is the code
        :return:
        """

        logger.debug("Starting registration request")
        registration = {
            "command": "registration",
            "signature": None,
            "payload": {
                "config": KCConfig.create_config_dict(KCConfig.config.json['config'])
            }
        }
        result = False
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        complete_url = ""
        try:
            # Send data
            # add  the agent_id to the URL
            complete_url = KCConfig.config.control_server
            if complete_url[len(complete_url)-1] != "/":
                complete_url += "/" + KCConfig.config.agent_email
            else:
                complete_url += KCConfig.config.agent_email

            encrypted_registration = Security.secure(registration, KCConfig.config.agent_apikey)
            data_text = json.dumps(encrypted_registration)
            r = requests.post(url=complete_url, data=data_text, headers=headers, timeout=KCConfig.config.rest_timeout)
            reg_res = r.json()
            resp_code = r.status_code
            if resp_code != 200:
                logger.warning("Registration response signals an error", code=resp_code,
                               response=reg_res)
                return result
            # let's process the registration result
            if Security.extract(reg_res, KCConfig.config.agent_apikey) is None:
                logger.error("Decryption failed", query=reg_res)
            else:
                if 'status' in reg_res:
                    if (reg_res['status'] == 'success') and ('data' in reg_res) \
                            and ('email' in reg_res['data']) and ('apikey' in reg_res['data']):
                        # all good, let's do it
                        apikey = reg_res['data']['apikey']
                        email = reg_res['data']['email']
                        name = reg_res['data']['name']
                        KCConfig.config.agent_email = email
                        KCConfig.config.agent_apikey = apikey
                        KCConfig.config.agent_name = name
                        # stop so we can start sending logs with the new
                        time.sleep(8)  # log dispatcher will pickup the new email in less than 5 seconds
                        try:
                            KCConfig.write_configuration(KCConfig.config)
                            KCConfig.read_configuration(force=True)
                            result = True
                        except Exception as ex:
                            logger.error("Failed to store registration data", cause=str(ex),
                                         request=KCConfig.config.to_string())
                    else:
                        logger.error("Registration failed", request=data_text,
                                     response=json.dumps(reg_res))
        except Exception as ex:
            logger.error("Error connecting to control channel", url=complete_url, cause=str(ex))
        finally:
            logger.debug("Registration completed")
            return result

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def do_ping(self, do_discovery):
        """
        We regularly check for updates in the discovery configuration
        :return:
        """

        logger.debug("Starting a regular PING request with configuration check")
        discovery = {
            "command": "ping",
            "signature": None,
            "payload": {
                "config": KCConfig.create_config_dict(KCConfig.config.json['config'])
            }
        }
        result = False
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        complete_url = ""
        try:
            # Send data
            # add  the agent_id to the URL
            complete_url = KCConfig.config.control_server
            if complete_url[len(complete_url)-1] != "/":
                complete_url += "/" + KCConfig.config.agent_email
            else:
                complete_url += KCConfig.config.agent_email

            encrypted_discovery = Security.secure(discovery, KCConfig.config.agent_apikey)
            data_text = json.dumps(encrypted_discovery)
            r = requests.post(url=complete_url, data=data_text, headers=headers, timeout=KCConfig.config.rest_timeout)
            reg_res = r.json()
            resp_code = r.status_code
            if resp_code != 200:
                return result

            # let's process the registration result
            if Security.extract(reg_res, KCConfig.config.agent_apikey) is None:
                logger.error("Decryption failed", query=reg_res)
                return result
            if 'status' in reg_res:
                if (reg_res['status'] == 'success') and ('data' in reg_res):
                    # all good, let's do it - first we may want to check the ip addresses are allowed
                    data = reg_res['data']
                    resolved = []
                    try:
                        if 'config' in data:
                            # we are getting a new config file, let's try to update it
                            if KCConfig.config.local_config:
                                logger.info("Keychest service pushed configuration changes but we manage the configuration locall")
                            else:
                                try:
                                    new_config = KCConfig.create_config_dict(data['config'])
                                    # test if it is for us
                                    if ('agent_email' not in new_config) or new_config['agent_email'] != KCConfig.config.agent_email:
                                        _name = new_config['agent_email'] if 'agent_email' in new_config else "<undefined>"
                                        logger.error("Received configuration for another agent", name=_name)
                                        return  # we should probably stop processing the rest
                                    identical = True
                                    for key, value in new_config.items():
                                        if key in ['git_version', 'agent_email', 'control_server'] or KCConfig.is_local_item(key):
                                            continue
                                        local_value = KCConfig.config.get_config(key)
                                        if local_value != value:
                                            try:
                                                KCConfig.config.set_config(key, value)
                                                new_value = KCConfig.config.get_config(key)
                                                if new_value != value:
                                                    logger.error("Failed update configuration value",
                                                                 name=key)
                                                else:
                                                    identical = False
                                                    logger.info("Configuration value has been updated",
                                                                name=key, old_value=local_value, new_value=new_value)
                                            except Exception as ex:
                                                logger.error("Failed to udpate configuration value - exception",
                                                             name=key, cause=str(ex))
                                    if not identical:
                                        KCConfig.write_configuration(KCConfig.config)
                                    self.set_banned_space()
                                    self.set_permitted_space()
                                except Exception as ex:
                                    logger.error("Error parsing new configuration", cause=str(ex))
                                pass
                            pass

                        # first we process DNS if any is provided -> it will replace IP range scanning
                        if ('dns_file' in data) and (data['dns_file'] is not None):
                            # try to read dns file
                            # the entry can have several paths
                            current_folder = os.getcwd()
                            for each_path in data['dns_file']:
                                # we  get an object
                                filename =  each_path['dns_file_path'] if 'dns_file_path' in each_path else None
                                if filename is None:
                                    logger.error("DNS file path not present", query=each_path)
                                    continue

                                # read the domain if present and normalize - it may be needed if not defined in the file
                                main_domain = each_path['dns_file_domain'] \
                                    if ('dns_file_domain' in each_path) and (each_path['dns_file_domain'] is not None)\
                                    else ""  # type: str
                                if (main_domain is not None) and (len(main_domain.strip()) < 1):
                                    main_domain =  ""
                                if main_domain is not None:
                                    main_domain = main_domain.strip().lower()

                                if os.path.exists(filename):
                                    if os.path.isfile(filename):
                                        try:
                                            # we may not have sufficient privilege to read
                                            open(filename, 'r').close()
                                            if len(main_domain):
                                                zone = dns.zone.from_file(filename, origin=main_domain)
                                            else:
                                                zone = dns.zone.from_file(filename)
                                            # update  origin / main domain
                                            if len(str(zone.origin)) > 1:
                                                main_domain = str(zone.origin).lower()
                                                if main_domain[len(main_domain)-1] == '.':
                                                    main_domain = main_domain[:-1]  # remove trailing dot

                                            name_map = DNSUtils.process_zone(zone, main_domain)
                                            filtered = ControlUtils.filter_banned(self, name_map)
                                            for each_filtered in filtered:
                                                if each_filtered not in resolved:
                                                    resolved.append(each_filtered)

                                        except dns.exception.DNSException as ex:
                                            logger.error("DNS zone file doesn't contain its "
                                                         "origin domain or other DNS-related error",
                                                         query=each_path, cause=str(ex))
                                        except Exception as ex:
                                            logger.error("DNS zone file found but can't be read", cause=str(ex),
                                                         query=str(filename), cwd=current_folder)
                                    else:
                                        logger.error("DNS file path does not point to a regular file",
                                                     query=str(filename), cwd=current_folder)
                                else:
                                    logger.error("DNS file doesn't exist or it can't be read",
                                                 query=str(filename), cwd=current_folder)
                            logger.info("DNS zone file processing completed", count=len(resolved))
                            pass
                        if ('dns_transfer' in data) and (data['dns_transfer'] is not None):  # type: dict
                            # try to do zone transfer
                            dnshost = None
                            dnsdomain = None
                            dnsip =  None
                            # noinspection PyTypeChecker
                            if 'dns_transfer_addr' in data['dns_transfer']:
                                # noinspection PyTypeChecker
                                dnshost = data['dns_transfer']['dns_transfer_addr']
                            # noinspection PyTypeChecker
                            if 'dns_transfer_domain' in data['dns_transfer']:
                                # noinspection PyTypeChecker
                                dnsdomain = data['dns_transfer']['dns_transfer_domain']
                            if dnshost is None:
                                logger.error("Request for DNS zone transfer has incorrect format - dnshost is missing")
                            if dnsdomain is None:
                                logger.error("Request for DNS zone transfer has incorrect format - dnsdomain is missing")

                            # let's check the host name first - we will run DNS queries against it
                            try:
                                dnsip = socket.gethostbyname(dnshost)
                            except Exception as ex:
                                logger.error("DNS server name provided is invalid", query=dnshost, cause=str(ex))

                            if dnshost and dnsdomain and dnsip:
                                # let's try the zone transfer
                                try:
                                    zone = dns.zone.from_xfr(dns.query.xfr(dnsip, dnsdomain))
                                    logger.info("DNS zone transfer completed")
                                    if len(str(zone.origin)) > 1:
                                        dnsdomain = str(zone.origin).lower()
                                        if dnsdomain[len(dnsdomain) - 1] == '.':
                                            dnsdomain = dnsdomain[:-1]  # remove trailing dot

                                    name_map = DNSUtils.process_zone(zone, dnsdomain)
                                    filtered = ControlUtils.filter_banned(self, name_map)
                                    for each_filtered in filtered:
                                        if each_filtered not in resolved:
                                            resolved.append(each_filtered)
                                    logger.info("DNS transfer completed and processed",
                                                count=len(filtered), total=len(resolved))
                                except Exception as ex:
                                    logger.error("DNS zone transfer request failed", host=dnsip,
                                                 domain=dnsdomain, cause=str(ex))

                            # at this point, name_map has a processed DNS zone records - let's copy it over to a
                            # result array while applying restrictions
                            #
                            # #  and let's send the results back
                            # network = {
                            #     "command": "network",
                            #     "signature": None,
                            #     "payload": {
                            #         "target": resolved
                            #     }
                            # }
                            # headers = {'Content-type': 'application/json'}
                            # try:
                            #     # Send data
                            #     # add  the agent_id to the URL
                            #     complete_url = os.path.join(KCConfig.config.control_server,
                            #                                 KCConfig.config.agent_email)
                            #     data_text = json.dumps(network)
                            #     r = requests.post(url=complete_url, data=data_text, headers=headers)
                            #     reg_res = r.json()
                            # except Exception as ex:
                            #     logger.error("Failed to send network nodes", response=reg_res, cause=str(ex))

                            pass
                        if (('ip_range' in data) and (len(data['ip_range']) > 0)) or (len(resolved) > 0):
                            resolved_done = []
                            # option 1 -> no DNS resolved, we will do a brute IP range test
                            if ('ip_range' in data) and (resolved == []):
                                # iterate over data items
                                pool = DiscoveryPool(KCConfig.config.discovery_threads)
                                time_now = time.time()
                                for each_range in data['ip_range']:
                                    if 'network' in each_range:
                                        port = each_range['port']
                                        # noinspection PyBroadException
                                        try:
                                            network = ip_network(each_range['network'], False)
                                            pass
                                        except Exception:
                                            continue
                                        for _each_ip in list(network):
                                            # first checked, if this IP address has been processed
                                            proceed = False
                                            if str(_each_ip) in self.host_inventory:
                                                if (time_now - self.host_inventory[str(_each_ip)]) > KCConfig.config.discovery_schedule:
                                                    proceed = True
                                                    logger.debug("Existing IP will be re-tested",
                                                                 ip=str(_each_ip), time=self.host_inventory[str(_each_ip)])
                                                else:
                                                    logger.trace("The IP address has already been tested",
                                                                 ip=str(_each_ip), time=self.host_inventory[str(_each_ip)])
                                            else:
                                                logger.info("New IP address", ip=str(_each_ip))
                                                proceed = True
                                            # then we can do name resolution
                                            if proceed:
                                                # noinspection PyBroadException,PyUnusedLocal
                                                pool.enqueue(test_ip, _each_ip, port, KCConfig.config.connect_timeout)
                                            self.host_inventory[str(_each_ip)] = time_now
                                # work is ready, let's start processing
                                pool.run()
                                time.sleep(2)
                                while not pool.done():
                                    _r = pool.results()
                                    if isinstance(_r, list):
                                        resolved_done += _r
                                    time.sleep(5)
                                # and a final pull
                                _r = pool.results()
                                if isinstance(_r, list):
                                    resolved_done += _r

                                pool.abort(block=True)
                                del pool  # close the pool and all its threads
                                pass
                            elif 'ip_range' in data:  # we did some DNS zone processing -> we use it as a filter
                                _networks = []
                                if 'ip_range' in data:
                                    for each_range in data['ip_range']:
                                        if 'network' in each_range:
                                            port = each_range['port']
                                            # noinspection PyBroadException
                                            try:
                                                network = ip_network(each_range['network'], False)
                                                _networks.append({'net': network, 'port': port})
                                            except Exception:
                                                continue
                                    # test DNS zone items and give them ports
                                    for each_host in resolved:
                                        try:
                                            _ip = ip_address(each_host['ip'])
                                            for each_network in _networks:
                                                if _ip in each_network['net']:
                                                    resolved_done.append({
                                                        'name': each_host['name'],
                                                        'ip': each_host['ip'],
                                                        'port': each_network['port']
                                                    })
                                        except Exception as ex:
                                            logger.warning("Failed to parse/process IP address",
                                                           query=each_host, cause=str(ex))
                                            pass
                            else:  # no IP range - we take everything with port 443
                                for each_host in resolved:
                                    resolved_done.append({
                                        'name': each_host['name'],
                                        'ip': each_host['ip'],
                                        'port': KCConfig.config.default_port
                                    })
                                pass
                            # now we need to send data back
                            network = {
                                "command": "network",
                                "signature": None,
                                "payload": {
                                    "target": resolved_done
                                }
                            }
                            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
                            try:
                                # Send data
                                # add  the agent_id to the URL
                                complete_url = KCConfig.config.control_server
                                if complete_url[len(complete_url) - 1] != "/":
                                    complete_url += "/" + KCConfig.config.agent_email
                                else:
                                    complete_url += KCConfig.config.agent_email

                                encrypted_network = Security.secure(network, KCConfig.config.agent_apikey)
                                data_text = json.dumps(network)
                                r = requests.post(url=complete_url, data=data_text,
                                                  headers=headers, timeout=KCConfig.config.rest_timeout)
                                reg_res = r.json()
                                resp_code = r.status_code
                                if resp_code != 200:
                                    logger.warning("Error when sending a list of resolved addresses to Keychest",
                                                   code=resp_code, response=reg_res)
                                    result = False
                                    return result
                            except Exception as ex:
                                logger.error("Failed to send network nodes", response=reg_res, cause=str(ex))
                                result = False
                        if 'ldap_pull' in data:
                            # try to pull certificate data from ldap
                            pass
                        if 'ad_pull' in data:
                            # try to pull data from AD
                            # noinspection PyTypeChecker
                            if (KCConfig.config.ad_password is None) or (KCConfig.config.ad_user is None):
                                logger.error("Request for AD access without username or password in local config file")
                            elif 'adhost' not in data['ad_pull']:
                                logger.error("Request for AD access does not contain the host name")
                            else:
                                adhost = None
                                addomain = None
                                # noinspection PyTypeChecker
                                if 'adhost' in data['ad_pull']:
                                    # noinspection PyUnusedLocal
                                    adhost = data['adhost']
                                # noinspection PyTypeChecker
                                if 'addomain' in data['ad_pull']:
                                    # noinspection PyUnusedLocal
                                    addomain = data['addomain']
                            pass
                        if 'pem_file' in data:
                            # try to read certificates
                            pass
                        result = True
                    except Exception as ex:
                        tb = "; ".join(traceback.format_exc(3).splitlines())
                        logger.error("Failed to process data for discovery", cause=str(ex),
                                     traceback=tb, request=reg_res)
                        result = False
                else:
                    logger.error("Discovery request failed", request=data_text,
                                 response=json.dumps(reg_res))
                    result = False
            else:
                logger.error("Discovery request failed - structure", request=data_text,
                             response=json.dumps(reg_res))
                result = False
        except Exception as ex:
            logger.error("Error connecting to control channel", url=complete_url, ccause=str(ex))
            return result
        finally:
            logger.debug("A regular PING completed")
            return result

    def do_request_jobs(self):
        """
        Send a request for new jobs and return a dictionary keyed by the proxy ports
        :return:
        :rtype: dict
        """

        logger.debug("Requesting new jobs from KeyChest service")
        # get rid of active ports
        threads_stopped = []
        result = None
        for key, value in self.active_proxies.items():
            if not value.is_alive():
                threads_stopped.append(key)
                if key not in self.proxy_ports:
                    self.proxy_ports.append(key)  # return the port to the pool of available

        for _thread in threads_stopped:
            del self.active_proxies[_thread]

        # we should now have a list of free ports

        # create info about the agent
        free_proxies = {
            "command": "jobs",
            "signature": None,
            "payload": {
                "ports": self.proxy_ports,
                "reverse": KCConfig.config.reverse_proxy,
                "timestamp": int(time.time()),
                "counter": self.counter
            }
        }
        self.counter += 1
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        complete_url = ""
        try:
            # Send data
            # add  the agent_id to the URL
            complete_url = KCConfig.config.control_server
            if complete_url[len(complete_url)-1] != "/":
                complete_url += "/" + KCConfig.config.agent_email
            else:
                complete_url += KCConfig.config.agent_email

            encrypted_free_proxies = Security.secure(free_proxies, KCConfig.config.agent_apikey)
            data_text = json.dumps(encrypted_free_proxies)
            r = requests.post(url=complete_url, data=data_text, headers=headers, timeout=KCConfig.config.rest_timeout * 2)
            jobs = r.json()
            resp_code = r.status_code
            if (resp_code != 200) or ('error' in jobs):
                logger.warning("Request for new jobs failed", code=resp_code,
                               response=jobs)
                result = None
                return result
            if Security.extract(jobs, KCConfig.config.agent_apikey) is None:
                logger.error("Decryption failed", query=jobs)
            else:
                if ('status' in jobs) and (jobs['status'] == 'success'):
                    if 'data' in jobs:
                        result = jobs['data']
                    else:
                        logger.warning("Control channel didn't return 'data' item in its response",
                                       response=json.dumps(jobs))
                        result = {}
                else:
                    logger.error("Control channel request failed", request=data_text,
                                 response=json.dumps(jobs))
                    result = None  # signal an error
        except Exception as ex:
            logger.error("Error connecting to control channel", url=complete_url, ccause=str(ex))
        finally:
            logger.debug("Job request completed")
            return result

    # noinspection PyMethodMayBeStatic
    def is_target_allowed(self, target, target_port, permitted_space=None, banned_space=None):
        """
        Checks if the target is in the allowed IP and port range
        :param target:
        :type target: str
        :param target_port:
        :type target_port: int
        :param permitted_space:
        :type permitted_space: list
        :param banned_space:
        :type banned_space: list
        :return:
        :rtype: bool
        """

        if ((permitted_space is None) or len(permitted_space) == 0)\
                and ((banned_space is None) or (len(banned_space) == 0)):
            return True

        # noinspection PyBroadException
        try:
            if TlsUtils.is_ip(target):
                _target = target
            else:
                _target = socket.gethostbyname(target)
            # we have an IP address

            for (banned_ip, banned_port) in banned_space:
                if (banned_port > 0) and (banned_port == target_port):
                    if isinstance(banned_ip, _BaseAddress):
                        if ip_address(target) == banned_ip:
                            return False  # banned
                    elif isinstance(banned_ip, _BaseNetwork):
                        if ip_address(target) in banned_ip:
                            return False  # banned

            # now let's check if permitted
            if len(permitted_space) == 0:
                return True
            else:
                permitted = False
                for (permitted_ip, permitted_port) in permitted_space:
                    if (permitted_port == 0) or (permitted_port == target_port):
                        if isinstance(permitted_ip, _BaseAddress):
                            if ip_address(target) == permitted_ip:
                                return True  # banned
                        elif isinstance(permitted_ip, _BaseNetwork):
                            if ip_address(target) in permitted_ip:
                                return False  # banned
                return permitted
        except Exception:
            return False

    # noinspection PyMethodMayBeStatic
    def start_new_proxy(self, port, job, permitted_space=None, banned_space=None):
        """
        This method will launch a new proxy to execute an audit job
        :param banned_space:
        :param permitted_space:
        :param port: for the the upstream proxy - it's from a pool, i.e. it limits number of threads
        :type port: int
        :param job:
        :return:
        :rtype: Union[Thread,None]
        """

        if job['type'] == 'PeriodicIpScanJob':
            target_port = job['port'] if 'port' in job else 443
            proto = job['proto'] if 'proto' in job else 'tcp'
            ip_int_beg = TlsUtils.ip_to_int(job['target']['ip_beg'])
            ip_int_end = TlsUtils.ip_to_int(job['target']['ip_end'])
            target = list(TlsUtils.iter_ips(ip_start_int=ip_int_beg, ip_stop_int=ip_int_end))

            upstream_port = job['upstream_port'] if 'upstream_port' in job else KCConfig.config.audit_server_port
            upstream_ip = job['upstream_host'] if 'upstream_host' in job else KCConfig.config.upstream_host
            upstream = (upstream_ip, upstream_port)
            job_id = job['key']
            send_upstream = json.dumps(job).encode()
            destination = (target, target_port)
            logger.debug("Starting a new proxy to audit a target - PeriodicIpScanJob", target=upstream, id=job_id)
            new_proxy = AgentProxy(proto, upstream, destination, job_id, send_upstream, reverse=True)
            # new_proxy.run()
            new_proxy.start()
            return new_proxy
        elif job['type'] == 'PeriodicObjectJob':
            target_port = job['port'] if 'port' in job else 443
            proto = job['proto'] if 'proto' in job else 'tcp'
            target = job['ip']
            if self.is_target_allowed(target, target_port, permitted_space, banned_space):
                upstream_port = job['upstream_port'] if 'upstream_port' in job else KCConfig.config.audit_server_port
                upstream_ip = job['upstream_ip'] if 'upstream_ip' in job else KCConfig.config.upstream_host
                upstream = (upstream_ip, upstream_port)
                job_id = job['key']
                send_upstream = json.dumps(job).encode()
                destination = (target, target_port)
                logger.debug("Starting a new proxy to audit a target - PeriodicObjectJob", target=upstream, id=job_id)
                new_proxy = AgentProxy(proto, upstream, destination, job_id, send_upstream, reverse=True)
                # new_proxy.run()
                new_proxy.start()
                return new_proxy
            else:
                logger.info("Request for banned IP address", query="%s:%d" % (target, target_port))
                return None
        else:
            return None

    def work_loop(self):

        last_discovery = 0
        last_ping = 0
        last_job_request = 0
        registered = False

        exit_flag = Event()
        while not (registered and KCConfig.config.do_register):
            try:
                # we start a RESTful client = control channel
                if KCConfig.config.agent_email != "dummy@keychest.net":
                    registered = True
                else:
                    registered = False
                while not (registered and KCConfig.config.do_register):
                    if not registered:
                        registered = self.do_registration()
                    else:  # we have a valid email and apikey - let's get cracking
                        registered = True
                        time_now = time.time()
                        if (time_now - last_ping) > KCConfig.config.control_schedule:
                            discovery_interval = (time_now - last_discovery) > KCConfig.config.discovery_schedule
                            if not KCConfig.config.reverse_proxy:
                                logger.error("This agent only supports the proxy mode 'reverse' set to True")
                                discovery_interval = False
                            success = self.do_ping(discovery_interval)
                            logger.debug("Ping completed", result=success)
                            if success:
                                last_ping = time_now
                                if discovery_interval:
                                    logger.debug("Discovery completed", result=success)
                                    last_discovery = time_now

                        # only do the following if in the reverse mode
                        if ((time_now - last_job_request) > KCConfig.config.job_schedule) \
                                and KCConfig.config.reverse_proxy:
                            self.update_proxy_range()
                            jobs = self.do_request_jobs()
                            if isinstance(jobs, dict) and len(jobs) > 0:
                                last_job_request = time.time()
                                for key, value in jobs.items():
                                    try:
                                        new_proxy = self.start_new_proxy(int(key), value)
                                        if new_proxy:
                                            self.active_proxies[int(key)] = new_proxy
                                    except Exception as ex:
                                        logger.error("Can't start a new proxy", cause=str(ex), key=key)
                            elif isinstance(jobs, dict):
                                last_job_request = time.time()  # no job, just update timestamp
                            else:
                                # job request failed
                                pass
                    # wait for next tick - wait smart
                    time_now = time.time()
                    wait1 = KCConfig.config.control_schedule - (time_now - last_ping)
                    wait2 = KCConfig.config.job_schedule - (time_now - last_job_request)
                    if wait1 < 5:
                        wait1 = 5
                    if wait2 < 5:
                        wait2 = 5
                    if wait1 < wait2:
                        logger.debug("Sleeping", delay=wait1)
                        exit_flag.wait(wait1)
                    else:
                        logger.debug("Sleeping", delay=wait2)
                        exit_flag.wait(wait2)
                pass
                # else:
                #     # we start a RESTful server listening for control channel requests
                #     pass
            except Exception as ex:
                tb = "; ".join(traceback.format_exc(5).splitlines())
                logger.error("Exception in the Agent work_loop", cause=str(ex), traceback=tb)

        # if the user requested registration only - signal it out
        return registered and KCConfig.config.do_register

    # noinspection PyMethodMayBeStatic
    def is_banned(self, _each_ip, port=443):
        each_ip = ip_address(_each_ip)
        try:
            for each_net in self.banned_space:
                if isinstance(each_net[0], _BaseAddress):
                    if (each_ip == each_net[0]) and ((port == each_net[1]) or (each_net[1] == 0)):
                        return True
                else:  # it's a network
                    if (each_ip in each_net[0]) and ((port == each_net[1]) or (each_net[1] == 0)):
                        return True

            if len(self.permitted_space) == 0:  # by default, we assume there are no restrictions
                return False
            for each_net in self.permitted_space:
                if isinstance(each_net[0], _BaseAddress):
                    if (each_ip == each_net[0]) and ((port == each_net[1]) or (each_net[1] == 0)):
                        return False
                else:  # it's a network
                    if (each_ip in each_net[0]) and ((port == each_net[1]) or (each_net[1] == 0)):
                        return False

            return True  # not allowed -> banned
        except Exception as ex:
            tb = "; ".join(traceback.format_exc(5).splitlines())
            logger.error("Exception when testing for banned IP addresses",
                         cause=str(ex), traceback=tb)
        return True   # this is the default
