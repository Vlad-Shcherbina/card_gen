function overflow(el)
{
    var curOverflow = el.style.overflow;
    if (!curOverflow || curOverflow === "visible")
        el.style.overflow = "hidden";

    var isOverflowing = el.clientWidth < el.scrollWidth ||
                        el.clientHeight < el.scrollHeight;

    el.style.overflow = curOverflow;

    return isOverflowing;
}

var elems = document.getElementsByTagName("div")
for (var i = 0; i < elems.length; i++) {
    e = elems[i];
    if (overflow(e)) {
        e.style.background = '#FF7070';
    }
}
