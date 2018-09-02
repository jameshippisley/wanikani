alert('here');

// #############################################################################
function WK_Rendaku()
{
    this.wki = new WKInteraction(GM_info.script.namespace);

    this.currentSubject = null;

    this.settings = {
        "debug": true
    };

}
/*
(function() {
    'use strict';

    // #########################################################################
    WK_Rendaku.prototype.injectRendakuSection = function(event, curPage)
    {
        // #####################################################################
        $(`#rendaku_section`).remove();

        const subject = this.wki.getSubject();

        this.log(`Injecting phonetic section (callback works).`);

        if (!this.wki.checkSubject(subject, [`rad`, `kan`]))
            return;

        if (subject.rad)
            subject.phon = this.kdb.mapWKRadicalToPhon(subject.rad);
        else
            subject.phon = this.kdb.getKPhonetic(subject.kan) || subject.kan;

        this.currentSubject = subject;
        this.log(`Working with the following input:`, subject);
        // #####################################################################
    }

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
*/
