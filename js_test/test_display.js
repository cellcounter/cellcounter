// Mocha Specification Cases

// Imports
const assert    = require('assert');
const { JSDOM } = require('jsdom');

// Setup
const url  = 'http://127.0.0.1:8000/';
let window, $;
const loadWebPage = (done) => {
   const handleWebPage = (dom) => {
      const waitForScripts = () => {
         window = dom.window;
         $ = dom.window.jQuery;
         $.when(window.initialised).done(function () {done();});
         };
      dom.window.onload = waitForScripts;
      };
   const options = { resources: 'usable', runScripts: 'dangerously', pretendToBeVisual: true };
   global.document = JSDOM.fromURL(url, options).then(handleWebPage);
   };
const closeWebPage = () => window.close();

////////////////////////////////////////////////////////////////////////////////////////////////////

function trigger_keydown(key, repeat) {
    var rpt = (typeof repeat === "undefined") ? 1 : repeat;
    var e = $.Event('keydown');

    var key_code;
    if(typeof key === "number") {
        key_code = key;
    } else if(typeof key === "string") {
        key_code = key.charCodeAt(0);
    }

    e.key = e.which = key_code;
    for(var i=0; i<rpt; i++)
        $(window.document).trigger(e);
}

function get_display(selector) {
    return window.getComputedStyle($(selector)[0])['display'];
}

function get_display_parent(selector) {
    return window.getComputedStyle($(selector).first().parent()[0])['display'];
}

function delay(interval) 
{
   return it('should delay', done => 
   {
      setTimeout(() => done(), interval)

   }).timeout(interval + 100) // The extra 100ms should guarantee the test will not fail due to exceeded timeout
}

describe('The web page', () => {

   before(function(done) {
      this.timeout(3000);
      loadWebPage(done);
   });

   after(closeWebPage);


   it('has the correct URL -> ' + url, () => {
      const actual =   { url: window.location.href };
      const expected = { url: url };
      assert.deepStrictEqual(actual, expected);
      });

    it('displays the keyboard', () => {
        assert.deepStrictEqual(get_display('div#counterbox'), "block");
    });

    it('triggers the keyboard to close', () => {
        $('#close_button').trigger('click');
    });

    //wait two seconds for the keyboard to close
    delay(1500);

    it('closes the keyboard and does not show stats', () => {

        assert.deepStrictEqual(get_display('div#counterbox'), "none");
        assert.deepStrictEqual(get_display('div#statistics'), "none");
    });

    it('does not count when the keyboard is closed', () => {
        trigger_keydown('d',1);
        trigger_keydown('q',5);

        var total = window.counter.get_total();

        assert.deepStrictEqual(total, 0);
    });

    it('triggers the keyboard to open', () => {
        $('div#openkeyboard').trigger('click');
    });

    delay(1500);

    it('shows the keyboard again', () => {
        assert.deepStrictEqual(get_display('div#counterbox'), "block");
    });

    it('counts and closes the keyboard', () => {
        trigger_keydown('d',1);

        var total = window.counter.get_total();

        assert.deepStrictEqual(total, 1);
        
        $('#close_button').trigger('click');
     });

    delay(1500);

    it('hides the keyboard and shows HTML results', () => {
        assert.deepStrictEqual(get_display('div#counterbox'), "none");
        assert.deepStrictEqual(get_display('div#statistics'), "block");
        assert.deepStrictEqual(get_display('div#statistics_html'), "block");
        assert.deepStrictEqual(get_display('div#statistics_text'), "none");
    });

    it('shows the text results', () => {
        $('#textview').trigger('click');

        assert.deepStrictEqual(get_display('div#statistics_html'), "none");
        assert.deepStrictEqual(get_display('div#statistics_text'), "block");
    });

    it('shows the html results again', () => {
        $('#htmlview').trigger('click');

        assert.deepStrictEqual(get_display('div#statistics_html'), "block");
        assert.deepStrictEqual(get_display('div#statistics_text'), "none");
    });

    it('shows the reset modal dialog', () => {
        $('.reset_button').trigger('click');

        assert.deepStrictEqual(window.counter.get_total(), 1);

        $('input#reset-count').trigger('click');

        assert.deepStrictEqual(window.counter.get_total(), 0);
    });

    delay(1500);

    it('shows the keyboard after reset', () => {
        assert.deepStrictEqual(get_display('div#counterbox'), "block");
        assert.deepStrictEqual(get_display('div#statistics'), "none");
    });

    it('shows the edit keyboard dialog', () => {
        assert.deepStrictEqual(get_display('div#editkeymapbox'), "none");

        $('#edit_button').trigger('click');

        assert.deepStrictEqual(get_display('div#editkeymapbox'), "block");
    });

    it('hides the edit keyboard dialog', () => {
        assert.deepStrictEqual(get_display_parent('div#editkeymapbox'), "block");

        $('.ui-dialog-buttonset button:contains("Close")').trigger('click');

        assert.deepStrictEqual(get_display_parent('div#editkeymapbox'), "none");
    });
    
});

