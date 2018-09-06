#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import ImageGrab

im = ImageGrab.grab()
im.save('./temp.jpg')