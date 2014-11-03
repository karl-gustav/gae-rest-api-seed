"use strict"

angular.module('app').config(function ($httpProvider) {
	$httpProvider.interceptors.push(function($window) {
		return {
			'responseError': function(rejection) {
				if (rejection.status == 401) {
				    $window.location.href = '/login?continue=' + escape($window.location.href)
				}
				return rejection;
			}
		};
	});
})
