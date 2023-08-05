#!/usr/bin/env python
##########################################################################
# $Id: turbine_session_script.py 4480 2013-12-20 23:20:21Z boverhof $
# Joshua R. Boverhof, LBNL
# See LICENSE.md for copyright notice!
#
#   $Author: boverhof $
#   $Date: 2013-12-20 15:20:21 -0800 (Fri, 20 Dec 2013) $
#   $Rev: 4480 $
#
###########################################################################
import sys
import json
import optparse
import glob
import uuid
import os
import time
import time
import dateutil.parser
import datetime
import logging as _log
from urllib.error import HTTPError
from turbine.commands import add_options, add_json_option, delete_page, post_page, \
    get_page, get_paging, get_paging_by_url, _open_config, getFromConfigWithDefaults, \
    _print_page, _print_numbered_lines, _print_as_json, load_pages_json, \
    HEADER_CONTENT_TYPE_JSON

from turbine.utility import basic_session_stats

SECTION = "Session"


def main_list(args=None, func=_print_numbered_lines):
    """Prints human readable listing of all session GUIDs.
    """
    op = optparse.OptionParser(usage="USAGE: %prog [options] CONFIG_FILE",
                               description=main_list.__doc__)

    add_options(op)
    add_json_option(op)
    (options, args) = op.parse_args(args)
    try:
        configFile = _open_config(*args)
    except Exception as ex:
        op.error(ex)

    if options.json:
        func = _print_as_json

    query = {}
    pages = get_paging(configFile, SECTION, options, **query)
    data = load_pages_json(pages)
    if func:
        func(data)
    return data


def jobs_status(configFile, sessionid):
    query = {}
    query['subresource'] = sessionid + "/status"
    data = get_page(configFile, SECTION, **query)

    return json.loads(data)


def main_jobs_status(args=None, func=_print_as_json):
    """session resource utility, lists all session resources
    """
    op = optparse.OptionParser(usage="USAGE: %prog [options] SESSIONID CONFIG_FILE",
                               description=main_jobs_status.__doc__)
    add_options(op)
    (options, args) = op.parse_args(args)

    if len(args) < 1:
        op.error('expecting >= 1 argument')

    sessionid = args[0]
    try:
        configFile = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    data = jobs_status(configFile, sessionid)
    if func:
        func(data)
    return data


def create_session(configFile):
    """ returns a GUID, must remove quotes
    """
    contents = post_page(configFile, SECTION, b'')
    _log.getLogger(__name__).debug("SESSION: %s", contents)
    return contents.strip('"')


def main_create_session(args=None, func=_print_page):
    """Creates new session resource and prints GUID of created session.
    """
    op = optparse.OptionParser(usage="USAGE: %prog CONFIG_FILE",
                               description=main_create_session.__doc__)

    (options, args) = op.parse_args(args)

    try:
        configFile = _open_config(*args)
    except Exception as ex:
        op.error(ex)

    page = create_session(configFile)
    data = uuid.UUID(page)
    if (func):
        func(data)
    return data


def create_jobs(configFile, sessionid, jobsList):
    """ jobsList is a list of jobs, usually provided from a JSON file
    """
    #assert (type(jobsList), list)
    content = bytes(json.dumps(jobsList), encoding='UTF-8')
    return post_page(
        configFile,
        SECTION,
        content,
        headers={'Content-Type': HEADER_CONTENT_TYPE_JSON},
        subresource=sessionid)


def main_create_jobs(args=None, func=_print_page):
    """Appends job descriptions to a session, prints the number of jobs added.
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID JOBS_FILE CONFIG_FILE",
                               description=main_create_jobs.__doc__)

    (options, args) = op.parse_args(args)
    if len(args) < 2:
        op.error('expecting >= 2 arguments')

    sessionid = args[0]
    jobs_file = args[1]
    try:
        configFile = _open_config(*args[2:])
    except Exception as ex:
        op.error(ex)

    log = _log.getLogger(__name__)
    log.debug("main_create_jobs")

    try:
        with open(jobs_file) as fd:
            input_data = json.load(fd)
    except FileNotFoundError:
        input_data = json.loads(jobs_file)

    assert(type(input_data) is list)

    for o in input_data:
        thisset = set(o.keys())
        assert thisset.issuperset(
            ["Input", "Simulation"]), "Each entry requires fields 'Input' and 'Simulation'"

    try:
        page = create_jobs(configFile, sessionid, input_data)
    except HTTPError as ex:
        log.error(ex)
        log.error(ex.fp.read())
        raise
    log.debug("PAGE: %s" % page)
    data = json.loads(page)
    if (func):
        func(data)
    return data


def stop_jobs(configFile, sessionid):
    return post_page(configFile, SECTION, b'', subresource='%s/stop' % sessionid)


def main_stop_jobs(args=None):
    """Move all jobs in state submit to pause.  Prints the number of jobs moved to state pause.
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID  CONFIG_FILE",
                               description=main_stop_jobs.__doc__)

    (options, args) = op.parse_args(args)
    if len(args) < 1:
        op.error('expecting >= 1 arguments')

    sessionid = args[0]
    try:
        configFile = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    print(stop_jobs(configFile, sessionid))


def main_delete(args=None, func=_print_page):
    """Delete session and all jobs it contains, prints number of jobs deleted as result of session delete.
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID  CONFIG_FILE",
                               description=main_delete.__doc__)

    (options, args) = op.parse_args(args)
    if len(args) < 1:
        op.error('expecting >= 1 arguments')

    sessionid = args[0]
    try:
        configFile = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    log = _log.getLogger(__name__)

    try:
        page = delete_page(configFile, SECTION, subresource='%s' % sessionid)
    except HTTPError as ex:
        log.error(ex)
        raise
    log.debug("PAGE: %s" % page)
    return int(page)

def post_session_results(configFile, sessionid):
    """ Request next page number with finished jobs
    """
    return post_page(configFile, SECTION, b'', subresource='%s/result/00000000-0000-0000-0000-000000000000' % sessionid)

def main_create_session_result_page(args=None, func=_print_page):
    """Terminate jobs in session in state setup, running.  Print number of jobs terminated.
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID  CONFIG_FILE",
                               description=main_kill_jobs.__doc__)

    (options, args) = op.parse_args(args)
    if len(args) < 1:
        op.error('expecting >= 1 arguments')

    sessionid = args[0]
    try:
        configFile = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    page = post_session_results(configFile, sessionid)
    #data = json.load(page)
    data = int(page)
    if func:
        func(data)
    return data


def main_get_session_result_page(args=None, func=_print_page):
    """Terminate jobs in session in state setup, running.  Print number of jobs terminated.
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID PAGE_NUMBER CONFIG_FILE",
                               description=main_kill_jobs.__doc__)
    (options, args) = op.parse_args(args)
    if len(args) < 2:
        op.error('expecting >= 2 arguments')


    sessionid = args[0]
    page_number = args[1]
    try:
        configFile = _open_config(*args[2:])
    except Exception as ex:
        op.error(ex)

    page = get_session_page_results(configFile, sessionid, int(page_number))

    if page:
        page = json.loads(page)

    #data = int(page)
    if func:
        func(page)
    return page


def get_session_page_results(configFile, sessionid, page_number):
    return get_page(configFile, SECTION, subresource="%s/result/00000000-0000-0000-0000-000000000000/%d" %(sessionid,page_number))


def kill_jobs(configFile, sessionid):
    return post_page(configFile, SECTION, b'', subresource='%s/kill' % sessionid)


def main_kill_jobs(args=None, func=_print_page):
    """Terminate jobs in session in state setup, running.  Print number of jobs terminated.
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID  CONFIG_FILE",
                               description=main_kill_jobs.__doc__)

    (options, args) = op.parse_args(args)
    if len(args) < 1:
        op.error('expecting >= 1 arguments')

    sessionid = args[0]
    try:
        configFile = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    page = kill_jobs(configFile, sessionid)
    #data = json.load(page)
    data = int(page)
    if func:
        func(data)
    return data


def start_jobs(configFile, sessionid):
    return post_page(
        configFile,
        SECTION,
        b'',
        headers={'Content-Type': HEADER_CONTENT_TYPE_JSON},
        subresource='%s/start' % sessionid)


def main_start_jobs(args=None, func=_print_page):
    """Move all jobs in states pause and create to submit.  Prints the number of jobs moved to state submit.
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID  CONFIG_FILE",
                               description=main_start_jobs.__doc__)

    (options, args) = op.parse_args(args)
    if len(args) < 1:
        op.error('expecting >= 1 arguments')

    sessionid = args[0]
    try:
        configFile = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    _log.getLogger(__name__).debug("main_start_jobs")
    page = start_jobs(configFile, sessionid)
    data = json.loads(page)
    if func:
        func(data)
    return data


def get_results(cp, sessionid, options):
    """ Gets all jobs from the session and return them as a list """
    # default values for a few important items

    url = '/'.join([cp.get(SECTION, 'url').strip('/'),sessionid])
    #rpp = getFromConfigWithDefaults(cp,SECTION, 'rpp', '100')
    verbose = getFromConfigWithDefaults(cp, SECTION, 'verbose', 'false')

    pagenum = options.page
    rpp = options.rpp

    query = {}
    query['subresource'] = sessionid
    query['verbose'] = verbose
    query['rpp'] = str(rpp)
    query['page'] = pagenum
    _log.getLogger(__name__).debug('query: %s' %(query))

    pages = []
    _log.getLogger(__name__).debug("downloading results 1-%d" % (int(rpp)))
    if (pagenum > 0):
        thispage = get_paging_by_url(url, cp, SECTION, query)
        pages.extend(thispage)
    else:
        pagenum = 1
        query['page'] = 1
        thispage = get_paging_by_url(url, cp, SECTION, query)
        while(thispage[0] != '[]'):
            pages.extend(thispage)
            pagenum += 1
            query['page'] = pagenum
            _log.getLogger(__name__).debug("downloading results %d-%d" %
                                           ((pagenum-1) * int(rpp), pagenum * int(rpp)))
            thispage = get_paging_by_url(url, cp, SECTION, query)

    #assert(type(pages), list)
    print("all results recieved.")
    data = load_pages_json(pages)
    return data


def main_get_results(args=None, func=_print_page):
    """Gets the results of all the completed jobs in this session
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID  CONFIG_FILE",
                               description=main_get_results.__doc__)

    add_options(op)

    (options, args) = op.parse_args(args)
    if len(args) < 1:
        op.error('expecting >= 1 arguments')

    sessionid = args[0]
    try:
        cp = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    data = get_results(cp, sessionid, options)
    if func:
        func(json.dumps(data, indent=2))
    return data


def main_session_stats(args=None):
    """session resource utility, prints basic session statistics
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID  CONFIG_FILE",
                               description=main_session_stats.__doc__)

    add_options(op)
    (options, args) = op.parse_args(args)
    if len(args) < 1:
        op.error('expecting >= 1 arguments')

    sessionid = args[0]
    try:
        configFile = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    pages = get_paging(configFile, SECTION, options, subresource=sessionid)
    data = load_pages_json(pages)

    basic_session_stats(sys.stdout, data, verbose=options.verbose)

    # if options.verbose:
    #    for i in success_l:
    #        print i['Output']
    return data


def main_session_graphs(args=None):
    """session resource utility, creates session stats graphs with R
    """
    op = optparse.OptionParser(usage="USAGE: %prog SESSIONID  CONFIG_FILE",
                               description=main_session_stats.__doc__)
    add_options(op)
    op.add_option("--plot", dest="plot", help="Plot type (see --list). "
                  "Any unique prefix is OK. (default=%default)",
                  default="density")
    op.add_option("--list", dest="do_list", action="store_true",
                  help="List plot types and metrics.")
    op.add_option("--metric", dest="opt_metric",
                  help="Metric to show in plot (see --list).")
    (options, args) = op.parse_args(args)
    # If --list, list plots and stop
    if options.do_list:
        print("Plot types:")
        for pt in sorted(Plot.TYPES):
            print("  {type:20s} {desc}".format(type=pt, desc=Plot.TYPES[pt]))
        print("Plot metrics:")
        for pm in Plot.METRICS:
            print("  {m:20s}".format(m=pm))
        sys.exit(0)
    if options.opt_metric is not None and \
       options.opt_metric not in Plot.METRICS:
        op.error("Bad metric {0}, must be in: {1}".format(options.opt_metric,
                                                          ', '.join(Plot.METRICS)))

    # Import R stuff
    try:
        import rpy2
    except ImportError as err:
        op.error("rpy2 and a working R installation are required.\n"
                 "Import error: {0}".format(err))
    from turbine import rpython

    # Parse options
    if len(args) != 2:
        op.error('expecting 2 arguments')
    if options.plot not in Plot.TYPES:  # XXX: accept prefix
        op.error('bad plot type {p}, use --list'.format(p=options.plot))
    sessionid = args[0]
    try:
        configFile = _open_config(*args[1:])
    except Exception as ex:
        op.error(ex)

    # Fetch data
    pages = get_paging(configFile, SECTION, options, subresource=sessionid)
    data = load_pages_json(pages)

    # Create R data frame
    tbl, hdr = session_perf_from_json(data)
    coltypes = rpython.get_coltypes([column[0] for column in tbl])
    df = rpython.make_data_frame(hdr, coltypes, cols=tbl)

    # Create and draw selected plot
    plot_opt = {}
    for k in dir(options):
        if k.startswith("opt_"):
            plot_opt[k[4:]] = getattr(options, k)
    plot = Plot(df, hdr, **plot_opt)
    device = "png"
    filename = "%s_%s.%s" % (options.plot, sessionid, device)
    getattr(plot, "plot_" + options.plot)(filename, device=device)

    return {options.plot: filename}


class Plot:
    TYPES = {
        "density": "Density plot of total timings",
        "multi_density": "Density plot of all timings",
        "multi_ts": "Time-series plot of all timings"
    }
    STATES = ['Submit', 'Setup', 'Running', 'Finished']
    METRICS = ['Queue', 'Setup', 'Run']
    OPTIONS = {
        "density": {"metric": METRICS[2]}
    }

    def __init__(self, df, hdr, **plot_opts):
        import rpy2.robjects.lib.ggplot2 as ggplot2
        self._g2 = ggplot2
        self._g2.theme_bw()
        self._data = df
        self._hdr = hdr
        from turbine.rpython import R
        self._R = R
        self._opts = plot_opts

    def plot_density(self, filename, device="png", device_opts={}):
        metric = self._opts.get("metric", self.OPTIONS["density"]["metric"])
        hdr_metric_idx = 2 + self.METRICS.index(metric)
        df, g2, h, r = self._data, self._g2, self._hdr, self._R
        pp = g2.ggplot(df) + \
            g2.aes_string(x=h[hdr_metric_idx], y='..scaled..') + \
            g2.geom_density() + \
            g2.scale_x_continuous(name="{0} time (seconds)".format(metric)) + \
            g2.scale_y_continuous(name="Density")
        r[device](filename, **device_opts)
        pp.plot()
        r['dev.off']()

    def _melt_states(self, df, names):
        return self._R.melt(df, id_var=names[:2],
                            measure=names[2:-1], variable_name='state')

    def plot_multi_density(self, filename, device="png", device_opts={}):
        df, g2, h, r = self._data, self._g2, self._hdr, self._R
        dfm = self._melt_states(df, h)
        pp = g2.ggplot(dfm) + \
            g2.aes_string(x='value', y='..scaled..',
                          colour='state', group='state') + \
            g2.geom_density() + \
            g2.scale_x_continuous(name="Time for state (seconds)") + \
            g2.scale_y_continuous(name="Density")
        r[device](filename, **device_opts)
        pp.plot()
        r['dev.off']()

    def plot_multi_ts(self, filename, device="png", device_opts={}):
        df, g2, h, r = self._data, self._g2, self._hdr, self._R
        dfm = self._melt_states(df, h)
        pp = g2.ggplot(dfm) + \
            g2.aes_string(x='num', y='value',
                          colour='state', group='state') + \
            g2.geom_line() + \
            g2.scale_y_continuous(name="Time for state (seconds)") + \
            g2.scale_x_continuous(name="Observation")
        r[device](filename, **device_opts)
        pp.plot()
        r['dev.off']()


def session_perf_from_json(data):
    """Create a set of columns from the session data.
    This set of columns will be easy to load into an R data frame,
    but could also be operated on in Python directly.

    Resulting columns are:
       (num, times, Setup, Running, Finished, Total)
    """
    states = Plot.STATES
    _dparse = dateutil.parser.parse
    # matrix result, first column is index, second is t0
    state = states[0]
    m = [range(len(data)), [_dparse(x[state]) for x in data]]
    n = len(data)
    # Add deltas for each state
    # first state doesn't subtract other deltas
    state = states[1]
    prev = [(_dparse(data[row][state]) - m[1][row]).total_seconds()
            for row in range(n)]
    m.append(prev)
    # middle to last state
    for col in range(2, len(states)):
        state = states[col]
        column = [(_dparse(data[row][state]) - m[1][row]).total_seconds()
                  - prev[row]
                  for row in range(n)]
        m.append(column)
        prev = [prev[i] + column[i] for i in range(n)]
    # add totals for last state
    state = states[-1]
    m.append([(_dparse(data[row][state]) - m[1][row]).total_seconds()
              for row in range(n)])
    # for row in range(n-10,n):
    #    for col in m:
    #        sys.stdout.write("{0} ".format(col[row]))
    #    print('')
    # return data and header
    return ((m, ['num', 'time'] + states[:-1] + ['Total']))


main = main_list
if __name__ == "__main__":
    main()
