// ==UserScript==
// @name        WaniKani Rendaku Information
// @version     0.2005
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
// @require     https://greasyfork.org/scripts/430565-wanikani-item-info-injector/code/WaniKani%20Item%20Info%20Injector.user.js?version=958983
// @require     https://raw.githubusercontent.com/jameshippisley/wanikani/51ec0bb201f179ac632dc9c0f4aa64b778428f39/user_scripts/rendaku_information_data.json
//
// @run-at      document-end
//
// @grant       GM_log
//
// ==/UserScript==

// The code below to insert custom lessons sections into the WaniKani pages is partially copied from
// https://github.com/mwil/wanikani-userscripts/tree/master/wanikani-phonetic-compounds
// Massive thanks to mwil for showing me how to make use of this code.

// #############################################################################
function WK_Rendaku()
{
    this.settings = {
        "debug": false
    };
}


(function() {
    'use strict';

    WK_Rendaku.prototype.createRendakuSection = function(word)
    {
        let p = null;

        var info = WK_RENDAKU_INFO_DATA[word]
        if (info) {
            p = document.createElement(`p`);
            p.innerHTML = info;
            this.log(`Created the Rendaku section, appending to the page!`);
        }
        else {
            this.log(`no info for ${word}`)
        }

        return p;
    };

    // #########################################################################
    WK_Rendaku.prototype.init = function()
    {

        this.log = this.settings.debug ?
            function(msg, ...args) {
                GM_log(`${GM_info.script.namespace}:`, msg, ...args);
            } :
            function() {};

        this.log(`The script element is:`, GM_info);

        // #####################################################################
        // Main hook, WK Item Info Injector will kick off this script once the
        // page is ready and we can access the subject of the page.
        wkItemInfo.forType(`vocabulary`).under(`reading`).appendSubsection(`Rendaku Information`, o => this.createRendakuSection(o.characters));
        // #####################################################################
    };
    // #########################################################################
}
)();
// #############################################################################


// #############################################################################
// #############################################################################
var wk_rendaku = new WK_Rendaku();

wk_rendaku.init();
