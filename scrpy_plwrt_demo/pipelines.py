from scrapy.exporters import CsvItemExporter

class ScrpyPlwrtDemoPipeline:
    def open_spider(self, spider):
        self.exporters = {
            'box_office': CsvItemExporter(open('csv/box_office_ranking.csv', 'wb'), fields_to_export=[
                'rank', 'title', 'release_year', 'country', 'reservation', 'audience', 'image_url'
            ]),
            'watcha': CsvItemExporter(open('csv/watcha_ranking.csv', 'wb'), fields_to_export=[
                'rank', 'title', 'release_year', 'country', 'image_url'
            ]),
            'netflix': CsvItemExporter(open('csv/netflix_ranking.csv', 'wb'), fields_to_export=[
                'rank', 'title', 'release_year', 'country', 'image_url'
            ]),
        }
        for exporter in self.exporters.values():
            exporter.start_exporting()

    def process_item(self, item, spider):
        section = item.get('section')
        if section in self.exporters:
            self.exporters[section].export_item(item)
        return item

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
