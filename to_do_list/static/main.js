$(document).ready(function () {
    $('.state').click(function () {
        const state = $(this);
        const tID = state.data('source');
        const new_state;
        if (state.text() === "In Progress") {
            new_state = "Complete";
        } else if (state.text() === "Complete") {
            new_state = "Todo";
        } else if (state.text() === "Todo") {
            new_state = "In Progress";
        }

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
});

