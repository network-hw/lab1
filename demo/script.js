$(document).ready(function() {
  var container = '#content', $container = $(container), $window = $(window), $document = $(document);

  var wookmark = new Wookmark(container, {
    offset: 30,
    autoResize: true,
    verticalOffset:50
  });

  function onScroll() {
    // Check if we're within 100 pixels of the bottom edge of the broser window.
    var winHeight = window.innerHeight ? window.innerHeight : $window.height(), // iphone fix
    closeToBottom = ($window.scrollTop() + winHeight > $document.height() - 100);

    // dummy logic, endless scroll
    if (closeToBottom) {
      // Get the first then items from the grid, clone them, and add them to the bottom of the grid
      var $items = $('.item', $container),
      $firstTen = $items.slice(0, 10).clone().css('opacity', 0);
      $container.append($firstTen);
      wookmark.initItems();
      wookmark.layout(true, function () {
        // Fade in items after layout
        setTimeout(function() {
          $firstTen.css('opacity', 1);
        }, 300);
      });
    }
  };
  
  // Capture scroll event.
  $window.bind('scroll.wookmark', onScroll);
});
