import logging
from django.shortcuts import render
from common_module.common_help_function import log_wrapper

logger = logging.getLogger("my_blog.homepage.views")


# Create your views here.
@log_wrapper(str_format="访问索引页", logger=logger)
def index_view(request):
    return render(request, 'index_home.html')
