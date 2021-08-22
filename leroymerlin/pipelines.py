# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroymerlinPipeline:
    def __init__(self):
        self.MONGO_HOST = "localhost"
        self.MONGO_PORT = 27017
        self.MONGO_DB = 'LM'

    def process_item(self, item, spider):
        self.specifications(item)
        try:
            item['prim_price'] = int(item['prim_price'])
        except ValueError:
            item['prim_price'] = float(item['prim_price'])
        self.to_mongo_vacancy(item, spider, self.MONGO_DB)

    def specifications(self, item):
        item.update({'specifications': {}})
        for el in range(len(item['spec_term'])):
            dct = {item['spec_term'][el]: item['spec_def'][el].replace('\n', '').replace('  ', '')}
            item['specifications'].update(dct)
        item.pop('spec_term')
        item.pop('spec_def')
        return item

    def to_mongo_vacancy(self, base, spider, MONGO_DB):
        with MongoClient(self.MONGO_HOST, self.MONGO_PORT) as client:
            db = client[MONGO_DB]
            users = db[spider.name]
            update_data = {
                "$set": {
                    "title": base['title'],
                    "prim_price": base['prim_price'],
                    "vendor_code": base['vcode'],
                    "specifications": base['specifications'],
                    "link": base['link']
                }
            }
            filter_data = {"link": base['link']}
            users.update_many(filter_data, update_data, upsert=True)


class LMPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        path = str()
        for el in item['path']:
            path = path + el + '/'
        path = path + item['vcode'] + '/' + request.url.split('/')[-1]
        return path

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
