(function (angular) {
  angular.module("tooltipster", []).directive('tooltipTarget', ['$compile', function ($compile) {
    return {
      restrict: 'A',
      scope: {
        tooltipTitle: '@',
        tooltipTarget: '@',
        tooltipContent: '='
      },
      link: function (scope, element, attrs) {

        // Set options for toolstipster
        scope.tooltipOptions = {};
        scope.tooltipOptions.theme = 'tooltipster-light';
        scope.tooltipOptions.contentAsHTML = true;
        scope.tooltipOptions.contentCloning = true;
        scope.tooltipOptions.side = 'bottom';
        scope.tooltipOptions.interactive = true;
        scope.tooltipOptions.delay = [250, 0]; // Delay of 250ms to show, 150ms to hide
        scope.tooltipOptions.functionAfter = function (instance, helper) {
          try {
            element.tooltipster('destroy');
          }
          catch (err) {
            //console.log('Tried to remove a hidden tooltip');
          }
        };

        // Receive broadcast when hide item for value changes
        scope.$on('setHideItemForValue', function (e, value) {
          //console.log('Get hide item for value: ' + value)
          scope.hideItemFor = value;
        });

        scope.tooltipOptions.functionBefore = function (instance, helper) {
          $compile(instance.__Content)(scope);

          scope.$apply();
        };

        // Only add the tooltip at the time of mouseover
        element.on('mouseenter', function () {

          if (element.hasClass("tooltipstered"))
            return;

          var tooltipOptions = scope.tooltipOptions || {};

          tooltipOptions.content = angular.element(scope.tooltipTarget);

          scope.$emit("getHideItemForValue", scope.tooltipContent);

          if (!scope.tooltipContent) {
            return;
          }

          if (scope.tooltipContent.pat_id1) {
            scope.$emit("activatePatient", scope.tooltipContent);
          } else if (scope.tooltipContent.chk_id) {
            scope.$emit("activateQCL", scope.tooltipContent);
          } else if (scope.tooltipContent.groupDescription) {
            scope.$emit("activateGroup", scope.tooltipContent);
          }

          scope.$apply();

          element.tooltipster(tooltipOptions);
          element.tooltipster('open');

        });

      }
    };
  }]);
})(angular);