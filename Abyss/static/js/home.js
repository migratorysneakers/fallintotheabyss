$(function () {
    $(document).ready(function () {
        $(".color-choice-carousel").carousel();
    });

    $('#form-user-file').on('change', function (e) {
        let name = $(e.target)[0].files[0].name;
        let extension = (name.slice((name.lastIndexOf('.') - 1 >>> 0) + 2)).toLowerCase();

        if (extension !== "jpg" && extension !== "jpeg" && extension !== "png") {
            $(e.target).val('');
            M.toast({
                html: 'We only accept image files :(',
                displayLength: '2000'
            });
        }
    });

    $('#clear-file-input').on('click', function (e) {
        $('#form-user-file').val('');
        $('#form-user-filename').val('')
    });

    $('#btn-submit-image').click(function () {
        let fileInput = $('#form-user-file');
        if (fileInput.val() !== '') {
            var form_data = new FormData($('#form-user-image')[0]);
            $.ajax({
                type: 'POST',
                url: '/getColor',
                data: form_data,
                contentType: false,
                dataType: "json",
                cache: false,
                processData: false,
                success: function (data) {
                    let hue = data[0][0];
                    let result = COLOR_BOUNDS.filter(bound => {
                        return hue <= bound;
                    });
                    let colorKeyword = COLORS[result[0]];
                    getSong(colorKeyword);
                },
                error: function (error) {
                    M.toast({
                        html: 'An error occurred :(',
                        displayLength: '2000'
                    });
                }
            });
        } else {
            let carousel = $(".choices-container").find(".carousel");
            let selected = M.Carousel.getInstance(carousel).center;
            let carouselItems = $(carousel.find(".carousel-item"));

            selected = selected < 0 ? carouselItems.length + selected : selected;
            let colorKeyword = $(carouselItems[selected]).attr("href").substring(1);

            getSong(colorKeyword);
        }
    });

    function getSong(colorKeyword) {
        let audioFeatures = AUDIO_FEATURES[colorKeyword];
        let color = colorKeyword.replace("-", "").toLowerCase();

        $.post('/getSongs', { color: color, audioFeatures: audioFeatures }, function (response, status) {
            if (status === "success") {
                $('body').html(response).ready(function () {
                    $('.tracklist-carousel').carousel();
                });
            } else {
                M.toast({
                    html: 'An error occurred :(',
                    displayLength: '2000'
                })
            }
        });
    }
});