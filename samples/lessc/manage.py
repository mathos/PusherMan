from fabric.api import settings
from fabric.contrib.files import exists
from fabric.operations import sudo
from pusher_man.manager import ManagerBase
from pusher_man.peddlers.package_installer import package_install
import os

__author__ = 'mathos'


class Manage(ManagerBase):

    def __init__(self, environment):

        super(Manage, self).__init__(environment)
        self.environment = environment
        self.current_directory = os.path.dirname(__file__)

    def pkg_management(self):
        """
        Return list of packages to have installed
        """
        return ['nodejs', 'python-software-properties', 'g++', 'make']

    def needs_installed(self):
        """
        Determine if installed
        """
        if exists('/usr/local/bin/lessc'):
            return False
        else:
            return True

    def install(self):
        """
        Installs
        """
        
        if exists('/usr/sbin/node'):
            sudo("apt-get remove -y node")
        if not exists('/usr/local/bin/lessc'):
            with settings(warn_only=True):
                sudo("add-apt-repository -y ppa:chris-lea/node.js")
                sudo("apt-get update", pty=False)
            package_install("nodejs")
            sudo("npm install -g less", pty=False)
            sudo("ln -s /usr/bin/lessc /usr/local/bin/lessc")
  
    #
    # @property
    # def install_method_order(self):
    #     """
    #     A list defining the order of methods to call to install
    #
    #     The list is made of either:
    #
    #     - A method
    #     - A tuple with the method to run, followed by which method to run if a True is returned
    #         and then which method to perform if it is false
    #
    #     """
    #     process = [
    #         (
    #             self.needs_installed,
    #             self.install,
    #             (
    #                 self.needs_update,
    #                 self.update,
    #                 self.config_sync
    #             )
    #         ),
    #         (self.is_running, self.reload, self.start),
    #         self.post_flight_chk_list
    #     ]
    #     return process
