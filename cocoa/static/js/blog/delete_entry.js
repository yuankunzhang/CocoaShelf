$(function() {
    var target_id;

    $('.delete-confirm-modal-btn').click(function() {
        target_id = $(this).attr('value');
        $('#delete-confirm-modal').modal();

        return false;
    });

    $('#delete-confirm-modal .btn-primary').click(function() {
        window.location = '/blog/delete/' + target_id + '/';
    });
});
