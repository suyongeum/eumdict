var scriptWindow;

// new Event polyfill
(function () {

    if (typeof window.CustomEvent === "function") return false;

    function CustomEvent(event, params) {
        params = params || {bubbles: false, cancelable: false, detail: undefined};
        var evt = document.createEvent('CustomEvent');
        evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);
        return evt;
    }

    CustomEvent.prototype = window.Event.prototype;
    window.CustomEvent = CustomEvent;
    window.Event = CustomEvent;
})();

$(document).ready(function () {

    var isAuthenticated = false;
    var userName = '';

    var replayBtnIcon = $('#replay-btn-icon');
    var audioListSelect = $('#audio-list');
    var numberOfRepetitionsSelect = $('#number-of-repetitions-select');
    var delayBetweenRepetitionsSelect = $('#delay-between-repetitions-select');
    var resultBlock = $('#result');
    var textBlock = $('#text');

    // var volumeSlider = $("#volume-slider");

    var lineId = 1;
    var linesAmount = 0;

    var playsCountdown = 0;
    var currentAudio;

    var settings = [];

    var contentId = 505;
    var uri = new Uri(window.location.href);
    var id = uri.getQueryParamValue('id');
    if (id) {
        contentId = parseInt(id);
    }

    if (typeof alertify !== 'undefined') {
        alertify = {};
        alertify.logPosition = function () {
        };
        alertify.error = function () {
        };
        alertify.info = function () {
        };

    }
    //alertify.logPosition('top right');



    clearInputAndResult();

    // currentAudio = $('#player');
    // currentAudio.src = '/get_audio?content_id=' + contentId + '&line_id=' + lineId;
    // currentAudio.load();

    currentAudio = new Audio('/get_audio?content_id=' + contentId + '&line_id=' + lineId);
    //volumeSlider.slider().data('slider').setValue(currentAudio.volume * 100);
    updateNextPrevButtonsState();

    // request current user
    $.ajax({
        url: '/login_info',
        success: function (data) {
            isAuthenticated = data.isAuthenticated;
            userName = data.name;
            loadLineNumbers();
            updateLineAllStatisticsIndicatorData();
            loadSettingsList();
            updateLastAttemptData();
            updateSentenceDifficulty();
        },
        error: function () {
            alertify.error('Cannot obtain login information')
        }
    });

    $('#login-btn').click(function () {
        var email = $('#email-tb').val();
        var password = $('#password-tb').val();

        if (!email || !password) {
            alertify.error('Enter email and password');
            return;
        }

        $.ajax({
            url: '/authenticate',
            data: {
                'email': email,
                'password': password
            },
            success: function () {
                if (scriptWindow) {
                    scriptWindow.close();
                }
                window.location.replace("/");
            },
            error: function (err) {
                console.error(err.responseText);
                alertify.error(err.responseText);
            }
        });

    });

    $('#logout-btn').click(function () {
        $.ajax({
            url: '/logout',
            success: function () {
                if (scriptWindow) {
                    scriptWindow.close();
                }
                window.location.replace("/");
            },
            error: function (err) {
                console.error(err.responseText);
                alert(err.responseText);
            }
        });
    });

    $('#register-btn').click(function () {
        $('#register-modal').modal();
    });

    $('#settings-btn').click(function () {
        $('#settings-modal').modal();
    });

    $('#settings-save-submit').click(function () {
        saveUserSettings();
    });

    $('#reg-submit').click(function () {

        var regName = $('#reg-name').val();
        var regEmail = $('#reg-email').val();
        var regPassword = $('#reg-password').val();

        $.ajax({
            type: "POST",
            url: '/register',
            data: {
                'name': regName,
                'email': regEmail,
                'password': regPassword
            },
            success: function () {
                if (scriptWindow) {
                    scriptWindow.close();
                }
                window.location.replace("/");
            },
            error: function (err) {
                console.error(err.responseText);
                $('#reg-error').text(err.responseText);
            }
        });

    });

    $('#script-btn').click(function () {

        scriptWindow = window.open("/script?content_id=" + contentId, "Script", "height=480,width=640");
        var scr = '$("#line' + (lineId - 1) + '", scriptWindow.document.body).addClass("hl")';
        setTimeout(scr, 1000);
    });

    $('#next-btn').click(function () {
        stopAudio();
        if (lineId >= linesAmount)
            return;
        lineId++;
        audioListSelect.val(lineId);
        lineIdChanged(lineId);
    });
    $('#prev-btn').click(function () {
        stopAudio();
        if (lineId <= 1)
            return;
        lineId--;
        audioListSelect.val(lineId);
        lineIdChanged(lineId);
    });

    $('#replay').click(function () {
        if (!currentAudio)
            return;

        if (playsCountdown > 0) {
            stopAudio();
            return;
        }

        var replays = parseInt($('#number-of-repetitions-select').val());
        var delay = parseInt($('#delay-between-repetitions-select').val());

        if (replays === 0) {
            playsCountdown = 1000;
        } else {
            playsCountdown = replays;
        }
        currentAudio.onended = function () {
            playsCountdown -= 1;
            if (playsCountdown <= 0) {
                console.log("The audio has ended");
                playEnded();
                return;
            }
            setTimeout(function () {
                currentAudio.play();
            }, delay);
        };

        playStarted();
        currentAudio.play();
        // var globalDelay = 0;
        // for (i = 0; i < replays; i++) {
        //     setTimeout(function(){ currentAudio.play(); }, globalDelay);
        //     globalDelay += duration + delay;
        // }

    });

    $('#check-btn').click(function () {

        var text = textBlock.val();
        if (text === '') {
            return;
        }

        stopAudio();

        $.ajax({
            url: '/check',
            data: {
                content_id: contentId,
                line_id: lineId,
                text: text
            },
            success: function (data) {
                console.log(data);
                setResult(data.result);
                // updateLineStatisticsData();
                //updateLineAllStatisticsData();
                updateLineAllStatisticsIndicatorData();
                updateLastAttemptData();

            },
            error: function () {
                console.error('Cannot check text')
            }
        });
    });

    $('#clear-btn').click(function () {
        clearInputAndResult();
    });

    audioListSelect.change(function () {
        stopAudio();
        lineId = this.value;
        lineIdChanged(lineId);
    });

    // volumeSlider.slider().on('change', function (e) {
    //     var newValue = e.value.newValue;
    //     currentAudio.volume = newValue / 100;
    // });

    function lineIdChanged(lineId) {

        highlightCurrentScriptLine();

        currentAudio = new Audio('/get_audio?content_id=' + contentId + '&line_id=' + lineId);

        // updateLineStatisticsData();
        // updateLineAllStatisticsData();
        updateLineAllStatisticsIndicatorData();

        updateLastAttemptData();

        updateSentenceDifficulty();

        updateNextPrevButtonsState();

        clearInputAndResult();

        if (isAuthenticated) {
            saveUserLastLine();
        }

    }

    function clearInputAndResult() {
        textBlock.val('');
        resultBlock.html('Corrected text will appear here');
        resultBlock.addClass('placeholder');
    }

    function setResult(value) {
        resultBlock.removeClass('placeholder');
        resultBlock.html(value);
    }

    function updateNextPrevButtonsState() {
        var prevButton = $('#prev-btn');
        var nextButton = $('#next-btn');

        if (lineId === 1) {
            prevButton.prop('disabled', true);
            nextButton.prop('disabled', false);
        }
        else if (lineId >= linesAmount) {
            prevButton.prop('disabled', false);
            nextButton.prop('disabled', true);
        }
        else {
            prevButton.prop('disabled', false);
            nextButton.prop('disabled', false);
        }
    }

    function playStarted() {
        replayBtnIcon.removeClass('glyphicon-play');
        replayBtnIcon.addClass('glyphicon-stop');
    }

    function playEnded() {
        replayBtnIcon.removeClass('glyphicon-stop');
        replayBtnIcon.addClass('glyphicon-play');
    }

    function stopAudio() {
        currentAudio.pause();
        if (currentAudio.currentTime !== 0) {
            currentAudio.currentTime = 0;
        }
        playsCountdown = 0;
        currentAudio.dispatchEvent(new Event('ended'));
    }

    function highlightCurrentScriptLine() {
        if (scriptWindow) {
            $("p", scriptWindow.document.body).removeClass('hl');
            $("#line" + (lineId - 1), scriptWindow.document.body).addClass('hl');
        }
    }

    function updateLineAllStatisticsIndicatorData() {

        $.ajax({
            url: '/line_statistics_all',
            data: {
                content_id: contentId,
                line_id: lineId,
                personalize: false
            },
            success: function (data) {
                var val = roundToTwo(data.data * 100);
                $('#all-indicator').css('width', val + '%').attr('aria-valuenow', val).text(val + '%');
            },
            error: function () {
                console.error('Cannot load line_statistics_all')
            }
        });

        if (isAuthenticated) {
            $('#me-indicator-block').removeClass('hidden')
            $.ajax({
                url: '/line_statistics_all',
                data: {
                    content_id: contentId,
                    line_id: lineId,
                    personalize: true
                },
                success: function (data) {
                    var val = roundToTwo(data.data * 100);
                    $('#my-indicator').css('width', val + '%').attr('aria-valuenow', val).text(val + '%');
                },
                error: function () {
                    console.error('Cannot load line_statistics_all')
                }
            });
        }

    }

    function updateLastAttemptData() {
        var lastAttemptBlock = $('#last-attempt');
        var lastAttemptTriesSpan = $('#last-attempt-tries');
        var lastAttemptDatetimeSpan = $('#last-attempt-datetime');
        var lastAttemptAmountSpan = $('#last-attempt-amount');
        var lastAttemptWordsSpan = $('#last-attempt-words');

        if (isAuthenticated) {
            $.ajax({
                url: '/last_attempt',
                data: {
                    content_id: contentId,
                    line_id: lineId
                },
                success: function (data) {
                    if (data.tries === 0) {
                        lastAttemptBlock.addClass('hidden');
                        return;
                    }

                    var datetime = moment(data.datetime);

                    lastAttemptBlock.removeClass('hidden');
                    lastAttemptTriesSpan.html(data.tries);
                    lastAttemptDatetimeSpan.html(datetime.fromNow());
                    lastAttemptDatetimeSpan.prop('title', datetime.format("MMMM Do YYYY, hh:mm:ss"));
                    lastAttemptAmountSpan.html(data.amount);
                    lastAttemptWordsSpan.html(data.words);
                },
                error: function () {
                    lastAttemptBlock.addClass('hidden');
                    console.error('Cannot load last attempt data');
                    alertify.error('Cannot load last attempt data');
                }
            });
        }
    }

    function updateSentenceDifficulty() {
        var sentenceDifficultySpan = $('#sentence-difficulty');
        $.ajax({
            url: '/sentence_difficulty',
            data: {
                content_id: contentId,
                line_id: lineId
            },
            success: function (data) {
                if (data.difficulty < 4) {
                    sentenceDifficultySpan.removeClass('label-warning');
                    sentenceDifficultySpan.removeClass('label-danger');
                    sentenceDifficultySpan.addClass('label-success');
                }
                else if (data.difficulty >= 4 && data.difficulty < 8) {
                    sentenceDifficultySpan.removeClass('label-success');
                    sentenceDifficultySpan.removeClass('label-danger');
                    sentenceDifficultySpan.addClass('label-warning');
                }
                else if (data.difficulty >= 8) {
                    sentenceDifficultySpan.removeClass('label-warning');
                    sentenceDifficultySpan.removeClass('label-success');
                    sentenceDifficultySpan.addClass('label-danger');
                }
                sentenceDifficultySpan.html(data.difficulty);
            },
            error: function () {
                console.error('Cannot load sentence difficulty data');
                alertify.error('Cannot load sentence difficulty data');
            }
        });


    }

    function loadSettingsList() {
        $.ajax({
            url: '/settings_list',
            success: function (data) {
                settings = data;
                loadUserSettings();
            },
            error: function () {
                alertify.error('Cannot obtain settings')
            }
        });
    }

    function loadUserSettings() {
        numberOfRepetitionsSelect.val(settings['number_of_repetitions'].default_value);
        delayBetweenRepetitionsSelect.val(settings['delay_between_repetitions'].default_value);

        if (isAuthenticated) {
            $.ajax({
                url: '/user_settings',
                success: function (data) {
                    if (data['number_of_repetitions']) {
                        numberOfRepetitionsSelect.val(data['number_of_repetitions']);
                    }
                    if (data['delay_between_repetitions']) {
                        delayBetweenRepetitionsSelect.val(data['delay_between_repetitions']);
                    }
                },
                error: function () {
                    alertify.error('Cannot obtain settings')
                }
            });
        } else {
            // load from local storage
            var numberOfRepetitions = Lockr.get('number_of_repetitions');
            var delayBetweenRepetitions = Lockr.get('delay_between_repetitions');
            if (numberOfRepetitions) {
                numberOfRepetitionsSelect.val(numberOfRepetitions);
            }
            if (delayBetweenRepetitions) {
                delayBetweenRepetitionsSelect.val(delayBetweenRepetitions);
            }
        }
    }

    function saveUserSettings() {
        var number_of_repetitions = numberOfRepetitionsSelect.val();
        var delay_between_repetitions = delayBetweenRepetitionsSelect.val();

        if (isAuthenticated) {
            $.ajax({
                type: "POST",
                url: '/save_user_settings',
                data: {
                    'number_of_repetitions': number_of_repetitions,
                    'delay_between_repetitions': delay_between_repetitions
                },
                success: function () {
                    $('#settings-modal').modal('hide');
                    alertify.success('Settings are saved');
                },
                error: function (err) {
                    alertify.error(err.responseText);
                    console.error(err.responseText);
                }
            });
        } else {
            Lockr.set('number_of_repetitions', number_of_repetitions);
            Lockr.set('delay_between_repetitions', delay_between_repetitions);
            $('#settings-modal').modal('hide');
            alertify.success('Settings are saved locally');
        }
    }

    function saveUserLastLine() {
        $.ajax({
            type: "POST",
            url: '/save_last_line',
            data: {
                'content_id': contentId,
                'line': lineId
            },
            success: function (data) {
            },
            error: function (err) {
                alertify.error(err.responseText);
                console.error(err.responseText);
            }
        });
    }

    function loadLineNumbers() {
        // request number of lines for current content
        $.ajax({
            url: '/line_number',
            data: {content_id: contentId},
            success: function (data) {
                linesAmount = data.lines;
                for (var k = 1; k <= data.lines; k++) {
                    audioListSelect.append($("<option/>", {
                        value: k,
                        text: k
                    }));
                }

                if (isAuthenticated) {
                    loadLastLineNumber();
                }
            },
            error: function () {
                console.error('Cannot load number of lines')
            }
        });
    }

    function loadLastLineNumber() {
        $.ajax({
            url: '/last_line',
            data: {},
            success: function (data) {
                if (data.line !== -1 && data.content_id === contentId) {
                    audioListSelect.val(data.line);
                    lineId = data.line;
                    lineIdChanged(lineId);
                }
            },
            error: function () {
                console.error('Cannot load number of lines')
            }
        });
    }

    function roundToTwo(num) {
        return +(Math.round(num + "e+2") + "e-2");
    }
});

