from shutil import copy2
import pyinotify

wm = pyinotify.WatchManager()

mask = pyinotify.IN_CLOSE_WRITE


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        print "Wrote:", event.pathname
        if event.pathname == '/tmp/foo3':
            copy2('/tmp/foo3', '/tmp/foo-new')
            print 'you touched my file!'

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wm.add_watch('/tmp', mask, rec=True)

notifier.loop()
