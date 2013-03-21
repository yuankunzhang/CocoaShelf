function initThumbnail(thumbnail_box) {
//$(window).load(function() {
    // if avatar exists
    if ($('#avatar')) {
        var THUMBNAIL_SIDE_LEN = 60;
        var THUMBNAIL_SIZE = {
            width: THUMBNAIL_SIDE_LEN,
            height: THUMBNAIL_SIDE_LEN
        };
        $('#avatar-preview').css(THUMBNAIL_SIZE);
        $('#avatar-preview .box').css(THUMBNAIL_SIZE);

        var avatar = $('#avatar').find('img');
        var avatarPreview = $('#avatar-preview .box img');
        var w = avatar.width();
        var h = avatar.height();

        if (!thumbnail_box) {
            var ruler = (w > h) ? h : w;
            x1 = Math.round(w / 2 - ruler / 2);
            y1 = Math.round(h / 2 - ruler / 2);
            x2 = Math.round(w / 2 + ruler / 2);
            y2 = Math.round(h / 2 + ruler / 2);
        } else {
            x1 = thumbnail_box.x1;
            y1 = thumbnail_box.y1;
            x2 = thumbnail_box.x2;
            y2 = thumbnail_box.y2;
        }

        function preview(img, selection) {
            if (!selection.width || !selection.height)
                return;

            var scaleX = THUMBNAIL_SIDE_LEN / selection.width;
            var scaleY = THUMBNAIL_SIDE_LEN / selection.height;

            avatarPreview.css({
                width: Math.round(scaleX * w),
                height: Math.round(scaleY * h),
                marginLeft: -Math.round(scaleX * selection.x1),
                marginTop: -Math.round(scaleY * selection.y1)
            });

            changeThumbnail(selection);
        }

        function changeThumbnail(selection) {
            $('#thumbnail-values input[name=x1]').val(selection.x1);
            $('#thumbnail-values input[name=y1]').val(selection.y1);
            $('#thumbnail-values input[name=x2]').val(selection.x2);
            $('#thumbnail-values input[name=y2]').val(selection.y2);
        }

        var area = avatar.imgAreaSelect({
            instance: true,
            handles: true,
            aspectRatio: '1:1',
            fadeSpeed: 200,
            onSelectChange: preview,
            persistent: true,
            x1: x1,
            y1: y1,
            x2: x2,
            y2: y2
        });

        preview(avatar, area.getSelection());
    }
//});
}
