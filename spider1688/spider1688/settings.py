# Scrapy settings for spider1688 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider1688'

SPIDER_MODULES = ['spider1688.spiders']
NEWSPIDER_MODULE = 'spider1688.spiders'

JOBDIR = '1688.com'  # crawl spider at breakpoint
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider1688 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'spider1688.middlewares.Spider1688SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'spider1688.middlewares.Spider1688DownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'spider1688.middlewares.Spider1688DownloaderMiddleware': 543,
}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'spider1688.pipelines.CategoryPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_URL = 'localhost'


PROXY_LIST = [
    {"ip_port": "http://211.137.52.158:8080"},
    {"ip_port": "http://111.47.154.34:53281"},
    {"ip_port": "http://183.220.145.3:80"},
    {"ip_port": "http://223.100.166.3:36945"},
    {"ip_port": "http://120.194.42.157:38185"},
    {"ip_port": "http://223.82.106.253:3128"},
    {"ip_port": "http://117.141.155.244:53281"},
    {"ip_port": "http://120.198.76.45:41443"},
    {"ip_port": "http://123.136.8.122:3128"},
    {"ip_port": "http://117.141.155.243:53281"},
    {"ip_port": "http://183.196.168.194:9000"},
    {"ip_port": "http://117.141.155.242:53281"},
    {"ip_port": "http://183.195.106.118:8118"},
    {"ip_port": "http://112.14.47.6:52024"},
    {"ip_port": "http://218.204.153.156:8080"},
    {"ip_port": "http://223.71.203.241:55443"},
    {"ip_port": "http://117.141.155.241:53281"},
    {"ip_port": "http://221.180.170.104:8080"},
    {"ip_port": "http://183.247.152.98:53281"},
    {"ip_port": "http://183.196.170.247:9000"},
]



