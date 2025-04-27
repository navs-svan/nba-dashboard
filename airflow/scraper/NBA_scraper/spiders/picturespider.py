# import scrapy
# from scrapy_playwright.page import PageMethod


# class PicturespiderSpider(scrapy.Spider):
#     name = "picturespider"
#     # allowed_domains = ["www.nba.com"]
#     # start_urls = ["https://www.nba.com/players"]

#     def start_requests(self):
#         url = "https://www.nba.com/players"
#         yield scrapy.Request(
#             url, 
#             meta={
#                 'playwright': True,
#                 'playwright_page_methods': [
#                     # wait for the dropdown list to load
#                     PageMethod("wait_for_selector", "div.PlayerList_pagination__c5ijE .DropDown_select__4pIg9"),
#                     PageMethod("click", "div.PlayerList_pagination__c5ijE .DropDown_select__4pIg9"),
#                     # select "All" option
#                     PageMethod("select_option", "div.PlayerList_pagination__c5ijE .DropDown_select__4pIg9", "-1"),
#                     # Allow extra time for large table loading
#                     PageMethod("wait_for_timeout", 6000),  
#                 ]
#             }
#         )

#     def parse(self, response):
#         table = response.css(
#             "table.players-list tbody tr div.RosterRow_playerHeadshot__tvZOn"
#         )
#         for row in table:

#             image_link = row.css("img::attr(src)").get()
#             player_name = row.css("img::attr(alt)").get().replace(" Headshot", "")

#             yield {"image_link": image_link, "player_name": player_name}
