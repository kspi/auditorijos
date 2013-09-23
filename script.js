function selectDay() {
    var value = $('select').val();
    $('div.diena').hide();
    $('div#' + value).show();    
}

function updateCheck(box) {
    if (box.checked) {
        $('.' + box.id).show();
    } else {
        $('.' + box.id).hide();
    }
}

function selectAud(box) {
    if (box) {
        updateCheck(box);
    } else {
        var checkboxes = $('input');
        for (var i in checkboxes) {
            updateCheck(checkboxes[i]);
        }
    }
}

window.onload = function() {
    var weekday = (new Date()).getDay() - 1;
    if (weekday > 4)
        weekday = 0;
    $('select').get(0).selectedIndex = weekday;
    selectDay();    
    selectAud();
};
