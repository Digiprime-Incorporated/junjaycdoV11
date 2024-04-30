// Fathony, 03 April 2019
odoo.define('x2nie.Sticky_TR.config',function (require) {
"use strict";

var core = require('web.core');
var Config = core.Class.extend({
    // Backbone-ish API
    alwaysFloating: false,
    alwaysShadowed: false
    
});

return Config;
    
});

