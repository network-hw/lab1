$(document).ready(function() {
  // Initialize template
  var genItem = Handlebars.compile($('#item-template').html());

  var container = '#content', $container = $(container), $window = $(window), $document = $(document);

  var wookmark = new Wookmark(container, {
    offset: 30,
    autoResize: true,
    verticalOffset:50
  });

  var loading = false;

  function retrieveItems(callback) {
    $.get("/gimme_a_hug", function(items) {
      items = eval(items);
      var newItems = [];
      for (var i = 0; i < items.length; i++) {
        newItems[i] = genItem(items[i]);
      }
      callback(newItems);
    });
  };

  function onScroll() {
    // Check if we're within 100 pixels of the bottom edge of the broser window.
    var winHeight = window.innerHeight ? window.innerHeight : $window.height(), // iphone fix
    closeToBottom = ($window.scrollTop() + winHeight > $document.height() - 100);

    if (closeToBottom && !loading) {
      loading = true;
      $('#loading').fadeIn(500);
      retrieveItems(function(newItems) {

        $container.append(newItems);
        var newItemsRef = $('.new-item', $container);
        wookmark.initItems();

        wookmark.layout(true, function () {
          loading = false;
          $('#loading').fadeOut(300);
          $(newItemsRef).animate({'opacity': 1}, 1000, function() {
            $(newItemsRef).removeClass('new-item');
            wookmark.initItems();
            wookmark.layout(true);
          });
        });
      });
    }
  };
  
  // Capture scroll event.
  $window.bind('scroll.wookmark', onScroll);
});
