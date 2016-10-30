import articles.views
from my_constant import const

import os


def update_gitbook_codes(request):
    """
    2016.10.30 实现 git push 功能
    :param request:
    :return:
    """
    notes_git_path = const.GITBOOK_CODES_PATH
    gitbook_category_dict = const.GITBOOK_CODES_REPOSITORY
    notes_path_parent_dir = const.NOTES_PATH_PARENT_DIR

    for gitbook_name, address in gitbook_category_dict.items():
        # 判断是否已经 git 过
        if not os.path.exists(os.path.join(notes_git_path, gitbook_name, ".git")):
            # 确保目录已经建立了
            os.system("mkdir -p {}".format(notes_git_path))

            # 没有 git 过则执行 git clone 操作
            command = ("cd {} && git clone {} {}"
                       .format(notes_git_path, address, gitbook_name))
        else:
            # 如果有 git 过则执行更新操作
            command = "cd {} && git reset --hard && git pull".format(os.path.join(notes_git_path, gitbook_name))
        os.system(command)
    return articles.views.home(request)
