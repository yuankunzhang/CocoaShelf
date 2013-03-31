function paginate(opt, baseurl) {
    var total = opt['total'];
    var current = opt['current'];

    var PREV = -2;
    var NEXT = -1;

    var pag = {
        items: [],
        push: function(p, l) {
            var prefix = (p == current) ? '<li class="active">' : '<li>';
            var item = prefix + '<a href="' + baseurl + p + '">';

            if (l === 0) {
                item = '<li class="disabled"><a href="#">';
            } else if (l == PREV) {
                if (current == 1) {
                    item = '<li class="disabled"><a href="#">';
                } else {
                    item = '<li><a href="' + baseurl + (current - 1) + '">';
                }
            } else if (l == NEXT) {
                if (current == total) {
                    item = '<li class="disabled"><a href="#">';
                } else {
                    item = '<li><a href="' + baseurl + (current + 1) + '">';
                }
            } else if (l) {
                item = '<li><a href="' + baseurl + l + '">';
            }

            item += p + '</a></li>';
            this.items.push(item);
        }
    };

    if (total == 1) {
        return;
    }

    // first item
    pag.push('&laquo;上一页', PREV);

    if (total <= 9) {
        for (var i = 1; i <= total; i++) {
            pag.push(i);
        }
    } else if (current <= 3) {
        for (var i = 1; i <= 7; i++) {
            pag.push(i);
        }
        pag.push('...', 0);
        pag.push(total);
    } else if (total - current <= 3) {
        pag.push(1);
        pag.push('...', 0);
        for (var i = 1; i <= 7; i++) {
            pag.push(total + i - 7);
        }
    } else {
        pag.push(1);
        pag.push('...', 0);
        for (var i =  2; i >= 0; i--) {
            pag.push(current - i);
        }
        for (var i = 1; i <=  2; i++) {
            pag.push(current + i);
        }
        pag.push('...', 0);
        pag.push(total);
    }

    // last item.
    pag.push('下一页&raquo;', NEXT);

    var pag_bar = $('.pagination ul');
    for (var i = 0; i < pag.items.length; i++) {
        pag_bar.append(pag.items[i]);
    }

    pag_bar.find('li.disabled a').click(function() {
        return false;
    });
}
