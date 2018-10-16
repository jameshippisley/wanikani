// ==UserScript==
// @name        WaniKani Review Countdown Timer
// @namespace   ajpazder
// @description Adds a time limit to review questions.
// @version     1.1.3
// @author      Johnathon Pazder
// @copyright   2016+, Johnathon Pazder
// @license     MIT; http://opensource.org/licenses/MIT
// @include     http*://www.wanikani.com/review/session*
// @run-at      document-end
// @grant       none
// ==/UserScript==

// Minor edit to add option to make script only warn instead of failing if you run out of time.

var countdown;
var settingsKey = 'wkfc_settings';
var settings = {
    timeLimitSeconds: 10,
    ignoredItemTypes: [], // May be "radical", "kanji", or "vocabulary"
    warningOnly: false
};

initialize();

function initialize() {
    loadCustomSettings();

    addStyleRules();
    addSettingsButton();
    addSettingsForm();

    whenLoadingIndicatorIsHidden(function () {
        initializeCountdownTimer();
        onReviewItemChange(initializeCountdownTimer);
    });
}

function loadCustomSettings() {
    var storedSettings = localStorage.getItem(settingsKey);
    if (!storedSettings) return;

    settings = JSON.parse(storedSettings);
}

function saveSettings() {
    localStorage.setItem(settingsKey, JSON.stringify(settings));
}

function addStyleRules() {
    $('body').append(
        '<style type="text/css">' +
          '#countdown-settings-button { display: inline-block; background: #ccc; padding: 8.5px; margin-right: 3px; border-top-left-radius: 4px; border-top-right-radius: 4px; }' +
          '#countdown-settings-button:hover { cursor: pointer; background: #d5d5d5; }' +
          '#countdown-settings { position: fixed; bottom: 55px; right: 67px; width: 165px; padding: 15px; border-radius: 5px; background: #fff; box-shadow: 2px 2px 2px rgba(0,0,0,.25); z-index: 100; }' +
          '@media(max-width: 768px) { #countdown-settings { right: 5px; } }' +
          '#countdown-settings::after { content: ""; width: 0; position: absolute; right: 20px; bottom: -25px; border-width: 25px 0 0px 20px; border-style: solid; border-color: #fff transparent; }' +
          '#countdown-settings input[type="number"] { width: 50px; border-radius: 4px; border: 1px solid #ccc; padding: 2px; }' +
          '#countdown-settings label.checkbox { display: block; margin-left: 15px; }' +
          '#countdown-settings label.checkbox input[type="checkbox"] { position: relative; top: 1px; }' +
        '</style>'
    );
}

function addSettingsButton() {
    $('#hotkeys').before(
        '<div id="countdown-settings-button">' +
          '<span class="icon-time"></span>' +
        '</div>'
    );

    setTimeout(function () {
        $('#countdown-settings-button').click(function () {
            var settingsForm = $('#countdown-settings');
            if (settingsForm.is(':visible')) {
                settingsForm.hide();
            }
            else {
                settingsForm.show();
                var timeInput = settingsForm.find('input[type="number"]');
                // We focus the input mainly so the settings form's keydown
                // handler will fire and close the form if escape is pressed.
                timeInput.focus();
                // We set the value here so that the cursor is at the end of
                // it when the input is focused.
                timeInput.val(settings.timeLimitSeconds);
            }
        });
    }, 50);
}

function addSettingsForm() {
    $('footer').before(
        '<div id="countdown-settings" style="display: none;">' +
          '<h4 style="margin: 0;margin-bottom: 10px;">Countdown Settings</h4>' +
          '<div>' +
            '<label>Time: </label>' +
            '<input type="number" min="1" style="width: 50px;" /> seconds' +
          '</div>' +
          '<div>' +
            '<label>Ignore:</label>' +
            '<label class="checkbox"><input type="checkbox" value="radical"> Radicals</label>' +
            '<label class="checkbox"><input type="checkbox" value="kanji"> Kanji</label>' +
            '<label class="checkbox"><input type="checkbox" value="vocabulary"> Vocab</label>' +
          '</div>' +
          '<div>' +
            '<label class="checkbox" style="margin-left:0px; margin-top:2px;"><input type="checkbox" value="warningOnly"> Warning Only</label>' +
          '</div>' +
        '</div>'
    );

    setTimeout(function () {
        $('#countdown-settings input[type="checkbox"]').each(function () {
            if ($(this).val() == 'warningOnly') {
                $(this).prop('checked', settings.warningOnly);
            }
            else if (settings.ignoredItemTypes.indexOf($(this).val()) > -1) {
                $(this).prop('checked', true);
            }
        });

        $('#countdown-settings input[type="number"]').on('change keyup', function () {
            var inputValue = $(this).val();
            var minValue = parseInt($(this).prop('min'));
            var saveValue = inputValue;
            if (saveValue < minValue) {
                saveValue = minValue;
                $(this).val(saveValue);
            }
            settings.timeLimitSeconds = saveValue;
            saveSettings();
        });

        $('#countdown-settings input[type="checkbox"]').change(function() {
            var checkboxValue = $(this).val();

            if (checkboxValue == 'warningOnly') {
                settings.warningOnly = $(this).is(':checked');
            }
            else {
                if ($(this).is(':checked')) {
                    settings.ignoredItemTypes.push(checkboxValue);
                }
                else {
                    var index = settings.ignoredItemTypes.indexOf(checkboxValue);
                    settings.ignoredItemTypes.splice(index, 1);
                }
            }
            saveSettings();
        });

        $('#countdown-settings').on('keydown', function (event) {
            if (event.keyCode == 27) {
                $(this).hide();
            }
        });
    }, 50);
}

function timeSettingChangedHandler() {
}

function whenLoadingIndicatorIsHidden(callback) {
    var target = document.getElementById('loading');
    // Mutation observer will watch for change to visibilty.
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            // We assume that the loading indicator is hidden
            // when its style attribute is modified.
            if (mutation.attributeName === 'style') {
                callback();
                return false;
            }
        });
    });
    observer.observe(target, { attributes: true });
}

function initializeCountdownTimer() {
    if (isIgnoredItemType()) {
        // With the reorder script running, it's possible for
        // a countdown to be started on a not ignored item,
        // but continued on an ignored item when the reorder
        // script sorts items.  This aims to prevent that.
        clearInterval(countdown);
        $('#countdown').remove();
    }
    else {
        startCountdown(settings.timeLimitSeconds);
    }
}

function onReviewItemChange(callback) {
	// currentItem seems to be updated even when switching
    // between reading and meaning for the same item.
    $.jStorage.listenKeyChange('currentItem', callback);
}

function isIgnoredItemType() {
    var isIgnored = false;
    settings.ignoredItemTypes.forEach(function (itemType) {
        var propertyName = itemType.substr(0, 3);
        if ($.jStorage.get('currentItem').hasOwnProperty(propertyName) ) {
            isIgnored = true;
            return false;
        }
    });
    return isIgnored;
}

function startCountdown(seconds) {
	// This function could potentially be called multiple times on
    // the same item so, just to be safe, we'll clear any existing
    // counter interval before we start a new one.
	clearInterval(countdown);

    var timeRemaining = seconds * 1000;
	var updateInterval = 100; // ms
	countdown = setInterval(function () {
		if (answerAlreadySubmitted()) {
			clearInterval(countdown);
			return;
		}

		var displayTime = (timeRemaining / 1000).toFixed(1);
		updateCountdownDisplay(displayTime);

		if (timeRemaining === 0) {
			clearInterval(countdown);
			submitWrongAnswer();
			return;
		}

		timeRemaining -= updateInterval;

	}, updateInterval);
}

function answerAlreadySubmitted() {
	return $("#user-response").is(":disabled");
}

function submitWrongAnswer() {
    if (settings.warningOnly) {
	    if (isReadingQuestion()) {
            setResponseTo('Hurry Up！');
	    }
	    else {
            setResponseTo('Hurry Up！');
	    }
    }
    else {
	    if (isReadingQuestion()) {
		    setResponseTo('さっぱりわすれた');
	    }
	    else {
		    setResponseTo('Umm… I forget.');
	    }
    }

	submitAnswer();
}

function isReadingQuestion() {
	return $('#question-type').hasClass('reading');
}

function setResponseTo(value) {
	$('#answer-form input').val(value);
}

function submitAnswer() {
	$('#answer-form button').click();
}

function updateCountdownDisplay(time) {
	// If this is only called once per question change, the counter doesn't show
	// for some reason.  There's probably some other JS running that overwrites it.
	if ($('#countdown').length === 0) {
		$('#question-type h1').append(' (<span id="countdown"></span>s)');
	}

	$('#countdown').text(time);
}
