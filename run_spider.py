# run_spider.py
import sys
import os
from scrapy.cmdline import execute

project_dir = '/home/amtspy/'
sys.path.append(project_dir)

# Replace 'amtspy' with the name of your Scrapy spider
spider_name = 'amtspy'

# The settings for your Scrapy spider, e.g., to output results to a file
settings = {
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output.json',  # Change this to the desired output file path
    # Other spider settings as needed
}

# Execute the Scrapy spider with the specified settings
execute(['scrapy', 'crawl', spider_name, '-t', settings['FEED_FORMAT'], '-o', settings['FEED_URI']])
