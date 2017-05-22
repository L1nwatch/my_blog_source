/**
 * Created by L1n on 17/5/22.
 */

$(document).ready(function () {
    $(".show-button").click(function () {
        // 为 li 添加 current 方便显示下一级标题
        $($(this).parent().parent()).toggleClass("current");
        // 为 a 添加 current 方便样式改变
        $($(this).parent()).toggleClass("current");

        // 将当前的 + 号改为减号
        $($(this)).toggleClass("fa-plus-square-o");
        $($(this)).toggleClass("fa-minus-square-o");
    });

    $(".a-show").click(function () {
        // 为 a 添加 current 方便显示跳转效果
        $(".a-show").removeClass("current");
        $($(this)).toggleClass("current");
    });

});