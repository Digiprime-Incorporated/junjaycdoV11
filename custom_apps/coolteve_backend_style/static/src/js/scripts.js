$(document).ready(function() {
  $(".o_sub_menu_content").slimScroll({
    height: "100%"
  });

  // $.AdminLTE.tree('.sidebar-menu');
  var mySkins = [
    "skin-blue",
    "skin-black",
    "skin-red",
    "skin-yellow",
    "skin-purple",
    "skin-green",
    "skin-blue-light",
    "skin-black-light",
    "skin-red-light",
    "skin-yellow-light",
    "skin-purple-light",
    "skin-green-light"
  ];

  // $('body').addClass('skin-blue');
  function changeSkin(cls) {
    $.each(mySkins, function(i) {
      $("body").removeClass(mySkins[i]);
    });

    $("body").addClass(cls);
    // store("skin", cls);
    return false;
  }

  var skin_style = $.trim($("div.skin-style").text());
  changeSkin(skin_style);

  
});
