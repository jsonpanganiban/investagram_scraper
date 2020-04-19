# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class SQLite3Pipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect('investagram.db')
        self.cur = self.connection.cursor()
        try:
            self.cur.execute('''
                CREATE TABLE investagram(
                    last_price TEXT,
                    change TEXT,
                    percent_change TEXT,
                    open TEXT,
                    high TEXT,
                    volume TEXT,
                    net_foreign TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute('''
            INSERT INTO investagram(last_price, change, percent_change, open, high, volume, net_foreign) VALUES(?,?,?,?,?,?, ?)
        ''', (
            item.get('last_price'),
            item.get('change'),
            item.get('percent_change'),
            item.get('open'),
            item.get('high'),
            item.get('volume'),
            item.get('net_foreign')
        ))
        self.connection.commit()
        return item
