#!/usr/bin/env python3

import cv2

import urllib
import numpy as np
import socket
import sys
import struct


class brops:

    def __init__(self, ip_addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ip_addr, 1234)
        self.streamUrl = 'http://%s:81/stream' % ip_addr
        self.stream = urllib.urlopen(self.streamUrl)
        self.buffer =  b''

    def send_command(self, speed, steer):
        data = struct.pack("<Iii", int(0xDEADBEEF), int(speed), int(steer))
        self.sock.sendto(data, self.server_address)

    def read_image(self):
        self.buffer += self.stream.read(1024)
        image_begin = self.buffer.find(b'\xff\xd8')
        image_end = self.buffer.find(b'\xff\xd9')
        if image_begin != -1 and image_end != -1:
            jpeg_image  = self.buffer[image_begin:image_end+2]
            self.buffer = self.buffer[image_end + 2:]
            cv_image = cv2.imdecode(np.frombuffer(jpeg_image, dtype=np.uint8), cv2.IMREAD_COLOR)

            return cv_image
        else:
           return None


