"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_archive(host):
    """Verify that the archive package repositories were added."""
    distribution = host.system_info.distribution
    codename = host.system_info.codename

    supported_distributions = ["debian"]
    # List all supported releases here
    supported_releases = ["buster"]

    # The archive package repos should be present for any Debian release
    # found in supported_releases.
    if distribution in supported_distributions:
        cmd = host.run("apt update")
        assert cmd.rc == 0

        if codename in supported_releases:
            assert f"archive.debian.org/debian {codename}" in cmd.stdout
        else:
            assert f"archive.debian.org/debian {codename}" not in cmd.stdout
