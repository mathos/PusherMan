from fabric.colors import yellow
from fabric.operations import sudo, run

__author__ = 'mathos'


def packages_update(sys_type="Ubuntu"):
    """
    Update the packagement libs
    """
    print yellow("Updating the system package manager", bold=True)
    print yellow("Just be cool, man!", bold=True)
    if sys_type == "Ubuntu":
        sudo("apt-get update", pty=False)
    elif sys_type == "Mac":
        run("brew update")


def package_install(package, sys_type='Ubuntu'):
    """
    Installs packages
    """

    if sys_type == "Ubuntu":
        sudo("DEBIAN_FRONTEND=noninteractive apt-get -y install "+package, pty=False)
    elif sys_type == "Mac":
        run("brew install "+package)


