#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import ImageGrab
import time

time.sleep(3)
im = ImageGrab.grab()
im.save('./temp.jpg')