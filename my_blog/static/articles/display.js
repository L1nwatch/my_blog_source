/**
 * Created by L1n on 17/5/22.
 */

function add_current_for_show(show_button) {
    // 为 li 添加 current 方便显示下一级标题
    $($(show_button).parent().parent()).toggleClass("current");
    // 为 a 添加 current 方便样式改变
    $($(show_button).parent()).toggleClass("current");

    // 将当前的 + 号改为减号
    $($(show_button)).toggleClass("fa-plus-square-o");
    $($(show_button)).toggleClass("fa-minus-square-o");
}

function add_current_for_a_show(class_name, a_show) {
    // 为 a 添加 current 方便显示跳转效果
    $(class_name).removeClass("current");
    $($(a_show)).toggleClass("current");
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