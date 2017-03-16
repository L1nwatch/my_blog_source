/* Search bar */

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
        $(this).parents("form.search_bar:first").find("input[type=text]").focus();

        var labelText = $(this).text();
        $(dropdownLabel).text(labelText);

        // 自动选择对应的选项
        id_search_choice.value = $(this).text().toLowerCase();
    });


});