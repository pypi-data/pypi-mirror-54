"""
BaseModelWithSoftDelete template for model generator
"""

TEMPLATE_ADMIN_SOFTDELETEMODEL = """import logging

from django.contrib import admin

from vb_baseapp.admin import CustomBaseModelAdminWithSoftDelete
from vb_baseapp.utils import console

from ..models import {model_name_title}

__all__ = ['{model_name_title}Admin']

logger = logging.getLogger('app')
console = console(source=__name__)


@admin.register({model_name_title})
class {model_name_title}Admin(CustomBaseModelAdminWithSoftDelete):
    # sticky_list_filter = None
    # hide_deleted_at = False
    pass

"""


__all__ = ['TEMPLATE_ADMIN_SOFTDELETEMODEL']
