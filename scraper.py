#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import requests
import re
from bs4 import BeautifulSoup
import urllib2

def scraper(url):
    r = requests.get(url)
    content = re.sub(r"<[^>]*>", " ", r.content)
    print content
    print_emails(content)
    print_urls(content)
    print_phone_numbers(content)
    print_images(r)
    print_href(r)


def print_emails(content):
    """Returns emails"""
    # create regular expression object
    email_regex = re.compile(
        r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    emails = email_regex.findall(content) # looking for patterns in the content

    for email in emails:
        print(email)


def print_phone_numbers(content):
    """Returns phone numbers"""
    # create regular expression object
    phone_regex = re.compile(
        r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]'
        + r'{2})\W*([0-9]{4})(\se?x?t?(\d*))?')
    phone_numbers = phone_regex.findall(content) # looking for patterns in the content
    for number in phone_numbers:
        print('{}-{}-{}'.format(number[0], number[1], number[2]))


def print_urls(content):
    """Returns urls"""
    # create regular expression object
    url_regex = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
        + r'|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = url_regex.findall(content) # looking for patterns in the content
    for url in urls:
        print(url)

def print_images(r):
    """Returns img tags"""
    print "in print_images "
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('img'):
        print(link.get('src')) 

def print_href(r):
    """Returns href tags"""
    print "in print_images"
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('a'):
        print(link.get('href'))


   def create_parser():
    """retrieves url from command line arguments """
    summary = "Extracts URLs, email addresses," \
        + " and phone numbers from specified website"
    parser = argparse.ArgumentParser(description=summary)
    parser.add_argument('url', help='url of website to be parsed')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    scraper(args.url)