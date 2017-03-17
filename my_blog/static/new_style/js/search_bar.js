/*
 * Search bar 相关 js
 * 2017.03.17 修正 focus 的 bug, 现在单击完下拉菜单就可以自动 focus 到 input 框了
 */

$(document).ready(function () {

    // Set up common variables
    // --------------------------------------------------

    var dropdown = ".search_dropdown";
    var dropdownLabel = dropdown + " > span";
    var dropdownList = dropdown + " ul";
    var dropdownListItems = dropdownList + " li";
    var id_search_choice = document.getElementById('id_search_choice');

    // Set up common functions
    // --------------------------------------------------

    function dropdownOn() {
        $(dropdownList).fadeIn(25);
        $(dropdown).addClass("active");
    }

    function dropdownOff() {
        $(dropdownList).fadeOut(25);
        $(dropdown).removeClass("active");
    }


    // Toggle new dropdown menu on click
    // --------------------------------------------------

    $(dropdown).click(function (event) {
        if ($(dropdown).hasClass("active")) {
            dropdownOff();
        } else {
            dropdownOn();
        }

        event.stopPropagation();
        return false;
    });

    $("html").click(dropdownOff);


    // Activate new dropdown option and show tray if applicable
    // --------------------------------------------------

    $(dropdownListItems).click(function () {
        $(this).siblings("li.selected").removeClass("selected");
        $(this).addClass("selected");

        // Focus the input
        $(this).parents("form").find("input").focus();

        var labelText = $(this).text();
        $(dropdownLabel).text(labelText);

        // 自动选择对应的选项
        id_search_choice.value = $(this).text().toLowerCase();
    });


});