import os
import sys

cwd = os.getcwd()
sys.path.append(os.getcwd())

import argparse
from fabric.colors import yellow, green, blue
from fabric.context_managers import settings
import configuration as CONFIG
from pusher_config import DEFAULT_PKGS
from peddlers.aws_env import ec2_digger
from peddlers.package_installer import packages_update, package_install

__author__ = 'mathos'


class PusherMan(object):
    self_managing = ['pkg_management']
    ec2_connections = dict()

    def get_systems_info(self):
        return ec2_digger(CONFIG.AWS_API_KEY, CONFIG.AWS_SECRET_KEY)

    def process_step(self, step, if_true_step=None, if_false_step=None):
        if self.process_executer(step):
            if if_true_step is None:
                return
            elif hasattr(if_true_step, '__call__'):
                self.process_executer(if_true_step)
            elif isinstance(if_true_step, tuple):
                self.process_step(if_true_step[0], if_true_step[1], if_true_step[2] if len(if_true_step) == 3 else None)

        else:
            if if_false_step is None:
                return
            elif hasattr(if_false_step, '__call__'):
                self.process_executer(if_false_step)
            elif isinstance(if_false_step, tuple):
                self.process_step(if_false_step[0], if_false_step[1],
                                  if_false_step[2] if len(if_false_step) == 3 else None)

    def process_executer(self, step):
        print "We are digging: "+blue(str(step.__name__).upper(), bold=True)
        print "\n"
        if step.__name__ in self.self_managing:
            if step.__name__ == 'pkg_management':
                self.package_installer(step())
            return True
        else:
            return step()

    def prepare(self):
        packages_update()
        print yellow("Installing pusherman default packages.  Dig?")
        for package in DEFAULT_PKGS:
            print "Installing Package: " + blue(package, bold=True)
            package_install(package)

    def package_installer(self, packages):
        print yellow("Installing packages.  It's going to be funkadelic man.")
        for package in packages:
            print "Installing Package: " + blue(package, bold=True)
            package_install(package)

    def process_pushers(self, server_list, superfly_list, user):

        for server in server_list:
            print "Working on the cool cat: "+blue(server, bold=True)+"\n"
            with settings(host_string=server, key_filename=CONFIG.LOCAL_AWS_KEY_FILE,
                          user=user, connection_attempts=10,
                          aws_key=CONFIG.AWS_API_KEY, aws_secret=CONFIG.AWS_SECRET_KEY):
                self.prepare()
                for superfly in superfly_list:
                    pusher = __import__(superfly + ".manage", fromlist=['Manage'])
                    pusher_man = pusher.Manage(server_list.get(server))

                    for step in pusher_man.install_method_order:
                        if hasattr(step, '__call__'):
                            self.process_executer(step)
                        elif isinstance(step, tuple):
                            self.process_step(step[0], step[1], step[2] if len(step) == 3 else None)


def main():
    parser = argparse.ArgumentParser(description='The Pusher Man!')
    parser.add_argument('install', help="Install")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-T', dest="tag_value", metavar="tag:value",
                       help="Tag and value of instance(s) you want to install on")
    group.add_argument('-H', dest='host', help="Host name if using")
    parser.add_argument('-u', dest='user', default=CONFIG.AWS_AMI_USERNAME, help="User name if using")
    parser.add_argument('install_classes', metavar="pusher_managers", nargs='+',
                        help="Pusher classes you want to install")

    parser_data = parser.parse_args()

    pushing = PusherMan()
    print "\n"

    if parser_data.tag_value is not None:
        server_dict, tag_dict = pushing.get_systems_info()

        server_list = dict()

        tag_name, tag_value = parser_data.tag_value.split(':')
        for server in tag_dict.get(tag_name.lower(), {}).get(tag_value.lower()):
            server_list[server] = server_dict.get(server)

    else:
        server_list = {parser_data.host: {}}

    superfly_list = parser_data.install_classes

    pushing.process_pushers(server_list, superfly_list, parser_data.user)
    print "\n\n"
    print green("Check you later!")


if __name__ == '__main__':
    main()
