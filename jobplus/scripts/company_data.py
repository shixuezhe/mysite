import scrapy

class CompanySpider(scrapy.Spider):
    name = 'companies'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/gongsi/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    def start_requests(self):
        urls = ['https://www.lagou.com/gongsi/{}/'.format(i) for i in range(1,11)]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers)

    def parse(self, response):
        for company in response.css('li.company-item'):
            yield {
                'name':company.xpath('.//p[contains(@class,"company-name")]/a/text()').extract_first(),
                'logo':company.xpath('.//div[@class="top"]/p/a/img/@src').extract_first(),
                'type':company.xpath('.//p[contains(@class,"indus-stage")]/text()').re(r'(.+)\s*/\s*(.+)/\s*(.+)')[0],
                'finance': company.xpath('.//p[contains(@class,"indus-stage")]/text()').re(r'(.+)\s*/\s*(.+)/\s*(.+)')[1],
                'staff_num': company.xpath('.//p[contains(@class,"indus-stage")]/text()').re(r'(.+)\s*/\s*(.+)/\s*(.+)')[2],
                'description':company.xpath('.//p[contains(@class,"advantage")]/text()').extract_first().strip()
            }
