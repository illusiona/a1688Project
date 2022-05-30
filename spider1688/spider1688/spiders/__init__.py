# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import re
pattern_est = re.compile(r"(\d+\u53f0)")
est_time = pattern_est.findall("132132123 123123123123台 123123123")
print(est_time)
