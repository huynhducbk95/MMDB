/**
 * Created by huynhduc on 15/12/2016.
 */

$('#evaluate_machine').click(function () {
    $("body, html").animate({
                scrollTop: $('.evaluate_learning').offset().top
            }, 600);
});

$('#btn_classification').click(function () {
    $("body, html").animate({
                scrollTop: $('.classification_machine').offset().top
            }, 600);
});

function predict() {
    var content = $('#content_machine').val();
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    var alogrithm = $('#sel1_machine').val();
    var text_extraction = $('#sel2_machine').val();
    var url = $('#predict_btn').data('url');
    var data = {
        content: content,
        alogrithm: alogrithm,
        text_extraction: text_extraction
    };
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        }
    });

    $.ajax(url, {
        type: 'POST',
        data: data,
        async: true,
        success: function (data) {
            result = data['result'];
            $('#result_content_machine').text(result);
            var selected_box = null;
            if (alogrithm === 'KNN'){
                if (text_extraction === 'Bag of word'){
                    selected_box = 'knn_bag_of_word';
                }else{
                    selected_box = 'knn_tf_idf';
                }
            }else{
                if (text_extraction === 'Bag of word'){
                    selected_box = 'svm_bag_of_word';
                }else{
                    selected_box = 'svm_tf_idf';
                }
            }
            $('#alogrithm_text').val(selected_box);
            $("body, html").animate({
                scrollTop: $('.evaluate_learning').offset().top
            }, 600);

        }

    })
}
$('#alogrithm_text').change(function () {
    var value = $(this).val();
    $('#graphic_1').attr('src','static/web_classification/images/'+value+'/confusion_matrix.png');
    $('#graphic_2').attr('src','static/web_classification/images/'+value+'/precision_recall.png');
    $('#graphic_3').attr('src','static/web_classification/images/'+value+'/ROC.png');
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).on('change', ':file', function() {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
});