$(".wrapper-img").click(function () {
    let categoryid = parseInt($(".cart-title").attr("id"));
    let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
       type: "POST",
       url: "/products/",
       data: {
           cats:categoryid,
           csrfmiddlewaretoken: csrftoken,
       },
       dataType: "json",
    });
});