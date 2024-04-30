mainMenu = document.getElementsByClassName("oe_application_menu_placeholder");

aLi = document.createElement("li");
anA = document.createElement("a");
anA.setAttribute("id", "toggle_sidebar_btn");

anI = document.createElement("i");
anI.setAttribute("class", "fa fa-bars");
anA.appendChild(anI);
aLi.appendChild(anA);

// anA.onclick = function() {
// 	sideBar = document.getElementsByClassName("o_sub_menu")[0];

// 	if (!sideBar.classList.contains('hide')){
// 		sideBar.classList.add('hide');
// 	}else{
// 		sideBar.classList.remove('hide');
// 	}
// };

window.onload = function() {
  mainMenu = mainMenu[0];
  mainMenu.insertBefore(aLi, mainMenu.firstChild);
};

$(document).ready(function() {
  $(document).on("click", "#toggle_sidebar_btn", function() {
    sideBar = $(".o_sub_menu");
    if (sideBar.is(":visible")) {
      sideBar.fadeOut(500, function() {
        sideBar.css("display", "none");
      });
    } else {
      sideBar.fadeIn(500, function() {
        sideBar.css("display", "flex");
      });
    }
    // alert('On Loaded six');
    //   alert("token");
    //   sidebar = $(".oe_application_menu_placeholder");
    //   toggleMenu = $("<li>");
    //   toggleMenu.append(
    //     $("<a>")
    //       .setAttr("id", "toggle_sidebar_btn")
    //       .append($("<i>").addClass("fa fa-bars"))
    //   );
    // // $(".o_sub_menu").animate(
    // //   {
    // //     width: "toggle"
    // //   },
    // //   "slow"
    // // );
    // // $(".o_sub_menu").animate({ width: "toggle" });
    // sideBar.toggle("slow", function(){
    // 	if(sideBar.is(":visible")){
    // 		// alert("The paragraph  is visible.");
    // 	} else{
    // 		// alert("The paragraph  is hidden.");
    // 	}
    // });
    // // sideBar.toggle(function(){
    // // 	$('.o_sub_menu').animate({width:0});
    // // 	$('.o_main_content').animate({left:0});
    // // },function(){
    // // 	$('.o_sub_menu').animate({width:220});
    // // 	$('.o_main_content').animate({left:220});
    // // 	// $('#A').animate({width:200});
    // // 	// $('#B').animate({left:200});
    // // });
  });
});
