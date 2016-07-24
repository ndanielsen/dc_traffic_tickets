/* Project specific Javascript goes here. */

(function($) {

  // Do the CSRf AJAX Modification
  var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});

  // Update the status and the version from the API.
  var statusURL = "/api/v1/status/?format=json";
  $.get(statusURL)
    .success(function(data) {

      if (data.status == "ok") {
        $("#footerStatus").text('Up and Running');
      } else {
        $("#footerStatus").text('Error');
      }
    })
    .fail(function() {
      $("#footerStatus").text('Error');
    });

  console.log("Traffic App is started and ready");

})(jQuery);
