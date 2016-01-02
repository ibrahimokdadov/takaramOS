$(function() {

   $('#title').editable({
            placement: "top",
            error: function (errors) {
            }
        });

   $('#description').editable({
            mode:"inline",
            placement: "right",
            error: function (errors) {
            }
        });

   $('#contact').editable({
            mode:"inline",
            placement: "right",
            error: function (errors) {
            }
        });



  });