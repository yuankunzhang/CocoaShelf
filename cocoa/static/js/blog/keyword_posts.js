$(function() {
    function nl2br(str){
        var breakTag = '</p><p>';    
        str = '<p>' + str + '</p>';
        return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1'+ breakTag +'$2');
    }

    function get_posts(user_id, keyword_id) {
        $.post('/blog/keywordposts/' + user_id + '/',
            {'keyword_id': keyword_id},
            function(data, status) {
                tmpl.encReg = '';

                // 预处理
                $.each(data.posts, function(i, v) {
                    v.content = nl2br(v.content);
                    console.debug(v.content);
                });

                var container = $('#posts');
                container.empty();
                container[0].innerHTML = tmpl('keyword-posts', data)
            }
        );
    }

    $('.keyword-list a').click(function() {
        $('.keyword-list li.active').removeClass('active');
        $(this).parent().addClass('active');

        var user_id = $('.keyword-list').attr('user');
        var keyword_id = $(this).attr('value');
        get_posts(user_id, keyword_id);

        return false;
    });
});
