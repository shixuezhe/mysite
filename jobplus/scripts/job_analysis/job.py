import scrapy


class LagouJob(scrapy.Spider):
    name = 'job'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/zhaopin/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    DOWNLOAD_DELAY = 30

    def start_requests(self):
        url_tmp = ['https://www.lagou.com/zhaopin/{}/'.format(i) for i in range(1, 31)]
        for url in url_tmp:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for job in response.css('li.con_list_item'):
            yield {
                'title': job.xpath('.//div[@class="p_top"]/a/h3/text()').extract_first(),
                'city': job.xpath('.//span[@class="add"]/em/text()').extract_first().split('·')[0],
                'area': job.xpath('.//span[@class="add"]/em/text()').extract_first(),
                'experience': job.xpath('.//div[@class="p_bot"]/div/text()').re(r'\s*(.+)\s*/\s*(.+)\s*')[0],
                'education': job.xpath('.//div[@class="p_bot"]/div/text()').re(r'\s*(.+)\s*/\s*(.+)\s*')[1],
                'salary_lower': job.xpath('.//span[@class="money"]/text()').re(r'(.+)k-(.+)k')[0],
                'salary_upper': job.xpath('.//span[@class="money"]/text()').re(r'(.+)k-(.+)k')[1],
                'tags': job.xpath('.//div[@class="list_item_bot"]/div/span/text()').extract(),
                'company': job.xpath('.//div[@class="company_name"]/a/text()').extract_first()
                }

