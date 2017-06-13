/**
 * Created by L1n on 17/5/22.
 */

/*
 该函数处理 span, 即加号、减号的点击操作
 */
function add_current_for_show(show_button) {
    // 为 父级-li 添加 current 方便显示下一级标题
    $($(show_button).parent()).toggleClass("current");

    // 如果当前为 + 号, 点击之后变 - 号, 确保确保同级 a 标签有 current
    if ($(show_button).hasClass("fa-plus-square-o")) {
        $(show_button).removeClass("fa-plus-square-o");
        $(show_button).addClass("fa-minus-square-o");
        $(show_button.siblings("a")).addClass("current")
    }

    // 如果当前为 - 号, 点击之后变 + 号, 确保同级 a 标签没有 current
    else if ($(show_button).hasClass("fa-minus-square-o")) {
        $(show_button).removeClass("fa-minus-square-o");
        $(show_button).addClass("fa-plus-square-o");
        $(show_button.siblings("a")).removeClass("current")
    }

}

/*
 该函数处理 a 标签被点击时的情况
 */
function add_current_for_a_show(class_name, a_show) {
    // 确保被点击时, 除了该 a 标签以外的所有 a 标签都不会有 current
    $(class_name).removeClass("current");
    $(a_show).addClass("current");
}

$(document).ready(function () {
    // 为第 1 级目录树添加展开按钮相关代码
    $(".show-button1").click(function () {
        add_current_for_show($(this));
    });

    // 为第 1 级目录树添加展开按钮相关代码
    $(".a-show1").click(function () {
        add_current_for_a_show(".a-show1", $(this));
    });

    // 为第 2 级目录树添加展开按钮相关代码
    $(".show-button2").click(function () {
        add_current_for_show($(this));
    });

    // 为第 2 级目录树添加展开按钮相关代码
    $(".a-show2").click(function () {
        add_current_for_a_show(".a-show2", $(this));
    });

    // 判断一级目录是否有多个, 如果小于 3 个则自动展开
    if ($(".toctree-l1").length < 3) {
        add_current_for_show($(".show-button1"));
        // 判断二级目录是否有多个, 如果小于 3 个则自动展开
        if ($(".toctree-l2").length < 3) {
            add_current_for_show($(".show-button2"));
        }
    }

});