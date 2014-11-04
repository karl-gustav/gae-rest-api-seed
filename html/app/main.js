"use strict"

angular.module('app', ['ngResource'])
    .factory('Item', function ($resource) {
        return $resource('/rest/items/:id', {id:'@id'}, {
            update: { method: 'PUT' }
        })

    })
    .controller('main', function ($scope, $http, $log, Item){
        $scope.newItem = new Item;

        Item.query(function (items) {
            $scope.items = items;
        }, $log.error);

        $scope.save = function () {
            $scope.newItem.$save(function (item) {
                $scope.items.push(item)
            }, $log.error);
            $scope.newItem = new Item;
        };

        $scope.toggle = function (item){
            item.checked = !item.checked;
            item.$update(function () {}, $log.error);
        };

        $scope.delete = function (index) {
            var item = $scope.items[index];
            item.$delete(function () {
                $scope.items.splice(index, 1);
            }, $log.error);
        };
    });

