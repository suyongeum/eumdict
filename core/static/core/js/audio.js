$(function () {
    soundManager.setup({
        // where to find flash audio SWFs, as needed
        url: '/static/swf/',
        onready: function () {
            audioReady();
        }
    });
});


function audioReady() {

    var contentId = 505;
    var lineId = 1;

    var soundId = '123'
    var audioUrl = '/get_audio?content_id=' + contentId + '&line_id=' + lineId;

    var mySound = soundManager.createSound({
        url: audioUrl,
        onfinish: function () {
            alert('The sound ' + this.id + ' finished playing.');
        }
    });

    mySound.play();



}