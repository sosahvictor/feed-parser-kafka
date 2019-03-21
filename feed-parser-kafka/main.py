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

feed_retriever.read_rss_file(rss_file_location, output_directory)
files_found = file_comparator.exec_find_files(output_directory)
kafka_producer.process_feed_file(files_found)
