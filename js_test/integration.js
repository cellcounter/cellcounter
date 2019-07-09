// Mocha Specification Cases

// Imports
const assert    = require('assert').strict;
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
describe('The web page', () => {

   before(loadWebPage);
   after(closeWebPage);


   it('has the correct URL -> ' + url, () => {
      const actual =   { url: window.location.href };
      const expected = { url: url };
      assert.deepStrictEqual(actual, expected);
      });

   it('has cell_types of correct length', () => {
      const count = Object.keys(window.cell_types).length;
      assert.deepStrictEqual(count, 13);
      });

    it('counts correctly', () => {
        //press 'q' 5 times
        var e = $.Event('keydown');
        e.key = e.which = 113; // 'q'
        for(var i = 0; i<5; i++)
            $(window.document).trigger(e);

        e.key = e.which = 65; // 'a'
        for(var i = 0; i<5; i++)
            $(window.document).trigger(e);

        var total = window.counter.get_total();

        assert.deepStrictEqual(total, 10);

        e.key = e.which = 8; // 'backspace'
        for(var i = 0; i<3; i++)
            $(window.document).trigger(e);

        var total = window.counter.get_total();

        assert.deepStrictEqual(total, 7);
      });

});

