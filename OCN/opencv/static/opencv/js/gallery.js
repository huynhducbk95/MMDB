/**
 * Created by huynhduc on 17/05/2017.
 */

$(document).ready(function () {

    loadGallery(true, 'a.thumbnail');

    //This function disables buttons when needed
    function disableButtons(counter_max, counter_current) {
        $('#show-previous-image, #show-next-image').show();
        if (counter_max == counter_current) {
            $('#show-next-image').hide();
        } else if (counter_current == 1) {
            $('#show-previous-image').hide();
        }
    }

    /**
     *
     * @param setIDs        Sets IDs when DOM is loaded. If using a PHP counter, set to false.
     * @param setClickAttr  Sets the attribute for the click handler.
     */

    function loadGallery(setIDs, setClickAttr) {
        var current_image,
            selector,
            counter = 0;

        $('#show-next-image, #show-previous-image').click(function () {
            if ($(this).attr('id') == 'show-previous-image') {
                current_image--;
            } else {
                current_image++;
            }

            selector = $('[data-image-id="' + current_image + '"]');
            updateGallery(selector);
        });

        function updateGallery(selector) {
            var $sel = selector;
            current_image = $sel.data('image-id');
            $('#image-gallery-caption').text($sel.data('caption'));
            $('#image-gallery-title').text($sel.data('title'));
            $('#image-gallery-image').attr('src', $sel.data('image'));
            disableButtons(counter, $sel.data('image-id'));
        }

        if (setIDs == true) {
            $('[data-image-id]').each(function () {
                counter++;
                $(this).attr('data-image-id', counter);
            });
        }
        $(setClickAttr).on('click', function () {
            updateGallery($(this));
        });
    }
});
$(document).ready(function () {
    $('.carousel').carousel({
        interval: 6000
    })
});

$('#btn_upload_video').change(function (event) {
    var filename = $('input[type=file]').val().split('\\').pop();
    if (filename == '') {
        $('#btn_watch_video').css('display', 'none');
        $('#video_name').text('');
    } else {
        $('#video_name').text(filename);
        var URL = window.URL || window.webkitURL;
        $('#btn_watch_video').css('display', 'block');
        $('#btn_analysis').css('display', 'block');
        file = event.target.files[0];
        var tmppath = URL.createObjectURL(event.target.files[0]);
        video_seletor = document.getElementById('source_video_upload');
        video_seletor.src = tmppath
    }
});
$("form#form_upload_file").submit(function () {
    var url = 'http://localhost:8000' + $('#myCarousel').data('url');
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData($(this)[0]);
    $('#loader').css('display', 'block');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        }
    });
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        async: true,
        success: function (data) {
            $('#loader').css('display', 'none');
            $('#myCarousel').css('display', 'block');
            var direc = data['directory'];
            var data = data['data'];
            $('#numofkeyframe').text(' ' + data.length + ' KeyFrame');
            var count = 0;
            var i = 0;
            while (i < data.length) {
                main_div = document.createElement('div');
                if (count == 0) {
                    $(main_div).addClass('item active');
                } else {
                    $(main_div).addClass('item');
                }
                var j = i;
                while ((j < i + 18) && (j < data.length)) {
                    div = document.createElement('div');
                    $(div).addClass('col-lg-2 col-md-2 col-xs-6 thumb');
                    a = document.createElement('a');
                    $(a).addClass('thumbnail frame_show');
                    a.setAttribute('data-toggle', 'modal');
                    a.setAttribute('data-shot', direc + '/shot/' + data[j][j + ''][0]);
                    a.setAttribute('data-frame', direc + '/' + data[j][j + ''][1]);
                    a.setAttribute('data-title', 'shot ' + j + ' 1');
                    a.setAttribute('data-target', '#image-gallery');
                    img = document.createElement('img');
                    $(img).addClass('img-response');
                    img.setAttribute('src', direc + '/' + data[j][j + ''][1]);
                    a.appendChild(img);
                    div.appendChild(a);
                    main_div.appendChild(div);
                    j += 1;
                }
                div_gallery = document.getElementById('gallery_frame');
                div_gallery.appendChild(main_div);
                i += 18;
                count += 1;
            }
        },
        cache: false,
        contentType: false,
        processData: false
    });

    return false;
});
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
// $("#gallery_frame").delegate("a", "click", function(){
//     // alert('you clicked me!');
//     var shot_url = $(this).data('shot');
//     var frame_url = $(this).data('frame');
//     alert(shot_url + '    ' + frame_url);
//     var shot_modal = document.getElementById('shot_modal_xxx');
//     shot_modal.setAttribute('src',shot_url);
//     var frame_modal = document.getElementById('frame_modal_xxx');
//     frame_modal.setAttribute('src',frame_url);
// });