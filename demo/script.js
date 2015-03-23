$(document).ready(function() {
  // Initialize template
  var genTextItem = Handlebars.compile($('#text-item-template').html());
  var genImageItem = Handlebars.compile($('#image-item-template').html());

  var container = '#content', $container = $(container), $window = $(window), $document = $(document);

  var wookmark = new Wookmark(container, {
    offset: 30,
    autoResize: true,
    verticalOffset:50
  });

  var loading = false;

  var dummyItem = {
    content: "在半个世纪的政治生涯里，李光耀带领新加坡在30年内发展成为亚洲最富裕繁荣的国家之一，被誉为“新加坡国父”，是20世纪最成功的政治家之一。而在对华关系上，他既是中国人民的老朋友，一些时候又令我们心情复杂。", 
    source: "Baidu",
    logo: "zhihu.png"
  };

  function retrieveItems(callback) {
    /*
    $.get("gimme/a/hug", function(items) {
      var newItems = [];
      for (var i = 0; i < items.length; i++) {
      }
    });
    */
    var newItems = [];
    for (var i = 0; i < 10; i++) {
      newItems[i] = genTextItem(dummyItem);
    }
    setTimeout(function(){callback(newItems);}, 2000);
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
          });
        });
      });
    }
  };
  
  // Capture scroll event.
  $window.bind('scroll.wookmark', onScroll);
});
