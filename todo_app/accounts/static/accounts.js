/**
 * Created by L1n on 16/9/2.
 */
var initialize = function (navigator, user, token, urls) {
    $("#id_login").on("click", function () {
        navigator.id.request();
    });

    navigator.id.watch({
        loggedInUser: user,
        onlogin: function (assertion) {
            var deferred = $.post(
                urls.login,
                {assertion: assertion, csrfmiddlewaretoken: token}
            );

            deferred.done(function () {
                window.location.reload();
            });
            deferred.fail(function () {
                navigator.id.logout();
            });
            /* 下面写法等价, 只是看着混乱了一些
             $.post(urls['login'], {assertion: assertion, csrfmiddlewaretoken: token}
             ).done(function () {
             window.location.reload();
             }).fail(function () {
             navigator.id.logout();
             });
             */
        },
        onlogout: function (assertion) {
            $.post(urls["logout"]);
        }
    });
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};