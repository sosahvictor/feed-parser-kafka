#! /usr/bin/python

import sys
import feed_retriever
import file_comparator
import kafka_producer

if len(sys.argv) != 3:
	print("Usage: " + sys.argv[0] + "<input file> <output directory>")
	sys.exit(1)

rss_file_location = sys.argv[1]
output_directory = sys.argv[2]

# Read, download and store RSS feed XMLs based on list of RSS feed URLs
feed_retriever.read_rss_file(rss_file_location, output_directory)

# Get list of RSS feed XML files that have changed compared to previous
# downloaded XML of the same source
files_found = file_comparator.exec_find_files(output_directory)

# Publish feeds from RSS feed XML files that changed or are new
kafka_producer.process_feed_file(files_found)
