import json #line:2
from django import template #line:4
register =template .Library ()#line:6
from import_export .admin import ImportExportMixinBase #line:8
from simplepro import conf #line:9
import simplepro #line:10
import simpleui #line:11
@register .simple_tag (takes_context =True )#line:14
def has_import_export (context ):#line:15
    O0OOO0OOO0O000OOO =context .get ('cl')#line:16
    return issubclass (O0OOO0OOO0O000OOO .__class__ ,ImportExportMixinBase )#line:17
@register .simple_tag (takes_context =True )#line:20
def get_display_name (context ):#line:21
    O0OOO0OOO0OOOO00O =context .get ('user')#line:22
    if O0OOO0OOO0OOOO00O :#line:24
        OOOOO0O0O0OO00O0O =''#line:25
        if O0OOO0OOO0OOOO00O .first_name :#line:27
            OOOOO0O0O0OO00O0O +=O0OOO0OOO0OOOO00O .first_name #line:28
        if O0OOO0OOO0OOOO00O .last_name :#line:29
            OOOOO0O0O0OO00O0O +=O0OOO0OOO0OOOO00O .last_name #line:30
    if not OOOOO0O0O0OO00O0O :#line:31
        OOOOO0O0O0OO00O0O =str (O0OOO0OOO0OOOO00O )#line:32
    return OOOOO0O0O0OO00O0O #line:33
@register .simple_tag #line:36
def get_server_url ():#line:37
    return conf .get_server_url ()#line:38
@register .simple_tag #line:41
def get_sp_version ():#line:42
    return simplepro .get_version ()#line:43
@register .simple_tag #line:46
def get_device_id ():#line:47
    return conf .get_device_id ()#line:48
@register .simple_tag #line:51
def get_simple_version ():#line:52
    return simpleui .get_version ()#line:53
