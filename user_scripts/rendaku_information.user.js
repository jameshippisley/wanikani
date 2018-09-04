// ==UserScript==
// @name        WaniKani Rendaku Information
// @version     0.1007
// @author      jameshippisley
// @description Adds information to Wanikani about why readings do or do not use rendaku.
// @license     GPL version 3 or any later version; http://www.gnu.org/copyleft/gpl.html
// @namespace   wk_rendaku
//
// @match      *://www.wanikani.com/*vocabulary/*
// @match      *://www.wanikani.com/review/session*
// @match      *://www.wanikani.com/lesson/session*
//
// @updateURL   https://raw.githubusercontent.com/jameshippisley/wanikani/master/user_scripts/rendaku_information.user.js
// @downloadURL https://raw.githubusercontent.com/jameshippisley/wanikani/master/user_scripts/rendaku_information.user.js
//
// @require     https://raw.githubusercontent.com/mwil/wanikani-userscripts/3c6ea0466951a1e58b75b2cb7a945ed7716082f7/utility/wk_interaction.js
// @require     https://raw.githubusercontent.com/jameshippisley/wanikani/bde48e18fb6af5c236a7c2fb12357f33c48a2403/user_scripts/rendaku_information_data.json
//
// @run-at      document-end
//
// @grant       GM_log
//
// ==/UserScript==

// The code below to insert custom lessons sections into the WaniKani pages is completely copied from (and calls)
// https://github.com/mwil/wanikani-userscripts/tree/master/wanikani-phonetic-compounds
// Massive thanks to mwil for showing me how to make use of this code.

// #############################################################################
function WK_Rendaku()
{
    this.wki = new WKInteraction(GM_info.script.namespace);

    this.currentSubject = null;

    this.settings = {
        "debug": false
    };
}


(function() {
    'use strict';

   // #########################################################################
    WK_Rendaku.prototype.injectRendakuSection = function(event, curPage)
    {
        // #####################################################################
        $(`#rendaku_section`).remove();

        const subject = this.wki.getSubject();

        this.log(`Injecting rendaku section (callback works).`);

        if (!this.wki.checkSubject(subject, [`voc`]))
            return;

        this.currentSubject = subject;
        this.log(`Working with the following input:`, subject);
        // #####################################################################

        // #####################################################################
        switch(curPage)
        {
            case this.wki.PageEnum.vocabulary:
                $(`section#note-reading`)
                    .before(this.createRendakuSection());
                break;
            case this.wki.PageEnum.reviews:
            case this.wki.PageEnum.lessons_reviews:
                if ($(`section#item-info-reading-mnemonic`).length)
                {
                    $(`section#item-info-reading-mnemonic`)
                        .after(this.createRendakuSection());

                    if ($(`section#item-info-reading-mnemonic`).is(`:hidden`))
                        $(`#rendaku_section`).hide();
                }
                else
                    $(`section#note-reading`)
                        .before(this.createRendakuSection());

                break;
            case this.wki.PageEnum.lessons:
                $(`div#supplement-voc-reading-exp`)
                    .after(this.createRendakuSection(`margin-top: 1.5em;`));
                break;
            default:
                GM_log(`Unknown page type ${curPage}, cannot inject info!`);
                return;
        }
        // #####################################################################

    }

    WK_Rendaku.prototype.createRendakuSection = function(style)
    {
        const $section = $(`<section></section>`)
                         .attr(`id`, `rendaku_section`)
                         .attr(`style`, style)
                         .addClass(`${GM_info.script.namespace} col1`);

        var word = this.currentSubject.voc
        var info = DATA[word]
        if (info) {
            $section.append(`<div><h2>Rendaku Information</h2><p>${info}</p></div>`);
            this.log(`Created the Rendaku section, appending to the page!`);
        }
        else {
            this.log(`no info for ${word}`)
        }

        return $section;
    };

    // #########################################################################
    WK_Rendaku.prototype.init = function()
    {

        this.log = this.settings.debug ?
            function(msg, ...args) {
                GM_log(`${GM_info.script.namespace}:`, msg, ...args);
            } :
            function() {};

        this.wki.init();

        this.log(`The script element is:`, GM_info);

        // #####################################################################
        // Main hook, WK Interaction will kick off this script once the page
        // is ready and we can access the subject of the page.
        $(document).on(`${GM_info.script.namespace}_wk_subject_ready`,
                       this.injectRendakuSection.bind(this));
        // #####################################################################
    };
    // #########################################################################

    // Just do it!
    // #########################################################################
    WK_Rendaku.prototype.run = function()
    {
        // Start page detection (and its callbacks once ready)
        this.wki.startInteraction.call(this.wki);
    };
    // #########################################################################
}
)();
// #############################################################################


// #############################################################################
// #############################################################################
var wk_rendaku = new WK_Rendaku();

wk_rendaku.init();
wk_rendaku.run();
