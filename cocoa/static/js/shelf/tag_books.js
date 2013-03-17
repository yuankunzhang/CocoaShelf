$(function() {
    function get_books(shelf_id, tag_id) {
        $.post('/shelf/' + shelf_id + '/tagbooks/', {'tag_id': tag_id},
            function(data, status) {
                target = $('.book-list ul');
                target.empty();

                $.each(data.books, function(i, v) {
                    html = '<li>' +
                        '<a target="_blank" href="/book/' +
                        v.id + '/">' +
                        '<img width=100 height=140 ' +
                        'src="/static/upload/cover/' + v.cover +
                        '"></a></li>';

                    target.append(html);
                });
            }
        );
    }

    $('.tag-list a').click(function() {
        $('.tag-list li.active').removeClass('active');
        $(this).parent().addClass('active');

        shelf_id = $('.tag-list').attr('shelf')
        tag_id = $(this).attr('value');
        get_books(shelf_id, tag_id);

        return false;
    });
});
