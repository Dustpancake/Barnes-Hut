import os
from ..Support import Config
from os.path import isfile, join, isdir

class FileAccess(object):
    path = "./frames/"
    def clean_up(self, path):
        files = self.get_filenames(path)
        for i in files:
            os.remove(i)

    def get_dirnames(self, path = None):
        if path == None: path = self.path
        files = [f for f in os.listdir(path) if isdir(join(path, f))]
        if len(files) == 0: files.append('0')
        path_files = [path + f for f in files]
        return path_files[:]

    def get_filenames(self, path = None):
        if path == None: path = self.path
        files = [f for f in os.listdir(path) if isfile(join(path, f))]
        path_files = [path + f for f in files]
        return path_files[:]

    def file_system(self, override):
        files = self.get_dirnames()
        num = []
        for file in files:
            num.append(self.make_number(file))
        num = max(num)
        if override == 1:
            self.path = self.path+str(num)+'/'
            self.clean_up(self.path)
        else:
            num = self.make_new_dir(num)
        self.save_config(num)

    def make_number(self, files):
        string = files.split("/")[-1]
        try:
            num = int(string)
        except:
            return -1
        return num

    def save_config(self, num):
        cp = Config()
        path = cp.path
        with open(path, 'r') as config_file:
            with open("./Barnes_Hut/config_files/config"+str(num)+"file.ini", 'w') as save:
                save.write(config_file.read())

    def make_new_dir(self, num):
        num += 1
        path = self.path + str(num) + "/"
        os.mkdir(path)
        self.path = path
        return num