#!/usr/bin/env python3

import cv2

import urllib
import urllib2
import numpy as np
import socket
import sys
import struct



class brops:

    def __init__(self, ip_addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ip_addr, 1234)
        self.streamUrl = 'http://%s:81/stream' % ip_addr
        self.getUrl = 'http://%s:80/control?var=framesize&val=7' % ip_addr
        self.stream = urllib.urlopen(self.streamUrl)
        self.buffer =  b''
        urllib2.urlopen(self.getUrl).read()

    def send_command(self, speed, steer):
        data = struct.pack("<Iii", int(0xDEADBEEF), int(speed), int(steer))
        self.sock.sendto(data, self.server_address)

    def read_image(self):
        self.buffer += self.stream.read(1024)
        image_begin = self.buffer.find(b'\r\n\xff\xd8')
        image_end = self.buffer.find(b'\xff\xd9\r\n')

        if image_begin != -1 and image_end != -1:
            if(image_begin > image_end):
                self.buffer = self.buffer[image_begin:]
                return None
            try:
                jpeg_image  = self.buffer[image_begin+2:image_end+2]
                self.buffer = self.buffer[image_end + 4:]
                cv_image = cv2.imdecode(np.frombuffer(jpeg_image, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('img', cv_image)
                key = cv2.waitKey(1)
                return cv_image
            except Exception as ex:
                print(ex)
                return None
        else:
           return None


