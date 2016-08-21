// function setupModule() {
//     // $('input').on('click', function() {
//     //      $('.has-error').hide();
//     // });
//     $('input').on('keypress', function () {
//         $('.has-error').hide();
//     });
// }
//
// QUnit.module('tests', {setup: setupModule});

// $('input').on("keypress", function () { // 查找所有 input 元素，然后在找到的每个元素上附属一个事件监听器，作用在 keypress 事件上。事件监听器是那个行间函数，其作用是隐藏类为 .has-error 的所有元素
//     $('.has-error').hide();
// });
//
jQuery(document).ready(function ($) {
    // $('input[name="text"]').keypress(function () {
    //     $('.has-error').hide();
    // });
    //
    $('input[name="text"]').on('keypress', function () {
        $('.has-error').hide();
    });

    $('input[name="text"]').on('click', function () {
        $('.has-error').hide();

    });
});

var hide_error = function () {
    $('input').on("keypress", function () {
        $(".has-error").hide();
    });
};

QUnit.module("module A ", {
    before: hide_error
});