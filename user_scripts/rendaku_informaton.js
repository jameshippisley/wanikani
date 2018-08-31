// ==UserScript==
// @name        WaniKani Rendaku Information
// @version     0.1002
// @author      jameshippisley
// @description Adds information to Wanikani about why readings do or do not use rendaku.
// @license     GPL version 3 or any later version; http://www.gnu.org/copyleft/gpl.html
// @namespace   wk_rendaku
//
// @match      *://www.wanikani.com/*vocabulary/*
// @match      *://www.wanikani.com/review/session*
// @match      *://www.wanikani.com/lesson/session*
//
// @updateURL   https://raw.githubusercontent.com/jameshippisley/wanikani/master/user_scripts/rendaku_informaton.js
// @downloadURL https://raw.githubusercontent.com/jameshippisley/wanikani/master/user_scripts/rendaku_informaton.js
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

    // Process the review page.
    else if (url.indexOf('review/session') != -1) {
        var current_item = ''

        // Display the information when the current item changes. Don't do this if they are
        // supposed to enter the reading.
        $.jStorage.listenKeyChange('currentItem', function(key) {
            var section = '<h2>Rendaku Information</h2><p>Your notes</p>'
            if (section && $('#answer-form input').attr('lang') == 'ja' && current_item != 'ok') {
                $('section#note-reading').before(section);
            }
        });

        $('div#all-info').on('click', function() {
            var section = '<h2>Rendaku Information</h2><p>Your notes</p>'
            if (section && current_item != 'ok') {
                current_item = 'ok'
                $('section#note-reading').before(section);
            }
        });
    }

    // Process the lesson page.
    else if (url.indexOf('lesson/session') != -1) {
        $.jStorage.listenKeyChange('l/currentLesson', function(key) {
            var section = '<h2>Rendaku Information</h2><p>Your notes</p>'
            if (section) {
                $('div#supplement-voc-reading-exp').after(section);
            }
        });
    }
});
