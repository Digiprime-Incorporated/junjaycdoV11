// Fathony, 19 Oktober 2018
odoo.define('x2nie.Sticky_TR',function (require) {
"use strict";

$.event.special.mresize.immediate = true;

var core = require('web.core');
var ListRenderer = require('web.ListRenderer');
var Sticky_Config = require('x2nie.Sticky_TR.config'); //let inheritor being loaded first

var _t = core._t;
var bus = core.bus;

  ListRenderer.include({
    
    /** It is usefull if Tree/List View is always sticky. 
     *  But we allow user to decide, so it is unistallable if user doesn't want it
     */
    stickingTh_getAlwaysFloating: function(){
      return false; //nothing here, activate it in Setting > General Settings
    },
    stickingTh_getAlwaysShadowed: function(){
      return false; //nothing here, activate it in Setting > General Settings
    },
    
    sticking_table_header: function(options){
      var self = this,
          $el = this.$el,
          $listenScroll = null,
          viewports$ = [],
          tableViewport = $el.find('null'),
          TABLEWRAPPER = '.table-responsive', //v11
          VIEWMANAGER = '.o_main_content > .o_content, body > .o_content', //v11
          FORMVIEW = '.o_view_manager_content .o_form_view', //v11
          MODAL = '.modal-dialog', 
          MODALBODY = '.modal-body.o_act_window', //v11
          MODALDIALOG = '.modal-dialog', //v11
          O2MCPANEL = '.o_x2m_control_panel', //v11
          CPANEL = '.o_control_panel', //v11
          TABLE = 'table.o_list_view', //v11
          HASBANNER = 'o_has_banner', //v12
          alwaysFloating= self.stickingTh_getAlwaysFloating(), // only for main Tree/ListView
          alwaysShadowed= self.stickingTh_getAlwaysShadowed()  // only for main Tree/ListView
      
      if(!self.sticky_config)
        self.sticky_config = new Sticky_Config();
      alwaysFloating= self.sticky_config.alwaysFloating // only for main Tree/ListView
      alwaysShadowed= self.sticky_config.alwaysShadowed // only for main Tree/ListView
      
      if (typeof options === 'string') {
        return self.$el.children(TABLE).stickyTableHeaders(options)
        
      }
      
      //1.a O2M LISTVIEW IN FORM:
      if($el.parents(FORMVIEW).length > 0) {
        tableViewport = $el.parents(VIEWMANAGER);
      }
      // DIALOG
      else if($el.parents(MODAL).length > 0) {
        alwaysFloating = false; //prevent floating here
        var b = tableViewport = $el.parents(MODALBODY);
        if(tableViewport.length > 0 ) {
          tableViewport.attr('style',
            '-webkit-transform:nont; -ms-transform:none;-o-transform:none; transform:none;');
          viewports$.push( tableViewport.parents('.modal.in') );
          tableViewport.add($el.parents(MODALDIALOG)).css({
            '-webkit-transform':'none', '-ms-transform':'none', '-o-transform':'none', 
            'transform':'none'});
        }
      }
      //1.b ROOT IS LISTVIEW WITH SEARCHBOX.
      else {
        tableViewport = $el.parents(VIEWMANAGER);
        $listenScroll = $el.is(TABLEWRAPPER) ? $el : $el.parents(TABLEWRAPPER);
      }
      
      
      if(tableViewport.length < -1 ){
        tableViewport = self.$el.parents('.modal-content.openerp > .modal-body.o_act_window');
        
        if(tableViewport.length > 0 ) {
          tableViewport.parents('.modal-dialog').attr('style',
            '-webkit-transform:nont; -ms-transform:none;-o-transform:none; transform:none');
          var overflow = tableViewport.css('overflow');
          if (!overflow || overflow == 'visible') {
            tableViewport = tableViewport.parents('.modal.in');
          }
        }
      }
      // console.log('FINALLY~~~~listview sticky header tableViewport FINALLY=',tableViewport);
      
      if(tableViewport.length > 0 ){
        if(tableViewport.prev().is(CPANEL)) {
          $listenScroll = $listenScroll ? $listenScroll.add( tableViewport.prev() ) : tableViewport.prev();
          }

        if($el.parents(HASBANNER).length > 0) {
          $listenScroll = $listenScroll ? $listenScroll.add( $el.parents(HASBANNER) ) : $el.parents(HASBANNER);
          }

        var options = {
          "viewports": [tableViewport].concat(viewports$),  //new
          'listenScroll': $listenScroll,
          'injectCSS': false,
          'alwaysFloating': alwaysFloating,
          'alwaysShadowed': alwaysShadowed          
          };
        
        self.$el.children(TABLE).stickyTableHeaders(options)
        
      }
    },
    _render: function () {
        var self = this
        return this._super.apply(this, arguments).then(function(){
        // return this._super().then(function(){
            
          var lazyreflow = $.debounce(50, self.sticking_table_header.bind(self));
          
          // REGISTER RESIZE ON NEW CREATED ONLY
          var $table = self.$el.children('table:first')
          lazyreflow();
        });
    },
    
  });
    
// return true;    
});

