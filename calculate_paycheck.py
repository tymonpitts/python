#! /usr/bin/python
import sys

rate = 77.0
withholding_rate = 0.27
gst_rate = 0.15
hours = float(sys.argv[1])
raw_total = rate * hours
gst = raw_total * gst_rate
withholding = raw_total * withholding_rate
actual_total = raw_total + gst - withholding
print 'Paycheck: %s' % actual_total
print 'GST: %s' % gst
print 'Withholding: %s' % withholding
