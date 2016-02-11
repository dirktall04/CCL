#!/usr/bin/env python
# -*- coding:utf-8 -*-
# reportResolutionOrdering.py
# Created on 2015-07-28
# @author: dtalley
# Last Updated: 2015-07-28


try:
    from cityconnectinglinktest.config import (ws, connection0, connection1, citylimits, stateroutelyr, cntyroutelyr, laneclass,  # @UnusedImport @UnresolvedImport
                        maintenance, resolve, LineFeatureClass, NewRouteKey, NewBeg, NewEnd, NewRoute,  # @UnusedImport @UnresolvedImport
                        schema)  # @UnusedImport @UnresolvedImport
except:
    try:
        from config import (ws, connection0, connection1, citylimits, stateroutelyr, cntyroutelyr, laneclass,  # @UnusedImport @UnresolvedImport
                        maintenance, resolve, LineFeatureClass, NewRouteKey, NewBeg, NewEnd, NewRoute,  # @UnusedImport @UnresolvedImport
                        schema)  # @UnusedImport @UnresolvedImport
    except:
        print "Import from cityconnectinglinktest.config failed."
    pass


if __name__ == "__main__":
    try:
        from dt_functions import ReportResolutionOrdering
    except:
        print "Import of the ReportResolutionOrdering function failed."
    ReportResolutionOrdering()
else:
    pass