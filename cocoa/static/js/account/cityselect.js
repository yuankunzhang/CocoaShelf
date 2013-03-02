(function($) {
    /*
     * A jQuery plugin.
     * Select province and city.
     */

    var methods = {
        init: function(options) {

            // some defaults
            $.extend($.fn.cityselect.settings, options);

            // set default location.
            locate_str = $.fn.cityselect.settings.locate_str;
            if (locate_str) {
                methods.setValue(locate_str);
            }

            // override the modal's 'show' method
            $('#cityselect-modal').bind('show.cityselect', methods.show);

            $('#cityselect-modal .btn-primary').bind('click.cityselect', methods.btnOkClick);
            $('#cityselect-modal .btn-primary').bind('blur.cityselect', methods.btnBlur);

            return this;
        },

        show: function() {
            // redraw the province select area.
            if (!$.fn.cityselect.settings.init_flag) {
                methods.getProvinceList();

                // if province_id is given, show city list.
                var p_id = $.fn.cityselect.settings.province_id
                if (p_id) {
                    methods.getCityList(p_id);
                }
            }

            $.fn.cityselect.settings.init_flag = true;
        },

        setValue: function(str, c_id) {
            var field = $.fn.cityselect.settings.value_field || 'city_id';

            c_id = c_id || $.fn.cityselect.settings.city_id;
            $('input[name="' + field + '"]').val(c_id);
            $('#cityselect-modal').modal('hide');
            $('#cityselect-target').html(str);
            $('#cityselect a[role="button"]').html('重新选择');
        },

        getProvinceList: function() {
            var p_id = $.fn.cityselect.settings.province_id;

            $.post('/location/provinces/', function(data, status) {
                $.each(data, function(i, v) {
                    if (p_id && p_id == v.province_id) {
                        $('#province-list').append(
                            '<li class="active"><a href="#" value="' +
                            v.province_id + '">' + v.name + '</a></li>'
                        );
                    } else {
                        $('#province-list').append(
                            '<li><a href="#" value="' + v.province_id +
                            '">' + v.name + '</a></li>'
                        );
                    }
                });

                methods.itemClick('province-list', methods.getCityList);
            }, 'json');
        },

        getCityList: function(p_id) {
            $.post('/location/cities/', { province_id: p_id },
                function(data, status) {
                    var c_id = $.fn.cityselect.settings.city_id;

                    $('#city-list').empty();
                    $.each(data, function(i, v) {
                        if (c_id && v.city_id == c_id) {
                            $('#city-list').append(
                                '<li class="active"><a href="#" value="' +
                                v.city_id + '">' + v.name + '</a></li>'
                            );
                        } else {
                            $('#city-list').append(
                                '<li><a href="#" value="' +
                                v.city_id + '">' + v.name + '</a></li>'
                            );
                        }
                    });

                    methods.itemClick('city-list');
                },
            'json');
        },

        itemClick: function(id, goFunc) {
            $('#' + id + ' li a').each(function() {
                $(this).click(function() {
                    $('#' + id + ' li').removeClass('active');
                    $(this).parent().addClass('active');

                    // when clicking a province item.
                    if (goFunc && typeof goFunc === 'function') {
                        goFunc($(this).attr('value'));
                    }

                    return false;
                });
            });
        },

        btnOkClick: function() {
            province = $('#province-list .active a');
            city = $('#city-list .active a');
            
            if (city.length == 0) {
                $(this).popover('show');
                return false;
            } else {
                str = province.html() + ' ' + city.html();
                methods.setValue(str, city.attr('value'));
            }

            return false;
        },

        btnBlur: function() {
            $(this).popover('hide');
        }
    }; // end methods
    
    $.fn.cityselect = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.cityselect');
        }
    };

    $.fn.cityselect.settings = {
        province_id: 0,
        city_id: 0,
        value_field: null,
        init_flag: false,
        locate_str: null
    };

})(jQuery);
