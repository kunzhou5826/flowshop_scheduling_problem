$(document).ready(function() {
  $("#nb_machines").change(function() {
    if ($("#algorithm").val() === "johnson") {
      if ($("#nb_machines") !== 2) {
        $("#nb_machines").val(2);
      }
    } else {
      if ($(this).val() <= 2) {
        $("#nb_machines").val(2);
      }
    }
  });

  $("#algorithm").change(function() {
    if ($(this).val() === "johnson") {
      $("#nb_machines").val(2);
    }
  });

  $("#solve").on("click", function() {
    $.ajax({
      url: "/solve",
      dataType: "json",
      type: "post",
      contentType: "application/json",
      data: JSON.stringify({
        algorithm: $("#algorithm").val(),
        data: $("#data").val(),
        nb_machines: $("#nb_machines").val(),
        nb_jobs: $("#nb_jobs").val()
      }),
      processData: false,
      success: function(data, textStatus, jQxhr) {
        Plotly.newPlot("gantt", JSON.parse(data["graph"]), {});
        $("#sequence").text(data["opt_seq"]);
        $("#opt_makespan").text(data["optim_makespan"]);
        var time_str = data["t_time"].toString() + " " + data["tt"].toString();
        $("#time").text(time_str);
      },
      error: function(jQxhr, textStatus, errorThrow) {
        console.log(textStatus);
      }
    });
  });
  $("#gen_random").on("click", function() {
    $.ajax({
      url: "/random",
      dataType: "text",
      type: "post",
      contentType: "application/json",
      data: JSON.stringify({
        nb_machines: $("#nb_machines").val(),
        nb_jobs: $("#nb_jobs").val()
      }),
      processData: false,
      success: function(data, textStatus, jQxhr) {
        $("#data").text(data);
      },
      error: function(jQxhr, textStatus, errorThrow) {
        alert("AJAX ERROR");
      }
    });
  });

  $("#gantt_toggle").click(function() {
    $("#gantt").fadeToggle();
  });
});
