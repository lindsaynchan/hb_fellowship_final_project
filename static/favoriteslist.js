angular.module("favoritesListings", ['ngRoute'])

    .config(function ($routeProvider) {
        $routeProvider

            .when('/all_favorites_listings', {
                templateUrl: '/static/favorite_listings.html',
                controller: 'ListingsController'
            })

            .when('/all_streaming', {
                templateUrl: '/static/favorites_streaming.html',
                controller: 'StreamingsController'
            });

    })

    .controller('ListingsController', function ($scope, $http) {

        $scope.isLoading = true;

        $http.get("/get_tv_listings")
        .then(function(response) {
            $scope.isLoading = false;
            $scope.shows = response.data;
        });

    })

    .controller('StreamingsController', function ($scope, $http) {

        $http.get("/all_streaming")
        .then(function(response) {
            $scope.streaming = response.data;
        });

});





