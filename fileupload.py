import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.*"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        # print("event src path", event.src_path)  # print now only for debug
        # print("event type", event.event_type)  # print now only for debug
        subprocess.call(["rsync", "-avz", "--delete", "--exclude=.*", SOURCE, DEST])

    def on_modified(self, event):
       self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    SOURCE = ""
    DEST = ""

    if len(sys.argv) is 1 or len(sys.argv) > 3:
        print("------------------------------------------------------------------------------")
        print("Specify correct commandline arguments. Use 1 or 2 arguments:")
        print("")
        print(" Usage with 1 argument:")
        print("    Current directory will be used as source")
        print("    Specify destination as: /path/to/dest OR user@ip.adr:/path/to/dest")
        print("")
        print("Example: python projectsync.py user@10.10.10.10:/path/to/dest")
        print("")
        print(" Usage with 2 arguments:")
        print("    First arg: Path to source folder")
        print("    Second arg: Path to destination folder")
        print("")
        print("Example: python projectsync.py /path/to/source user@10.10.10.10:/path/to/dest")
        print("")
        print("To sync to remote destination use second argument of format:")
        print("username@ip.adress.of.host:/path/to/folder")
        print("Transfer via rsync, so destination computer should have your ssh key installed")
        print("------------------------------------------------------------------------------")
        exit()

    elif len(sys.argv) is 2:
        SOURCE = os.getcwd()
        if not SOURCE.endswith("/"):
            SOURCE = SOURCE + "/"
        DEST = sys.argv[1]
        if DEST.endswith("/"):
            DEST = DEST[:-1]

    elif len(sys.argv) is 3:
        SOURCE = sys.argv[1]
        if not SOURCE.endswith("/"):
            SOURCE = SOURCE + "/"
        DEST = sys.argv[2]
        if DEST.endswith("/"):
            DEST = DEST[:-1]


    print("Watcher will copy files from: %s" % SOURCE)
    print("Watcher will copy files to: %s" % DEST)
    print("")
    print("Running inital transfer of existing files.")
    subprocess.call(["rsync", "-avz", "--delete", "--exclude=.*", SOURCE, DEST])

    print("")
    print('Filewatcher started.')
    observer = Observer()
    observer.schedule(MyHandler(), path=SOURCE, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
