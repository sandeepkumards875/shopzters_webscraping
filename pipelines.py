# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#from items import SareesItem
import random

from scrapy.pipelines.images import ImagesPipeline
'''class customimagepipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        #file_name=slugify(item['product_name'],max_length=200)
        #file_name=''
        #for i in range(len(item['image_urls'])):
        #num=random.randrange(1,15)
        file_name=item['PRODUCT_NAME']+str(random.randrange(1,100))
        #num=random.randrange(1,15)
        return f"full/{file_name}.jpg"'''
import os

from scrapy.pipelines.images import ImagesPipeline


'''class FolderStructureImagePipeline(ImagesPipeline):
    """Store Images using a folder tree structure.
    DEPTH attribute can be used to specify the depth of the tree.
    """
    DEPTH = 1

    def tree_path(self, path: str) -> str:
        """Generate a folder tree based on given path.
        I.e: path/to/image.jpg -> path/to/i/m/a/image.jpg
        
        :param path: original image filepath.
        :return: image filepath with extra folder tree.
        """
        filename = os.path.basename(path)
        dirname = os.path.dirname(path)
        return os.path.join(
            dirname, *[_ for _ in filename[:self.DEPTH]], filename
        )

    def file_path(self, request, response=None, info=None):
        return self.tree_path(
            super().file_path(request, response, info)
        )

    def thumb_path(self, request, thumb_id, response=None, info=None):
        return self.tree_path(
            super().thumb_path(request, thumb_id, response, info)
        )'''
'''from pathlib import PurePosixPath
from urllib.parse import urlparse

from scrapy.pipelines.images import ImagesPipeline


import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter["image_paths"] = image_paths
        return item'''
'''class customimagepipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        #file_name=slugify(item['product_name'],max_length=200)
        file_name=item['PRODUCT_NAME']
        #num=random.randrange(1,15)
        return f"full/{file_name}.jpg"'''
    
import slugify    
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
import shutil
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):

        for result in [x for ok, x in results if ok]:
            path = result['path']
            print("path :",path)
            slug = item['PRODUCT_NAME']
            print(slug)
            settings = get_project_settings()
            storage = settings.get('IMAGES_STORE')
            print(storage)

            target_path = os.path.join(storage, slug, os.path.basename(path))
            path = os.path.join(storage, path)

            # If path doesn't exist, it will be created
            if not os.path.exists(os.path.join(storage, slug)):
                os.makedirs(os.path.join(storage, slug))
            shutil.move(path, target_path)

        if self.IMAGES_RESULT_FIELD in item.fields:
            item[self.IMAGES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item

        