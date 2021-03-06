__author__ = "Remigius Kalimba"
'''Add a timer so it does this automatically everyday at a set time'''

from os import path, mkdir, listdir, rename, environ
import sys
import json
import os
import undo
from crontab import CronTab
import getpass


if sys.version_info >= (3,):
    from tkinter import *
    from tkinter import messagebox as tkMessageBox
else:
    from tkinter import *
    import tkMessageBox

Extensions = json.load(open(os.path.dirname(os.path.abspath(__file__))+'/Extension.json'))

folders = [x for x in Extensions]

class App(Frame):
    def clean(self):
        main()
        tkMessageBox.showinfo("Complete", "Desktop clean finished.")

    def quit_all(self):
        quit()
        sys.exit(0)

    def check(self, item):
        if item in folders:
            folders.remove(item)
        else:
            folders.append(item)

    def undo_all(self):
        undo.execute()

    def schedule_start(self):
        my_cron = CronTab(user=getpass.getuser())
        job = my_cron.new(command=str(sys.executable+' '+os.path.dirname(os.path.abspath(__file__))+"/cronCleanUp.py"),
                          comment="OrganiseDesktop")
        job.day.every(1)
        my_cron.write()

    def schedule_end(self):
        my_cron = CronTab(user=getpass.getuser())
        my_cron.remove_all(comment="OrganiseDesktop")
        my_cron.write()

    def create(self):
        self.winfo_toplevel().title("Desktop Cleaner")

        self.shortcuts = Checkbutton(self)
        self.shortcuts["text"] = "Shortcuts"
        self.shortcuts.select()
        self.shortcuts["command"] = lambda: self.check('shortcut')
        self.shortcuts.pack({"side": "top"})

        self.malware = Checkbutton(self)
        self.malware["text"] = "Malware"
        self.malware.select()
        self.malware["command"] = lambda: self.check('malware')
        self.malware.pack({"side": "top"})

        self.zip = Checkbutton(self)
        self.zip["text"] = "Archives"
        self.zip.select()
        self.zip["command"] = lambda: self.check('zip')
        self.zip.pack({"side": "top"})

        self.music = Checkbutton(self)
        self.music["text"] = "Music"
        self.music.select()
        self.music["command"] = lambda: self.check('music')
        self.music.pack({"side": "top"})

        self.images = Checkbutton(self)
        self.images["text"] = "Images"
        self.images.select()
        self.images["command"] = lambda: self.check('image')
        self.images.pack({"side": "top"})

        self.exe = Checkbutton(self)
        self.exe["text"] = "Executables"
        self.exe.select()
        self.exe["command"] = lambda: self.check('executable')
        self.exe.pack({"side": "top"})

        self.movies = Checkbutton(self)
        self.movies["text"] = "Movies"
        self.movies.select()
        self.movies["command"] = lambda: self.check('movie')
        self.movies.pack({"side": "top"})

        self.text = Checkbutton(self)
        self.text["text"] = "Text"
        self.text.select()
        self.text["command"] = lambda: self.check('text')
        self.text.pack({"side": "top"})

        self.d3 = Checkbutton(self)
        self.d3["text"] = "CAD Files"
        self.d3.select()
        self.d3["command"] = lambda: self.check('D3work')
        self.d3.pack({"side": "top"})

        self.code = Checkbutton(self)
        self.code["text"] = "Code"
        self.code.select()
        self.code["command"] = lambda: self.check('programming')
        self.code.pack({"side": "top"})

        self.clean_button = Button(self)
        self.clean_button["text"] = "Clean"
        self.clean_button["command"] = self.clean
        self.clean_button.pack({"side": "left"})

        self.quit_button = Button(self)
        self.quit_button["text"] = "Exit"
        self.quit_button["command"] = self.quit_all
        self.quit_button.pack({"side": "left"})

        self.undo_button = Button(self)
        self.undo_button['text'] = 'Undo'
        self.undo_button['command'] = self.undo_all
        self.undo_button.pack({"side": "left"})

        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.schedule_button = Button(self)
            self.schedule_button['text'] = 'Schedule'
            self.schedule_button['command'] = self.schedule_start
            self.schedule_button.pack({"side": "left"})

            self.remove_schedule_button = Button(self)
            self.remove_schedule_button['text'] = 'Remove \nSchedule'
            self.remove_schedule_button['command'] = self.schedule_end
            self.remove_schedule_button.pack({"side": "right"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create()


class OrganiseDesktop():
    def __init__(self):
        '''
        This is an initialization function, I do not wish to explain this.

        This is a smart way to get the username
        We could also have used os.environ, this brings a list and a lot of information we can manipulate.
        '''

        #
        # References:   https://en.wikipedia.org/wiki/Environment_variable#Default_values
        #               https://en.wikipedia.org/wiki/Windows_NT#Releases
        #
        if sys.platform == 'win32':
            self.desktopdir = path.join(environ['USERPROFILE'], 'Desktop')

            # Determine Windows version; check if this is XP; accordingly, read target folders
            if not sys.getwindowsversion() == 10:
                if sys.getwindowsversion().major < 6:
                    self.Alldesktopdir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')
                else:
                    self.Alldesktopdir = path.join(environ['PUBLIC'], 'Desktop')
            print(self.desktopdir)
            print(self.Alldesktopdir)
            '''list of folders to be created'''
        elif sys.platform == 'linux' or 'darwin':
            self.desktopdir = path.join(environ['HOME'], 'Desktop')
        else:
            print("{} version not implemented".format(sys.platform))
            raise NotImplementedError

    def makdir(self):
        '''
        This function makes the needed folders if they are not already found.
        '''
        try:
            '''For all the folders in the folder_name list, if that folder is not(False) on the main_desktop
               then create that folder.
            '''
            if sys.platform == 'win32':
                for nam in folders:
                    if path.isdir(self.desktopdir + '\\' + nam) is False:
                        mkdir(self.desktopdir + "\\" + nam)
            elif sys.platform == 'linux' or 'darwin':
                for nam in folders:
                    if path.isdir(self.desktopdir + '/' + nam) is False:
                        mkdir(self.desktopdir + "/" + nam)
        except Exception as e:
            print(e)

    def mapper(self):
        '''
        This function checks the two folders (current user desktop and all user desktop),
        if on windows, only checks one folder if on linux or macOS,
        it takes all the items there and puts them into two respective lists which are
        returned and used by the mover function
        '''
        if sys.platform == 'linux' or sys.platform == 'darwin' or sys.getwindowsversion()[0] == 10:
            return [listdir(self.desktopdir)]
        maps = [listdir(self.desktopdir), listdir(self.Alldesktopdir)]
        return maps

    def mover(self, maps, separator):
        '''
        This function gets two lists with all the things on the desktops
        and copies them into their respective folders, using a forloop and if statements
        '''

        '''
        Extension Lists
        '''
        # # image extensions source: https://fileinfo.com/filetypes/raster_image,
        #                            https://fileinfo.com/filetypes/vector_image, and
        #                            https://fileinfo.com/filetypes/camera_raw
        # # music extensions source: https://fileinfo.com/filetypes/audio
        # # movie extensions source: http://bit.ly/2wvYjyr
        # # text extensions source:  http://bit.ly/2wwcfZs
        map1 = maps[0]
        try:

            '''Anything from the All_users_desktop goes to shortcuts, mainly because that's all that's ever there (i think)'''
            if separator != '/' and not sys.getwindowsversion()[0] == 10:
                map2 = maps[1]
                for item in map2:
                    '''This is a cmd command to move items from one folder to the other'''
                    rename(self.Alldesktopdir + separator + item, self.desktopdir + separator + item)
            for file_or_folder in map1:
                if file_or_folder not in folders and not file_or_folder.startswith(".") and not file_or_folder.startswith(".."):
                    found = False
                    for sorting_folder in folders:
                        if os.path.isdir(self.desktopdir + separator + file_or_folder):
                            rename(self.desktopdir + separator + file_or_folder,
                                   self.desktopdir + separator + 'zips' + separator + file_or_folder)
                            found = True
                            break
                        for extension in Extensions[sorting_folder]:
                            if str(file_or_folder.lower()).endswith(extension) and \
                               str(file_or_folder) != "Clean.lnk" and \
                               str(file_or_folder) != "Clean.exe.lnk":
                                rename(self.desktopdir + separator + file_or_folder,
                                           self.desktopdir + separator + sorting_folder + separator + file_or_folder)
                                if separator == '/':
                                    os.system('cd ..')
                                found = True
                                break
                    if not found:
                        print("I do not know what to do with " + file_or_folder + " please update me!")
        except () as e:
            print(e)

    def writter(self, maps):
        '''
        This function writes the two lists of all the items left on the desktop
        just incase something isn't right and we need a log.
        '''
        lists1 = maps[0]

        writeOB = open('Read_Me.txt', 'w')
        writeOB.write("This is a list of all the items on your desktop before it was cleaned.\n"
                      "Email this list to kalimbatech@gmail.com if anything is not working as planned, it will help with debugging\n"
                      "Together we can make a better app\n\n")

        for i in lists1:
            writeOB.write(i)
            writeOB.write("\n")

        if sys.platform == 'win32' and not sys.getwindowsversion()[0] == 10:
            lists2 = maps[1]
            for i in lists2:
                writeOB.write(i)
                writeOB.write("\n")
        writeOB.close()


def main():
    fh = open("hello.txt", "w")
    lines_of_text = ["one"]
    fh.writelines(lines_of_text)
    fh.close()
    ''' The oh so magnificent main function keeping shit in order '''
    projectOB = OrganiseDesktop()
    projectOB.makdir()
    maps = projectOB.mapper()
    if sys.platform == 'win32':
        projectOB.mover(maps, separator='\\')
    elif sys.platform == 'linux' or 'darwin':
        projectOB.mover(maps, separator='/')
    projectOB.writter(maps)
    fh = open("hello.txt", "w")
    lines_of_text = ["two"]
    fh.writelines(lines_of_text)
    fh.close()


if __name__ == "__main__":
    root = Tk()
    root.resizable = False
    root.minsize(width=350, height=330)
    root.maxsize(width=350, height=330)
    app = App(root)
    root.protocol('WM_DELETE_WINDOW', app.quit_all)
    app.mainloop()
    root.destroy()
