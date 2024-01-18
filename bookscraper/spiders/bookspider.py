import scrapy
from urllib.parse import urljoin

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            name = book.css("h3 a::text").get()
            price = book.css(".product_price .price_color::text").get()
            url = book.css("h3 a").attrib['href']

            yield {
                "name": name,
                "price": price,
                "url": url
            }

        next_page = response.css("li.next a::attr(href)").get()

        if next_page is not None:
            next_page_url = urljoin(response.url, next_page)  # type: ignore
            yield response.follow(next_page_url, callback=self.parse)