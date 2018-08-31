// ==UserScript==
// @name        WaniKani Rendaku Information
// @version     0.1003
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

    function get_rendaku_section(word) {
        return `<div><h2>Rendaku Information</h2><p>Your notes for ${word}</p></div>`;
    }

    // Switch based on the content of the URL.
    var url = document.URL;

    // Process the vocabulary page.
    if (url.indexOf('vocabulary') != -1) {
        var word = $('header span.vocabulary-icon span').text().trim();
        var section = get_rendaku_section(word);
        if (section) {
            $('section#note-reading').before(section);
        }
    }

    // Process the review page.
    else if (url.indexOf('review/session') != -1) {
        var current_word = ''

        // Display the information when the current item changes. Don't do this if they are
        // supposed to enter the reading.
        $.jStorage.listenKeyChange('currentItem', function(key) {
            var word = $.jStorage.get(key).voc;
            var section = get_rendaku_section(word);
            if (section && $('#answer-form input').attr('lang') == 'ja' && current_word != word) {
                $('section#note-reading').before(section);
                current_word = word;
            }
        });

        $('div#all-info').on('click', function() {
            var word = $.jStorage.get('currentItem').voc;
            var section = get_rendaku_section(word);
            if (section && current_word != word) {
                $('section#note-reading').before(section);
                current_word = word;
            }
        });
    }

    // Process the lesson page.
    else if (url.indexOf('lesson/session') != -1) {
        var current_lesson_word = '';
        $.jStorage.listenKeyChange('l/currentLesson', function(key) {
            var word = $.jStorage.get(key).voc;
            var section = get_rendaku_section(word);
            console.log(`word = ${word} current_lesson_word = ${current_lesson_word}`)
            if (section && current_lesson_word != word) {
                if (current_lesson_word != '') {
                    $('div#supplement-voc-reading-exp').next().remove();
                }
                $('div#supplement-voc-reading-exp').after(section);
                current_lesson_word = word
            }
        });
    }
});
