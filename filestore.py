from __future__ import print_function
import os
import shutil
import logging
class FileStore(object):
    SESSION_PREFIX = "Session_"
    SUBSESSION_PREFIX = "Subsession_"
    @staticmethod
    def get_next_session_number(directory):
        subdirs = os.listdir(directory)
        num_idx = len(FileStore.SESSION_PREFIX)
        sessions = [int(s[num_idx:]) for s in subdirs if s.startswith(FileStore.SESSION_PREFIX)]
        if sessions:
            return max(sessions) + 1
        else:
            return 0

    @staticmethod
    def get_next_subsession_number(directory):
        subdirs = os.listdir(directory)
        num_idx = len(FileStore.SUBSESSION_PREFIX)
        subsessions = [int(s[num_idx:]) for s in subdirs if s.startswith(FileStore.SUBSESSION_PREFIX)]
        if subsessions:
            return max(subsessions) + 1
        else:
            return 0

    def __init__(self, directory=".", log=True):
        self.root = os.path.join(os.getcwd(), directory)
        self.log = log

        if not os.path.exists(self.root):
            os.makedirs(self.root)
        self.new_session()
        self.new_subsession()

        if log:
            logging.basicConfig(filename=os.path.join(self.root,"_log.txt"), 
                                format='%(asctime)s %(message)s',
                                level=logging.DEBUG)


    def new_session(self):
        self.session_number = FileStore.get_next_session_number(self.root)
        self.session_name = "%s%d" % (self.SESSION_PREFIX, self.session_number)
        self.session_path = os.path.join(self.root, self.session_name)
        os.mkdir(self.session_path)

    def new_subsession(self):
        self.subsession_number = FileStore.get_next_subsession_number(self.session_path)
        self.subsession_name = "%s%d" % (self.SUBSESSION_PREFIX, self.subsession_number)
        self.subsession_path = os.path.join(self.session_path, self.subsession_name)
        os.mkdir(self.subsession_path)

    def add(self, name):
        if not os.path.exists(name):
            raise ValueError("File not found: %s" % name)
        stat = hex(hash(os.stat(name)))
        fname = stat + "_" + os.path.basename(name)
        if fname in os.listdir(self.subsession_path):
            logging.info("It appears this file (%s) is already in the %s. Starting a new session." % \
                                                                   (fname, self.__class__.__name__))
            self.new_subsession()
            logging.info("New Subsession:" % os.path.join(self.subsession_path))

        logging.info("Copying %s to %s" % (name, os.path.join(self.subsession_path, fname)))
        shutil.copyfile(name, os.path.join(self.subsession_path, fname))

if __name__ == "__main__":
    filestore = FileStore("_d")
