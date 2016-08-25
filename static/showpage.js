angular.module("showInformation", ['ngRoute'])

    .config(function ($routeProvider) {
        $routeProvider

            .when('/show_info', {
                templateUrl: '/static/show_info.html',
                controller: 'ShowInfoController'
            })

            .when('/streaming', {
                templateUrl: '/static/streaming_info.html',
                controller: 'StreamingController'
            })

            .when('/tv_listing', {
                templateUrl: '/static/tv_listing_info.html',
                controller: 'TVListingController'
            })

            .otherwise ({
                redirectTo: '/show_info'
            });
    })

    .controller('ShowInfoController', function ($scope, $http) {

        $http.get("/show_info?guidebox_id=" + guidebox_id)
        .then(function(response) {
            $scope.show_info = response.data;
        });
        console.log($scope.show_info);



        $http.get("/seasons_info?guidebox_id=" + guidebox_id)
        .then(function(response) {
            $scope.seasons_info = response.data;
        });
        console.log($scope.seasons_info);
    })

    .controller('StreamingController', function ($scope, $http) {

        $http.get("/streaming?guidebox_id=" + guidebox_id)
        .then(function(response) {
            $scope.streaming = response.data;
        });
    })

    .controller('TVListingController', function ($scope, $http) {

        $http.get("/tv_listing?guidebox_id=" + guidebox_id)
        .then(function(response) {
            $scope.listings = response.data;
        });
});





