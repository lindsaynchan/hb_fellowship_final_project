angular.module('showInformation', ['ngRoute'])
    
    .config(function ($routeProvider) {
        $routeProvider

            .when('/show_info', {
                templateUrl: '/static/show_info.html'
            })

            .when('/streaming', {
                templateUrl: '/static/streaming_info.html'
            })

            .when('/tv_listing', {
                templateUrl: '/static/tv_listing_info.html'
            });
    }
);
