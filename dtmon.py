#!/usr/bin/python
"""drain job in single mode
Usage: dtmon.py config [ copy ]
    config = YAML file or top-level dir
    copy   = copy files only - do not delete anything
"""
__author__ = "siznax 2010"

# for man page, "pydoc dtmon"

import sys, os

# to be contained within ia_upldr
class upldr:

    def __init__(self,fname):
        """ initialize configuration """
        self.name = os.path.basename(__file__)
        self.init_config(fname)

    def validate_config(self):
        """ validate given config file """
        try:
            config.validate(self.config)
            print "config OK:", self.config_fname
            # config.pprint_config(self.config)
        except Exception as detail:
            print "Error:", detail
            sys.exit("Aborted: invalid config: "+self.config_fname)

    def configure_instance(self):
        """ set this instance's config params """
        self.drainme = self.config['job_dir']+ "/DRAINME"
        self.sleep = self.config["sleep_time"]
        self.ias3cfg = os.environ["HOME"]+ "/.ias3cfg" 
        if os.path.isfile(self.ias3cfg) == False:
            sys.exit("Error: ias3cfg file not found: "+self.ias3cfg)
        
    def init_config(self,fname):
        """ initial config pass """
        self.config_fname = fname
        self.config = config.get_config(fname)
        self.validate_config()
        self.configure_instance()

    def update_config(self):
        """ update config before each drain job """
        self.config = config.get_config(self.config_fname)
        self.validate_config()
        self.configure_instance()

    def drain_job(self):
        """ call s3-drain-job.sh """
        import subprocess
        try:
            subprocess.check_call(["s3-drain-job.sh"])
        except Exception, e:
            print "process failed:", e
            sys.exit()

    def process(self):
        """ if DRAINME file exists, update config, drain job, sleep """
        import time
        utils.echo_start(self.name)
        while True:
            self.update_config()
            if os.path.isfile(self.drainme):
                self.drain_job()
            else:
                print "DRAINME file not found: ", self.drainme
            print "sleep("+str(self.sleep)+")"
            time.sleep(self.sleep)
        utils.echo_finish(self.name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        """ usage """
        print os.path.basename(__file__), __doc__, __author__
        sys.exit(1)
    else:
        """ process """
        import config, utils 
        if os.path.isdir(sys.argv[1]):
            print "config = dir TBD"
        else:
            dt = upldr(sys.argv[1])
            # utils.reflect(dt)
            dt.process()
            
else:
    """ on import """
    print "imported", __name__