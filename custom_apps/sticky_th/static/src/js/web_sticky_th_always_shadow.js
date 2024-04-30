// Fathony, 28 Oktober 2018
odoo.define('x2nie.Sticky_TR.always.shadow',function (require) {
"use strict";

var core = require('web.core');
var ListRenderer = require('web.ListRenderer');
var Sticky_TR = require('x2nie.Sticky_TR'); //let inheritor being loaded first
var Sticky_Config = require('x2nie.Sticky_TR.config'); //let inheritor being loaded first

var _t = core._t;
var bus = core.bus;

  Sticky_Config.include({
      alwaysShadowed: true,
  });
  
  ListRenderer.include({
		
    /** It is usefull if Tree/List View is always sticky. In this case, we notice by visual element: shadow!
     *  But we allow user to decide, so it is unistallable if user doesn't want it
     */
		stickingTh_getAlwaysShadowed: function(){
      return true;
    },
        
  });
    
});

