function getVal(txt) {
    var match = txt.match(/[0-9]+/)
    if (match) {
        return +match[0];
    } else {
        return 0;
    }
}

$("svg g.cell").each(function(index, item) {
    var val = getVal($(item).children("title").text())
    console.log("val at index" + index + " is: " + val);
    if (val < 10) {
        $(item).children("text").attr("style", "display:none;")
    }
})