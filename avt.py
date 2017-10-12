#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
import json
import csv
import re
import argparse
import settings


class AVT(object):
	def __init__(self):
		pass

	def log_parse(self, log):
		print '[*] Analyzing log files ...'

		log = [x for x in log if 'Failed password' in x]
		ip_ptrn = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
		time_ptrn = re.compile(r'^\S+\s\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}')

		access_times = [time_ptrn.findall(x)[0] for x in log]
		ips = [ip_ptrn.findall(x)[0] for x in log]
		hosts = {x: ips.count(x) for x in ips}.items()

		print '[*] ' + str(len(log)) + ' Attacks from ' + str(len(hosts)) + ' hosts detected.'

		self.atks = [{'date':access_times[ips.index(hosts[x][0])], 'ip':hosts[x][0], 'num':hosts[x][1]} for x in xrange(len(hosts))]
		return self.atks

	def geoIP(self):
		print '[*] Finding their location from their ip address ...'
		self.geoips = [json.loads(requests.get('http://www.freegeoip.net/json/{0}'.format(x['ip'])).text) for x in self.atks]
		return self.geoips

	def geoip2geojson(self, save_json):
		point = {"type":"Feature", "properties":{"ip":"ip", "date":"date", "num":"num"}, "geometry":{"type":"Point","coordinates":[10,20]}}
		points = []
		for x in xrange(len(self.geoips)):
			tmp = copy.deepcopy(point)
			tmp['geometry']["coordinates"] = [self.geoips[x]["longitude"], self.geoips[x]["latitude"]]
			tmp["properties"]["ip"] = self.geoips[x]["ip"]
			tmp["properties"]["date"] = self.atks[x]["date"]
			tmp["properties"]["num"] = self.atks[x]["num"]
			points.append(tmp)

		self.geojson = {"type": "FeatureCollection", "features": points}
		if save_json:
			json.dump(self.geojson, open('attacks.geojson', "w"))
		return self.geojson

	def genhtml(self):
		template = open(settings.template_html_path).read().split('\n'*5)
		self.geojson = 'var geojson = ' + self.geojson
		html = '\n'.join([template[0], self.geojson, template[1]])
		return html


def main(fpath, save_json, out):
	avt = AVT()
	lines = open(fpath).read().splitlines()

	atks = avt.log_parse(lines)
	atks_with_location = avt.geoIP()
	geojson = avt.geoip2geojson(save_json)
	html = avt.genhtml(geojson)
	open(out, 'w').write(html)

if __name__=='__main__':
	print '\n\t\tAttack Visualization Tool\n'
	parser = argparse.ArgumentParser()
	#parser.add_argument('protocol')
	parser.add_argument('-f', '--file', dest='file', required=True)
	parser.add_argument('-o', '--output', dest='out', required=True)
	parser.add_argument('-j', '--json', dest='json')
	parser.add_argument('-d', '--database', dest='db')
	args = parser.parse_args()

	main(args.file, args.json, args.out)
