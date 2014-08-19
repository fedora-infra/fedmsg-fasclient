# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='fedmsg_fasclient',
    version='0.6',
    description='A fedmsg consumer that runs the fasClient based on fedmsg FAS messages',
    license="LGPLv2+",
    author='Janez Nemanič, Ralph Bean and Pierre-Yves Chibon',
    author_email='admin@fedoraproject.org',
    url='https://github.com/fedora-infra/fedmsg-fasclient',
    install_requires=["fedmsg"],
    packages=[],
    py_modules=['fedmsg_fasclient'],
    entry_points="""
    [moksha.consumer]
    fedmsg_fasclient = fedmsg_fasclient:FasClientConsumer
    """,
)
