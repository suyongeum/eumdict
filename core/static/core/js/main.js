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

/**
 * Protect window.console method calls, e.g. console is not defined on IE
 * unless dev tools are open, and IE doesn't define console.debug
 *
 * Chrome 41.0.2272.118: debug,error,info,log,warn,dir,dirxml,table,trace,assert,count,markTimeline,profile,profileEnd,time,timeEnd,timeStamp,timeline,timelineEnd,group,groupCollapsed,groupEnd,clear
 * Firefox 37.0.1: log,info,warn,error,exception,debug,table,trace,dir,group,groupCollapsed,groupEnd,time,timeEnd,profile,profileEnd,assert,count
 * Internet Explorer 11: select,log,info,warn,error,debug,assert,time,timeEnd,timeStamp,group,groupCollapsed,groupEnd,trace,clear,dir,dirxml,count,countReset,cd
 * Safari 6.2.4: debug,error,log,info,warn,clear,dir,dirxml,table,trace,assert,count,profile,profileEnd,time,timeEnd,timeStamp,group,groupCollapsed,groupEnd
 * Opera 28.0.1750.48: debug,error,info,log,warn,dir,dirxml,table,trace,assert,count,markTimeline,profile,profileEnd,time,timeEnd,timeStamp,timeline,timelineEnd,group,groupCollapsed,groupEnd,clear
 */
(function () {
    // Union of Chrome, Firefox, IE, Opera, and Safari console methods
    var methods = ["assert", "cd", "clear", "count", "countReset",
        "debug", "dir", "dirxml", "error", "exception", "group", "groupCollapsed",
        "groupEnd", "info", "log", "markTimeline", "profile", "profileEnd",
        "select", "table", "time", "timeEnd", "timeStamp", "timeline",
        "timelineEnd", "trace", "warn"];
    var length = methods.length;
    var console = (window.console = window.console || {});
    var method;
    var noop = function () {
    };
    while (length--) {
        method = methods[length];
        // define undefined methods as noops to prevent errors
        if (!console[method])
            console[method] = noop;
    }
})();

(function () {
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    if (window.AudioContext) {
        window.audioContext = new window.AudioContext();
    }
    var fixAudioContext = function (e) {
        if (window.audioContext) {
            // Create empty buffer
            var buffer = window.audioContext.createBuffer(1, 1, 22050);
            var source = window.audioContext.createBufferSource();
            source.buffer = buffer;
            // Connect to output (speakers)
            source.connect(window.audioContext.destination);
            // Play sound
            if (source.start) {
                source.start(0);
            } else if (source.play) {
                source.play(0);
            } else if (source.noteOn) {
                source.noteOn(0);
            }
        }
        // Remove events
        document.removeEventListener('touchstart', fixAudioContext);
        document.removeEventListener('touchend', fixAudioContext);
    };
    // iOS 6-8
    document.addEventListener('touchstart', fixAudioContext);
    // iOS 9
    document.addEventListener('touchend', fixAudioContext);
})();

$(function () {

    soundManager.setup({
        // where to find flash audio SWFs, as needed
        url: '/static/swf/',
        onready: function () {
            audioReady();
        }
    });

    var isAuthenticated = false;
    var userName = '';

    var replayBtnIcon = $('#replay-btn-icon');
    var audioListSelect = $('#audio-list');
    var numberOfRepetitionsSelect = $('#number-of-repetitions-select');
    var delayBetweenRepetitionsSelect = $('#delay-between-repetitions-select');
    var resultBlock = $('#result');
    var textBlock = $('#text');
    var emailTextbox = $('#email-tb');
    var passwordTextbox = $('#password-tb');
    var regNameTextbox = $('#reg-name');
    var regEmailTextbox = $('#reg-email');
    var regPasswordTextbox = $('#reg-password');
    var regErrorPlaceholder = $('#reg-error');
    var circleGreen = $('#circle-green');
    var circleYellow = $('#circle-yellow');
    var circleRed = $('#circle-red');
    var topMistakesList = $('#top-mistakes-list');
    var topMistakesMessage = $('#top-mistakes-message');
    var definitionBlock = $('#definition-block');

    var contentId = 505;
    var lineId = 1;
    var linesAmount = 0;

    var delay = 0;
    var replays = 1000;
    var playsCountdown = 0;
    var currentAudio;

    var greenEnd = 2;
    var yellowStart = 2, yellowEnd = 3;
    var redStart = 3;

    var settings = [];

    var current_uri = window.location.href;
    var base_uri = current_uri.split('?')[0];
    var uri = new Uri(current_uri);
    var id = uri.getQueryParamValue('id');
    if (id) {
        contentId = parseInt(id);
    }

    clearInputAndResult();

    function audioReady() {
        updateAudioSourse(contentId, lineId);
        updateNextPrevButtonsState();
    }

    // request current user
    $.ajax({
        url: '/login_info',
        success: function (data) {
            isAuthenticated = data.isAuthenticated;
            userName = data.name;
            loadLineNumbers();
            //updateLineAllStatisticsIndicatorData();
            updateLineTopMistakes();
            loadSettingsList();
            updateLastAttemptData();
            updateSentenceDifficulty();
        },
        error: function () {
            alertify.error('Cannot obtain login information')
        }
    });

    window.onunload = closeScriptWindow;

    Mousetrap.bind('alt+]', next);
    Mousetrap.bind('alt+[', previous);
    Mousetrap.bind('alt+p', replay);
    Mousetrap.bind('alt+c', check);
    Mousetrap.bind('alt+s', script);

    $('#register-btn').click(function () {
        $('#register-modal').modal();
    });

    $('#settings-btn').click(function () {
        $('#settings-modal').modal();
    });

    $('#login-btn').click(login);
    $('#logout-btn').click(logout);
    $('#settings-save-submit').click(saveUserSettings);
    $('#reg-submit').click(register);
    $('#script-btn').click(script);
    $('#next-btn').click(next);
    $('#prev-btn').click(previous);
    $('#replay').click(replay);
    $('#check-btn').click(check);
    $('#clear-btn').click(clearInputAndResult);

    audioListSelect.change(function () {
        stopAudio();
        lineId = this.value;
        lineIdChanged(lineId);
    });

    function script() {
        scriptWindow = window.open("/script?content_id=" + contentId, "Script", "height=480,width=640");
        var scr = '$("#line' + (lineId - 1) + '", scriptWindow.document.body).addClass("hl")';
        setTimeout(scr, 1000);
    }

    function closeScriptWindow() {
        if (scriptWindow) {
            scriptWindow.close();
        }
    }

    function check() {
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
                //updateLineAllStatisticsIndicatorData();
                updateLastAttemptData();
                showDefinitions();

            },
            error: function () {
                console.error('Cannot check text')
            }
        });
    }

    function replay() {
        if (!currentAudio)
            return;

        if (playsCountdown > 0) {
            stopAudio();
            return;
        }

        replays = parseInt($('#number-of-repetitions-select').val());
        delay = parseInt($('#delay-between-repetitions-select').val());

        if (replays === 0) {
            playsCountdown = 1000;
        } else {
            playsCountdown = replays;
        }
        playStarted();
        currentAudio.play();
    }

    function onPlayFinished() {
        playsCountdown -= 1;
        console.log('Replays left: ' + playsCountdown)
        if (playsCountdown <= 0) {
            console.log("The audio has ended");
            playEnded();
            return;
        }

        setTimeout(function () {
            currentAudio.play();
        }, delay);
    }

    function next() {
        stopAudio();
        if (lineId >= linesAmount)
            return;
        lineId++;
        audioListSelect.val(lineId);
        lineIdChanged(lineId);
    }

    function previous() {
        stopAudio();
        if (lineId <= 1)
            return;
        lineId--;
        audioListSelect.val(lineId);
        lineIdChanged(lineId);
    }

    function lineIdChanged(lineId) {

        highlightCurrentScriptLine();

        updateAudioSourse(contentId, lineId);

        // updateLineAllStatisticsIndicatorData();

        updateLineTopMistakes();

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
        playsCountdown = 0;
        currentAudio.stop();
    }

    function highlightCurrentScriptLine() {
        try {
            if (scriptWindow) {
                var lineDomId = "line" + (lineId - 1);
                $("p", scriptWindow.document.body).removeClass('hl');
                $("#" + lineDomId, scriptWindow.document.body).addClass('hl');
                scriptWindow.document.getElementById(lineDomId).scrollIntoView(false);

            }
        } catch (err) {
            console.error(err)
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

    function updateLineTopMistakes() {
        topMistakesList.empty();
        $.ajax({
            url: '/8080/top_mistakes',
            data: {
                content_id: contentId,
                line_id: lineId
            },
            success: function (data) {
                if (data.errors.length == 0) {
                    topMistakesMessage.text('No data');
                } else {
                    topMistakesMessage.text('');
                }
                for (var i = 0; i < data.errors.length; i++) {
                    topMistakesList.append('<li>' + data.errors[i] + '</li>');
                }
            },
            error: function () {
                console.error('Cannot load top_mistakes')
            }
        });
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

    function showDefinitions() {
        definitionBlock.empty();
        $.ajax({
            url: '/definitions',
            data: {
                corrected_sentence: resultBlock.html()
            },
            success: function (data) {
                if (data.definitions.length > 0) {
                    for (var i = 0; i < data.definitions.length; i++) {
                        definitionBlock.append('<li><strong>' + data.definitions[i]['word']
                            + '</strong> (' + data.definitions[i]['type'] + ') ー ' + data.definitions[i]['definition'] +  '</li>');
                    }
                }
            },
            error: function () {
                console.error('Cannot load definitions')
            }
        });
    }

    function updateSentenceDifficulty() {

        $.ajax({
            url: '/sentence_difficulty',
            data: {
                content_id: contentId,
                line_id: lineId
            },
            success: function (data) {
                if (data.difficulty < greenEnd) {
                    circleGreen.removeClass('transparent');
                    circleYellow.addClass('transparent');
                    circleRed.addClass('transparent');
                    circleGreen.prop('title', data.difficulty);
                }
                else if (data.difficulty >= yellowStart && data.difficulty < yellowEnd) {
                    circleGreen.addClass('transparent');
                    circleYellow.removeClass('transparent');
                    circleRed.addClass('transparent');
                    circleYellow.prop('title', data.difficulty);
                }
                else if (data.difficulty >= redStart) {
                    circleGreen.addClass('transparent');
                    circleYellow.addClass('transparent');
                    circleRed.removeClass('transparent');
                    circleRed.prop('title', data.difficulty);
                }
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

    function login() {
        var email = emailTextbox.val();
        var password = passwordTextbox.val();

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

                $.ajax({
                    url: '/last_line',
                    data: {},
                    success: function (data) {
                        if (data.line !== -1 && data.content_id != -1) {
                            window.location.replace(base_uri + '?id=' + data.content_id);
                        }
                        else {
                            window.location.replace(current_uri);
                        }
                    },
                    error: function () {
                        window.location.replace(current_uri);
                    }
                });

                window.location.replace(current_uri);
            },
            error: function (err) {
                console.error(err.responseText);
                alertify.error(err.responseText);
            }
        });
    }

    function logout() {
        $.ajax({
            url: '/logout',
            success: function () {
                if (scriptWindow) {
                    scriptWindow.close();
                }
                window.location.replace(current_uri);
            },
            error: function (err) {
                console.error(err.responseText);
                alert(err.responseText);
            }
        });
    }

    function register() {
        var regName = regNameTextbox.val();
        var regEmail = regEmailTextbox.val();
        var regPassword = regPasswordTextbox.val();

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
                window.location.replace(current_uri);
            },
            error: function (err) {
                console.error(err.responseText);
                regErrorPlaceholder.text(err.responseText);
            }
        });
    }

    function constructAudioUrl(contentId, lineId) {
        return '/get_audio?content_id=' + contentId + '&line_id=' + lineId;
    }

    function updateAudioSourse(contentId, lineId) {
        if (currentAudio) currentAudio.destruct();
        currentAudio = soundManager.createSound({
            url: constructAudioUrl(contentId, lineId),
            onfinish: onPlayFinished,
            onstop: onPlayFinished
        });
        currentAudio.load();
    }
});


