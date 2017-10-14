function get(e) {
    return document.getElementById(e)
}

function highlightCode(e) {
    if (hc.checked) {
        var a = e.innerHTML;
        a = a.replace(/\{([\s\S]+?)\}/g, function (e) {
            return e.replace(/\'(.*?)\'/g, "<span class='st'>'$1'</span>").replace(/\"(.*?)\"/g, "<span class='st'>\"$1\"</span>").replace(/(\{|\n|;)?(.[^\{]*?):(.[^\{]*?)(;|\})/g, "$1<span class='pr'>$2</span>:<span class='vl'>$3</span>$4").replace(/<span class='pr'>\{/g, "{<span class='pr'>")
        }), a = a.replace(/&lt;(.*?)('|")(.*?)('|")&gt;/g, function (e) {
            return e.replace(/'(.*?)'/g, "<span class='vl'>'$1'</span>").replace(/"(.*?)"/g, "<span class='vl'>\"$1\"</span>")
        }), a = a.replace(/\{([\s\S]+?)\}/g, function (e) {
            return e.replace(/([\(\)\{\}\[\]\:\;\,]+)/g, "<span class='pn'>$1</span>").replace(/\!important/gi, "<span class='im'>!important</span>")
        }), a = a.replace(/\/\*([\w\W]+?)\*\//gm, "<span class='cm'>/*$1*/</span>"), e.innerHTML = "<code>" + a + "</code>", hr.style.display = "block", rt.style.display = "block"
    } else hr.style.display = "none", rt.style.display = "none"
}

function compressCSS(e) {
    var a = get(e),
        c = /@(media|-w|-m|-o|keyframes|page)(.*?)\{([\s\S]+?)?\}\}/gi,
        n = a.value,
        t = n.length;
    n = sa.checked || sc.checked ? n.replace(/\/\*[\w\W]*?\*\//gm, "") : n.replace(/(\n+)?(\/\*[\w\W]*?\*\/)(\n+)?/gm, "\n$2\n"), n = n.replace(/([\n\r\t\s ]+)?([\,\:\;\{\}]+?)([\n\r\t\s ]+)?/g, "$2"), n = sc.checked ? n : n.replace(/\}(?!\})/g, "}\n"), n = bi.checked ? n.replace(c, function (e) {
        return e.replace(/\n+/g, "\n  ")
    }) : n.replace(c, function (e) {
        return e.replace(/\n+/g, "")
    }), n = bi.checked && !sc.checked ? n.replace(/\}\}/g, "}\n}") : n, n = bi.checked && !sc.checked ? n.replace(/@(media|-w|-m|-o|keyframes)(.*?)\{/g, "@$1$2{\n  ") : n, n = cm.checked ? n.replace(/;\}/g, "}") : n.replace(/\}/g, ";}").replace(/;+\}/g, ";}").replace(/\};\}/g, "}}"), n = n.replace(/\:0(px|em|pt)/gi, ":0"), n = n.replace(/ 0(px|em|pt)/gi, " 0"), n = n.replace(/\s+\!important/gi, "!important"), n = n.replace(/(^\n+|\n+$)/, ""), a.value = n, hr.innerHTML = "/* " + (t - n.length) + " of " + t + " unused characters has been removed. */\n" + n.replace(/</g, "&lt;").replace(/>/g, "&gt;"), highlightCode(hr)
}

function clearField(e) {
    var a = get(e);
    a.value = "", a.focus()
}

// function selectAll(e) {
//     get(e).focus(), get(e).select()
// }

var hc = get("highlightCode"),
    sa = get("stripAllComment"),
    sc = get("superCompact"),
    cm = get("keepLastComma"),
    bi = get("betterIndentation"),
    bs = get("breakSelector"),
    tt = get("toTab"),
    // to = get("tabOpt").getElementsByTagName("input"),
    sb = get("spaceBetween"),
    ip = get("inlineSingleProp"),
    rs = get("removeLastSemicolon"),
    il = get("inlineLayout"),
    si = get("singleBreak"),
    hr = get("highlightedResult"),
    rt = document.getElementsByTagName("h2")[1];

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// ajax 相关代码
$(document).ready(function () {
    $("#id_caesar_decrypt_button").click(function () {
        $.ajax({
            type: "post",
            url: "data",
            data: {
                "raw_data": $("#id_input_box").val(),
                "csrfmiddlewaretoken": csrftoken
            },
            success: function (result) {
                $("#id_output_box").val(result);
            }
        });
    });
});

// 复制到剪切板的代码
(function () {
    new Clipboard('#id_copy_button');
})();

// 设置 active
$(document).ready(function () {
    // $("#id_toolhub_home").removeClass("active");
    $("#id_encoding_cipher").addClass("active");
});