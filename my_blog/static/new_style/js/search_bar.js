/* Search bar */


$(document).ready(function () {

    // Set up common variables
    // --------------------------------------------------

    var dropdown = ".search_dropdown";
    var dropdownList = dropdown + " select";
    var dropdownListItems = dropdownList + " option";


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
        $(this).siblings("option.selected").removeClass("selected");
        $(this).addClass("selected");

        // Focus the input
        $(this).parents("form.search_bar:first").find("input").focus();


    });


});