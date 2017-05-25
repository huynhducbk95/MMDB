/**
 * Created by huynhduc on 17/05/2017.
 */
// $(document).ready(function() {
//     $('.carousel').carousel({
//       interval: 6000
//     })
//   });

$('#btn_upload_video').change(function (event) {
    var filename = $('input[type=file]').val().split('\\').pop();
    if (filename == '') {
        // $('#btn_watch_video').css('display', 'none');
        // $('#video_name').text('');
        // $('#btn_analysis').css('display','none');
        // $('#ctn_slide').css('display','none');
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
    var url = 'http://localhost:8000' + $('#numofkeyframe').data('url');
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData($(this)[0]);
    $('#gallery_frame').empty();
    $('#loader').css('display', 'block');
    $('#ctn_slide').css('display','none');
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
            $('#fh5co-home').css('display','block');
            var direc = data['directory'];
            var data = data['data'];
            $('#numofkeyframe').text(' ' + data.length + ' KeyFrame');
            var count = 0;
            var carousel = document.createElement('div');
            $(carousel).addClass('carousel slide');
            $(carousel).attr('id','myCarousel');
            var carousel_inner = document.createElement('div');
            $(carousel_inner).addClass('carousel-inner');
            $(carousel_inner).css('height','350');
            $(carousel_inner).attr('id','gallery_frame');
            carousel.appendChild(carousel_inner);
            var nav = document.createElement('nav');
            $(nav).attr('id','ctn_slide');
            var ul = document.createElement('ul');
            $(ul).addClass('control-box pager');
            var li_1 = document.createElement('li');
            var a_1 = document.createElement('a');
            a_1.setAttribute('data-slide','prev');
            a_1.setAttribute('href','#myCarousel');
            var i_1 = document.createElement('i');
            $(i_1).addClass("glyphicon glyphicon-chevron-left");
            a_1.appendChild(i_1);
            li_1.appendChild(a_1);
            ul.appendChild(li_1);

            var li_2 = document.createElement('li');
            var a_2 = document.createElement('a');
            a_2.setAttribute('data-slide','next');
            a_2.setAttribute('href','#myCarousel');
            var i_2 = document.createElement('i');
            $(i_2).addClass("glyphicon glyphicon-chevron-right");
            a_2.appendChild(i_2);
            li_2.appendChild(a_2);
            ul.appendChild(li_2);
            nav.appendChild(ul);
            carousel.appendChild(nav);
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
                    $(img).css('width','155');
                    $(img).css('height','88');
                    a.appendChild(img);
                    div.appendChild(a);
                    main_div.appendChild(div);
                    j += 1;
                }
                carousel_inner.appendChild(main_div);
                i += 18;
                count += 1;
            }
            var result = document.getElementById('slide_result');
            result.appendChild(carousel);
            $(carousel).carousel({
                interval: 6000
            })
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
$("#slide_result").delegate("a", "click", function () {
    // alert('you clicked me!');
    var shot_url = $(this).data('shot');
    var frame_url = $(this).data('frame');
    var shot_modal = document.getElementById('shot_modal_xxx');
    // shot_modal.setAttribute('src', '/media/anni007_USHqeUN__result__0/rog/shot/test.mp4');
    shot_modal.setAttribute('src', shot_url);
    $('#xxxxx').val(shot_url);
    var frame_modal = document.getElementById('frame_modal_xxx');
    frame_modal.setAttribute('src', frame_url);
});
$(".modal-wide").on("show.bs.modal", function () {
    var height = $(window).height() - 200;
    $(this).find(".modal-body").css("max-height", height);
});