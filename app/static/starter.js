function escapeRegExp(string) {
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

$(document).ready(function () {
    $('#timetable-adder').click(function (e) {
        e.preventDefault();
        var li_template = $('#timetable').children('li.timetable-item').last();
        var last_idx = +$(li_template.children('input')[0]).attr('id').replace('shows-', '').replace('-start_time', '');
        var tpl = li_template.html().replace(new RegExp(escapeRegExp('shows-' + last_idx), 'g'), 'shows-' + (last_idx + 1));
        $('#timetable').append('<li class="timetable-item">' + tpl + '</li>');
    });
});
