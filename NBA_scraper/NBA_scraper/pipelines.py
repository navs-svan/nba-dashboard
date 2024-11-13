# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import psycopg2


class NbaScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # convert date to proper format
        format = "%a, %b %d, %Y"
        date_value = adapter.get("date")
        date = datetime.datetime.strptime(date_value, format)
        adapter["date"] = date.date()

        # add hours to gametime
        if time_value:=adapter.get("minutes"):
            gametime = "00:" + time_value
            adapter["minutes"] = gametime
        else:
            adapter["minutes"] = '0 hours 0 minutes 0 seconds'

        return item


class PostgresPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # Start Connection
        hostname = settings.get("DB_HOST")
        username = settings.get("DB_USER")
        password = settings.get("DB_PASS")
        database = settings.get("DB_DATA")

        self.connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            database=database,
            port=5432,
        )
        self.cur = self.connection.cursor()

        # Create Table
        self.cur.execute(
            """ 
                CREATE TABLE IF NOT EXISTS props(
                    id serial PRIMARY KEY,
                    date DATE,
                    home_court BOOLEAN,
                    team VARCHAR(64),
                    opponent VARCHAR(64),

                    name VARCHAR(64),
                    minutes INTERVAL,
                    field_goals INTEGER,
                    fg_attempts INTEGER,
                    fg_percent NUMERIC,
                    fg_three INTEGER,
                    fg_three_attempts INTEGER,
                    fg_three_percent NUMERIC,
                    ft_made INTEGER,
                    ft_attempt INTEGER,
                    ft_percent NUMERIC,
                    rb_offensive INTEGER,
                    rb_defensive INTEGER,
                    rb_total INTEGER,
                    assists INTEGER,
                    steals INTEGER,
                    blocks INTEGER,
                    turnovers INTEGER,
                    personal_fouls INTEGER,
                    points INTEGER,
                    game_score NUMERIC,
                    plus_minus INTEGER,

                    true_shoot_percent NUMERIC,
                    efg_percent NUMERIC,
                    fg_three_attempt_rate NUMERIC,
                    ft_attempt_rate NUMERIC,
                    rb_off_percent NUMERIC,
                    rb_def_percent NUMERIC,
                    rb_tot_percent NUMERIC,
                    assist_percent NUMERIC,
                    steal_percent NUMERIC,
                    block_percent NUMERIC,
                    turnover_percent NUMERIC,
                    usage_percent NUMERIC,
                    off_rating INTEGER,
                    def_rating INTEGER,
                    box_plus_minus NUMERIC

            )              
            """
        )

        self.connection.commit()

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                """INSERT INTO props(
                            date,
                            home_court,
                            team,
                            opponent,
                            name,
                            minutes,
                            field_goals,
                            fg_attempts,
                            fg_percent,
                            fg_three,
                            fg_three_attempts,
                            fg_three_percent,
                            ft_made,
                            ft_attempt,
                            ft_percent,
                            rb_offensive,
                            rb_defensive,
                            rb_total,
                            assists,
                            steals,
                            blocks,
                            turnovers,
                            personal_fouls,
                            points,
                            game_score,
                            plus_minus,
                            true_shoot_percent,
                            efg_percent,
                            fg_three_attempt_rate,
                            ft_attempt_rate,
                            rb_off_percent,
                            rb_def_percent,
                            rb_tot_percent,
                            assist_percent,
                            steal_percent,
                            block_percent,
                            turnover_percent,
                            usage_percent,
                            off_rating,
                            def_rating,
                            box_plus_minus
                            ) VALUES (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                                )""",
                (
                    item["date"],
                    item["home_court"],
                    item["team"],
                    item["opponent"],
                    item["name"],
                    item["minutes"],
                    item["field_goals"],
                    item["fg_attempts"],
                    item["fg_percent"],
                    item["fg_three"],
                    item["fg_three_attempts"],
                    item["fg_three_percent"],
                    item["ft_made"],
                    item["ft_attempt"],
                    item["ft_percent"],
                    item["rb_offensive"],
                    item["rb_defensive"],
                    item["rb_total"],
                    item["assists"],
                    item["steals"],
                    item["blocks"],
                    item["turnovers"],
                    item["personal_fouls"],
                    item["points"],
                    item["game_score"],
                    item["plus_minus"],
                    item["true_shoot_percent"],
                    item["efg_percent"],
                    item["fg_three_attempt_rate"],
                    item["ft_attempt_rate"],
                    item["rb_off_percent"],
                    item["rb_def_percent"],
                    item["rb_tot_percent"],
                    item["assist_percent"],
                    item["steal_percent"],
                    item["block_percent"],
                    item["turnover_percent"],
                    item["usage_percent"],
                    item["off_rating"],
                    item["def_rating"],
                    item["box_plus_minus"],
                ),
            )
        except psycopg2.errors.InFailedSqlTransaction:
            self.cur.execute("ROLLBACK")

        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

