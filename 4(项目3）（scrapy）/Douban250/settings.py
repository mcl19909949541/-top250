
BOT_NAME = 'Douban250'

SPIDER_MODULES = ['Douban250.spiders']
NEWSPIDER_MODULE = 'Douban250.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'

ROBOTSTXT_OBEY = False

LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
   'Douban250.pipelines.Douban250Pipeline': 300,
}

# #存储为csv 设置Pipiline_ToCSV
# ITEM_PIPELINES = {
#    'Douban250.pipelines.savefileTongscrapyPipeline' : 300,
# }

# 存储为json 设置JsonPipeline
ITEM_PIPELINES = {
    'Douban250.pipelines.JsonPipeline' : 300,
}
FEED_EXPORT_ENCODING='UTF-8'  #设置存储编码为utf-8,存json中文就不会乱码，不加就乱码

# #存储到mysql
# ITEM_PIPELINES = {
#        'Douban250.pipelines.HellospiderPipeline': 300,
# }
#
# ROBOTSTXT_OBEY = False

# #保存图片
# ITEM_PIPELINES = { 'Dpuban250.pipelines.Top250Pipeline': 1,}
# IMAGES_STORE = 'pitcures'   #存储图片的文件夹位置