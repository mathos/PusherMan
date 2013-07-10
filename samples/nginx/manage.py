from fabric.api import settings
from fabric.operations import sudo
from pusher_man.manager import ManagerBase
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
        return ['nginx-extras', 'libnet-nslookup-perl']

    def is_running(self):
        """
        Determines that the proecess is running
        """
        with settings(warn_only=True):
            status = sudo('/etc/init.d/nginx status')
            if status is not None and status.find("nginx is running") >= 0:
                return True
            else:
                return False

    def start(self):
        """"
        Starts the process
        """
        print "Start!"
        sudo("/etc/init.d/nginx start")
        sudo("/etc/init.d/nginx status")

    def reload(self):
        """"
        Reload/Restart the process
        """
        sudo("/etc/init.d/nginx restart")
        sudo("/etc/init.d/nginx status")
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
