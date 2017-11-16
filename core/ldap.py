import cherrypy
import logging
from ..config import setup as config

try:
    import ldap3
except ImportError as e:
    logging.exception("We need to install the python3-ldap3 library")


class LDAP:
    server = None
    link = None

    def __init__(self):
        if 'bindUser' in config.LDAP:
            self.link_with_define_user()
        else:
            self.link()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.link is not None:
            self.link.unbind()

    def connect(self, user, password):
        if not self.link.bind():
            return False

        if not self.link.search('dc=ad,dc=cauca,dc=ca', '(uid={0})'.format(user), ldap3.SUBTREE):
            return False

        for entry in self.link.response:
            if self.check_password(entry["dn"], password):
                return True

        return False

    def check_group(self, user, group):
        if not self.link.search('dc=ad,dc=cauca,dc=ca', '(cn={0})'.format(group), ldap3.SUBTREE, attributes=['memberUid']):
            return False

        for entry in self.link.response:
            if user in entry['attributes']['memberUid']:
                return True

    def check_password(self, dn, password):
        self.link.unbind()
        self.link = ldap3.Connection(self.server, user=dn, password=password)

        return self.link.bind()

    def link(self):
        self.server = ldap3.Server(config.LDAP['server'], use_ssl=True)
        self.link = ldap3.Connection(self.server)

    def link_with_define_user(self):
        user = config.LDAP['bindUser']
        password = config.LDAP['bindPassword']

        if 'ldap-user' in cherrypy.session and cherrypy.session['ldap-user']:
            user = cherrypy.session['ldap-user']
            password = cherrypy.session['ldap-password']

        self.server = ldap3.Server(config.LDAP['server'], use_ssl=True)
        self.link = ldap3.Connection(
            self.server,
            user='%s,%s' % (user, config.LDAP['baseDN']),
            password=password)