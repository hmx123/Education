import xadmin

from .models import EmailVerifyRecord,Banner
from xadmin import views

#xadmin中这里是继承object，不再是继承admin
class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 搜索的字段
    search_fields = ['code', 'email', 'send_type']
    # 过滤
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index', 'add_time']


# 创建xadmin最基本管理器配置
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True

# xadmin 全局配置
class GlobalSetting(object):
    #title
    site_title = '后台管理平台'
    # footer
    site_footer = ''
    # 收起菜单
    menu_style = 'accordion'

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
