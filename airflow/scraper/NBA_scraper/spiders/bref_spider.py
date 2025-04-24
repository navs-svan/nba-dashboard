import scrapy
from NBA_scraper.items import PlayerProps


class BrefSpiderSpider(scrapy.Spider):
    name = "bref_spider"
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "https://www.basketball-reference.com/leagues/NBA_2025_games-october.html"
    ]

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10,  # Stop after 10 items
    }

    def parse(self, response):
        months = response.css("div.filter div")
        for month in months:
            month_url = month.css("a::attr(href)").get()

            yield response.follow(month_url, callback=self.parse_page)

        # month_url = "/leagues/NBA_2025_games-october.html"
        yield response.follow(month_url, callback=self.parse_page)

    def parse_page(self, response):
        rows = response.css("table#schedule tbody tr:not([class=thead])")
        for row in rows:
            if boxscore_url := row.css(
                'td[data-stat="box_score_text"] a::attr(href)'
            ).get():
                game_data = {
                    "date": row.css('th[data-stat="date_game"] a::text').get(),
                    "away_team": row.css(
                        'td[data-stat="visitor_team_name"] a::text'
                    ).get(),
                    "home_team": row.css(
                        'td[data-stat="home_team_name"] a::text'
                    ).get(),
                }

                yield response.follow(
                    boxscore_url, callback=self.parse_boxscore, cb_kwargs=game_data
                )

    def parse_boxscore(self, response, date, away_team, home_team):

        props = PlayerProps()
        team_tupe = (away_team, home_team)
        homecourt = (False, True)
        basic_stats_table = response.css('table[id$="game-basic"] tbody')
        advance_stats_table = response.css('table[id$="game-advanced"] tbody')

        for index, (basic_table, advance_table) in enumerate(zip(basic_stats_table, advance_stats_table)):
            basic_rows = basic_table.css('tr:not([class*="thead"])')
            advance_rows = advance_table.css('tr:not([class*="thead"])')
            for basic, advance in zip(basic_rows, advance_rows):

                props["name"] = basic.css("th a::text").get()
                props["minutes"] = basic.css('[data-stat="mp"]::text').get()
                props["field_goals"] = basic.css('[data-stat="fg"]::text').get()
                props["fg_attempts"] = basic.css('[data-stat="fga"]::text').get()
                props["fg_percent"] = basic.css('[data-stat="fg_pct"]::text').get()
                props["fg_three"] = basic.css('[data-stat="fg3"]::text').get()
                props["fg_three_attempts"] = basic.css('[data-stat="fg3a"]::text').get()
                props["fg_three_percent"] = basic.css('[data-stat="fg3_pct"]::text').get()
                props["ft_made"] = basic.css('[data-stat="ft"]::text').get()
                props["ft_attempt"] = basic.css('[data-stat="fta"]::text').get()
                props["ft_percent"] = basic.css('[data-stat="ft_pct"]::text').get()
                props["rb_offensive"] = basic.css('[data-stat="orb"]::text').get()
                props["rb_defensive"] = basic.css('[data-stat="drb"]::text').get()
                props["rb_total"] = basic.css('[data-stat="trb"]::text').get()
                props["assists"] = basic.css('[data-stat="ast"]::text').get()
                props["steals"] = basic.css('[data-stat="stl"]::text').get()
                props["blocks"] = basic.css('[data-stat="blk"]::text').get()
                props["turnovers"] = basic.css('[data-stat="tov"]::text').get()
                props["personal_fouls"] = basic.css('[data-stat="pf"]::text').get()
                props["points"] = basic.css('[data-stat="pts"]::text').get()
                props["game_score"] = basic.css('[data-stat="game_score"]::text').get()
                props["plus_minus"] = basic.css('[data-stat="plus_minus"]::text').get()

                props["true_shoot_percent"] = advance.css('[data-stat="ts_pct"]::text').get()
                props["efg_percent"] = advance.css('[data-stat="efg_pct"]::text').get()
                props["fg_three_attempt_rate"] = advance.css('[data-stat="fg3a_per_fga_pct"]::text').get()
                props["ft_attempt_rate"] = advance.css('[data-stat="fta_per_fga_pct"]::text').get()
                props["rb_off_percent"] = advance.css('[data-stat="orb_pct"]::text').get()
                props["rb_def_percent"] = advance.css('[data-stat="drb_pct"]::text').get()
                props["rb_tot_percent"] = advance.css('[data-stat="trb_pct"]::text').get()
                props["assist_percent"] = advance.css('[data-stat="ast_pct"]::text').get()
                props["steal_percent"] = advance.css('[data-stat="stl_pct"]::text').get()
                props["block_percent"] = advance.css('[data-stat="blk_pct"]::text').get()
                props["turnover_percent"] = advance.css('[data-stat="tov_pct"]::text').get()
                props["usage_percent"] = advance.css('[data-stat="usg_pct"]::text').get()
                props["off_rating"] = advance.css('[data-stat="off_rtg"]::text').get()
                props["def_rating"] = advance.css('[data-stat="def_rtg"]::text').get()
                props["box_plus_minus"] = advance.css('[data-stat="bpm"]::text').get()

                props["home_court"] = homecourt[index]
                props["date"] = date
                props["team"] = team_tupe[index]
                props["opponent"] = tuple(reversed(team_tupe))[index]

                yield props
