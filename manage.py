#!/usr/bin/env python
import os
import sys
import environ

if __name__ == '__main__':


    # ensure that we are always using appropriate settings
    ROOT_DIR = environ.Path(__file__) - 1  # (dc_traffic_tickets/config/settings/common.py - 3 = dc_traffic_tickets/)
    APPS_DIR = ROOT_DIR.path('dc_traffic_tickets')
    env = environ.Env()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', env('DJANGO_SETTINGS_MODULE'))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
