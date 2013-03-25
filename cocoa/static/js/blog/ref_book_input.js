$(function() {
    // 隐藏图书id列表框
    $('#post-ref-books').parent().parent().hide();

    $('#add-ref-books-modal .btn-primary').click(function() {
        var el_input = $('#add-ref-books-modal input');
        var el_output = $('#post-ref-books');
        var el_display = $('#ref-books ul');
        var seperator = ', ';

        var book_ids = [];
        el_input.each(function() {
            book_ids.push($(this).val());
        });

        $.post('/blog/prepare_ref_books/', {book_ids: book_ids},
            function(data, status) {
                $.each(data.books, function(i, v) {
                    var id_list = el_output.val().split(seperator);

                    // 如果还没有引用这本书
                    if ($.inArray(v.id.toString(), id_list) == -1) {
                        if (el_output.val() == '') {
                            el_output.val(v.id);
                        } else {
                            el_output.val(el_output.val() + seperator + v.id);
                        }
                        el_display.append('<li><span class="span2">' +
                            v.title + '</span><span class="span2">' +
                            v.author + '</span>' +
                            '<a class="badge" href="#" value="' + v.id +
                            '">x</a></li>');

                        el_display.find('li:last-child a.badge').click(
                            function() {
                                var id = $(this).attr('value');
                                var tmp = [];
                                var id_list = el_output.val().split(seperator);
                                for (var i = 0; i < id_list.length; i++) {
                                    if (id != id_list[i]) {
                                        tmp.push(id_list[i]);
                                    }
                                }
                                el_output.val(tmp.join(', '));
                                $(this).parent().remove();

                                return false;
                            });
                    }
                });
            }
        );

        $('#add-ref-books-modal input').val('');
        $('#add-ref-books-modal').modal('hide');
        return false;
    });
});
