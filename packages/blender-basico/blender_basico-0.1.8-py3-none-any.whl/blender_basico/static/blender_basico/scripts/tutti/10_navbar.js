/* Show/Hide Navigation Bar on scroll
 * from http://jsfiddle.net/mariusc23/s6mLJ/31/
*/
var didScroll;
var lastScrollTop = 0;
var $navBar = $('nav.navbar-primary');
var navBarHeight = $navBar.outerHeight();

$(window).scroll(function(event){
	didScroll = true;
});

setInterval(function() {
	if (didScroll) {
		hasScrolled();
		didScroll = false;
	}
}, 250);

function hasScrolled() {
	var st = $(this).scrollTop();

	// Make sure they've scroll enough
	if(Math.abs(lastScrollTop - st) <= 5)
		return;

	// If they scrolled down and are past the navbar, add class .navbar-hidden.
	if (st > lastScrollTop && st > navBarHeight){
		// Scroll Down
		$('body').addClass('is-navbar-hidden');

		$navBar
			.removeClass('navbar-shown')
			.addClass('navbar-hidden');
	} else {
		// Scroll Up
		if(st + $(window).height() < $(document).height()) {

			$('body').removeClass('is-navbar-hidden');

			$navBar
				.removeClass('navbar-hidden')
				.addClass('navbar-shown');
		}
	}

	lastScrollTop = st;
}

/*
 * Add class to the body when the navbar is expanded.
 * This way we can style the whole page, menus, or to prevent the
 * navbar from being hidden on scroll on mobile.
 */
$('nav.navbar-primary').on('shown.bs.collapse', function () {
	$('body').addClass('is-navbar-expanded');
});

$('nav.navbar-primary').on('hidden.bs.collapse', function () {
	$('body').removeClass('is-navbar-expanded');
});
