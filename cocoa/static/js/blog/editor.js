$(document).ready(function() {
    // fix form's placeholder
    $('input').placeholder();

    /*
     * ace editor
     */
    var editor = ace.edit('editor');
    var textarea = $('textarea');

    editor.getSession().setMode('ace/mode/markdown');
    editor.getSession().setValue(textarea.val());
    //editor.setTheme('ace/theme/github');

    $('#mode-switch').change(function() {
        editor.setKeyboardHandler('ace/keyboard/' + $(this).val());
    });

    $('#form-submit-btn').click(function() {
        textarea.val(editor.getSession().getValue());
        console.debug(textarea.val());
    });


    // 插入图片
    var insert_img_btn = $('#insert-img-modal .btn-primary');
    var cansel_btn = $('#insert-img-modal .btn-cansel');
    var img_info = $('#insert-img-modal #img-info');

    var img_markdown_tag, url, name;

    function init() {
        img_markdown_tag = url = name = '';
        insert_img_btn.attr('disabled', 'disabled');
        $('#target-img').empty();
        $('#photos').show();
        img_info.hide();
    }

    init();

    var uploader = $('#fileupload');
    uploader.fileupload({
        dataType:           'json',
        autoUpload:         true,
        fileInput:          uploader.find('input:file'),
        acceptFileTypes:    /(\.|\/)(gif|jpe?g|png)$/i,
        maxFileSize:        3 * 1024 * 1024,
        success:            function(data, status) {
            url = data.files[0].url;
            name = data.files[0].name.split('.')[0];

            $('#target-img').append('<img src="' + url + '">');
            insert_img_btn.removeAttr('disabled');
            img_info.show();
        }
    });

    $('#photos li img').click(function() {
        url = $(this).attr('src');
        var full_name = url.split('/').slice(-1)[0];
        name = full_name.split('.')[0];

        $('#photos').slideUp().hide(100);
        $('#target-img').append('<img src="' + url + '">');
        insert_img_btn.removeAttr('disabled');
        img_info.show();
    });

    insert_img_btn.click(function() {
        var width = img_info.find('input[name=width]').val();
        var alt = img_info.find('input[name=alt]').val();
        alt = alt || name;

        if (width) {
            img_markdown_tag = '![' + alt +'](' + url + ')@' + width;
        } else {
            img_markdown_tag = '![' + alt +'](' + url + ')';
        }

        var content = editor.getValue() + img_markdown_tag;
        editor.setValue(content, 1);

        $('#insert-img-modal').modal('hide');
        init();
        editor.focus();
    });

    cansel_btn.click(function() {
        $('#insert-img-modal').modal('hide');
        init();
        editor.focus();
    });
});
