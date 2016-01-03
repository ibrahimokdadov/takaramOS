$(function() {

   $('#x-title').editable({
            placement: "top",
            error: function (errors) {
            }
        });

   $('#x-description').editable({
            mode:"inline",
            placement: "right",
            error: function (errors) {
            }
        });

   $('#x-contact').editable({
            mode:"inline",
            placement: "right",
            error: function (errors) {
            }
        });



  });