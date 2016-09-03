/**
 * Created by L1n on 16/9/2.
 */
var initialize = function (navigator) {
    $("#id_login").on("click", function () {
        navigator.id.request();
    })
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};