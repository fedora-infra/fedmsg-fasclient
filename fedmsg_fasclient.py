# -*- coding: utf-8 -*-
""" A fedmsg consumer that listens to FAS messages to run fasclient via Ansible

Authors:    Janez Nemanič <janez.nemanic@gmail.com>
            Ralph Bean <rbean@redhat.com>
            Pierre-Yves Chibon <pingou@pingoured.fr>

"""

import pprint
import subprocess
import fedmsg.consumers
import moksha.hub.reactor


class FasClientConsumer(fedmsg.consumers.FedmsgConsumer):

    # Because we are interested in a variety of topics, we tell moksha that
    # we're interested in all of them (it doesn't know how to do complicated
    # distinctions).  But then we'll filter later in our consume() method.
    topic = '*'
    interesting_topics = [
        'org.fedoraproject.prod.fas.group.member.sponsor',
        'org.fedoraproject.prod.fas.group.member.remove',
        'org.fedoraproject.prod.fas.user.update',
    ]

    config_key = 'fasclient.consumer.enabled'

    def __init__(self, hub):
        super(GenACLsConsumer, self).__init__(hub)

        # This is required.  It is the number of seconds that we should wait
        # until we ultimately act on a pkgdb message.
        self.delay = self.hub.config['fasclient.consumer.delay']

        # This is the serial that is passed onto ansible specifying how many
        # hosts to run at the same time.
        self.serial = self.hub.config.get('fasclient.consumer.serial', 3)

        # We use this to manage our state
        self.queued_messages = []

    def consume(self, msg):
        if msg['topic'] not in self.interesting_topics:
            return

        # Only run fasclient if the user changed his/her ssh key in FAS
        if msg['topic'] == 'org.fedoraproject.prod.fas.user.update':
            if 'ssh_key' not in msg['msg']['fields']:
                return

        # Skip the run when certain groups are updated
        if  msg['topic'].startswith('org.fedoraproject.prod.fas.group.member.'):
            if msg['group'] in ['cla_fpca']:
                return

        msg = msg['body']
        self.log.info("Got a message %r" % msg['topic'])

        def delayed_consume():
            if self.queued_messages:
                try:
                    self.action(self.queued_messages)
                finally:
                    # Empty our list at the end of the day.
                    self.queued_messages = []
            else:
                self.log.debug("Woke up, but there were no messages.")

        self.queued_messages.append(msg)

        moksha.hub.reactor.reactor.callLater(self.delay, delayed_consume)

    def action(self, messages):
        self.log.debug("Acting on %s" % pprint.pformat(messages))

        command = '/usr/bin/sudo -i ansible "fasClient -i" all -f %s' % (
            self.serial)
        command = command.split()

        self.log.info("Running %r" % command)
        process = subprocess.Popen(args=command)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            self.log.info("%r was successful" % command)
        else:
            self.log.error("%r exited with %r, stdout: %s, stderr: %s" % (
                command, process.returncode, stdout, stderr))
