'use strict';

/* Services */

// Demonstrate how to register services
// In this case it is a simple value service.
var basic_inventory_serv = angular.module('smartbook.services', ['ngResource']);

basic_inventory_serv.value('version', '0.1');

basic_inventory_serv.factory('share', function()
{
    return {
        messages : {
            show : false,
            type : '',
            message : ''
        },
        loader : {
            show : false
        }
    };
});