(function($, window) {

  if ($('#tags_field').length) {
    $('#tags_field').select2({
        tags: true
      });
  }

}).call(this, jQuery, window);
