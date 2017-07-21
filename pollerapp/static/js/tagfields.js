$(function() {
  $(document).on('click', '.btn-add', function(e) {
    console.log(e);
    console.log(this);

    e.preventDefault();

    // jquery selector selecting DOM element 'controls' and 'form' element that is child of that class with selector filter 'first'
    // a copy of currentEntry will be appended to this div as newEntry
    var controlForm = $('.controls form:first'),
      // this is the button object, here using parents() to select ancestors of this (the button) filtered by a selector, specifically getting the first DOM element ancestor of this (the button) of class 'entry'
      currentEntry = $(this).parents('.entry:first'),
      // create a new field by cloning currentEntry and append that to form element
      newEntry = $(currentEntry.clone()).appendTo(controlForm);

    newEntry.find('input').val('');
    controlForm.find('.entry:not(:last) .btn-add')
      .removeClass('btn-add').addClass('btn-remove')
      .removeClass('btn-success').addClass('btn-danger')
      .html('<span class="glyphicon glyphicon-minus"></span>');


    console.log("controlForm: ")
    console.log(controlForm)
    console.log("currentEntry: ")
    console.log(currentEntry)
    console.log("newEntry: ")
    console.log(newEntry)

  }).on('click', '.btn-remove', function(e) {
    $(this).parents('.entry:first').remove();

    e.preventDefault();
    return false;
  });
});


var tagsArray;
// Poll Twitter submit button
document.getElementById("submitTagsbtn").addEventListener("click",
  function(event) {

    $("#warningPanel").hide();
    $("#JSONdisplay").hide();
    $("#downloadJSON").html("");

    tagsArray = [];
    document.querySelectorAll('input').forEach(function(element) {
      if (element.value != '' && element.type != 'hidden') {
        tagsArray.push(element.value);
      }
    });
    console.log(tagsArray);
    console.log(tagsArray.length);
    if (tagsArray.length == 0) {
      $("#warningPanel").show();
      return null
    } else {
      var $this = $(this);
      $this.button('loading');
    }

    tagsPackage = JSON.stringify(tagsArray);
    pollTwitter(tagsPackage);
  }, false);


function pollTwitter(tagsPackage) {
  getCookie();
  var XHR = new XMLHttpRequest();
  XHR.open("POST", "/pollerapp/twitter-api/");
  XHR.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  XHR.setRequestHeader("X-CSRFToken", csrfToken);
  XHR.send(tagsPackage);
  XHR.onreadystatechange = function() {
    if (XHR.readyState == XMLHttpRequest.DONE && XHR.status == 200) {

      if (XHR.responseText !== "None") {
        document.getElementById("JSONdisplay").innerHTML = XHR.responseText;
        $('#JSONdisplay').show();

        var data = "text/json;charset=utf-8," + encodeURIComponent(XHR.responseText);
        $('<a href="data:' + data + '" download="TwitterPoller.json"><button type="button" class="btn btn-info">download JSON</button>').appendTo('#downloadJSON');
        $('<button type="button" class="btn btn-primary" onClick="window.open(&quot/static/JSONOutput/testoutput.json&quot);">get JSON URL</button>').appendTo('#downloadJSON');

        $('#submitTagsbtn').button('reset');

      } else {
        console.log(XHR.responseText);
      }
    } else {
      console.log(XHR.status);
    }
  }
}

var csrfToken;

function getCookie() {
  var name = 'csrftoken';
  var re = new RegExp(name + "=([^;]+)");
  var value = re.exec(document.cookie);
  //csrfToken = 'csrftoken=' + value[1];
  csrfToken = value[1];
}
