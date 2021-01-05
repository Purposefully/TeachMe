$(function () {
    $("[name='search']").on("keyup", function () {
        let form_data = $("#library_search").serialize()
        $.ajax({
            url: "/library_search",
            method: "POST",
            data: form_data,
        }).done(function (res) {
            $("#library_cards").html(res)
        })
    })

    $("#library_search").on("submit", function (e) {
        e.preventDefault()
    })
})
