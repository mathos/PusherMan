__author__ = 'mathos'


class ManagerBase(object):

    def __init__(self, environment_dict):
        """
        Sets up an instances, passes in environment info
        """

    def needs_update(self):
        """
        Determines if an update is needed
        """
        pass

    def update(self):
        """
        Preform Update
        """
        pass

    def needs_installed(self):
        """
        Determine if installed
        """
        pass

    def install(self):
        """
        Installs
        """
        pass

    def pkg_management(self):
        """
        Return list of packages to have installed
        """
        return []

    def required_installs(self):
        """
        Return a list of other Pusher's that need to run to get going
        """
        return []

    def pip_managment(self):
        """
        Return a list of python packages to pip install
        """
        return []

    def config_sync(self):
        """
        Config script sync
        """
        pass

    def is_running(self):
        """
        Determines that the proecess is running
        """
        pass

    def start(self):
        """"
        Starts the process
        """
        pass

    def reload(self):
        """"
        Reload/Restart the process
        """
        pass

    def pre_flight_chk_list(self):
        """
        Anything to validate or setup prior to running
        """
        pass

    def post_flight_chk_list(self):
        """
        Anything to validate or setup prior to running
        """
        pass


    @property
    def install_method_order(self):
        """
        A list defining the order of methods to call to install

        The list is made of either:

        - A method
        - A tuple with the method to run, followed by which method to run if a True is returned
            and then which method to perform if it is false

        """
        process = [
            self.required_installs,
            self.pre_flight_chk_list,
            self.pkg_management,
            self.pip_managment,
            (
                self.needs_installed,
                self.install,
                (
                    self.needs_update,
                    self.update,
                    self.config_sync
                )
            ),
            (self.is_running, self.reload, self.start),
            self.post_flight_chk_list
        ]
        return process