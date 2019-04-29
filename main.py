# -*- coding: UTF-8 -*-

import sys
import os
import argparse

from pythinkutils.common.log import g_logger
from pythinkutils.config.Config import g_config



def main():
    g_logger.info(g_config.get("mysql", "host"))

    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, default="pro", help="--env prd/dev")
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()