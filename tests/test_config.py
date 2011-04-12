from __future__ import with_statement
from os import path, makedirs, environ
import shutil

from nose.plugins.skip import SkipTest

import _mssql

cdir = path.dirname(__file__)
tmpdir = path.join(cdir, 'tmp')
config_dump_path = path.join(tmpdir, 'freetds-config-dump.txt')

def setup_module():
    if not path.isdir(tmpdir):
        makedirs(tmpdir)

class TestConfig(object):
    def connect(self, **kwargs):
        environ['TDSDUMPCONFIG'] = config_dump_path
        try:
            _mssql.connect(**kwargs)
            assert False
        except _mssql.MSSQLDriverException, e:
            # we get this when the name of the server is not valid
            if 'Connection to the database failed' not in str(e):
                raise
        except _mssql.MSSQLDatabaseException, e:
            # we get this when the name or IP can be obtained but the connection
            # can not be made
            # e.args[0] is currently a tuple, but I think thats a bug
            if e.args[0][0] != 20009:
                raise
        with open(config_dump_path, 'rb') as fh:
            return fh.read()


    def test_config_values(self):
        config_dump = self.connect(
            server='dontnameyourserverthis',
            user = 'bob',
            database = 'tempdb',
            )
        assert 'server_name = <pymssql dynamic>' in config_dump
        assert 'server_host_name = dontnameyourserverthis' in config_dump
        assert 'user_name = bob' in config_dump
        # it would be nice if this was the DB name, see test_dbsetldbname()
        assert 'database = \n' in config_dump
        assert 'port = 1433' in config_dump
        # not sure why 7.1 version is used instead of 8.0 which is the
        # default
        assert 'major_version = 7' in config_dump
        assert 'minor_version = 1' in config_dump

    def test_dbsetldbname(self):
        # sybdb.h defines DBSETLDBNAME, we should try to use that to get
        # the DB in the config dump for debugging purposes
        raise SkipTest # test_dbsetldbname

    def test_tds_protocal_version_42(self):
        config_dump = self.connect(tds_version='4.2')
        assert 'major_version = 4' in config_dump
        assert 'minor_version = 2' in config_dump

    def test_tds_protocal_version_70(self):
        config_dump = self.connect(tds_version='7.0')
        assert 'major_version = 7' in config_dump
        assert 'minor_version = 0' in config_dump

    def test_tds_protocal_version_80(self):
        # why do we get 7.1 if we request 8.0?  The below test fails currently
        # hence the skip
        raise SkipTest # test_tds_protocal_version_80

        config_dump = self.connect(tds_version='8.0')
        assert 'major_version = 8' in config_dump
        assert 'minor_version = 0' in config_dump

    def test_tds_protocal_version_invalid(self):
        try:
            self.connect(tds_version='1.0')
            assert False
        except _mssql.MSSQLException, e:
            assert 'unrecognized tds version: 1.0' == str(e)

    def test_nonstandard_port(self):
        config_dump = self.connect(port='1435')
        assert 'port = 1435' in config_dump

    def test_tds_nonstandard_port_int(self):
        #it should convert it to a string
        config_dump = self.connect(port=1435)
        assert 'port = 1435' in config_dump