// Generated by CoffeeScript 1.8.0
(function() {
  $(document).ready(function() {
    return $(document).on('click', '.is-gone', function(e) {
      var form, img;
      form = $(this).closest('.thing').find('form');
      img = $(this).find('img');
      e.preventDefault();
      form.submit();
      return img.toggleClass('gone');
    });
  });

}).call(this);