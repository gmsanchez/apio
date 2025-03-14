"""Implementation of the Apio system commands"""

# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import re
import sys
import click

from apio import util
from apio import pkg_util
from apio.apio_context import ApioContext


class System:  # pragma: no cover
    """System class. Managing and execution of the system commands"""

    def __init__(self, apio_ctx: ApioContext):

        self.apio_ctx = apio_ctx

    def _lsftdi_fatal_error(self, result: util.CommandResult) -> None:
        """Handles a failure of a 'lsftdi' command. Print message and exits."""
        #
        assert result.exit_code != 0, result
        click.secho(result.out_text)
        click.secho(f"{result.err_text}", fg="red")
        click.secho("Error: the 'lsftdi' command failed.", fg="red")

        # -- A special hint for zadig on windows.
        if self.apio_ctx.is_windows():
            click.secho(
                "\n"
                "[Hint]: did you install the ftdi driver using "
                "'apio drivers --ftdi-install'?",
                fg="yellow",
            )
            sys.exit(1)

    def lsusb(self) -> int:
        """Run the lsusb command. Returns exit code."""

        result = self._run_command("lsusb", silent=False)

        return result.exit_code if result else 1

    def lsftdi(self) -> int:
        """Runs the lsftdi command. Returns exit code."""

        result = self._run_command("lsftdi", silent=True)

        if result.exit_code != 0:
            # -- Print error message and exit.
            self._lsftdi_fatal_error(result)

        click.secho(result.out_text)
        return 0

    def lsserial(self) -> int:
        """List the serial ports. Returns exit code."""

        serial_ports = util.get_serial_ports()
        click.secho(f"Number of Serial devices found: {len(serial_ports)}")

        for serial_port in serial_ports:
            port = serial_port.get("port")
            description = serial_port.get("description")
            hwid = serial_port.get("hwid")
            click.secho(port, fg="cyan")
            click.secho(f"Description: {description}")
            click.secho(f"Hardware info: {hwid}\n")

        return 0

    def get_usb_devices(self) -> list:
        """Return a list of the connected USB devices
         This list is obtained by running the "lsusb" command

         * OUTPUT:  A list of objects with the usb devices
        Ex. [{'hwid':'1d6b:0003'}, {'hwid':'8087:0aaa'}, ...]

        It raises an exception in case of not being able to
        execute the "lsusb" command
        """

        # -- Initial empty usb devices list
        usb_devices = []

        # -- Run the "lsusb" command!
        result = self._run_command("lsusb", silent=True)

        if result.exit_code != 0:
            click.secho(result.out_text)
            click.secho(result.err_text, fg="red")
            raise RuntimeError("Error executing lsusb")

        # -- Get the list of the usb devices. It is read
        # -- from the command stdout
        # -- Ex: [{'hwid':'1d6b:0003'}, {'hwid':'04f2:b68b'}...]
        usb_devices = self._parse_usb_devices(result.out_text)

        # -- Return the devices
        return usb_devices

    def get_ftdi_devices(self) -> list:
        """Return a list of the connected FTDI devices
         This list is obtained by running the "lsftdi" command

         * OUTPUT:  A list of objects with the FTDI devices
        Ex. [{'index': '0', 'manufacturer': 'AlhambraBits',
              'description': 'Alhambra II v1.0A - B07-095'}]

        It raises an exception in case of not being able to
        execute the "lsftdi" command
        """

        # -- Initial empty ftdi devices list
        ftdi_devices = []

        # -- Run the "lsftdi" command.
        result = self._run_command("lsftdi", silent=True)

        # -- Exit if error.
        if result.exit_code != 0:
            self._lsftdi_fatal_error(result)

        # -- Get the list of the ftdi devices. It is read
        # -- from the command stdout
        # -- Ex: [{'index': '0', 'manufacturer': 'AlhambraBits',
        # --      'description': 'Alhambra II v1.0A - B07-095'}]
        ftdi_devices = self._parse_ftdi_devices(result.out_text)

        # -- Return the devices
        return ftdi_devices

        # -- Print error message and exit.

    def _run_command(
        self, command: str, *, silent: bool
    ) -> util.CommandResult:
        """Execute the given system command
        * INPUT:
          * command: Command to execute  (Ex. "lsusb")
          * silent: What to do with the command output
            * False --> Do not print on the console
            * True  --> Print on the console

        * OUTPUT: An ExecResult with the command's outcome.
        """

        # -- Check that the required package exists.
        pkg_util.check_required_packages(self.apio_ctx, ["oss-cad-suite"])

        # -- Set system env for using the packages.
        pkg_util.set_env_for_packages(self.apio_ctx)

        # pylint: disable=fixme
        # TODO: Is this necessary or does windows accepts commands without
        # the '.exe' extension?
        if self.apio_ctx.is_windows():
            command = command + ".exe"

        # -- Set the stdout and stderr callbacks, when executing the command
        # -- Silent mode (True): No callback
        on_stdout = None if silent else self._on_stdout
        on_stderr = None if silent else self._on_stderr

        # -- Execute the command!
        result = util.exec_command(
            command,
            stdout=util.AsyncPipe(on_stdout),
            stderr=util.AsyncPipe(on_stderr),
        )

        # -- Return the result of the execution
        return result

    @staticmethod
    def _on_stdout(line):
        """Callback function. It is executed when the command prints
        information on the standard output
        """
        click.secho(line)

    @staticmethod
    def _on_stderr(line):
        """Callback function. It is executed when the command prints
        information on the standard error
        """
        click.secho(line, fg="red")

    @staticmethod
    def _parse_usb_devices(text: str) -> list:
        """Get a list of usb devices from the input string
        * INPUT: string that contains usb devices
            (Ex. "... 1d6b:0003 ... 8087:0aaa ...")
        * OUTPUT: A list of objects with the usb devices
          Ex. [{'hwid':'1d6b:0003'}, {'hwid':'8087:0aaa'}, ...]
        """

        # -- Build the regular expression for representing
        # -- patterns like '1d6b:0003'
        pattern = r"(?P<hwid>[a-f0-9]{4}:[a-f0-9]{4}?)\s"

        # -- Get the list of strings with that patter
        # -- Ex. ['1d6b:0003','8087:0aaa'...]
        hwids = re.findall(pattern, text)

        # -- Output empty list
        usb_devices = []

        # -- Build the list
        for hwid in hwids:

            # -- Create the Object with the hardware id
            usb_device = {"hwid": hwid}

            # -- Add the object to the output list
            usb_devices.append(usb_device)

        # -- Return the final list
        return usb_devices

    @staticmethod
    def _parse_ftdi_devices(text):
        pattern = r"Number\sof\sFTDI\sdevices\sfound:\s(?P<n>\d+?)\n"
        match = re.search(pattern, text)
        num = int(match.group("n")) if match else 0

        pattern = r".*Checking\sdevice:\s(?P<index>.*?)\n.*"
        index = re.findall(pattern, text)

        pattern = r".*Manufacturer:\s(?P<n>.*?),.*"
        manufacturer = re.findall(pattern, text)

        pattern = r".*Description:\s(?P<n>.*?)\n.*"
        description = re.findall(pattern, text)

        ftdi_devices = []

        for i in range(num):
            ftdi_device = {
                "index": index[i],
                "manufacturer": manufacturer[i],
                "description": description[i],
            }
            ftdi_devices.append(ftdi_device)

        return ftdi_devices
