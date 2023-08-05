# -*- coding: utf-8 -*-
"""
Package Open Source functionality of Moler.
"""
__author__ = 'Grzegorz Latuszek, Marcin Usielski, Michal Ernst'
__copyright__ = 'Copyright (C) 2018-2019, Nokia'
__email__ = 'grzegorz.latuszek@nokia.com, marcin.usielski@nokia.com, michal.ernst@nokia.com'

from moler.config import devices as devices_config
from moler.instance_loader import create_instance_from_class_fullname
from moler.helpers import copy_list
from moler.exceptions import WrongUsage


class DeviceFactory(object):
    _devices = {}

    @classmethod
    def create_all_devices(cls):
        for device_name in devices_config.named_devices:
            cls.get_device(name=device_name)

    @classmethod
    def get_device(cls, name=None, device_class=None, connection_desc=None, connection_hops=None, initial_state=None,
                   establish_connection=True):
        """
        Return connection instance of given io_type/variant.

        :param name: name of device defined in configuration.
        :param device_class: 'moler.device.unixlocal', 'moler.device.unixremote', ...
        :param connection_desc: 'io_type' and 'variant' of device connection.
        :param connection_hops: connection hops to create device SM.
        :param initial_state: initial state for device e.g. UNIX_REMOTE.
        :param establish_connection: True to open connection, False if it does not matter.
        :return: requested device.
        """
        if (not name) and (not device_class):
            raise WrongUsage("Provide either 'name' or 'device_class' parameter (none given)")
        if name and device_class:
            raise WrongUsage("Use either 'name' or 'device_class' parameter (not both)")

        if name in cls._devices.keys():
            dev = cls._devices[name]
            if establish_connection and not dev.is_established():
                dev.goto_state(state=dev.initial_state)
        else:
            dev = cls._create_device(name=name, device_class=device_class, connection_desc=connection_desc,
                                     connection_hops=connection_hops, initial_state=initial_state,
                                     establish_connection=establish_connection)
        return dev

    @classmethod
    def get_devices_by_type(cls, device_type):
        """
        Returns list of devices filtered by device_type.

        :param device_type: type of device. If None then return all devices.
        :return: List of devices. Can be an empty list.
        """
        if device_type is None:
            devices = copy_list(src=cls._devices.values(), deep_copy=False)
        else:
            devices = list()
            for device in cls._devices.values():
                if isinstance(device, device_type):
                    devices.append(device)
        return devices

    @classmethod
    def _try_select_device_connection_desc(cls, device_class, connection_desc):
        if connection_desc is None:
            connection_desc = devices_config.default_connection
        if connection_desc is None:
            whats_wrong = "No connection_desc selected"
            selection_method = "directly or via configuration"
            raise KeyError("{} ({}) for '{}' connection".format(whats_wrong,
                                                                selection_method,
                                                                device_class))
        return connection_desc

    @classmethod
    def _try_take_named_device_params(cls, name, device_class, connection_desc, connection_hops, initial_state):
        if name:
            if name not in devices_config.named_devices:
                whats_wrong = "was not defined inside configuration"
                raise KeyError("Device named '{}' {}".format(name, whats_wrong))
            device_class, connection_desc, connection_hops, initial_state = devices_config.named_devices[name]

        return device_class, connection_desc, connection_hops, initial_state

    @classmethod
    def _clear(cls):
        for device in cls._devices.values():
            del device
        cls._devices = {}

    @classmethod
    def _create_device(cls, name, device_class, connection_desc, connection_hops, initial_state, establish_connection):
        """
        Creates and returns connection instance of given io_type/variant.

        :param name: name of device defined in configuration.
        :param device_class: 'moler.device.unixlocal', 'moler.device.unixremote', ...
        :param connection_desc: 'io_type' and 'variant' of device connection.
        :param connection_hops: connection hops to create device SM.
        :param initial_state: initial state for device e.g. UNIX_REMOTE.
        :param establish_connection: True to open connection, False if it does not matter.
        :return: requested device.
        """
        if connection_hops is not None:
            if "CONNECTION_HOPS" not in connection_hops.keys():
                new_connection_hops = dict()
                new_connection_hops["CONNECTION_HOPS"] = connection_hops

                connection_hops = new_connection_hops

        if not establish_connection:
            initial_state = None
        device_class, connection_desc, connection_hops, initial_state = cls._try_take_named_device_params(
            name, device_class, connection_desc, connection_hops, initial_state)
        if device_class and (not connection_desc):
            connection_desc = cls._try_select_device_connection_desc(device_class, connection_desc)

        constructor_parameters = {
            "name": name,
            "io_type": connection_desc["io_type"],
            "variant": connection_desc["variant"],
            "sm_params": connection_hops,
            "initial_state": initial_state
        }
        device = create_instance_from_class_fullname(class_fullname=device_class,
                                                     constructor_parameters=constructor_parameters)

        if establish_connection:
            device.goto_state(state=device.initial_state)

        if name:
            cls._devices[name] = device
        else:
            cls._devices[device.name] = device

        return device
