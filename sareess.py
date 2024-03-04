import scrapy
from sarees.items import SareesItem


class SareessSpider(scrapy.Spider):
    name = "sareess"
    allowed_domains = ["shopzters.com"]
    #start_urls = ["https://shopzters.com/collections/sarees"]

    def start_requests(self):
        urlss='https://shopzters.com/collections/sarees?page={}'   
        #10
        for i in range(1,11):
            aurl=urlss.format(i)
            yield scrapy.Request(url=aurl,callback=self.producturls)

    def producturls(self, response):
        sarees=response.xpath("//div[@class='grid-product__content']/a")
        for saree in sarees:
            rurl=saree.xpath("./@href").get()
            aurl=response.urljoin(rurl)
            #print(aurl)
            yield scrapy.Request(url=aurl,callback=self.parse2)

    def parse2(self,response):
        pname=response.xpath("//div[@class='product-single__meta']//h1/text()").get().strip('\n')   
        price=response.xpath("//span[@class='product__price']/span/text()").get()
        color=response.xpath("//fieldset[@name='Color']/div/label/text()").get()
        size=response.xpath("//fieldset[@name='Size']/div/label/text()").getall()
        desc=[]
        descs=response.xpath("//div[@class='product-block']/div[@class='rte']//text()").getall()
        for i in descs:
            desc.append(i.strip("' \n '"))

        '''if response.xpath("//div[@class='product-block']/div[@class='rte']/text()").get():
            desc.append(response.xpath("//div[@class='product-block']/div[@class='rte']/text()").get())
        elif response.xpath("//div[@class='product-block']/div[@class='rte']/div/span/text()").get():
            desc.append(response.xpath("//div[@class='product-block']/div[@class='rte']/div/span/text()").get())
        elif response.xpath("//div[@class='product-block']/div[@class='rte']//ul/li/text()").getall():   
            for i in response.xpath("//div[@class='product-block']/div[@class='rte']//ul/li/text()").getall():
                desc.append(i)
        else:
            desc.append("") '''       
        rawimgurls=response.xpath("//div[@class='product__thumb-item']/a/@href").getall()
        #sp=response.xpath("//div[@class='collapsible-content__inner rte']/p/text()").getall()
        sp=response.xpath("(//div[@class='collapsible-content__inner rte'])[1]/p/text()").getall()
        ep=response.xpath("(//div[@class='collapsible-content__inner rte'])[2]/p/text()").getall()
        #print(sp)
        
        iurls=[]
        for im in rawimgurls:
            iurls.append(response.urljoin(im))
        '''yield{
            "PRODUCT_NAME":pname,
            "PRICE":price,
            "COLOR":color,
            "DESCRIPTION":desc,
            "SHIPPINGPOLICY":sp,
            "EXCHANGE_POLICY":ep,
            'image_urls':iurls,
            'path': f'{pname}/' 
        }'''
        item=SareesItem()
        item['PRODUCT_NAME']=pname
        item['PRICE']=price
        item['COLOR']=color
        item['SIZE']=size
        item['DESCRIPTION']=desc
        item['SHIPPINGPOLICY']=sp
        item['EXCHANGE_POLICY']=ep
        item['image_urls']=iurls
        yield item
