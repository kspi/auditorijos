function selectDay() {
    var value = settings.day.options[settings.day.selectedIndex].value;
    $('div.diena').hide();
    $('div#' + value).show();    
}

function selectAud() {
    var checkboxes = $('input');
    for (var i in checkboxes) {
        if (checkboxes[i].checked) {
            $('.' + checkboxes[i].id).show();
        } else {
            $('.' + checkboxes[i].id).hide();
        }
    }
}

window.onload = function() {
    settings.day.selectedIndex = (new Date()).getDay() - 1;
    selectDay();
    
    selectAud();
};
