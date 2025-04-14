# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

class ScrpyPlwrtDemoPipeline:
    def open_spider(self, spider):
        self.exporters = {
            'box_office': CsvItemExporter(open('csv/box_office_ranking.csv', 'wb')),
            'watcha': CsvItemExporter(open('csv/watcha_ranking.csv', 'wb')),
            'netflix': CsvItemExporter(open('csv/netflix_ranking.csv', 'wb'))
        }
        for exporter in self.exporters.values():
            exporter.start_exporting()

    def process_item(self, item, spider):
        section = item.get('section')  # 🔥 섹션 값 추출
        if section in self.exporters:
            self.exporters[section].export_item(item)
        return item

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
