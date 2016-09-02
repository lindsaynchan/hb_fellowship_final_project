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

        $http.get("/get_random_gif")
        .then(function(response){
            $scope.isLoading = true;
            $scope.randomGif = response.data;
        });

        $http.get("/show_info?guidebox_id=" + guidebox_id)
        .then(function(response) {
            $scope.isLoading = false;
            $scope.show_info = response.data;
        });
        console.log($scope.show_info);

        $http.get("/seasons_info?guidebox_id=" + guidebox_id)
        .then(function(response) {
            $scope.isLoading = false;
            $scope.seasons_info = response.data;
        });
        console.log($scope.seasons_info);
    })

    .controller('StreamingController', function ($scope, $http) {

        $http.get("/get_random_gif")
        .then(function(response){
            $scope.isLoading = true;
            $scope.randomGif = response.data;
        });

        $http.get("/streaming?guidebox_id=" + guidebox_id)
        .then(function(response) {
            $scope.isLoading = false;
            $scope.streaming = response.data;
        });
    })

    .controller('TVListingController', function ($scope, $http) {

        $http.get("/get_random_gif")
        .then(function(response){
            $scope.isLoading = true;
            $scope.randomGif = response.data;
        });

        $http.get("/tv_listing?guidebox_id=" + guidebox_id)
        .then(function(response) {
            $scope.isLoading = false;
            $scope.listings = response.data;
            $scope.listingsExist = true;
            $scope.listingsDoNotExist = false;
            if (response.data.length <= 1) {
                $scope.listingsExist = false;
                $scope.listingsDoNotExist = true;
            }
        });
});




