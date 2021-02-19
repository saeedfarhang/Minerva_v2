from datetime import datetime
import pytz
from main.models import Tag
def tehran_now():
    tz = pytz.timezone('Asia/tehran')
    return datetime.now(tz)


# tagnamelist = ["tag1", "tag2", ...]
def tagname_to_tagid(data,tagname_list):
    tagid_list = []
    for tag_name in tagname_list:
        try:
            tag_item = Tag.objects.get(title=tag_name)
        except :
            Tag.objects.create(title=tag_name).save()
            tag_item = Tag.objects.get(title=tag_name)
        tagid_list.append(tag_item.id)
        data.update({'tags':tagid_list})