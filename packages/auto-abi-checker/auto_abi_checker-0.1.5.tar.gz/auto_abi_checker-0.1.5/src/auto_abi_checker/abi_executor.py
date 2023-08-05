#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

import subprocess
from tempfile import mkdtemp
from os import chdir
from os.path import join, isdir
from auto_abi_checker.utils import _check_call, error, info, subinfo, main_step_info


class ABIExecutor():
    def __init__(self, compilation_flags=''):
        self.bin = 'abi-compliance-checker'
        self.ws = mkdtemp()
        self.ws_abi_dump = join(self.ws, 'abi_dumps')
        self.ws_report = join(self.ws, 'compat_reports', 'X_to_X')
        self.report_name = 'test_name_report'
        self.compilation_flags = compilation_flags
        self.no_fail_if_emtpy = False
        self.empty_objects_found = False

    def run(self, orig_src, new_src, report_dir='', no_fail_if_emtpy=False):
        main_step_info("Run abichecker")
        # Use orig value as report name
        self.report_name = orig_src.name
        self.no_fail_if_emtpy = no_fail_if_emtpy
        # if compilation_flags is set respect the value
        if not self.compilation_flags:
            self.compilation_flags = self.get_compilation_flags(
                    orig_src, new_src)
        chdir(self.ws)
        if report_dir:
            if not isdir(report_dir):
                error("The directory to host the report does not exists: " + report_dir)
            self.ws_report = report_dir
        if self.dump(orig_src) != 0:
            error("ABI Dump from " + str(orig_src) + " failed")
        if self.dump(new_src) !=0:
            error("ABI Dump from " + str(new_src) + " failed")
        self.generate_report(orig_src, new_src)

    def get_compilation_flags(self, orig_src, new_src):
        r = list(orig_src.compilation_flags)
        r.extend(x for x in new_src.compilation_flags if x not in r)
        return " ".join(r)

    def get_dump_file(self, src_class):
        return join(self.ws_abi_dump,
                    src_class.name, 'X', 'ABI.dump')

    def get_compat_report_file(self):
        return join(self.ws_report, 'compat_report.html')

    def dump(self, src_class):
        cmd = [self.bin,
               '-l', src_class.name,
               '-dump', src_class.ws_files,
               '-gcc-options', self.compilation_flags]
        print(" - Run '%s'" % ' '.join(cmd))
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode('utf-8')
            if "library objects are not found" in error_msg or \
               "header files are not found" in error_msg:
                self.empty_objects_found = True
                if self.no_fail_if_emtpy:
                    subinfo("Skip error on no headers/objects found")
                    return 0
                error("No headers/objects found in " + str(src_class))
            # If unknown error print it to help user debug
            print("\n" + error_msg)
            return 1

        return 0

    def generate_report(self, orig_src, new_src):
        if self.empty_objects_found:
            msg = "No real report generated since empty dumps were found"
            self.generate_fake_report(msg)
            main_step_info(msg)
            return 0

        result = _check_call([self.bin,
                             '-l', self.report_name,
                             '-report-path', self.get_compat_report_file(),
                             '-old', self.get_dump_file(orig_src),
                             '-new', self.get_dump_file(new_src)])

        if result != 0:
            return result

        main_step_info("Generated: " + self.get_compat_report_file())

    def generate_fake_report(self, msg):
        html_str = """
            <!DOCTYPE html>
            <html>
            <body>

            <h1>API/ABI API compatibility report by auto-abi-checker</h1>

            <p>""" + msg + """</p>

            </body>
            </html>
        """

        report_file = open(self.get_compat_report_file(), "w")
        report_file.write(html_str)
        report_file.close()
