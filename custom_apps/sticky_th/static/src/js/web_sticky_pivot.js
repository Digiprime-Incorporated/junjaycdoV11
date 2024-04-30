// Fathony, 1 January 2019



odoo.define('x2nie.Sticky_PivotRenderer',function (require) {
"use strict";

$.event.special.mresize.immediate = true;

var core = require('web.core');
var Sticky_Config = require('x2nie.Sticky_TR.config'); 
var PivotRenderer = require('web.PivotRenderer');


PivotRenderer.include({
    
    sticking_table_header: function(options){
      var self = this,
          $el = this.$el,
          $listenScroll = null,
          viewports$ = [],
          tableViewport = $el.find('null'),
          TABLEWRAPPER = '.o_pivot', //v11
          VIEWMANAGER = '.o_main_content > .o_content, body > .o_content', //v11
          FORMVIEW = '.o_view_manager_content .o_form_view', //v11
          MODAL = '.modal-dialog', 
          MODALBODY = '.modal-body.o_act_window', //v11
          MODALDIALOG = '.modal-dialog', //v11
          O2MCPANEL = '.o_x2m_control_panel', //v11
          CPANEL = '.o_control_panel', //v11
          TABLE = 'table.bordered', //v11
          alwaysFloating= true, //self.stickingTh_getAlwaysFloating(), // only for main Tree/ListView
          alwaysShadowed= true //self.stickingTh_getAlwaysShadowed()  // only for main Tree/ListView
      
      if(!self.sticky_config)
        self.sticky_config = new Sticky_Config();
      alwaysFloating= self.sticky_config.alwaysFloating // only for main Tree/ListView
      alwaysShadowed= self.sticky_config.alwaysShadowed // only for main Tree/ListView
      
      
      self.$el.removeData('plugin_stickyTableHeaders');
      if (typeof options === 'string') {
        return self.$el.stickyTableHeaders(options)
        
      }
      
      
        // tableViewport = $el.parents(VIEWMANAGER);
        tableViewport = $(VIEWMANAGER);
        $listenScroll = $el.is(TABLEWRAPPER) ? $el : $el.parents(TABLEWRAPPER);
      
      if(tableViewport.length > 0 ){
        if(tableViewport.prev().is(CPANEL)) {
          $listenScroll = $listenScroll ? $listenScroll.add( tableViewport.prev() ) : tableViewport.prev();
          }

        var options = {
          "viewports": [tableViewport].concat(viewports$),  //new
          'listenScroll': $listenScroll,
          'injectCSS': false,
          'cellResize': false,
          'alwaysFloating': alwaysFloating,
          'alwaysShadowed': alwaysShadowed          
          };
        
        // self.$el.children(TABLE).stickyTableHeaders(options)
        self.$el.stickyTableHeaders(options)
        
      }
    },
    _render: function () {
        var self = this,
            firstTime = this.$el.children().length == 0;
        return this._super.apply(this, arguments).then(function(){
        // return this._super().then(function(){
            console.log('pivot', self.$el)
            if(firstTime){                
              var lazyreflow = $.debounce(5, self.sticking_table_header.bind(self));
              var lazyreflow0 = $.debounce(50, function(){
                    self.$el.removeData('plugin_stickyTableHeaders');
                    self.sticking_table_header.bind(self)
              });
              
              // REGISTER RESIZE ON NEW CREATED ONLY
              // var $table = self.$el.children('table:first')
              lazyreflow();
            }
            else{                
              // special for pivot, the html has been already destroyed here.
              self.$el.removeData('plugin_stickyTableHeaders');
              self.sticking_table_header()
            }
        });
    },
    
    
})

});



odoo.define('x2nie.sticky_PivotModel', function (require) {
"use strict";

var PivotModel = require('web.PivotModel');

PivotModel.include({

    /**
     * Expand (open up) a given header, be it a row or a column.
     *
     * @todo: add discussion on the number of read_group that it will generate,
     * which is (r+1) or (c+1) I think
     *
     * @param {any} header
     * @param {any} field
     * @returns
     */
    // expandHeader: function (header, field) {
})
});


odoo.define('x2nie.sticky_PivotController', function (require) {
"use strict";

var PivotController = require('web.PivotController');

PivotController.include({
 sticking_table_header: function(options){
      var self = this,
          $el = this.$el,
          $listenScroll = null,
          viewports$ = [],
          tableViewport = $el.find('null'),
          TABLEWRAPPER = '.o_pivot', //v11
          VIEWMANAGER = '.o_main_content > .o_content, body > .o_content', //v11
          FORMVIEW = '.o_view_manager_content .o_form_view', //v11
          MODAL = '.modal-dialog', 
          MODALBODY = '.modal-body.o_act_window', //v11
          MODALDIALOG = '.modal-dialog', //v11
          O2MCPANEL = '.o_x2m_control_panel', //v11
          CPANEL = '.o_control_panel', //v11
          TABLE = 'table.bordered', //v11
          alwaysFloating= true, //self.stickingTh_getAlwaysFloating(), // only for main Tree/ListView
          alwaysShadowed= true //self.stickingTh_getAlwaysShadowed()  // only for main Tree/ListView
      
      if (typeof options === 'string') {
        // return self.$el.children(TABLE).stickyTableHeaders(options)
        return self.$el.stickyTableHeaders(options)
        
      }
      
      
        tableViewport = $el.parents(VIEWMANAGER);
        $listenScroll = $el.is(TABLEWRAPPER) ? $el : $el.parents(TABLEWRAPPER);
      
      if(tableViewport.length > 0 ){
        if(tableViewport.prev().is(CPANEL)) {
          $listenScroll = $listenScroll ? $listenScroll.add( tableViewport.prev() ) : tableViewport.prev();
          }

        var options = {
          "viewports": [tableViewport].concat(viewports$),  //new
          'listenScroll': $listenScroll,
          'injectCSS': false,
          'alwaysFloating': alwaysFloating,
          'alwaysShadowed': alwaysShadowed          
          };
        
        // self.$el.children(TABLE).stickyTableHeaders(options)
        self.$el.stickyTableHeaders(options)
        
      }
    },
    /**
     * @private
     */
    _update000: function () {
        // this._updateButtons();
        var self = this;
        return this._super.apply(this, arguments).then(function(){
            // self.renderer.sticking_table_header.bind(self)
            self.sticking_table_header('destroy')
            self.sticking_table_header()
        });
    },

})

});
    