import platform
from inqry import system_profiler
from inqry import macdisk


# import sys
# if sys.platform == 'win32':
#   import win32_sysinfo as sysinfo
# elif sys.platform == 'darwin':
#   import mac_sysinfo as sysinfo
# elif 'linux' in sys.platform:
#   import linux_sysinfo as sysinfo
#  etc

def create_specs_from_system_profiler_hardware_output(output):
    return SystemSpecs(output)


def mac_os():
    """
    This function is used as the primary means of obtaining basic Mac
    hardware components.
    """
    return create_specs_from_system_profiler_hardware_output(
        system_profiler.hardware())


def _get_internal_storage():
    disk_list = macdisk.get_all_physical_disks()
    internal_disks = [disk for disk in disk_list if disk.is_internal]
    return internal_disks


def windows():
    """
    This function is used as the primary means of obtaining basic Windows
    machine hardware components.
    """
    pass


class SystemSpecs(object):
    """Represents the machine's system specifications before it's data is used
    to form an asset object.

    A SystemSpecs object should be able to be used to access several system
    profile specs, even if they are not used by the Asset class.

    A SystemSpecs object should also be able to be used the same way,
    regardless of which operating system the specs were generated from"""

    def __init__(self, attributes):
        """TODO"""
        self.os_type = platform.system()
        self.attributes = attributes

    def list_all(self):
        return [self.storage,
                self.name,
                self.model,
                self.serial,
                self.cpu_name,
                self.cpu_speed,
                self.cpu_processors,
                self.cpu_cores,
                self.memory]

    @property
    def storage(self):
        mac_hardware = self.attributes
        mac_hardware['Internal Disks'] = _get_internal_storage()
        return mac_hardware.get('Internal Disks')

    @property
    def serial(self):
        return self.attributes.get('Serial Number (system)')

    @property
    def cpu_name(self):
        hw = self.attributes
        return hw.get('Processor Name')

    @property
    def cpu_processors(self):
        processors = self.attributes.get('Number of Processors')
        return processors

    @property
    def cpu_cores(self):
        cores = self.attributes.get('Total Number of Cores')
        return cores

    @property
    def cpu_speed(self):
        speed = self.attributes.get('Processor Speed')
        return speed

    @property
    def memory(self):
        memory = self.attributes.get('Memory')
        return memory

    @property
    def model(self):
        model = self.attributes.get('Model Identifier')
        return model

    @property
    def name(self):
        name = self.attributes.get('Model Name')
        return name
