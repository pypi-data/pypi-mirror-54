#!/usr/bin/env python3
# @Author: carlosgilgonzalez
# @Date:   2019-07-11T23:33:30+01:00
# @Last modified by:   carlosgilgonzalez
# @Last modified time: 2019-10-20T23:57:55+01:00

import ast
import subprocess
import shlex
import time
import serial
import struct
import multiprocessing


name = 'upydevice'


class W_UPYDEVICE:
    def __init__(self, ip_target, password, name=None, bundle_dir=''):
        self.password = password
        self.ip = ip_target
        self.response = None
        self.output = None
        self.bundle_dir = bundle_dir
        self.long_output = []
        self.name = name
        self.dev_class = 'WIRELESS'
        if name is None:
            self.name = 'wupydev_{}'.format(self.ip.split('.')[-1])

    def _send_recv_cmd2(self, cmd):  # test method
        resp_recv = False
        command = shlex.split(cmd)
        while not resp_recv:
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                resp_recv = True
            except Exception as e:
                pass

        stdout = process.communicate()
        try:
            resp = ast.literal_eval(
                stdout[0].decode('utf-8').split('\n')[6][4:-1])
        except Exception as e:
            try:
                resp = stdout[0].decode('utf-8').split('\n')[6][4:-1]
            except Exception as e:
                resp = None

            pass
        return resp, stdout

    def _cmd_r(self, cmd, pt=False):  # test method
        command = 'web_repl_cmd_r  -c "{}" -p {} -t {}'.format(
            cmd, self.password, self.ip)
        resp = self._send_recv_cmd2(command)
        if pt:
            print(resp[0])
        return resp[0]

    def _cmd(self, cmd):  # test method
        command = 'web_repl_cmd -c "{}" -p {} -t {}'.format(
            cmd, self.password, self.ip)
        resp = self.send_recv_cmd2(command)
        return resp[0]

    def _run_command_rl(self, command):  # test method
        end = False
        lines = []
        process = subprocess.Popen(
            shlex.split(command), stdout=subprocess.PIPE)
        while end is not True:
            if process.poll() is None:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip().decode()
                    lines.append(line)
                    if output.strip() == b'### closed ###':
                        end = True
            else:
                break
        rc = process.poll()
        return rc, lines

    def _cmd_rl(self, command, rt=False, evl=True):  # test method
        cmd = command
        cmd_str = 'web_repl_cmd_r -c "{}" -t {} -p {}'.format(
            cmd, self.ip, self.password)
        cmd_resp = self._run_command_rl(cmd_str)
        resp = cmd_resp[1]
        output = []
        for line in resp[6:]:
            if line == '### closed ###':
                pass
            else:
                try:
                    if line[0] == '>':
                        print(line[4:])
                        output.append(line[4:])
                    else:
                        print(line)
                        output.append(line)
                except Exception as e:
                    if len(line) == 0:
                        pass
                    else:
                        print(e)
                        pass
        if rt:
            if evl:
                return ast.literal_eval(output[0])
            else:
                return output

    def cmd(self, command, silent=False, p_queue=None, capture_output=False, bundle_dir=''):  # best method
        cmd_str = self.bundle_dir+'web_repl_cmd_r -c "{}" -t {} -p {}'.format(
            command, self.ip, self.password)
        if bundle_dir is not '':
            cmd_str = bundle_dir+'web_repl_cmd_r -c "{}" -t {} -p {}'.format(
                command, self.ip, self.password)
        # print(group_cmd_str)
        self.long_output = []
        cmd = shlex.split(cmd_str)
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            for i in range(6):
                proc.stdout.readline()
            while proc.poll() is None:
                resp = proc.stdout.readline()[:-1].decode()
                if len(resp) > 0:
                    if resp[0] == '>':
                        if not silent:
                            print(resp[4:])
                        self.response = resp[4:]
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp[4:])
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp[4:]), block=False)
                            except Exception as e:
                                pass
                    else:
                        if not silent:
                            print(resp)
                        self.response = resp
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp)
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp), block=False)
                            except Exception as e:
                                pass
                else:
                    if not silent:
                        print(resp)

        except KeyboardInterrupt:
            time.sleep(1)
            result = proc.stdout.readlines()
            for message in result:
                print(message[:-1].decode())

    def cmd_p(self, command, silent=False, p_queue=None, capture_output=False, bundle_dir=''):  # best method
        cmd_str = self.bundle_dir+'web_repl_cmd_r -c "{}" -t {} -p {}'.format(
            command, self.ip, self.password)
        if bundle_dir is not '':
            cmd_str = bundle_dir+'web_repl_cmd_r -c "{}" -t {} -p {}'.format(
                command, self.ip, self.password)
        # print(group_cmd_str)
        self.long_output = []
        cmd = shlex.split(cmd_str)
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            for i in range(6):
                proc.stdout.readline()
            while proc.poll() is None:
                resp = proc.stdout.readline()[:-1].decode()
                if len(resp) > 0:
                    if resp[0] == '>':
                        if not silent:
                            print('{}:{}'.format(self.name, resp[4:]))
                        self.response = resp[4:]
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp[4:])
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp[4:]), block=False)
                            except Exception as e:
                                pass
                    else:
                        if not silent:
                            print('{}:{}'.format(self.name, resp))
                        self.response = resp
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp)
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp), block=False)
                            except Exception as e:
                                pass
                else:
                    if not silent:
                        print('{}:{}'.format(self.name, resp))
        except KeyboardInterrupt:
            time.sleep(1)
            result = proc.stdout.readlines()
            for message in result:
                print(message[:-1].decode())

    def reset(self, bundle_dir='', output=True):
        reset_cmd_str = self.bundle_dir+'web_repl_cmd_r -c "{}" -t {} -p {}'.format('D',
                                                                                    self.ip, self.password)
        if bundle_dir is not '':
            reset_cmd_str = bundle_dir+'web_repl_cmd_r -c "{}" -t {} -p {}'.format('D',
                                                                                   self.ip, self.password)
        reset_cmd = shlex.split(reset_cmd_str)
        if output:
            print('Rebooting device...')
        try:
            proc = subprocess.Popen(
                reset_cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            for i in range(6):
                proc.stdout.readline()
            while proc.poll() is None:
                resp = proc.stdout.readline()[:-1].decode()
                if len(resp) > 0:
                    if resp[0] == '>':
                        if output:
                            print(resp[4:])
                    else:
                        if output:
                            print(resp)
                else:
                    if output:
                        print(resp)
            if output:
                print('Done!')
        except KeyboardInterrupt:
            time.sleep(1)
            result = proc.stdout.readlines()
            for message in result:
                print(message[:-1].decode())

    def get_output(self):
        try:
            self.output = ast.literal_eval(self.response)
        except Exception as e:
            pass


# S_UPYDEVICE

class S_UPYDEVICE:
    def __init__(self, serial_port, timeout=100, baudrate=9600, name=None, bundle_dir=''):
        self.serial_port = serial_port
        self.returncode = None
        self.timeout = timeout
        self.baudrate = baudrate
        self.name = name
        self.dev_class = 'SERIAL'
        self.bundle_dir = bundle_dir
        if name is None:
            self.name = 'supydev_{}'.format(self.serial_port.split('/')[-1])
        self.picocom_cmd = shlex.split(
            'picocom -port {} -qcx {} -b{}'.format(self.serial_port, self.timeout, self.baudrate))
        self.response = None
        self.response_object = None
        self.output = None
        self.long_output = []
        self.serial = serial.Serial(self.serial_port, self.baudrate)
        self.reset()
        # self._reset()
        self.serial.close()

    def get_output(self):
        try:
            self.output = ast.literal_eval(self.response)
        except Exception as e:
            pass

    def enter_cmd(self):
        if not self.serial.is_open:
            self.serial.open()
        self.serial.write(struct.pack('i', 0x0d))  # CR
        self.serial.close()

    def cmd(self, command, silent=False, p_queue=None, capture_output=False, timeout=None, bundle_dir=''):
        self.long_output = []
        self.picocom_cmd = shlex.split(self.bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
            shlex.quote(command), self.timeout, self.baudrate, self.serial_port))
        if timeout is not None:
            self.picocom_cmd = shlex.split(self.bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                shlex.quote(command), timeout, self.baudrate, self.serial_port))
        if bundle_dir is not '':
            self.picocom_cmd = shlex.split(bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                shlex.quote(command), self.timeout, self.baudrate, self.serial_port))
            if timeout is not None:
                self.picocom_cmd = shlex.split(bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                    shlex.quote(command), timeout, self.baudrate, self.serial_port))
        try:
            proc = subprocess.Popen(
                self.picocom_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            time.sleep(0.2)
            for i in range(2):
                self.enter_cmd()
            while proc.poll() is None:
                resp = proc.stdout.readline()[:-1].decode()
                if len(resp) > 0:
                    if resp[0] == '>':
                        if not silent:
                            print(resp[4:])
                        self.response = resp[4:]
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp[4:])
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp[4:]), block=False)
                            except Exception as e:
                                pass
                    else:
                        if resp != '{}\r'.format(command):
                            if not silent:
                                print(resp)
                        self.response = resp
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp)
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp), block=False)
                            except Exception as e:
                                pass
                else:
                    if not silent:
                        print(resp)

        except KeyboardInterrupt:
            time.sleep(1)
            result = proc.stdout.readlines()
            for message in result:
                print(message[:-1].decode())

    def cmd_p(self, command, silent=False, p_queue=None, capture_output=False, timeout=None, bundle_dir=''):
        self.long_output = []
        self.picocom_cmd = shlex.split(self.bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
            shlex.quote(command), self.timeout, self.baudrate, self.serial_port))
        if timeout is not None:
            self.picocom_cmd = shlex.split(self.bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                shlex.quote(command), timeout, self.baudrate, self.serial_port))
        if bundle_dir is not '':
            self.picocom_cmd = shlex.split(bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                shlex.quote(command), self.timeout, self.baudrate, self.serial_port))
            if timeout is not None:
                self.picocom_cmd = shlex.split(bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                    shlex.quote(command), timeout, self.baudrate, self.serial_port))
        try:
            proc = subprocess.Popen(
                self.picocom_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            time.sleep(0.2)
            for i in range(2):
                self.enter_cmd()
            while proc.poll() is None:
                resp = proc.stdout.readline()[:-1].decode()
                if len(resp) > 0:
                    if resp[0] == '>':
                        if not silent:
                            print('{}:{}'.format(self.name, resp[4:]))
                        self.response = resp[4:]
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp[4:])
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp[4:]), block=False)
                            except Exception as e:
                                pass
                    else:
                        if resp != '{}\r'.format(command):
                            if not silent:
                                print('{}:{}'.format(self.name, resp))
                        self.response = resp
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp)
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp), block=False)
                            except Exception as e:
                                pass
                else:
                    if not silent:
                        print('{}:{}'.format(self.name, resp))

        except KeyboardInterrupt:
            time.sleep(1)
            result = proc.stdout.readlines()
            for message in result:
                print(message[:-1].decode())

    def reset(self, output=True):
        if output:
            print('Rebooting upydevice...')
        if not self.serial.is_open:
            self.serial.open()
        # time.sleep(1)
        while self.serial.inWaiting() > 0:
            self.serial.read()
        # print(self.serial.inWaiting())
        # time.sleep(1)
        self.serial.write(struct.pack('i', 0x0d))
        self.serial.write(struct.pack('i', 0x04))  # EOT
        self.serial.write(struct.pack('i', 0x0d))  # CR
        self.serial.flush()
        # print(self.serial.inWaiting())
        while self.serial.inWaiting() > 0:
            self.serial.read()
        # print(self.serial.inWaiting())
        self.serial.write(struct.pack('i', 0x0d))
        # time.sleep(1)
        self.serial.close()
        if output:
            print('Done!')


# PYBOARD


class PYBOARD:
    def __init__(self, serial_port, timeout=100, baudrate=9600, name=None, bundle_dir=''):
        self.serial_port = serial_port
        self.returncode = None
        self.timeout = timeout
        self.baudrate = baudrate
        self.picocom_cmd = None
        self.response = None
        self.response_object = None
        self.name = name
        self.dev_class = 'SERIAL'
        self.bundle_dir = bundle_dir
        if name is None:
            self.name = 'pyboard_{}'.format(self.serial_port.split('/')[-1])
        self.output = None
        self.long_output = []
        self.serial = serial.Serial(self.serial_port, self.baudrate)
        self.reset(output=False)
        self.reset(output=False)
        # self.serial.close()
        for i in range(3):
            self.enter_cmd()

    def get_output(self):
        try:
            self.output = ast.literal_eval(self.response)
        except Exception as e:
            pass

    def enter_cmd(self):
        if not self.serial.is_open:
            self.serial.open()
        self.serial.write(struct.pack('i', 0x0d))  # CR
        # self.serial.close()

    def cmd(self, command, out_print=True, p_queue=None, capture_output=False, silent=False, timeout=None, bundle_dir=''):
        out_print = not silent
        self.long_output = []
        self.picocom_cmd = shlex.split(self.bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
            shlex.quote(command), self.timeout, self.baudrate, self.serial_port))
        if timeout is not None:
            self.picocom_cmd = shlex.split(self.bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                shlex.quote(command), timeout, self.baudrate, self.serial_port))
        if bundle_dir is not '':
            self.picocom_cmd = shlex.split(bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                shlex.quote(command), self.timeout, self.baudrate, self.serial_port))
            if timeout is not None:
                self.picocom_cmd = shlex.split(bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                    shlex.quote(command), timeout, self.baudrate, self.serial_port))
        try:
            proc = subprocess.Popen(
                self.picocom_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            time.sleep(0.05)  # KEY FINE TUNNING
            for i in range(2):
                self.enter_cmd()
            while proc.poll() is None:
                resp = proc.stdout.readline()[:-1].decode()
                if len(resp) > 0:
                    if resp[0] == '>':
                        if out_print:
                            print(resp[4:])
                        self.response = resp[4:]
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp[4:])
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp[4:]), block=False)
                            except Exception as e:
                                pass
                    else:
                        if resp != '{}\r'.format(command):
                            if out_print:
                                print(resp)
                        self.response = resp
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp)
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp), block=False)
                            except Exception as e:
                                pass
                else:
                    print(resp)

            while self.serial.inWaiting() > 0:
                self.serial.read()

        except KeyboardInterrupt:
            time.sleep(1)
            result = proc.stdout.readlines()
            for message in result:
                print(message[:-1].decode())

    def cmd_p(self, command, out_print=True, p_queue=None, capture_output=False, silent=False, timeout=None, bundle_dir=''):
        out_print = not silent
        self.long_output = []
        self.picocom_cmd = shlex.split(self.bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
            shlex.quote(command), self.timeout, self.baudrate, self.serial_port))
        if timeout is not None:
            self.picocom_cmd = shlex.split(self.bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                shlex.quote(command), timeout, self.baudrate, self.serial_port))
        if bundle_dir is not '':
            self.picocom_cmd = shlex.split(bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                shlex.quote(command), self.timeout, self.baudrate, self.serial_port))
            if timeout is not None:
                self.picocom_cmd = shlex.split(bundle_dir+'picocom -t {} -qx {} -b{} {}'.format(
                    shlex.quote(command), timeout, self.baudrate, self.serial_port))
        try:
            proc = subprocess.Popen(
                self.picocom_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            time.sleep(0.05)  # KEY FINE TUNNING
            for i in range(2):
                self.enter_cmd()
            while proc.poll() is None:
                resp = proc.stdout.readline()[:-1].decode()
                if len(resp) > 0:
                    if resp[0] == '>':
                        if out_print:
                            print('{}:{}'.format(self.name, resp[4:]))
                        self.response = resp[4:]
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp[4:])
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp[4:]), block=False)
                            except Exception as e:
                                pass
                    else:
                        if resp != '{}\r'.format(command):
                            if out_print:
                                print('{}:{}'.format(self.name, resp))
                        self.response = resp
                        self.get_output()
                        if capture_output:
                            self.long_output.append(resp)
                        if p_queue is not None:
                            try:
                                p_queue.put(ast.literal_eval(resp), block=False)
                            except Exception as e:
                                pass
                else:
                    print('{}:{}'.format(self.name, resp))

            while self.serial.inWaiting() > 0:
                self.serial.read()

        except KeyboardInterrupt:
            time.sleep(1)
            result = proc.stdout.readlines()
            for message in result:
                print(message[:-1].decode())

    def reset(self, output=True):
        if output:
            print('Rebooting pyboard...')
        if not self.serial.is_open:
            self.serial.open()
        # time.sleep(1)
        while self.serial.inWaiting() > 0:
            self.serial.read()
        # print(self.serial.inWaiting())
        # time.sleep(1)
        self.serial.write(struct.pack('i', 0x0d))
        self.serial.write(struct.pack('i', 0x04))  # EOT
        self.serial.write(struct.pack('i', 0x0d))  # CR
        self.serial.flush()
        # print(self.serial.inWaiting())
        while self.serial.inWaiting() > 0:
            self.serial.read()
        # print(self.serial.inWaiting())
        self.serial.write(struct.pack('i', 0x0d))
        # time.sleep(1)
        # self.serial.close()
        if output:
            print('Done!')


class GROUP:
    def __init__(self, devs=[None], name=None):
        self.name = name
        self.devs = {dev.name: dev for dev in devs}
        self.dev_process_raw_dict = None
        self.output = None
        self.output_queue = {dev.name: multiprocessing.Queue(maxsize=1) for dev in devs}

    def cmd(self, command, group_silent=False, dev_silent=False, ignore=[], include=[]):
        if len(include) == 0:
            include = [dev for dev in self.devs.keys()]
        for dev in include:
            if dev not in ignore:
                if not group_silent:
                    print('Sending command to {}'.format(dev))
                self.devs[dev].cmd(command, silent=dev_silent)
        self.output = {dev: self.devs[dev].output for dev in include}

    def cmd_p(self, command, group_silent=False, dev_silent=False, ignore=[], include=[], blocking=True, id=False):
        if not id:
            self.dev_process_raw_dict = {dev: multiprocessing.Process(target=self.devs[dev].cmd, args=(command, dev_silent, self.output_queue[dev])) for dev in self.devs.keys()}
            if len(include) == 0:
                include = [dev for dev in self.devs.keys()]
            for dev in ignore:
                include.remove(dev)
            if not group_silent:
                print('Sending command to: {}'.format(', '.join(include)))
            for dev in include:
                # self.devs[dev].cmd(command, silent=dev_silent)
                self.dev_process_raw_dict[dev].start()

            while blocking:
                dev_proc_state = [self.dev_process_raw_dict[dev].is_alive() for dev in self.dev_process_raw_dict.keys()]
                if all(state is False for state in dev_proc_state):
                    time.sleep(0.1)
                    if not group_silent:
                        print('Done!')
                    break

            try:
                self.output = {dev: self.output_queue[dev].get(timeout=2) for dev in include}
            except Exception as e:
                pass
            for dev in include:
                self.devs[dev].output = self.output[dev]
        else:
            self.dev_process_raw_dict = {dev: multiprocessing.Process(target=self.devs[dev].cmd_p, args=(command, dev_silent, self.output_queue[dev])) for dev in self.devs.keys()}
            if len(include) == 0:
                include = [dev for dev in self.devs.keys()]
            for dev in ignore:
                include.remove(dev)
            if not group_silent:
                print('Sending command to: {}'.format(', '.join(include)))
            for dev in include:
                # self.devs[dev].cmd(command, silent=dev_silent)
                self.dev_process_raw_dict[dev].start()

            while blocking:
                dev_proc_state = [self.dev_process_raw_dict[dev].is_alive() for dev in self.dev_process_raw_dict.keys()]
                if all(state is False for state in dev_proc_state):
                    time.sleep(0.1)
                    if not group_silent:
                        print('Done!')
                    break

            try:
                self.output = {dev: self.output_queue[dev].get(timeout=2) for dev in include}
            except Exception as e:
                pass
            for dev in include:
                self.devs[dev].output = self.output[dev]

    def reset(self, group_silent=False, output_dev=True, ignore=[], include=[]):
        if len(include) == 0:
            include = [dev for dev in self.devs.keys()]
        for dev in include:
            if dev not in ignore:
                if not group_silent:
                    print('Rebooting {}'.format(dev))
                self.devs[dev].reset(output=output_dev)
