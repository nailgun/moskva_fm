import datetime
import pygtk
pygtk.require('2.0')
import gtk

class TimePicker(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self, spacing=2)
        self.hours = gtk.SpinButton()
        self.hours.set_increments(1, 2)
        self.hours.set_range(0, 23)
        self.minutes = gtk.SpinButton()
        self.minutes.set_increments(1, 10)
        self.minutes.set_range(0, 59)
        self.pack_start(self.hours, False)
        self.pack_start(gtk.Label(':'), False)
        self.pack_start(self.minutes, False)

        now = datetime.datetime.now()
        self.hours.set_value(now.hour)
        self.minutes.set_value(now.minute)

    def get_time(self):
        return self.hours.get_value_as_int(), self.minutes.get_value_as_int()

    def set_time(self, hours, minutes):
        self.hours.set_value(hours)
        self.minutes.set_value(minutes)

def init_calendar(calendar):
    now = datetime.datetime.now()
    def callback(calendar):
        year,month,day = calendar.get_date()
        if year == now.year and (month+1) == now.month:
            calendar.mark_day(now.day)
        else:
            calendar.unmark_day(now.day)

    calendar.mark_day(now.day)
    calendar.connect('month-changed', callback)

def pick_times():
    dialog = gtk.Dialog(title='Pick start and end times')

    hbox = gtk.HBox(spacing=5)

    vbox = gtk.VBox(spacing=2)
    vbox.pack_start(gtk.Label('Start'), False)
    start_date = gtk.Calendar()
    init_calendar(start_date)
    vbox.pack_start(start_date)
    start_time = TimePicker()
    vbox.pack_start(start_time)
    hbox.pack_start(vbox, False)

    before = datetime.datetime.now() - datetime.timedelta(hours=1)
    start_date.select_month(before.month-1, before.year)
    start_date.select_day(before.day)
    start_time.set_time(before.hour, before.minute)

    vbox = gtk.VBox(spacing=2)
    vbox.pack_start(gtk.Label('End'), False)
    end_date = gtk.Calendar()
    init_calendar(end_date)
    vbox.pack_start(end_date)
    end_time = TimePicker()
    vbox.pack_start(end_time)
    hbox.pack_start(vbox, False)

    dialog.vbox.pack_start(hbox, False)

    ok = gtk.Button('Select')
    dialog.vbox.pack_start(ok, False)

    def callback(widget):
        dialog.response(1)
    ok.connect('clicked', callback);

    dialog.show_all()
    response = dialog.run()
    assert response == 1

    year, month, day = start_date.get_date()
    hour, minute = start_time.get_time()
    start = datetime.datetime(year, month+1, day, hour, minute)

    year, month, day = end_date.get_date()
    hour, minute = end_time.get_time()
    end = datetime.datetime(year, month+1, day, hour, minute)

    return start, end
