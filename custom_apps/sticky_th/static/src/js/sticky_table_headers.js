function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
var startTime, endTime;

function start() {
  startTime = new Date();
};

function end(title) {
  endTime = new Date();
  var timeDiff = endTime - startTime; //in ms
  // strip the ms
  // timeDiff /= 1000;

  // get seconds 
  var seconds = Math.round(timeDiff);
  console.log(title || 'Stopwatch', seconds + " ms");
}


/*! Copyright (c) 2011 by Jonas Mosbech - https://github.com/jmosbech/StickyTableHeaders
  MIT license info: https://github.com/jmosbech/StickyTableHeaders/blob/master/license.txt */

;
(function($, window, undefined) {
  'use strict';

  function _boundingWidth($cell){
    var boundingClientRect = $cell[0].getBoundingClientRect();
    if (boundingClientRect.width) {
      return boundingClientRect.width; // #39: border-box bug
    } else {
      return boundingClientRect.right - boundingClientRect.left; // ie8 bug: getBoundingClientRect() does not have a width property
    }
  }
  
  function _computedStyleWidth($cell){
      return width = parseFloat(window.getComputedStyle($cell[0], null).width);
  }
  function _ie8Width($cell){
      // ie8 only
        var leftPadding = parseFloat($cell.css('padding-left'));
        var rightPadding = parseFloat($cell.css('padding-right'));
        // Needs more investigation - this is assuming constant border around this cell and it's neighbours.
        var border = parseFloat($cell.css('border-width'));
        return $cell.outerWidth() - leftPadding - rightPadding - border;
  }
  function _cellWidth($cell){
      return $cell.width()
  }
  // function _boundingWidth($cell){}
  // function _boundingWidth($cell){}
  // function _boundingWidth($cell){}
  
  var name = 'stickyTableHeaders',
    id = 0,
    defaults = {
      fixedOffset: 0,
      cellResize: true,
      leftOffset: 0,
      marginTop: 0,
      objDocument: document,
      objHead: 'head',
      objWindow: window,
      // scrollableArea: window,
      cacheHeaderHeight: false,
      alwaysFloating: false,
      alwaysShadowed: false,
      injectCSS: true,
      $leftStatic: [], //fake $().
      $fistLeft: false,
      stickyMergedCols: false, // only applicable in grouped th aka colspan= greater than 1
      cssClass: 'sticky-TH sticky-0-TH',
      cssClassClone: 'sticky-TH clonned-TH',
      cssClassFloating: 'floating-TH'
    };

  function Plugin(el, options) {
    // To avoid scope issues, use 'base' instead of 'this'
    // to reference this class from internal events and functions.
    var base = this;

    // Access to jQuery and DOM versions of element
    base.$el = $(el);
    base.el = el;
    base.id = id++;
    base.isListView = false;

    // Listen for destroyed, call teardown
    base.$el.bind('destroyed',
      $.proxy(base.teardown, base));

    // Cache DOM refs for performance reasons
    base.$clonedHeader = null;
    base.$originalHeader = null;

    // Cache header height for performance reasons
    base.cachedHeaderHeight = null;

    // Keep track of state
    base.isSticky = false;
    base.hasBeenSticky = false;
    base.leftOffset = null;
    base.topOffset = null;
    base.$viewports = null;

    base.init = function() {
      base.setOptions(options);

      // base.$el.each(function () {
      // var $this = $(this);
      var $this = base.$el;

      // remove padding on <table> to fix issue #7
      $this.css('padding', 0);

      // base.$originalHeader = $('thead:first', this);
      base.$originalHeader = $('thead:first', base.$el);
      base.$clonedHeader = base.$originalHeader.clone();
      $this.trigger('clonedHeader.' + name, [base.$clonedHeader]);

      base.$clonedHeader.addClass(base.options.cssClassClone);
      // base.$clonedHeader.css({display: 'none', opacity: 0.0});
      base.$clonedHeader.css({
        opacity: 0.0
      });

      base.$originalHeader.addClass(base.options.cssClass);
      base.$originalHeader.css({ /*'background': getRandomColor(), */
        position: 'absolute',
        right: 0,
        top: 0,
        left: 0
      })

      base.$originalHeader.after(base.$clonedHeader);
      
      //merged th
      base.$mergeHeaderCells = base.options.stickyMergedCols ? base.$originalHeader.find("th[colspan]").filter("th[colspan!='1']") : $();
      

      if (base.options.injectCSS) {
        base.$printStyle = $('<style type="text/css" id="sticky-css-' + base.id + '" name="stickyheader-css" media="print">' +
          // '.tableFloatingHeader{display:none !important;}' +
          // '.'+base.options.cssClass+'{position:static !important;}' +
          '.' + base.options.cssClass + '{position:absolute !important; right:0, top:0, left:0}' +
          '</style>');
        base.$head.append(base.$printStyle);
      };

      base.toggleHeaders();
      base.bind();

    };

    base.thResize = function() {
        // start();
      var
        $th = $(this), 
        $pair = $th.data().sticky_table_pair,
        width;
        //get width
        if($pair && $pair.length > 0){
            width = base.globalGetWidth($th)
        } else{
            
            // do old way whichis lambreta
                
                // window.setTimeout(function(bar){
            var
                // index = $th.index(),
                // $pair = base.$originalHeaderCells.eq(index),
                pindex = $th.parent().index(),
                index = $th.index(),
                // $pair = base.$originalHeader.eq(pindex).eq(index)
                $pair = base.$originalHeader.find('tr:nth-child('+(pindex+1)+')').find('td,th').eq(index)
              // end('var thResize:')  

              if (!$pair[0].style['min-width'] || ($th.width() != $pair.width())) {
                  // start()
                var width = base.getCellWidth($th)
                    // end('getcellwiddth')
                }

        }
        $pair.css({
          'min-width': width,
          'max-width': width
        });
        // },1)
        // def.resolve(true)
    };

    base.destroy = function() {
      base.$el.unbind('destroyed', base.teardown);
      base.teardown();
    };

    base.teardown = function() {
      if (base.isSticky) {
        base.$originalHeader.css('position', 'static');
      }
      $.removeData(base.el, 'plugin_' + name);
      base.unbind();

      base.$clonedHeader.remove();
      base.$originalHeader.removeClass(base.options.cssClass);
      base.$originalHeader.css('visibility', 'visible');
      if (base.options.injectCSS && base.$printStyle) {
        base.$printStyle.remove();
      }

      base.el = null;
      base.$el = null;
    };

    base.bind = function() {
        var self = this;
      // base.$scrollableArea.on('scroll.' + name, base.toggleHeaders);
      base.$viewports.on('scroll.' + name, base.toggleHeaders);
      start()
      base.$listenScroll.on('mresize.' + name, base.toggleHeaders);
      end('on-mreseize')
      
      base.$listenScroll.on('scroll.' + name, base.toggleHeaders);
      if (!base.isWindowScrolling) {
        base.$window.on('scroll.' + name + base.id, base.setPositionValues);
        base.$window.on('resize.' + name + base.id, base.toggleHeaders);
        base.$viewports.on('mresize.' + name, base.toggleHeaders);
      }
      

      base.$originalHeaderLastCells = base.$originalHeader.find('tr:last-child>th, tr:last-child>td');
      base.$clonedHeaderLastCells = base.$clonedHeader.find('tr:last-child>th, tr:last-child>td');
      
      base.$originalHeaderCells = $('th,td', base.$originalHeader);
      // console.log('cell-count=',base.$originalHeaderCells.length)
      base.$clonedHeaderCells = $('th,td', base.$clonedHeader);
      //setup
      base.setupPairs(base.$clonedHeaderCells, base.$originalHeaderCells);
      if(base.options.cellResize) {
          
            base.$clonedHeaderCells.on('mresize.' + name, base.thResize);

            //new 2019-02-05 x2nie
            // start()
            // base.setupPairs(base.$clonedHeaderCells, base.$originalHeaderCells);
            // end('setup-mresize')

            start()
            base.$clonedHeaderCells.trigger('mresize')
            // base.$clonedHeaderCells.triggerHandler('mresize')
            end('trigger-mresize')
      } else {
            // not automatically resize? at least first cell in header is correct
            // if(base.options.$fistLeft){
                // base.setupPairs(base.$clonedHeaderCells, base.$originalHeaderCells); //set globalGetWidth
                
                // 1st
                var $td1 = base.$clonedHeaderCells.first();
                $td1.on('mresize.' + name, function(){
                    var width = base.globalGetWidth($td1);
                    base.$originalHeaderCells.first().css({
                      'min-width': width,
                      'max-width': width
                    });
                    
                    if(base.options.$leftStatic.length > 0){
                        base.options.$leftStatic.css({
                          'min-width': width
                          // 'max-width': width
                        });
                    };
                });
                $td1.trigger('mresize.' + name); //do now!
                
                // last                
                /*var $td2 = base.$clonedHeaderCells.last();
                $td2.on('mresize.' + name, function(){
                    var width = base.globalGetWidth($td2);
                    base.$originalHeaderCells.last().css({
                      'min-width': width,
                      'max-width': width
                    });
                });
                $td2.trigger('mresize.' + name); //do now!
                */
                base.$originalHeaderLastCells.each(function(index){
                    var $ori = $(base.$originalHeaderLastCells[index]);
                    var $clone = $(base.$clonedHeaderLastCells[index]);
                    var width = base.globalGetWidth($clone);
                    $ori.css({
                      'min-width': width,
                      'max-width': width
                    });
                })
                // base.$clonedHeaderLastCells = base.$clonedHeader.find('tr:last-child>th, tr:last-child>td');

            // }
            if(base.options.$fistLeft0){
                base.setupPairs(base.$clonedHeaderCells, base.$originalHeaderCells); //set globalGetWidth
                // var $th = base.$el.find('tbody)
                var width = base.globalGetWidth(base.options.$fistLeft);
                base.$originalHeaderCells.first().css({
                  'min-width': width,
                  'max-width': width
                });
          }
      }
      //merged th
      base.$mergeHeaderCells.each(function(){
          // return;
          var $th = $(this);
          // $th.parent().css('height', $th.parent().css('height') );
          // $th.css('height', $th.css('height') );
          
          //calculate max-width
          // $th.data('max-width', $th.css('width') );
          $th.data('max-width', base.globalGetWidth($th) );
          
          
          $th.data('inner-width', $th.width() );
          $th.data('padding-left', parseInt($th.css('padding-left')) );
          $th.data('padding-right', parseInt($th.css('padding-right')) );
          
          //calculate min-width
          $th.css('position', 'absolute' );
          $th.data('min-width', parseInt($th.css('width')) );
          $th.css({'position':'initial'/*, 'width': $th.data('max-width')*/ });
          
          // $th.text( $th.width() +'spanleft:'+$th.css('padding-left') +' spanright:'+$th.css('padding-right') )
      })
    };
    
    base.setupPairs = function($clonedHeaders, $origHeaders) {
        var $cell = $origHeaders.eq(0),
            fn;
        // I assumed that all cell has similar style, so I am checking once and apply to all
          if ($cell.css('box-sizing') === 'border-box') {
            fn = _boundingWidth
          } else {
            var $origTh = $('th:first,td:first', base.$originalHeader);
            if ($origTh.css('border-collapse') === 'collapse') {
              if (window.getComputedStyle) {
                // width = parseFloat(window.getComputedStyle($cell[0], null).width);
                fn = _computedStyleWidth
              } else {
                fn = _ie8Width ;
                /*
                // ie8 only
                var leftPadding = parseFloat($cell.css('padding-left'));
                var rightPadding = parseFloat($cell.css('padding-right'));
                // Needs more investigation - this is assuming constant border around this cell and it's neighbours.
                var border = parseFloat($cell.css('border-width'));
                width = $cell.outerWidth() - leftPadding - rightPadding - border;
                */
              }
            } else {
              // width = $cell.width();
              fn = _cellWidth
            }
      }
      base.globalGetWidth = fn;
      
      if(base.options.cellResize) {
          
        $origHeaders.each(function(index) {
            // var $cell = $origHeaders.eq(index);
            var $cell = $(this);
            var $pair = $clonedHeaders.eq(index);
            
            $pair.data('sticky_table_pair', $cell)
            
            
        });
      };
    };

    base.unbind = function() {
      // unbind window events by specifying handle so we don't remove too much
      base.$viewports.off('.' + name, base.toggleHeaders);
      base.$listenScroll.off('.' + name, base.toggleHeaders);
      if (!base.isWindowScrolling) {
        base.$window.off('.' + name + base.id, base.setPositionValues);
        base.$window.off('.' + name + base.id, base.toggleHeaders);
      }
      base.$clonedHeaderCells.off('.' + name, base.thResize);
    };

    base.debounce = function(fn, delay) {
      return $.throttle(delay, fn);
    };

    base.toggleHeaders = base.debounce(function() {
      if (base.$el) {
        //reset        
        var i = 0,
          x = base.viewports.length,
          // $viewport = $(base.viewports[0]);
          $viewport = null;
        // var overflow = $viewport.css('overflow'); //TODO: shall be 'overflow-y'
        var overflow = null;
        while ((!overflow || overflow == 'visible') && (i < x)) {
          $viewport = $(base.viewports[i]);
          overflow = $viewport.css('overflow');
          i++;
        }
        if (!overflow || overflow == 'visible') { //scrollbar still not detected?
          $viewport = $(base.viewports[0]);
          overflow = $viewport.css('overflow');
          while ($viewport.length && (!overflow || overflow == 'visible')) {
            $viewport = $viewport.parent();
            if ($viewport[0] == window || $viewport.is('body')) //here, body|window is always has scrollbar.
              break;
            overflow = $viewport.css('overflow');
          }
        }

        if (!$viewport || !$viewport.length) {
          console.log('premateur exit: no viewport')
          return;
        }

        //viewport is maybe a new created by theme. eg.: suddenly overflow=visible on small screen
        //so, take care the scroll
        if (!base.$viewports.filter($viewport).length) { // not a member?
          $viewport.on('scroll.' + name, base.toggleHeaders)
          base.$viewports = base.$viewports.add($viewport) //set as member
        }

        base.$currentViewport = $viewport; //UPDATE.
        // --------------------------------------------------
        var $this = base.$el,
          newLeft,
          newTopOffset = base.isWindowScrolling ? (
            isNaN(base.options.fixedOffset) ?
            base.options.fixedOffset.outerHeight() :
            base.options.fixedOffset
          ) :
          $viewport.offset().top + (!isNaN(base.options.fixedOffset) ? base.options.fixedOffset : 0),
          offset = $this.offset(),

          scrollTop = $viewport.scrollTop() + newTopOffset,
          scrollLeft = $viewport.scrollLeft(),

          headerHeight = base.options.cacheHeaderHeight ? base.cachedHeaderHeight : base.$clonedHeader.height(),

          autoFloating = base.options.alwaysFloating && (newTopOffset >= offset.top),

          scrolledPastTop = base.isWindowScrolling ?
          scrollTop > offset.top :
          newTopOffset > offset.top,
          notScrolledPastBottom = (base.isWindowScrolling ? scrollTop : 0) <
          (offset.top + $this.height() - headerHeight - (base.isWindowScrolling ? 0 : newTopOffset));

        // console.log('top=', newTopOffset);
        if ((autoFloating || scrolledPastTop) && notScrolledPastBottom) {
          var po = $this.offsetParent().offset();
          //newTopOffset += (offset.top - po.top);

          newLeft = offset.left /*- scrollLeft*/ + base.options.leftOffset;
          // console.log('~@! stick offset.left=',offset.left,' - scrollLeft=',scrollLeft);

          // SHOW FLOATING : show shadow if past-top or force shadow
          base.$originalHeader.toggleClass(base.options.cssClassFloating, base.options.alwaysShadowed || scrolledPastTop);

          base.$originalHeader.css({
            // base.$originalHeader.addClass(base.options.cssClassFloating).css({
            'position': 'fixed',
            'margin-top': base.options.marginTop,
            'right': 'auto',
            //'left': newLeft,
            'z-index': base.$el.zIndex() + 3
          });
          base.leftOffset = newLeft;
          base.topOffset = newTopOffset;
          // base.$clonedHeader.css('display', '');
          if (!base.isSticky) {
            base.isSticky = true;
            // make sure the width is correct: the user might have resized the browser while in static mode
            // base.updateWidth();
            $this.trigger('enabledStickiness.' + name);
          }
          base.setPositionValues();
        } else if (base.isSticky) {
          // base.$originalHeader.css('position', 'static');
          base.$originalHeader.css({
            'position': 'absolute',
            'right': 0,
            'top': 0,
            'left': 0,
            'clip': 'auto'
          }).removeClass(base.options.cssClassFloating);
          // base.$clonedHeader.css('display', 'none');
          base.isSticky = false;
          //base.resetWidth($('td,th', base.$clonedHeader), $('td,th', base.$originalHeader));
          $this.trigger('disabledStickiness.' + name);
        }
      }
    }, 25);

    // base.setPositionValues = base.debounce(function () {
    base.setPositionValues = function() {
      var winScrollTop = base.$window.scrollTop(),
        winScrollLeft = base.$window.scrollLeft();
      if (!base.isSticky ||
        winScrollTop < 0 || winScrollTop + base.$window.height() > base.$document.height() ||
        winScrollLeft < 0 || winScrollLeft + base.$window.width() > base.$document.width()) {
        return;
      }
      var
        clipleft = base.$currentViewport.offset().left - base.leftOffset,
        clipright = clipleft + base.$currentViewport.prop("clientWidth"), // El. width minus scrollbar width,
        ckuo = 'rect(0px,' + clipright + 'px,200px,' + clipleft + 'px)';
      base.$originalHeader.css({
        'top': base.topOffset - (base.isWindowScrolling ? 0 : winScrollTop),
        'left': base.leftOffset - (base.isWindowScrolling ? 0 : winScrollLeft),
        'clip': ckuo
      });
      
      //merged th
      base.$mergeHeaderCells.each(function(i){
          var $th = $(this);
          // $th.css('background-color', 'yellow');
          if(!$th.text()) return;
          
          var left = $th.offset().left;
          var width = $th.data('max-width');
          if(!width)
            return;
          // console.log(i,$th.parent().index(), $th.index(),  $th.text(), left, width  )
          
          var padl = $th.data('padding-left');
          var newPadL = undefined;
          
          if($th.is('.o_pivot_header_cell_closed') || left >= 0){
              // $th.css('padding-left', $th.data('padding-left'))
              newPadL = padl;
          } else {
              //sticky merged th. show offscreen text
              // var width = 
              // if(left<0){
                  // var inner = $th.data('inner-width');
                  var inner = $th.data('min-width');
                  var xleft = -left;
                  // padl = parseInt($th.data('padding-left'));
                  var padr = $th.data('padding-right');
                  // width += left; // width = width - -left;
                  var rightAlignedSpanLeft = (width - padr) - inner;
                  // var leftAlignedSpanLeft = (width - xleft) + padl + xleft;
                  var leftAlignedSpanLeft = xleft + padl ;
                  // var space = $th.data('inner-width') 
                  newPadL = (leftAlignedSpanLeft + inner + padr) < width ? leftAlignedSpanLeft : rightAlignedSpanLeft;
              // }              
          }
          if(newPadL != parseInt($th.css('padding-left')))
            $th.css('padding-left', newPadL)
          // console.log('change:',$th.parent().index(), $th.index(),  $th.text(), newPadL )
          // $th.parent().css('height', $th.parent().css('height') );
          // $th.css('height', $th.css('height') );
          
          //calculate max-width
          // $th.data('max-width', $th.css('width') );
          // $th.data('max-width', base.globalGetWidth($th) );
          
          //calculate min-width
          // $th.css('position', 'absolute' );
          // $th.data('min-width', $th.css('width') );
          // $th.css({'position':'initial'/*, 'width': $th.data('max-width')*/ });
          
          // $th.text( $th.width() )
      });

      
      // left sidebar
      if(base.options.$leftStatic.length > 0){
          base.options.$leftStatic.css({
                    'left': base.$currentViewport.scrollLeft() +1 //$(this).scrollLeft() + 15 //Why this 15, because in the CSS, we have set left 15, so as we scroll, we would want this to remain at 15px left
                });
      }
    }

    base.getCellWidth = function($cell) {
      var width;

      if ($cell.css('box-sizing') === 'border-box') {
        var boundingClientRect = $cell[0].getBoundingClientRect();
        if (boundingClientRect.width) {
          width = boundingClientRect.width; // #39: border-box bug
        } else {
          width = boundingClientRect.right - boundingClientRect.left; // ie8 bug: getBoundingClientRect() does not have a width property
        }
      } else {
        var $origTh = $('th', base.$originalHeader);
        if ($origTh.css('border-collapse') === 'collapse') {
          if (window.getComputedStyle) {
            width = parseFloat(window.getComputedStyle($cell[0], null).width);
          } else {
            // ie8 only
            var leftPadding = parseFloat($cell.css('padding-left'));
            var rightPadding = parseFloat($cell.css('padding-right'));
            // Needs more investigation - this is assuming constant border around this cell and it's neighbours.
            var border = parseFloat($cell.css('border-width'));
            width = $cell.outerWidth() - leftPadding - rightPadding - border;
          }
        } else {
          width = $cell.width();
        }
      }

      return width;
    };

    base.setOptions = function(options) {
      base.options = $.extend({}, defaults, options);
      base.viewports = base.options.viewports || [];
      $.each(base.viewports, function(index, value) {
        base.$viewports = base.$viewports ? base.$viewports.add($(value)) : $(value);
      });

      base.$window = $(base.options.objWindow);
      base.$head = $(base.options.objHead);
      base.$document = $(base.options.objDocument);
      base.$currentViewport = $(base.viewports[0]); //here because setPositionValues() maybe called before toggleHeader
      base.$listenScroll = $(base.options.listenScroll);
    };

    base.updateOptions = function(options) {
      base.setOptions(options);
      // scrollableArea might have changed
      base.unbind();
      base.bind();
      // base.updateWidth();
      base.toggleHeaders();
    };

    // Run initializer
    base.init();
  }

  // A plugin wrapper around the constructor,
  // preventing against multiple instantiations
  $.fn[name] = function(options) {
    return this.each(function() {
      var instance = $.data(this, 'plugin_' + name);
      if (instance) {
        if (typeof options === 'string') {
          instance[options].apply(instance);
        } else {
          instance.updateOptions(options);
        }
      } else if (options !== 'destroy') {
        $.data(this, 'plugin_' + name, new Plugin(this, options));
      }
    });
  };

})(jQuery, window);