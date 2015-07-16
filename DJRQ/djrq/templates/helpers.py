from humanize import naturaltime
from datetime import datetime


def artist_link(row):
    return "<a href='/artist/%s'>%s</a>" % (row.artist.id, row.artist.fullname)

def album_link(row):
    return "<a href='/album/%s'>%s</a>" % (row.album.id, row.album.fullname)

def aa_link(row):
    artist = row
    print "Helper:", row
    return "<a href='/artist/%s'>%s</a>" % (row.id, row.fullname)

def fix_dot(value):
    if value == '.':
        value = '.dot'
    return value

def nt_from_now(value):
    if type(value) == unicode:
        try:
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S").strftime("%s")
        except:
            pass
    try:
        return naturaltime(datetime.now() - datetime.fromtimestamp(float(value)))
    except:
        return value

def nt(value):
    return naturaltime(value)


def secs_to_h_m_s(value):
        m, s = divmod(value, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        return d, h, m, s

def human_time(value):
    try:
        d, h, m, s = secs_to_h_m_s(float(value))
    except:
        print "aborting humantime"
        return value
    v = ""
    fmt = "{:.0f}"
    if d > 0:
        v = "{:.0f}".format(d) + " day"
        if d > 1:
            v +="s"
        v += ", "
    if h > 0:
        v += fmt.format(h) + " hour"
        if d > 1:
            v +="s"
        v += ", "
    v += fmt.format(m) + ":" + fmt.format(s)
    return v

def colon(value):
    try:
        d, h, m, s = secs_to_h_m_s(float(value))
    except:
        print "aborting colon"
        return value
    v = ""
    fmt = "{:02.0f}"
    if d > 0:
        v = "{:.0f}".format(d) + " day"
        if d > 1:
            v +="s"
        v += ", "
    if h > 0:
        v += fmt.format(h) + ":"
    v += fmt.format(m) + ":" + fmt.format(s)
    return v

def when_last_played(lastplay):
    try:
        return nt_from_now(lastplay[-1].date_played)
    except:
        return "&nbsp;"

def last_played_by(lastplay):
    try:
        lp_by = lastplay[-1].user_name
    except:
        lp_by = "&nbsp;"
    else:
        lp_by += " " + when_last_played(lastplay)
        if len(lastplay) >= 1:
            lp_by += " <span class='badge' data-toggle='tooltip' data-original-title='<ul>"
            for lp in lastplay:
                un = lp.user_name.replace("'", "&apos;")
                lp_by += '<li>%s %s</li>' % (un, when_last_played([lp]))
            lp_by += "</ul>'>%s</span>" % len(lastplay)
    return lp_by
