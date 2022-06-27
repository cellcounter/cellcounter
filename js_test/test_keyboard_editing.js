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

   it('is not editing the keyboard', () => {
      const editing = window.editing_keyboard;
      assert.deepStrictEqual(editing, false);
      });

    it('has the correct default keyboard mapping', () => {
      const keyboard_map = window.keyboard_map;
      assert.deepStrictEqual(keyboard_map.label, "Default desktop");
      assert.deepStrictEqual(keyboard_map.mappings.length, 13);
    });

    it('edits the keyboard mapping on button press', () => {
      $('#edit_button').trigger('click');

      const editing = window.editing_keyboard;
      assert.deepStrictEqual(editing, true);
    });

    it('has the correct default options', () => {
      assert.deepEqual($('#multi_key').is(':checked'), true);
      assert.deepEqual($('#auto_advance').is(':checked'), false);
    });

    it('clears the keyboard mapping', () => {
      $('#clearkeyboard').trigger('click');
      const keyboard_map = window.keyboard_map;

      assert.deepStrictEqual(keyboard_map.mappings.length, 0)
    });

    it('maps keys to the keyboard', () => {
      const keyboard_map = window.keyboard_map;
      var keys = ['c','x','z','g','f','d','s','a','t','r','e','w','q'];

      expected_mappings = [];
      for(var i=0; i<keys.length; i++) {
        $('#swatch_'+(i+1)).trigger('click');
        trigger_keydown(keys[i], 1);
        expected_mappings.push({cellid: i+1, key: keys[i]});
      }

      assert.deepEqual(keyboard_map.mappings, expected_mappings);

    });

    it('closes the keyboard editor', () => {

      $('button#revert_keyboard_map').trigger('click');
      const editing = window.editing_keyboard;
      assert.deepStrictEqual(editing, false);

    });

   delay(1500);

    it('and reverts the keyboard map', () => {
      const keyboard_map = window.keyboard_map;
      var keys = ['q','w','e','r','t','x','z','a','s','f','d','c','g'];
      var expected_mappings = [], actual_mappings = [];
      for(var i=0; i<keys.length; i++) {
        expected_mappings.push({cellid: i+1, key: keys[i]});
      }

      for(var i=0; i<keyboard_map.mappings.length; i++) {
        var cellid = keyboard_map.mappings[i].cellid;
        var key = keyboard_map.mappings[i].key;
        actual_mappings.push({cellid: cellid, key: key});
      }

      expected_mappings.sort((a, b) => {return a['cellid']-b['cellid']});
      actual_mappings.sort((a, b) => {return a['cellid']-b['cellid']});

      assert.deepEqual(actual_mappings, expected_mappings);

    });

    it('reopens the keyboard editor', () => {
      $('#edit_button').trigger('click');

      const editing = window.editing_keyboard;
      assert.deepStrictEqual(editing, true);

    });

    it('maps keys to the keyboard', () => {
      const keyboard_map = window.keyboard_map;
      var keys = ['c','q','z','g','f','d','s','a','t','r','e','w','x'];

      expected_mappings = [];
      for(var i=0; i<keys.length; i++) {
        $('#swatch_'+(i+1)).trigger('click');
        trigger_keydown(keys[i], 1);
        expected_mappings.push({cellid: i+1, key: keys[i]});
      }

      assert.deepEqual(keyboard_map.mappings, expected_mappings);

    });

    it('closes the keyboard editor', () => {

      $('button#save_keyboard_map').trigger('click');
      const editing = window.editing_keyboard;
      assert.deepStrictEqual(editing, false);

    });

   delay(1500);

    it('and preserves the keyboard map', () => {
      const keyboard_map = window.keyboard_map;
      var keys = ['c','q','z','g','f','d','s','a','t','r','e','w','x'];
      var expected_mappings = [], actual_mappings = [];
      for(var i=0; i<keys.length; i++) {
        expected_mappings.push({cellid: i+1, key: keys[i]});
      }

      for(var i=0; i<keyboard_map.mappings.length; i++) {
        var cellid = keyboard_map.mappings[i].cellid;
        var key = keyboard_map.mappings[i].key;
        actual_mappings.push({cellid: cellid, key: key});
      }

      expected_mappings.sort((a, b) => {return a['cellid']-b['cellid']});
      actual_mappings.sort((a, b) => {return a['cellid']-b['cellid']});

      assert.deepEqual(actual_mappings, expected_mappings);

    });

    it('only allows one key per celltype', () => {
      $('#edit_button').trigger('click');

      const editing = window.editing_keyboard;
      assert.deepStrictEqual(editing, true);

      $('#clearkeyboard').trigger('click');
      const keyboard_map = window.keyboard_map;

      assert.deepStrictEqual(keyboard_map.mappings.length, 0)

      $('#swatch_1').trigger('click');

      trigger_keydown('q', 1);

      assert.deepEqual(keyboard_map.mappings, [{cellid: 1, key: 'q'}]);

      trigger_keydown('w', 1);

      assert.deepEqual(keyboard_map.mappings, [{cellid: 1, key: 'w'}]);

    });

    it('allows multiple keys per celltype', () => {
      $('#clearkeyboard').trigger('click');
      const keyboard_map = window.keyboard_map;

      assert.deepStrictEqual(keyboard_map.mappings.length, 0)

      $('#multi_key').trigger('click');
      assert.deepEqual($('#multi_key').is(':checked'), false);
      
      trigger_keydown('q', 1);

      assert.deepEqual(keyboard_map.mappings, [{cellid: 1, key: 'q'}]);

      trigger_keydown('w', 1);

      assert.deepEqual(keyboard_map.mappings, [{cellid: 1, key: 'q'}, {cellid: 1, key: 'w'}]);

      $('#multi_key').trigger('click');
      assert.deepEqual($('#multi_key').is(':checked'), true);

    });

    it('closes the keyboard editor', () => {

      $('button#revert_keyboard_map').trigger('click');
      const editing = window.editing_keyboard;
      assert.deepStrictEqual(editing, false);

    });

    delay(1500);

    it('automatically advances through the celltypes', () => {
      $('#edit_button').trigger('click');

      const editing = window.editing_keyboard;
      assert.deepStrictEqual(editing, true);

      $('#clearkeyboard').trigger('click');
      const keyboard_map = window.keyboard_map;

      assert.deepStrictEqual(keyboard_map.mappings.length, 0)

      $('#auto_advance').trigger('click');
      assert.deepEqual($('#auto_advance').is(':checked'), true);

      var keys = ['c','q','z','g','f','d','s','a','t','r','e','w','x'];

      var expected_mappings = [], actual_mappings = [];
      for(var i=0; i<keys.length; i++) {
        trigger_keydown(keys[i], 1);
        expected_mappings.push({cellid: i+1, key: keys[i]});
      }

      assert.deepStrictEqual(keyboard_map.mappings.length, 13);
      assert.deepEqual(keyboard_map.mappings, expected_mappings);
      
      $('#auto_advance').trigger('click');
      assert.deepEqual($('#auto_advance').is(':checked'), false);

    });

});

