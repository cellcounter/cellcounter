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

describe('The web page', function () {

   before(function(done) {
      this.timeout(3000);
      loadWebPage(done);
   });

   after(closeWebPage);

   this.timeout(4000);

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
        trigger_keydown('q',5);

        //press 'a' 5 times
        trigger_keydown('a',5);

        var total = window.counter.get_total();

        assert.deepStrictEqual(total, 10);

        //press backspace 3 times
        trigger_keydown(8,3);

        var total = window.counter.get_total();

        assert.deepStrictEqual(total, 7);
    });

    it('resets the counter correctly', () => {

        assert($("#confirm-reset").is(":hidden"));

        $('.reset_button').trigger('click');

        assert.deepStrictEqual(window.counter.get_total(), 7);

        $('input#reset-count').trigger('click');

        assert.deepStrictEqual(window.counter.get_total(), 0);

        assert($("#confirm-reset").is(":hidden"));

    });

    it('counts each celltype', function (done) {

        this.timeout(20000);

        var counter = window.counter;

        var cell_ids = counter.get_cell_ids();
        var keys = ['q','w','e','r','t','a','s','d','f','g','z','x','c'];

        assert.deepStrictEqual(cell_ids.length, keys.length);

        for(var i=0; i<keys.length; i++) {
            trigger_keydown(keys[i], i+1);
        }

        assert.deepStrictEqual(counter.get_total(), (keys.length+1)*keys.length/2);
        done();
    });

    it('displays the results correctly', () => {

        // results div should be hidden initially
        assert.deepStrictEqual(get_display('div#statistics'), "none");

        $('#close_button').trigger('click');

        // results div should be displayed when the close button is "clicked"
        assert.deepStrictEqual(get_display('div#statistics'), "block");

        // html results should be displayed
        assert.deepStrictEqual(get_display('div#statistics_html'), "block");

        // and text results hidden
        assert.deepStrictEqual(get_display('div#statistics_text'), "none");

    });

    it('with the correct counts and percentages', () => {
        var cell_type_order = ['Blasts','Promyelocytes','Myelocytes','Metamyelocytes','Neutrophils','Monocytes','Basophils','Eosinophils','Lymphocytes','Plasma cells','Erythroid','Other','Lymphoblasts'];

        var expected_counts = [5,4,3,2,1,9,12,11,7,8,6,13,10];

        var sum = expected_counts.reduce((a,b) => a + b, 0);

        $('div#statistics_html').find('tr.count-results-detail').each( function (index) {
            var tds = $(this).find('td');
            assert.deepStrictEqual(tds.first().text(), cell_type_order[index]);
            assert.deepStrictEqual(tds.eq(2).html(),Math.floor(expected_counts[index]/sum*100+0.5)+"%");
            assert.deepStrictEqual(tds.eq(3).html(),"0%");
            assert.deepStrictEqual(parseInt(tds.eq(4).html()),expected_counts[index]);
            assert.deepStrictEqual(parseInt(tds.eq(5).html()),0);
        });

        assert.deepStrictEqual(parseInt($('td#total-count').text()), sum);
        assert.deepStrictEqual($('td#me-ratio').text(), "7.00");

    });

});

