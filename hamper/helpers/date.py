#
# HamperDate is a class to encapsulate the expiration date of certificates.
# 
# The expiration date is the only way of identifying which certificate to use 
# when signing a distribution provisioning profile.
#
#

class HamperDate(object):
	HDAbbreviatedMonthJanuary   = "Jan"
	HDAbbreviatedMonthFebruary  = "Feb"
	HDAbbreviatedMonthMarch     = "Mar"
	HDAbbreviatedMonthApril     = "Apr"
	HDAbbreviatedMonthMay  	    = "May"
	HDAbbreviatedMonthJune	    = "Jun"
	HDAbbreviatedMonthJuly	    = "Jul"
	HDAbbreviatedMonthAugust    = "Aug"
	HDAbbreviatedMonthSeptember = "Sep"
	HDAbbreviatedMonthOctober   = "Oct"
	HDAbbreviatedMonthNovember  = "Nov"
	HDAbbreviatedMonthDecember  = "Dec"

	HDAbbreviatedMonthsList = [HDAbbreviatedMonthJanuary, HDAbbreviatedMonthFebruary, HDAbbreviatedMonthMarch, HDAbbreviatedMonthApril, HDAbbreviatedMonthMay, HDAbbreviatedMonthJune, HDAbbreviatedMonthJuly, HDAbbreviatedMonthAugust, HDAbbreviatedMonthSeptember, HDAbbreviatedMonthOctober, HDAbbreviatedMonthNovember, HDAbbreviatedMonthDecember]

	def __init__(self, month=0, day=0, year=0):
		super(HamperDate, self).__init__()
		self.month = month
		self.day   = day
		self.year  = year

	def readable_date(self):
		if int(self.month) < len(HamperDate.HDAbbreviatedMonthsList):
			return HamperDate.HDAbbreviatedMonthsList[int(self.month)-1] + " " + self.day + ", " + self.year