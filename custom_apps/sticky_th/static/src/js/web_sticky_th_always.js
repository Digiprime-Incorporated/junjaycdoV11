// Fathony, 27 Oktober 2018
odoo.define('x2nie.Sticky_TR.always',function (require) {
"use strict";

var core = require('web.core');
var ListRenderer = require('web.ListRenderer');
var Sticky_TR = require('x2nie.Sticky_TR'); //let inheritor loaded first
var Sticky_Config = require('x2nie.Sticky_TR.config'); //let inheritor being loaded first

var _t = core._t;
var bus = core.bus;

  Sticky_Config.include({
      alwaysShadowed: true,
  });

  ListRenderer.include({
		
    /** It is usefull if Tree/List View is always sticky. 
     *  But we allow user to decide, so it is unistallable if user doesn't want it
     */
		stickingTh_getAlwaysFloating: function(){
      var O2MCPANEL = '.o_x2m_control_panel', //v11
          alwaysFloating = !this.$el.prev().is(O2MCPANEL)
      return alwaysFloating
    },
        
  });
    
});

