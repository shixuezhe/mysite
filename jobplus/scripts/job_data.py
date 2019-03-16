import scrapy

class JobSpider(scrapy.Spider):
    name = 'jobs'
 
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/zhaopin/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    def start_requests(self):
        url_tmp = ['https://www.lagou.com/zhaopin/{}/'.format(i) for i in range(1,21)]
        for url in url_tmp:
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers)

    def parse(self, response):
        for job in response.css('li.con_list_item'):
            yield {
                'name':job.xpath('.//div[@class="p_top"]/a/h3/text()').extract_first(),
                'location':job.xpath('.//span[@class="add"]/em/text()').extract_first(),
                'experience':job.xpath('.//div[@class="p_bot"]/div/text()').re(r'\s*(.+)\s*/\s*(.+)\s*')[0],
                'degree':job.xpath('.//div[@class="p_bot"]/div/text()').re(r'\s*(.+)\s*/\s*(.+)\s*')[1],
                'wage_low':job.xpath('.//span[@class="money"]/text()').re(r'(.+)-(.+)')[0],
                'wage_high': job.xpath('.//span[@class="money"]/text()').re(r'(.+)-(.+)')[1],
                'tags':job.xpath('.//div[@class="list_item_bot"]/div/span/text()').extract()
                }


