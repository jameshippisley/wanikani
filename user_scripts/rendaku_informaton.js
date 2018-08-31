// ==UserScript==
// @name        WaniKani Rendaku Information
// @version     0.1
// @author      jameshippisley
// @description Adds information to Wanikani about why readings do or do not use rendaku.
// @license     GPL version 3 or any later version; http://www.gnu.org/copyleft/gpl.html
// @namespace   wk_rendaku
//
// @match      *://www.wanikani.com/*vocabulary/*
// @match      *://www.wanikani.com/review/session*
// @match      *://www.wanikani.com/lesson/session*
//
// @updateURL   https://github.com/jameshippisley/wanikani/raw/master/user_scripts/rendaku_information.js
// @downloadURL https://https://github.com/jameshippisley/wanikani/raw/master/user_scripts/rendaku_information.js
//
// @run-at      document-end
// ==/UserScript==

$(function() {
    'use strict';

    // Switch based on the content of the URL.
    var url = document.URL;

    // Process the vocabulary page.
    if (url.indexOf('vocabulary') != -1) {
        var section = '<h2>Rendaku Information</h2><p>Your notes</p>'
        if (section) {
            $('section#note-reading').before(section);
        }
    }

/*    // Process the review page.
    else if (url.indexOf('review/session') != -1) {
        // Display the information when the current item changes. Don't do this if they are
        // supposed to enter the reading.
        $.jStorage.listenKeyChange('currentItem', function(key) {
            var section = GetPartOfSpeechData($.jStorage.get(key).voc, DATA);
            if (section && $('#answer-form input').attr('lang') != 'ja') {
                $('div#item-info').prepend(section.append('<br />'));
            }
        });

        // If the 'all-info' button is pressed, then display it.
        $('div#all-info').on('click', function() {
            var section = GetPartOfSpeechData($.jStorage.get('currentItem').voc, DATA);
            if (section) {
                $('div#item-info').prepend(section.append('<br />'));
            }
        });
    }

    // Process the lesson page.
    else if (url.indexOf('lesson/session') != -1) {
        $.jStorage.listenKeyChange('l/currentLesson', function(key) {
            var section = GetPartOfSpeechData($.jStorage.get(key).voc, DATA);
            if (section) {
                $('div#supplement-voc-meaning').append(section.prepend('<br />'));
            }
        });
    } */
});
