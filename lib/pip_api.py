import email.parser
import json
import shutil
import time

import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets


class api:
    def __init__(self):
        self.program = "pip"
        # hertz
        self.polling_rate = 10
        # seconds
        self.timeout = 60

        # first thing, check if pip is in PATH
        if not self.check_in_path(self.program):
            raise IOError(self.program + "not found in PATH")

        self.invalidate_cache()

    def check_in_path(self, name):
        """Checks if given name exists in the system PATH"""
        return bool(shutil.which(name))

    def invalidate_cache(self):
        """Deletes the cache"""
        self.all_cache = None
        self.outdated_cache = None
        self.updated_cache = None

    def pip_command_finished(self, return_code):
        """Run when subprocess finishes. Checks response code and sets a variable"""
        # if return code is not 0
        if return_code:
            self.pip_command_data_ready()
            self.process.terminate()
            self.process_finished = True

            raise IOError(
                self.program
                + " command exited with non-zero response code:\n "
                + self.process.readAllStandardError().data().decode()
            )

        # for commands that aren't writing the partial outputs to a widget,
        # force grab all data
        if not self.process_output:
            self.pip_command_data_ready()

        self.process_finished = True

    def pip_command_data_ready(self, output=None):
        """Get new data from the subproccess and direct it to the output,
        and combine with exisitng data"""
        # grab new data and send it output widget
        new_data = self.process.readAll().data().decode()
        # reset timeout
        self.poll_count = 0

        if output:
            output(new_data)

        # add new data to entire output
        self.process_output += new_data

    def run_pip_command(self, command, output=None):
        """Runs a pip command and returns the stdout as a string
        Optionally directs output to a function that is meant to receive new data
        as a string"""

        # clear output and reset finished state
        self.process_output = ""
        self.process_finished = False

        self.process = QtCore.QProcess()

        # optionally provide a function in which to send new output data to
        if output:
            # first write out the run command
            output(self.program + " " + " ".join(command))
            # write out anymore incoming data
            self.process.readyRead.connect(lambda: self.pip_command_data_ready(output))

        self.poll_count = 0

        self.process.finished.connect(self.pip_command_finished)
        self.process.start(self.program, command)

        # check to see if command has finished
        # and process gui events

        while not self.process_finished:
            QtWidgets.QApplication.processEvents()
            time.sleep(1 / self.polling_rate)

            # give up after 20 seconds
            self.poll_count += 1
            if self.poll_count >= self.timeout * self.polling_rate:
                self.process.terminate()
                raise TimeoutError(self.program + " command timeout exceeded")

        return self.process_output

    def get_package_list_from_json(self, json_data):
        """Returns a list of packages from json data"""
        packages = []

        for package in json_data:
            packages.append(package["name"])

        return packages

    def get_package_data_from_command(self, command, output=None):
        """Takes a pip command and runs it, and returns list of dictionaries"""
        # get output as json
        command.append("--format=json")
        # run command
        result = self.run_pip_command(command, output)
        # convert to json
        packages = json.loads(result)
        return packages

    def get_packages(self, skip_cache=False, output=None):
        """Returns list of all installed packages"""
        outdated = self.get_outdated_packages(skip_cache, output)

        QtWidgets.QApplication.processEvents()

        alll = self.get_all_packages(skip_cache, output)
        for package in outdated:
            # remove any packages in all package data that occurs in the outdated list
            alll[:] = [d for d in alll if d.get("name") != package["name"]]
        return outdated + alll

    def get_all_packages(self, skip_cache=False, output=None):
        """Returns json of all packages"""
        command = ["list"]

        if skip_cache or self.all_cache is None:
            # if the cache should be skipped
            # or if the cache shouldn't be skipped, but there is no cache
            packages = self.get_package_data_from_command(command, output)
            self.all_cache = packages

        return self.all_cache

    def get_outdated_packages(self, skip_cache=False, output=None):
        """Returns json of all outdated packages"""
        command = ["list", "-o"]

        if skip_cache or self.outdated_cache is None:
            # if the cache should be skipped
            # or if the cache shouldn't be skipped, but there is no cache
            packages = self.get_package_data_from_command(command, output)
            self.outdated_cache = packages

        return self.outdated_cache

    '''
    def get_updated_packages(self, skip_cache=False, output=None):
        """Returns json of all updated packages"""
        command = ["list", "-u"]
        # this command actually doesn't return beta packages such as black

        if skip_cache or self.updated_cache == None:
            # if the cache should be skipped
            # or if the cache shouldn't be skipped, but there is no cache
            packages = self.get_package_data_from_command(command, output)
            self.updated_cache = packages

        return self.updated_cache
    '''

    def get_package_information(self, package):
        """Returns information about package"""
        command = ["show"]
        command.append(package)

        output = self.run_pip_command(command)
        # the return result is valid email headers
        return email.parser.Parser().parsestr(output)

    def install_packages(self, packages, output=None):
        """Installs a list of packages"""
        command = ["install"]
        command += packages

        self.run_pip_command(command, output)
        self.invalidate_cache()

    def update_packages(self, packages, output=None):
        """Updates a list of packages"""
        command = ["install", "--upgrade"]
        command += packages

        self.run_pip_command(command, output)
        self.invalidate_cache()

    def uninstall_packages(self, packages, output=None):
        """Uninstall a list of packages"""
        command = ["uninstall", "-y"]
        command += packages

        self.run_pip_command(command, output)
        self.invalidate_cache()
