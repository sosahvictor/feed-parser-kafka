import re
import datetime
import urllib2

def read_rss_file(rss_file_location, output_directory):
	rss_file = open(rss_file_location, "r")
	now = datetime.datetime.now()
	suffix = now.strftime("_%Y%m%d%H%M%S.xml")

	for rss in rss_file:
		rss = rss.strip()
		if len(rss) <= 1:
			continue

		filename = re.compile("http://|https://").split(rss)[1]
		last_dot_index = filename.rfind(".")
		filename = filename[:last_dot_index]
		filename = re.sub("\.|\/", "_", filename)
		filename = filename + suffix
		download_rss(rss, filename, output_directory)

def download_rss(url, filename, output_directory):
	print("Downloading content from " + url)
	print("Creating local file " + output_directory + "/" + filename)
	response = urllib2.urlopen(url)
	xml_content = response.read()
	file_output = open(output_directory + "/" + filename, "w");
	file_output.write(xml_content)

