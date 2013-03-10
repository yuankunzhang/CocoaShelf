$(function() {
    var CategoryTree = {
        getSubCategories: function(level, parent_id) {
            if (level == 0) {
                target = $('#second-level');
                target.next('ul.divider').css('visibility', 'hidden');
                $('#third-level').empty();
            } else if (level == 1) {
                target = $('#third-level');
            }

            target.empty()

            $.post('/category/categories/' + parent_id + '/',
                function(data, status) {
                    $.each(data, function(i, v) {
                        target.append(
                            '<li><a href="#" value="' + v.id +
                            '">' + v.name + '</a></li>'
                        );
                    });
                    
                    CategoryTree.treeClick(level + 1);
                },
            'json');
        },

        treeClick: function(level) {
            if (level == 0) {
                tree = $('#first-level');
            } else if (level == 1) {
                tree = $('#second-level');
            } else if (level == 2) {
                tree = $('#third-level');
            }
            
            tree.find('a').click(function(e) {
                console.debug(e);
                $(this).parent().parent().find('li.active').removeClass('active');
                $(this).parent().addClass('active');

                if (level < 2) {
                    CategoryTree.disableSubmit();
                    $(this).parent().parent().next('ul.divider').css('visibility', 'visible');

                    CategoryTree.getSubCategories(level, $(this).attr('value'));
                } else {
                    CategoryTree.enableSubmit();
                }

                CategoryTree.setSelectPath();
                e.preventDefault();
            });
        },

        setSelectPath: function() {
            var dom = $('#select-path');
            var first_level_select = $('#first-level li.active a').html();
            var second_level_select = $('#second-level li.active a').html();
            var third_level_select = $('#third-level li.active a').html();

            var html = '请选择：';
            var seperator = '&nbsp;&nbsp;&gt;&nbsp;&nbsp;';
            
            if (first_level_select) {
                html += first_level_select;

                if (second_level_select) {
                    html += seperator + second_level_select;

                    if (third_level_select) {
                        html += seperator + third_level_select;
                    }
                }
            }

            dom.html(html);
        },

        disableSubmit: function() {
            btn = $('.ok a');
            btn.attr('href', '#');
            btn.addClass('disabled');
            btn.click(function(e) {
                e.preventDefault();
            });
        },

        enableSubmit: function() {
            btn = $('.ok a');
            btn.attr('href', $('#third-level li.active a').attr('value'));
            btn.removeClass('disabled');
            btn.unbind('click').click();
        },

        init: function() {
            CategoryTree.disableSubmit();
            CategoryTree.treeClick(0);
        }
    };

    CategoryTree.init();
});
