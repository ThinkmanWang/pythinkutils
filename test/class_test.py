# -*- coding: UTF-8 -*-

import sys
import os
import abc

class Base(object):

    # @abc.abstractmethod
    def func1(self):
        print("From Base")

    def do(self):
        self.func1()

class Extend(Base):
    # pass
    def func1(self):
        print("From Extend")


if __name__ == '__main__':
    obj = Extend()
    obj.do()