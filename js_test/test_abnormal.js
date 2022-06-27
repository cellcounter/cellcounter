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

function delay(interval) 
{
   return it('should delay', done => 
   {
      setTimeout(() => done(), interval)

   }).timeout(interval + 500) // The extra 500ms should guarantee the test will not fail due to exceeded timeout
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

    it('counts abnormal cells correctly', () => {
        //press 'q' 5 times
        trigger_keydown('q',5);

        trigger_keydown(' ', 1);

        //press 'a' 5 times
        trigger_keydown('a',5);

        var total = window.counter.get_total();
        var ab_total = window.counter.get_abnormal_total();

        assert.deepStrictEqual(total, 10);
        assert.deepStrictEqual(ab_total, 5);

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

        assert.deepStrictEqual(counter.get_total(), (keys.length+1)*keys.length/2 + 10);
        assert.deepStrictEqual(counter.get_abnormal_total(), (keys.length+1)*keys.length/2 + 5);
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

        var expected_counts = [5,4,3,2,1+5,9,12,11,7,8,6+5,13,10];
        var expected_normal_counts = [0,0,0,0,0+5,0,0,0,0,0,0,0,0];
        var expected_abnormal_counts = [5,4,3,2,1,9,12,11,7,8,6+5,13,10];

        var sum = expected_counts.reduce((a,b) => a + b, 0);

        $('div#statistics_html').find('tr.count-results-detail').each( function (index) {
            var tds = $(this).find('td');
            assert.deepStrictEqual(tds.first().text(), cell_type_order[index]);
            var expected = expected_counts[index] == 0 ? 'N/A' : Math.floor(expected_counts[index]/sum*100+0.5)+"%";
            assert.deepStrictEqual(tds.eq(2).html(), expected);
            assert.deepStrictEqual(tds.eq(3).html(),Math.floor(expected_abnormal_counts[index]/expected_counts[index]*100+0.5)+"%");
            assert.deepStrictEqual(parseInt(tds.eq(4).html()),expected_normal_counts[index]);
            assert.deepStrictEqual(parseInt(tds.eq(5).html()),expected_abnormal_counts[index]);
        });

        $('div#statistics_html').find('tr.count-results-detail').each( function (index) {
            var tds = $(this).find('td');
            for(var i=0; i<6; i++) {
                assert.deepStrictEqual(window.getComputedStyle(tds.eq(i)[0])['display'], "table-cell");
            }
        });
    });

    it('does not remove cells when keyboard is closed', () => {

        var total = window.counter.get_total();

        trigger_keydown(8, total-5);

        assert.deepStrictEqual(window.counter.get_total(), total);

        $('div#openkeyboard').trigger('click');
    });

    delay(1500);
    
    it('removes all abnormal cells', () => {

        var total = window.counter.get_total();

        trigger_keydown(8, total-5);

        assert.deepStrictEqual(window.counter.get_total(), 5);
        assert.deepStrictEqual(window.counter.get_abnormal_total(), 0);

        $('#close_button').trigger('click');
    });

    it('with the correct counts and percentages', () => {
        var cell_type_order = ['Blasts','Promyelocytes','Myelocytes','Metamyelocytes','Neutrophils','Monocytes','Basophils','Eosinophils','Lymphocytes','Plasma cells','Erythroid','Other','Lymphoblasts'];

        var expected_counts = [0,0,0,0,0+5,0,0,0,0,0,0,0,0];
        var expected_normal_counts = [0,0,0,0,0+5,0,0,0,0,0,0,0,0];
        var expected_abnormal_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0];

        var sum = expected_counts.reduce((a,b) => a + b, 0);

        $('div#statistics_html').find('tr.count-results-detail').each( function (index) {
            var tds = $(this).find('td');
            assert.deepStrictEqual(tds.first().text(), cell_type_order[index]);
            var expected = sum == 0 ? 'N/A' : Math.floor(expected_counts[index]/sum*100+0.5)+"%";
            assert.deepStrictEqual(tds.eq(2).html(), expected);
            var expected_ab = expected_counts[index] == 0 ? 'N/A' : Math.floor(expected_abnormal_counts[index]/expected_counts[index]*100+0.5)+"%";
            assert.deepStrictEqual(tds.eq(3).html(), expected_ab);
            assert.deepStrictEqual(parseInt(tds.eq(4).html()),expected_normal_counts[index]);
            assert.deepStrictEqual(parseInt(tds.eq(5).html()),expected_abnormal_counts[index]);
        });

        $('div#statistics_html').find('tr.count-results-detail').each( function (index) {
            var tds = $(this).find('td');
            for(var i=0; i<6; i++) {
                if(i==3 || i==5)
                    assert.deepStrictEqual(window.getComputedStyle(tds.eq(i)[0])['display'], "none");
                else
                    assert.deepStrictEqual(window.getComputedStyle(tds.eq(i)[0])['display'], "table-cell");
            }
        });
    });
    
});

