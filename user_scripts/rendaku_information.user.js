// ==UserScript==
// @name        WaniKani Rendaku Information
// @version     0.2020
// @author      jameshippisley
// @description Adds information to Wanikani about why readings do or do not use rendaku.
// @license     GPL version 3 or any later version; http://www.gnu.org/copyleft/gpl.html
// @namespace   wk_rendaku
//
// @match       https://www.wanikani.com/*
// @match       https://preview.wanikani.com/*
//
// @updateURL   https://raw.githubusercontent.com/jameshippisley/wanikani/master/user_scripts/rendaku_information.user.js
// @downloadURL https://raw.githubusercontent.com/jameshippisley/wanikani/master/user_scripts/rendaku_information.user.js
//
// @require     https://greasyfork.org/scripts/430565-wanikani-item-info-injector/code/WaniKani%20Item%20Info%20Injector.user.js?version=1111117
// @require     https://raw.githubusercontent.com/jameshippisley/wanikani/51ec0bb201f179ac632dc9c0f4aa64b778428f39/user_scripts/rendaku_information_data.json
//
// @run-at      document-end
//
// @grant       none
//
// ==/UserScript==

// #############################################################################
function WK_Rendaku()
{
    this.settings = {
        hideTrivial: false,
        hideUnexceptional: false
    };
    this.currentlyLoadingSettings = false; // if wkof is available and currently loading the settings, this will be a Promise resolving after the settings are loaded
    this.itemInfoHandle = null;
}


(function() {
    'use strict';

    /* global WK_RENDAKU_INFO_DATA, wkof, wkItemInfo */

    WK_Rendaku.prototype.createRendakuSection = function(word)
    {
        let info = WK_RENDAKU_INFO_DATA[word];
        if (!info) return null;

        let trivial = info.includes(`no possible rendaku`);
        const unexceptional = info.includes(`none of the exceptional circumstances`);
        let waitForSettings = trivial && unexceptional && this.currentlyLoadingSettings;

        let paragraphConstructor = () => {
            if (trivial && this.settings.hideTrivial) return null;
            if (unexceptional && this.settings.hideUnexceptional) return null;
            let p = document.createElement(`p`);
            p.innerHTML = info;
            return p;
        };

        if (waitForSettings) {
            return this.currentlyLoadingSettings.then(paragraphConstructor);
        } else {
            return paragraphConstructor();
        }
    };

    WK_Rendaku.prototype.setupMenu = function()
    {
        wkof.Menu.insert_script_link({name: `rendaku_information`, submenu: `Settings`, title: `Rendaku Information`, on_click: this.openSettings.bind(this)});
        return wkof.Settings.load(`rendaku_information`, this.settings).then(() => Object.assign(this.settings, wkof.settings.rendaku_information));
    }

    WK_Rendaku.prototype.openSettings = function()
    {
        let dialog = new wkof.Settings({
            script_id: `rendaku_information`,
            title: `Rendaku Information Settings`,
            on_save: this.saveSettings.bind(this),
            content: {
                hideTrivial: {
                    type: `checkbox`,
                    label: `Hide trivial info`,
                    hover_tip: `If the rendaku information is trivial, don't show the section at all.`
                },
                hideUnexceptional: {
                    type: `checkbox`,
                    label: `Hide info on unexceptional circumstances`,
                    hover_tip: `If the onyomi doesn't rendaku or if the kunyomi does rendaku as generally expected, don't show the section at all.`}
                }
        });
        dialog.open();
    }

    WK_Rendaku.prototype.saveSettings = function()
    {
        Object.assign(this.settings, wkof.settings.rendaku_information);
        this.itemInfoHandle.renew();
    }

    // #########################################################################
    WK_Rendaku.prototype.init = function()
    {
        if (typeof wkof === `object`) {
            wkof.include(`Menu,Settings`);
            this.currentlyLoadingSettings = wkof.ready(`Menu,Settings`).then(this.setupMenu.bind(this)).then(() => { this.currentlyLoadingSettings = false; });
        }

        // #####################################################################
        // Main hook, WK Item Info Injector will kick off this script once the
        // page is ready and we can access the subject of the page.
        this.itemInfoHandle = wkItemInfo.forType(`vocabulary`).under(`reading`).appendSubsection(`Rendaku Information`, o => this.createRendakuSection(o.characters));
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
