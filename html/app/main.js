"use strict"

angular.module('app', []).controller('main', function ($scope, $http, $log){
    $scope.newItem = {};

    $http.get('/rest/items/')
        .success(function (items) {
            $scope.items = items;
        })
        .error($log.error)

    $scope.save = function () {
        $http.post('/rest/items/', $scope.newItem)
            .success(function (item) {
                $scope.items.push(item)
            })
            .error($log.error)
        $scope.newItem = {};
    };

    $scope.toggle = function (item){
        item.checked = !item.checked;
        $http.put('/rest/items/' + item.id, item).error($log.error)
    };

    $scope.delete = function (index) {
        var item = $scope.items[index];
        $http.delete('/rest/items/' + item.id)
            .success(function () {
                $scope.items.splice(index, 1);
            })
            .error($log.error)
    };
});

