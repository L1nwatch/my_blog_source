# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.07.13 新增 log 操作
2017.07.09 重构一下视图, 现在 summary 的内容也是由代码生成而不是硬编码的了
2017.07.02 重构一下视图, 现在菜单栏是由代码生成的而不是硬编码的了
2017.06.30 新增 life_summary 视图函数
"""

# 标准库
from django.shortcuts import render
import logging

# 自己的模块
import my_constant as const
from common_module.common_help_function import log_wrapper

logger = logging.getLogger("my_blog.app_timeline.views")


def create_sidebar_items():
    """
    为左边的菜单栏创建 items
    """
    items = list()

    for each_id, each_number, each_name in zip(const.LIFE_SUMMARY_SIDEBAR_IDS,
                                               range(len(const.LIFE_SUMMARY_SIDEBAR_NAMES)),
                                               const.LIFE_SUMMARY_SIDEBAR_NAMES):
        items.append(const.LIFE_SUMMARY_SIDEBAR_ITEMS(each_id, each_number, each_name))

    return items


def create_summary_1():
    """
    笔记有点多,分开来创建吧
    :return: const.SUMMARY_STRUCTURE
    """
    # id-1 的笔记
    id_1_field_note_1 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "清扬，薄荷味，洗完确实没头屑，但是有油", ""),
                         const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "沙宣，黑色，千万不要买；红色那款想试就试吧", ""),
                         const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "马油，很好，洗了没油也没头皮屑", ""),
                         const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "洗发水不要买那款油脂平衡的，洗得很不舒服", ""),
                         ]

    id_1_field_note_2 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(1, "沐浴露买那个日本的资生堂可悠然(KUYURA)",
                                                             ["蓝色的那款, 恬静清香型, 洗完没味道好像, 反正没怎么感觉到",
                                                              "绿色的那款, 碧野悠悠型, 还没用过",
                                                              "橙色的那款, 花漾之恋型, 还没用过",
                                                              "粉红的那款, 欣怡幽香型, 还没用过"]),
                         const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "还有需要买个类似于搓泥的东西来洗脚（搓泥浴宝）", "")]

    id_1_field_note_3 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "洗衣液买汰渍的，挺香", "")]

    id_1_field = [const.SUMMARY_FIELD_STRUCTURE("洗发水", id_1_field_note_1),
                  const.SUMMARY_FIELD_STRUCTURE("沐浴露", id_1_field_note_2),
                  const.SUMMARY_FIELD_STRUCTURE("洗衣液", id_1_field_note_3),
                  ]

    return const.SUMMARY_STRUCTURE("one", "洗漱用品", id_1_field)


def create_summary_2():
    """
    笔记有点多,分开来创建吧
    :return: const.SUMMARY_STRUCTURE
    """
    field_note_1 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "以后不要再住布丁了", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "住酒店最好有窗户", ""),
                    ]

    field_note_2 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "厕所要有水龙头啊，要不然刷鞋不方便", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "合租的话至少要有 2 个厕所, 当然最好是一人一个厕所", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "租的房子一定得有能够代替收快递的门房之类的, 最好有速递易这样的自提箱", "")]

    fields = [const.SUMMARY_FIELD_STRUCTURE("出差旅行住酒店", field_note_1),
              const.SUMMARY_FIELD_STRUCTURE("出租房", field_note_2),
              ]

    return const.SUMMARY_STRUCTURE("two", "租房", fields)


def create_summary_3():
    """
    笔记有点多,分开来创建吧
    :return: const.SUMMARY_STRUCTURE
    """
    field_note_1 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "优衣库 180/108B 偏大", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "以后不管买什么，都买 175 的，不管是不是外套还是啥的，只看身高！", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "买安卓 fq 的都买 L 号的", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "迪卡侬的外套，建议买 L 的", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "裤子 3 条不够用，起码 4 条", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(2, "",
                                                        ["短裤可以去迪卡侬买拉链短裤",
                                                         "反光运动服迪卡侬有",
                                                         "裤子买跟亚马逊那条一样的材料，不会乱叫"]),
                    ]

    field_note_2 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "买鞋以后都买 44 码的", ""), ]

    fields = [const.SUMMARY_FIELD_STRUCTURE("衣服", field_note_1),
              const.SUMMARY_FIELD_STRUCTURE("鞋子", field_note_2),
              ]

    return const.SUMMARY_STRUCTURE("three", "服装", fields)


def create_summary_4():
    """
    笔记有点多,分开来创建吧
    :return: const.SUMMARY_STRUCTURE
    """
    field_note_1 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "录音手环绝对不买 JNN 家的，太坑了，BUG 一大堆，下次电子产品还是买知名厂家的吧", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0,
                                                        "以后买手环，手表之类的，不要买带子是扣子扣的那种，容易掉，要买类似于手表的那种，有个小针穿过去的。或者看看iwatch 是怎么设计的",
                                                        ""),
                    ]

    field_note_2 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "耳机盒子 8 cm 左右差不多", ""),
                    ]

    fields = [const.SUMMARY_FIELD_STRUCTURE("录音手环", field_note_1),
              const.SUMMARY_FIELD_STRUCTURE("耳机", field_note_2),
              ]

    return const.SUMMARY_STRUCTURE("four", "电子装备", fields)


def create_summary_5():
    """
    笔记有点多,分开来创建吧
    :return: const.SUMMARY_STRUCTURE
    """
    field_note_1 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "需要区分自己是不是油性，如果是的话则要经常清理", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "目前的计划是，只清理耳朵外围的，一旦出现听力衰减等情况就去医院处理", ""),
                    ]

    field_note_2 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "可以查看历史价格，没必要等 0 点抢券啥的，平时想买直接领券，有好券直接买，不用等时间了", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "使用 Apple Pay 一律京东闪付", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "其余情况看哪家支付有优惠就用哪家，比如招商银行提示有优惠就用招商银行", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "要买到比实际卖价更便宜的产品，自己去度娘下载一些获取内部优惠券的插件，比如店侦探，查淘客，淘客助手等等", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0,
                                                        "当你想到购买某件刚需性，并且淡旺季很明显的产品时，往前推2个月，是买那件东西最便宜的时候，比如电风扇，5月份天气热了，3月份-4月份是买电风扇是最便宜的",
                                                        ""),
                    ]

    field_note_3 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(1, "洗衣袋",
                                                        ["只用来洗袜子和内裤",
                                                         "买大一点的洗衣袋",
                                                         "俩洗衣袋不够用，最好买三个以上",
                                                         "袜子和内裤还能分开来洗的"]),
                    ]

    field_note_4 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "清洁舌苔", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "至少 3 分钟（电动牙刷 2 分钟）", ""),
                    ]

    fields = [const.SUMMARY_FIELD_STRUCTURE("耵聍清理的问题", field_note_1),
              const.SUMMARY_FIELD_STRUCTURE("购物/付款问题", field_note_2),
              const.SUMMARY_FIELD_STRUCTURE("洗衣服", field_note_3),
              const.SUMMARY_FIELD_STRUCTURE("刷牙", field_note_4),
              ]

    return const.SUMMARY_STRUCTURE("five", "生活习惯", fields)


def create_summary_6():
    """
    笔记有点多,分开来创建吧
    :return: const.SUMMARY_STRUCTURE
    """
    field_note_1 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "买肥皂盒的时候要买带盖子的（如果需要买肥皂盒的话）", ""),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(1, "保持器盒子：",
                                                        ["高：2.9cm，勉强可以接受",
                                                         "长：7 cm，太大，少个 3 cm 还差不多",
                                                         "宽：8 cm，太大，少个 3 cm 还差不多"]),
                    const.SUMMARY_FIELD_NOTES_STRUCTURE(0, "插座买个带按钮的", ""),
                    ]

    fields = [const.SUMMARY_FIELD_STRUCTURE("各种杂物", field_note_1),
              ]

    return const.SUMMARY_STRUCTURE("six", "生活用品", fields)


def create_summary_7():
    """
    笔记有点多,分开来创建吧
    :return: const.SUMMARY_STRUCTURE
    """
    field_note_1 = [const.SUMMARY_FIELD_NOTES_STRUCTURE(1, "吃桃子要不要削皮?",
                                                        ["小桃子: 没毛, 洗完可以直接吃",
                                                         "大桃子：有毛, 对毛敏感的最好削皮吃"]),
                    ]

    fields = [const.SUMMARY_FIELD_STRUCTURE("水果", field_note_1),
              ]

    return const.SUMMARY_STRUCTURE("seven", "饮食", fields)


def create_summarys():
    """
    为笔记内容创建 summarys, 方便传给视图显示
    :return: list(), 每一个是 summary
    """
    result = list()

    for x in [create_summary_1(), create_summary_2(), create_summary_3(), create_summary_4(),
              create_summary_5(), create_summary_6(), create_summary_7()]:
        result.append(x)

    return result


@log_wrapper(str_format="访问了生活经历", level="info", logger=logger)
def life_summary(request):
    items = create_sidebar_items()
    summarys = create_summarys()
    return render(request, const.LIFE_SUMMARY_TEMPLATE, context={"post_items": items,
                                                                 "summarys": summarys})
