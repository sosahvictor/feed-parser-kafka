from confluent_kafka import Producer
import os
import datetime
import json
import xml.etree.ElementTree as ET

conf = {'bootstrap.servers': 'localhost:9092', 'client.id': 'rss'}
producer = Producer(conf)

ns = {
	'dc': 'http://purl.org/dc/elements/1.1/',
	'atom': 'http://www.w3.org/2005/Atom'
}

def process_feed_file(files):
	for feed_file in files:
		parse_xml_feed(feed_file)
		

def parse_xml_feed(feed_file):
	print("Pushing feed file: " + feed_file)
	tree = ET.parse(feed_file)
	channel_element = tree.getroot()[0]

	for feed_item in channel_element.iter('item'):
		author = feed_item.find('dc:creator',ns).text if feed_item.find('dc:creator', ns) is not None else feed_item.find('author').text
		url = feed_item.find('atom:link', ns).attrib['href'] if feed_item.find('atom:link', ns) is not None else feed_item.find('link').text

		feed = {
			"title" : feed_item.find('title').text,
			"author" : author,
			"description" : feed_item.find('description').text,
			"url" : url
		}
		json_data = json.dumps(feed)
		now = datetime.datetime.now()
		timestamp = now.strftime("%Y%m%d%H%M%S%f")
		producer.produce(topic= 'test', key=timestamp, value=json_data)

	producer.flush()

