(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_test"] = factory(require("react"));
	else
		root["dazzler_test"] = factory(root["React"]);
})(window, function(__WEBPACK_EXTERNAL_MODULE_react__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"test": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	var jsonpArray = window["webpackJsonpdazzler_name_"] = window["webpackJsonpdazzler_name_"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push([2,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/internal/test_components/components/ComponentAsAspect.jsx":
/*!***********************************************************************!*\
  !*** ./src/internal/test_components/components/ComponentAsAspect.jsx ***!
  \***********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return ComponentAsAspect; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }




var ComponentAsAspect =
/*#__PURE__*/
function (_React$Component) {
  _inherits(ComponentAsAspect, _React$Component);

  function ComponentAsAspect() {
    _classCallCheck(this, ComponentAsAspect);

    return _possibleConstructorReturn(this, _getPrototypeOf(ComponentAsAspect).apply(this, arguments));
  }

  _createClass(ComponentAsAspect, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          identity = _this$props.identity,
          single = _this$props.single,
          array = _this$props.array,
          shape = _this$props.shape;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        id: identity
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "single"
      }, single), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "array"
      }, array.map(function (e, i) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
          key: i
        }, e);
      })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "shape"
      }, shape.shaped));
    }
  }]);

  return ComponentAsAspect;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


ComponentAsAspect.defaultProps = {};
ComponentAsAspect.propTypes = {
  single: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.element,
  array: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.element),
  shape: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
    shaped: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.element
  }),

  /**
   *  Unique id for this component
   */
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Update aspects on the backend.
   */
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/internal/test_components/components/DefaultProps.jsx":
/*!******************************************************************!*\
  !*** ./src/internal/test_components/components/DefaultProps.jsx ***!
  \******************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return DefaultProps; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }




var DefaultProps =
/*#__PURE__*/
function (_Component) {
  _inherits(DefaultProps, _Component);

  function DefaultProps() {
    _classCallCheck(this, DefaultProps);

    return _possibleConstructorReturn(this, _getPrototypeOf(DefaultProps).apply(this, arguments));
  }

  _createClass(DefaultProps, [{
    key: "render",
    value: function render() {
      var id = this.props.id;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        id: id
      }, Object.entries(this.props).map(function (k, v) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
          id: "".concat(id, "-").concat(k),
          key: "".concat(id, "-").concat(k)
        }, k, ": ", JSON.stringify(v));
      }));
    }
  }]);

  return DefaultProps;
}(react__WEBPACK_IMPORTED_MODULE_0__["Component"]);


DefaultProps.defaultProps = {
  string_default: 'Default string',
  string_default_empty: '',
  number_default: 0.2666,
  number_default_empty: 0,
  array_default: [1, 2, 3],
  array_default_empty: [],
  object_default: {
    foo: 'bar'
  },
  object_default_empty: {}
};
DefaultProps.propTypes = {
  id: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  string_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  string_default_empty: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  number_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  number_default_empty: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  array_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,
  array_default_empty: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,
  object_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  object_default_empty: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object
};

/***/ }),

/***/ "./src/internal/test_components/components/TestComponent.jsx":
/*!*******************************************************************!*\
  !*** ./src/internal/test_components/components/TestComponent.jsx ***!
  \*******************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return TestComponent; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }




/**
 * Test component with all supported props by dazzler.
 * Each prop are rendered with a selector for easy access.
 */

var TestComponent =
/*#__PURE__*/
function (_Component) {
  _inherits(TestComponent, _Component);

  function TestComponent() {
    _classCallCheck(this, TestComponent);

    return _possibleConstructorReturn(this, _getPrototypeOf(TestComponent).apply(this, arguments));
  }

  _createClass(TestComponent, [{
    key: "render",
    value: function render() {
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        id: this.props.id
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "array"
      }, this.props.array_prop && JSON.stringify(this.props.array_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "bool"
      }, Object(ramda__WEBPACK_IMPORTED_MODULE_2__["isNil"])(this.props.bool_prop) ? '' : this.props.bool_prop ? 'True' : 'False'), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "number"
      }, this.props.number_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "object"
      }, this.props.object_prop && JSON.stringify(this.props.object_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "string"
      }, this.props.string_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "symbol"
      }, this.props.symbol_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "enum"
      }, this.props.enum_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "union"
      }, this.props.union_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "array_of"
      }, this.props.array_of_prop && JSON.stringify(this.props.array_of_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "object_of"
      }, this.props.object_of_prop && JSON.stringify(this.props.object_of_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "shape"
      }, this.props.shape_prop && JSON.stringify(this.props.shape_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "required_string"
      }, this.props.required_string));
    }
  }]);

  return TestComponent;
}(react__WEBPACK_IMPORTED_MODULE_0__["Component"]);


TestComponent.defaultProps = {
  string_with_default: 'Foo'
};
TestComponent.propTypes = {
  /**
   * The ID used to identify this component in the DOM.
   * Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
   */
  id: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Array props with
   */
  array_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,
  bool_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  func_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func,
  number_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  object_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  string_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  symbol_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.symbol,
  any_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.any,
  string_with_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  enum_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOf(['News', 'Photos']),
  // An object that could be one of many types
  union_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOfType([prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string, prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number]),
  // An array of a certain type
  array_of_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number),
  // An object with property values of a certain type
  object_of_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.objectOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number),
  // An object taking on a particular shape
  shape_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
    color: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
    fontSize: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number
  }),
  required_string: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  // These don't work good.
  nested_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
    string_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
    nested_shape: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
      nested_array: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
        nested_array_string: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
        nested_array_shape: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
          prop1: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
          prop2: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string
        })
      })),
      nested_shape_shape: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
        prop3: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
        prop4: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool
      })
    })
  }),
  array_of_array: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number)),
  children: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/internal/test_components/index.js":
/*!***********************************************!*\
  !*** ./src/internal/test_components/index.js ***!
  \***********************************************/
/*! exports provided: TestComponent, DefaultProps, ComponentAsAspect */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _components_TestComponent__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./components/TestComponent */ "./src/internal/test_components/components/TestComponent.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "TestComponent", function() { return _components_TestComponent__WEBPACK_IMPORTED_MODULE_0__["default"]; });

/* harmony import */ var _components_DefaultProps__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/DefaultProps */ "./src/internal/test_components/components/DefaultProps.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "DefaultProps", function() { return _components_DefaultProps__WEBPACK_IMPORTED_MODULE_1__["default"]; });

/* harmony import */ var _components_ComponentAsAspect__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/ComponentAsAspect */ "./src/internal/test_components/components/ComponentAsAspect.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ComponentAsAspect", function() { return _components_ComponentAsAspect__WEBPACK_IMPORTED_MODULE_2__["default"]; });






/***/ }),

/***/ 2:
/*!*****************************************************!*\
  !*** multi ./src/internal/test_components/index.js ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/internal/test_components/index.js */"./src/internal/test_components/index.js");


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ })

/******/ });
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24iLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvaW50ZXJuYWwvdGVzdF9jb21wb25lbnRzL2NvbXBvbmVudHMvQ29tcG9uZW50QXNBc3BlY3QuanN4Iiwid2VicGFjazovL2RhenpsZXJfW25hbWVdLy4vc3JjL2ludGVybmFsL3Rlc3RfY29tcG9uZW50cy9jb21wb25lbnRzL0RlZmF1bHRQcm9wcy5qc3giLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvaW50ZXJuYWwvdGVzdF9jb21wb25lbnRzL2NvbXBvbmVudHMvVGVzdENvbXBvbmVudC5qc3giLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvaW50ZXJuYWwvdGVzdF9jb21wb25lbnRzL2luZGV4LmpzIiwid2VicGFjazovL2RhenpsZXJfW25hbWVdL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0iXSwibmFtZXMiOlsiQ29tcG9uZW50QXNBc3BlY3QiLCJwcm9wcyIsImlkZW50aXR5Iiwic2luZ2xlIiwiYXJyYXkiLCJzaGFwZSIsIm1hcCIsImUiLCJpIiwic2hhcGVkIiwiUmVhY3QiLCJDb21wb25lbnQiLCJkZWZhdWx0UHJvcHMiLCJwcm9wVHlwZXMiLCJQcm9wVHlwZXMiLCJlbGVtZW50IiwiYXJyYXlPZiIsInN0cmluZyIsInVwZGF0ZUFzcGVjdHMiLCJmdW5jIiwiRGVmYXVsdFByb3BzIiwiaWQiLCJPYmplY3QiLCJlbnRyaWVzIiwiayIsInYiLCJKU09OIiwic3RyaW5naWZ5Iiwic3RyaW5nX2RlZmF1bHQiLCJzdHJpbmdfZGVmYXVsdF9lbXB0eSIsIm51bWJlcl9kZWZhdWx0IiwibnVtYmVyX2RlZmF1bHRfZW1wdHkiLCJhcnJheV9kZWZhdWx0IiwiYXJyYXlfZGVmYXVsdF9lbXB0eSIsIm9iamVjdF9kZWZhdWx0IiwiZm9vIiwib2JqZWN0X2RlZmF1bHRfZW1wdHkiLCJudW1iZXIiLCJvYmplY3QiLCJUZXN0Q29tcG9uZW50IiwiYXJyYXlfcHJvcCIsImlzTmlsIiwiYm9vbF9wcm9wIiwibnVtYmVyX3Byb3AiLCJvYmplY3RfcHJvcCIsInN0cmluZ19wcm9wIiwic3ltYm9sX3Byb3AiLCJlbnVtX3Byb3AiLCJ1bmlvbl9wcm9wIiwiYXJyYXlfb2ZfcHJvcCIsIm9iamVjdF9vZl9wcm9wIiwic2hhcGVfcHJvcCIsInJlcXVpcmVkX3N0cmluZyIsInN0cmluZ193aXRoX2RlZmF1bHQiLCJib29sIiwiZnVuY19wcm9wIiwic3ltYm9sIiwiYW55X3Byb3AiLCJhbnkiLCJvbmVPZiIsIm9uZU9mVHlwZSIsIm9iamVjdE9mIiwiY29sb3IiLCJmb250U2l6ZSIsImlzUmVxdWlyZWQiLCJuZXN0ZWRfcHJvcCIsIm5lc3RlZF9zaGFwZSIsIm5lc3RlZF9hcnJheSIsIm5lc3RlZF9hcnJheV9zdHJpbmciLCJuZXN0ZWRfYXJyYXlfc2hhcGUiLCJwcm9wMSIsInByb3AyIiwibmVzdGVkX3NoYXBlX3NoYXBlIiwicHJvcDMiLCJwcm9wNCIsImFycmF5X29mX2FycmF5IiwiY2hpbGRyZW4iLCJub2RlIl0sIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTztBQ1ZBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsZ0JBQVEsb0JBQW9CO0FBQzVCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtB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d0M7QUFGZSxPQUFoQjtBQVZNLEtBQWhCO0FBRlcsR0FBaEIsQ0F2Q1M7QUEwRHRCcUIsZ0JBQWMsRUFBRTdELGlEQUFTLENBQUNFLE9BQVYsQ0FBa0JGLGlEQUFTLENBQUNFLE9BQVYsQ0FBa0JGLGlEQUFTLENBQUN1QixNQUE1QixDQUFsQixDQTFETTtBQTREdEJ1QyxVQUFRLEVBQUU5RCxpREFBUyxDQUFDK0QsSUE1REU7QUE2RHRCM0UsVUFBUSxFQUFFWSxpREFBUyxDQUFDRyxNQTdERTtBQThEdEJDLGVBQWEsRUFBRUosaURBQVMsQ0FBQ0s7QUE5REgsQ0FBMUIsQzs7Ozs7Ozs7Ozs7O0FDeERBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFDQTtBQUNBOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNGQSxtRCIsImZpbGUiOiJkYXp6bGVyX3Rlc3RfMWMwMmVhNmI0ZDhmODgxNTI0NGQuanMiLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX3Rlc3RcIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl90ZXN0XCJdID0gZmFjdG9yeShyb290W1wiUmVhY3RcIl0pO1xufSkod2luZG93LCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18pIHtcbnJldHVybiAiLCIgXHQvLyBpbnN0YWxsIGEgSlNPTlAgY2FsbGJhY2sgZm9yIGNodW5rIGxvYWRpbmdcbiBcdGZ1bmN0aW9uIHdlYnBhY2tKc29ucENhbGxiYWNrKGRhdGEpIHtcbiBcdFx0dmFyIGNodW5rSWRzID0gZGF0YVswXTtcbiBcdFx0dmFyIG1vcmVNb2R1bGVzID0gZGF0YVsxXTtcbiBcdFx0dmFyIGV4ZWN1dGVNb2R1bGVzID0gZGF0YVsyXTtcblxuIFx0XHQvLyBhZGQgXCJtb3JlTW9kdWxlc1wiIHRvIHRoZSBtb2R1bGVzIG9iamVjdCxcbiBcdFx0Ly8gdGhlbiBmbGFnIGFsbCBcImNodW5rSWRzXCIgYXMgbG9hZGVkIGFuZCBmaXJlIGNhbGxiYWNrXG4gXHRcdHZhciBtb2R1bGVJZCwgY2h1bmtJZCwgaSA9IDAsIHJlc29sdmVzID0gW107XG4gXHRcdGZvcig7aSA8IGNodW5rSWRzLmxlbmd0aDsgaSsrKSB7XG4gXHRcdFx0Y2h1bmtJZCA9IGNodW5rSWRzW2ldO1xuIFx0XHRcdGlmKGluc3RhbGxlZENodW5rc1tjaHVua0lkXSkge1xuIFx0XHRcdFx0cmVzb2x2ZXMucHVzaChpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF1bMF0pO1xuIFx0XHRcdH1cbiBcdFx0XHRpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF0gPSAwO1xuIFx0XHR9XG4gXHRcdGZvcihtb2R1bGVJZCBpbiBtb3JlTW9kdWxlcykge1xuIFx0XHRcdGlmKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChtb3JlTW9kdWxlcywgbW9kdWxlSWQpKSB7XG4gXHRcdFx0XHRtb2R1bGVzW21vZHVsZUlkXSA9IG1vcmVNb2R1bGVzW21vZHVsZUlkXTtcbiBcdFx0XHR9XG4gXHRcdH1cbiBcdFx0aWYocGFyZW50SnNvbnBGdW5jdGlvbikgcGFyZW50SnNvbnBGdW5jdGlvbihkYXRhKTtcblxuIFx0XHR3aGlsZShyZXNvbHZlcy5sZW5ndGgpIHtcbiBcdFx0XHRyZXNvbHZlcy5zaGlmdCgpKCk7XG4gXHRcdH1cblxuIFx0XHQvLyBhZGQgZW50cnkgbW9kdWxlcyBmcm9tIGxvYWRlZCBjaHVuayB0byBkZWZlcnJlZCBsaXN0XG4gXHRcdGRlZmVycmVkTW9kdWxlcy5wdXNoLmFwcGx5KGRlZmVycmVkTW9kdWxlcywgZXhlY3V0ZU1vZHVsZXMgfHwgW10pO1xuXG4gXHRcdC8vIHJ1biBkZWZlcnJlZCBtb2R1bGVzIHdoZW4gYWxsIGNodW5rcyByZWFkeVxuIFx0XHRyZXR1cm4gY2hlY2tEZWZlcnJlZE1vZHVsZXMoKTtcbiBcdH07XG4gXHRmdW5jdGlvbiBjaGVja0RlZmVycmVkTW9kdWxlcygpIHtcbiBcdFx0dmFyIHJlc3VsdDtcbiBcdFx0Zm9yKHZhciBpID0gMDsgaSA8IGRlZmVycmVkTW9kdWxlcy5sZW5ndGg7IGkrKykge1xuIFx0XHRcdHZhciBkZWZlcnJlZE1vZHVsZSA9IGRlZmVycmVkTW9kdWxlc1tpXTtcbiBcdFx0XHR2YXIgZnVsZmlsbGVkID0gdHJ1ZTtcbiBcdFx0XHRmb3IodmFyIGogPSAxOyBqIDwgZGVmZXJyZWRNb2R1bGUubGVuZ3RoOyBqKyspIHtcbiBcdFx0XHRcdHZhciBkZXBJZCA9IGRlZmVycmVkTW9kdWxlW2pdO1xuIFx0XHRcdFx0aWYoaW5zdGFsbGVkQ2h1bmtzW2RlcElkXSAhPT0gMCkgZnVsZmlsbGVkID0gZmFsc2U7XG4gXHRcdFx0fVxuIFx0XHRcdGlmKGZ1bGZpbGxlZCkge1xuIFx0XHRcdFx0ZGVmZXJyZWRNb2R1bGVzLnNwbGljZShpLS0sIDEpO1xuIFx0XHRcdFx0cmVzdWx0ID0gX193ZWJwYWNrX3JlcXVpcmVfXyhfX3dlYnBhY2tfcmVxdWlyZV9fLnMgPSBkZWZlcnJlZE1vZHVsZVswXSk7XG4gXHRcdFx0fVxuIFx0XHR9XG5cbiBcdFx0cmV0dXJuIHJlc3VsdDtcbiBcdH1cblxuIFx0Ly8gVGhlIG1vZHVsZSBjYWNoZVxuIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcblxuIFx0Ly8gb2JqZWN0IHRvIHN0b3JlIGxvYWRlZCBhbmQgbG9hZGluZyBjaHVua3NcbiBcdC8vIHVuZGVmaW5lZCA9IGNodW5rIG5vdCBsb2FkZWQsIG51bGwgPSBjaHVuayBwcmVsb2FkZWQvcHJlZmV0Y2hlZFxuIFx0Ly8gUHJvbWlzZSA9IGNodW5rIGxvYWRpbmcsIDAgPSBjaHVuayBsb2FkZWRcbiBcdHZhciBpbnN0YWxsZWRDaHVua3MgPSB7XG4gXHRcdFwidGVzdFwiOiAwXG4gXHR9O1xuXG4gXHR2YXIgZGVmZXJyZWRNb2R1bGVzID0gW107XG5cbiBcdC8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG4gXHRmdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cbiBcdFx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG4gXHRcdGlmKGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdKSB7XG4gXHRcdFx0cmV0dXJuIGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdLmV4cG9ydHM7XG4gXHRcdH1cbiBcdFx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcbiBcdFx0dmFyIG1vZHVsZSA9IGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdID0ge1xuIFx0XHRcdGk6IG1vZHVsZUlkLFxuIFx0XHRcdGw6IGZhbHNlLFxuIFx0XHRcdGV4cG9ydHM6IHt9XG4gXHRcdH07XG5cbiBcdFx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG4gXHRcdG1vZHVsZXNbbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG4gXHRcdC8vIEZsYWcgdGhlIG1vZHVsZSBhcyBsb2FkZWRcbiBcdFx0bW9kdWxlLmwgPSB0cnVlO1xuXG4gXHRcdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG4gXHRcdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbiBcdH1cblxuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZXMgb2JqZWN0IChfX3dlYnBhY2tfbW9kdWxlc19fKVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5tID0gbW9kdWxlcztcblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGUgY2FjaGVcbiBcdF9fd2VicGFja19yZXF1aXJlX18uYyA9IGluc3RhbGxlZE1vZHVsZXM7XG5cbiBcdC8vIGRlZmluZSBnZXR0ZXIgZnVuY3Rpb24gZm9yIGhhcm1vbnkgZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kID0gZnVuY3Rpb24oZXhwb3J0cywgbmFtZSwgZ2V0dGVyKSB7XG4gXHRcdGlmKCFfX3dlYnBhY2tfcmVxdWlyZV9fLm8oZXhwb3J0cywgbmFtZSkpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgbmFtZSwgeyBlbnVtZXJhYmxlOiB0cnVlLCBnZXQ6IGdldHRlciB9KTtcbiBcdFx0fVxuIFx0fTtcblxuIFx0Ly8gZGVmaW5lIF9fZXNNb2R1bGUgb24gZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yID0gZnVuY3Rpb24oZXhwb3J0cykge1xuIFx0XHRpZih0eXBlb2YgU3ltYm9sICE9PSAndW5kZWZpbmVkJyAmJiBTeW1ib2wudG9TdHJpbmdUYWcpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgU3ltYm9sLnRvU3RyaW5nVGFnLCB7IHZhbHVlOiAnTW9kdWxlJyB9KTtcbiBcdFx0fVxuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgJ19fZXNNb2R1bGUnLCB7IHZhbHVlOiB0cnVlIH0pO1xuIFx0fTtcblxuIFx0Ly8gY3JlYXRlIGEgZmFrZSBuYW1lc3BhY2Ugb2JqZWN0XG4gXHQvLyBtb2RlICYgMTogdmFsdWUgaXMgYSBtb2R1bGUgaWQsIHJlcXVpcmUgaXRcbiBcdC8vIG1vZGUgJiAyOiBtZXJnZSBhbGwgcHJvcGVydGllcyBvZiB2YWx1ZSBpbnRvIHRoZSBuc1xuIFx0Ly8gbW9kZSAmIDQ6IHJldHVybiB2YWx1ZSB3aGVuIGFscmVhZHkgbnMgb2JqZWN0XG4gXHQvLyBtb2RlICYgOHwxOiBiZWhhdmUgbGlrZSByZXF1aXJlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnQgPSBmdW5jdGlvbih2YWx1ZSwgbW9kZSkge1xuIFx0XHRpZihtb2RlICYgMSkgdmFsdWUgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKHZhbHVlKTtcbiBcdFx0aWYobW9kZSAmIDgpIHJldHVybiB2YWx1ZTtcbiBcdFx0aWYoKG1vZGUgJiA0KSAmJiB0eXBlb2YgdmFsdWUgPT09ICdvYmplY3QnICYmIHZhbHVlICYmIHZhbHVlLl9fZXNNb2R1bGUpIHJldHVybiB2YWx1ZTtcbiBcdFx0dmFyIG5zID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yKG5zKTtcbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KG5zLCAnZGVmYXVsdCcsIHsgZW51bWVyYWJsZTogdHJ1ZSwgdmFsdWU6IHZhbHVlIH0pO1xuIFx0XHRpZihtb2RlICYgMiAmJiB0eXBlb2YgdmFsdWUgIT0gJ3N0cmluZycpIGZvcih2YXIga2V5IGluIHZhbHVlKSBfX3dlYnBhY2tfcmVxdWlyZV9fLmQobnMsIGtleSwgZnVuY3Rpb24oa2V5KSB7IHJldHVybiB2YWx1ZVtrZXldOyB9LmJpbmQobnVsbCwga2V5KSk7XG4gXHRcdHJldHVybiBucztcbiBcdH07XG5cbiBcdC8vIGdldERlZmF1bHRFeHBvcnQgZnVuY3Rpb24gZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBub24taGFybW9ueSBtb2R1bGVzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm4gPSBmdW5jdGlvbihtb2R1bGUpIHtcbiBcdFx0dmFyIGdldHRlciA9IG1vZHVsZSAmJiBtb2R1bGUuX19lc01vZHVsZSA/XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0RGVmYXVsdCgpIHsgcmV0dXJuIG1vZHVsZVsnZGVmYXVsdCddOyB9IDpcbiBcdFx0XHRmdW5jdGlvbiBnZXRNb2R1bGVFeHBvcnRzKCkgeyByZXR1cm4gbW9kdWxlOyB9O1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQoZ2V0dGVyLCAnYScsIGdldHRlcik7XG4gXHRcdHJldHVybiBnZXR0ZXI7XG4gXHR9O1xuXG4gXHQvLyBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGxcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubyA9IGZ1bmN0aW9uKG9iamVjdCwgcHJvcGVydHkpIHsgcmV0dXJuIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChvYmplY3QsIHByb3BlcnR5KTsgfTtcblxuIFx0Ly8gX193ZWJwYWNrX3B1YmxpY19wYXRoX19cbiBcdF9fd2VicGFja19yZXF1aXJlX18ucCA9IFwiXCI7XG5cbiBcdHZhciBqc29ucEFycmF5ID0gd2luZG93W1wid2VicGFja0pzb25wZGF6emxlcl9uYW1lX1wiXSA9IHdpbmRvd1tcIndlYnBhY2tKc29ucGRhenpsZXJfbmFtZV9cIl0gfHwgW107XG4gXHR2YXIgb2xkSnNvbnBGdW5jdGlvbiA9IGpzb25wQXJyYXkucHVzaC5iaW5kKGpzb25wQXJyYXkpO1xuIFx0anNvbnBBcnJheS5wdXNoID0gd2VicGFja0pzb25wQ2FsbGJhY2s7XG4gXHRqc29ucEFycmF5ID0ganNvbnBBcnJheS5zbGljZSgpO1xuIFx0Zm9yKHZhciBpID0gMDsgaSA8IGpzb25wQXJyYXkubGVuZ3RoOyBpKyspIHdlYnBhY2tKc29ucENhbGxiYWNrKGpzb25wQXJyYXlbaV0pO1xuIFx0dmFyIHBhcmVudEpzb25wRnVuY3Rpb24gPSBvbGRKc29ucEZ1bmN0aW9uO1xuXG5cbiBcdC8vIGFkZCBlbnRyeSBtb2R1bGUgdG8gZGVmZXJyZWQgbGlzdFxuIFx0ZGVmZXJyZWRNb2R1bGVzLnB1c2goWzIsXCJjb21tb25zXCJdKTtcbiBcdC8vIHJ1biBkZWZlcnJlZCBtb2R1bGVzIHdoZW4gcmVhZHlcbiBcdHJldHVybiBjaGVja0RlZmVycmVkTW9kdWxlcygpO1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIENvbXBvbmVudEFzQXNwZWN0IGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgICByZW5kZXIoKSB7XG4gICAgICAgIGNvbnN0IHtpZGVudGl0eSwgc2luZ2xlLCBhcnJheSwgc2hhcGV9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxkaXYgaWQ9e2lkZW50aXR5fT5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInNpbmdsZVwiPntzaW5nbGV9PC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJhcnJheVwiPlxuICAgICAgICAgICAgICAgICAgICB7YXJyYXkubWFwKChlLCBpKSA9PiAoXG4gICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGtleT17aX0+e2V9PC9kaXY+XG4gICAgICAgICAgICAgICAgICAgICkpfVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwic2hhcGVcIj57c2hhcGUuc2hhcGVkfTwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5Db21wb25lbnRBc0FzcGVjdC5kZWZhdWx0UHJvcHMgPSB7fTtcblxuQ29tcG9uZW50QXNBc3BlY3QucHJvcFR5cGVzID0ge1xuICAgIHNpbmdsZTogUHJvcFR5cGVzLmVsZW1lbnQsXG4gICAgYXJyYXk6IFByb3BUeXBlcy5hcnJheU9mKFByb3BUeXBlcy5lbGVtZW50KSxcbiAgICBzaGFwZTogUHJvcFR5cGVzLnNoYXBlKHtcbiAgICAgICAgc2hhcGVkOiBQcm9wVHlwZXMuZWxlbWVudCxcbiAgICB9KSxcblxuICAgIC8qKlxuICAgICAqICBVbmlxdWUgaWQgZm9yIHRoaXMgY29tcG9uZW50XG4gICAgICovXG4gICAgaWRlbnRpdHk6IFByb3BUeXBlcy5zdHJpbmcsXG5cbiAgICAvKipcbiAgICAgKiBVcGRhdGUgYXNwZWN0cyBvbiB0aGUgYmFja2VuZC5cbiAgICAgKi9cbiAgICB1cGRhdGVBc3BlY3RzOiBQcm9wVHlwZXMuZnVuYyxcbn07XG4iLCJpbXBvcnQgUmVhY3QsIHtDb21wb25lbnR9IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIERlZmF1bHRQcm9wcyBleHRlbmRzIENvbXBvbmVudCB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7aWR9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxkaXYgaWQ9e2lkfT5cbiAgICAgICAgICAgICAgICB7T2JqZWN0LmVudHJpZXModGhpcy5wcm9wcykubWFwKChrLCB2KSA9PiAoXG4gICAgICAgICAgICAgICAgICAgIDxkaXYgaWQ9e2Ake2lkfS0ke2t9YH0ga2V5PXtgJHtpZH0tJHtrfWB9PlxuICAgICAgICAgICAgICAgICAgICAgICAge2t9OiB7SlNPTi5zdHJpbmdpZnkodil9XG4gICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICkpfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5EZWZhdWx0UHJvcHMuZGVmYXVsdFByb3BzID0ge1xuICAgIHN0cmluZ19kZWZhdWx0OiAnRGVmYXVsdCBzdHJpbmcnLFxuICAgIHN0cmluZ19kZWZhdWx0X2VtcHR5OiAnJyxcbiAgICBudW1iZXJfZGVmYXVsdDogMC4yNjY2LFxuICAgIG51bWJlcl9kZWZhdWx0X2VtcHR5OiAwLFxuICAgIGFycmF5X2RlZmF1bHQ6IFsxLCAyLCAzXSxcbiAgICBhcnJheV9kZWZhdWx0X2VtcHR5OiBbXSxcbiAgICBvYmplY3RfZGVmYXVsdDoge2ZvbzogJ2Jhcid9LFxuICAgIG9iamVjdF9kZWZhdWx0X2VtcHR5OiB7fSxcbn07XG5cbkRlZmF1bHRQcm9wcy5wcm9wVHlwZXMgPSB7XG4gICAgaWQ6IFByb3BUeXBlcy5zdHJpbmcsXG5cbiAgICBzdHJpbmdfZGVmYXVsdDogUHJvcFR5cGVzLnN0cmluZyxcbiAgICBzdHJpbmdfZGVmYXVsdF9lbXB0eTogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIG51bWJlcl9kZWZhdWx0OiBQcm9wVHlwZXMubnVtYmVyLFxuICAgIG51bWJlcl9kZWZhdWx0X2VtcHR5OiBQcm9wVHlwZXMubnVtYmVyLFxuXG4gICAgYXJyYXlfZGVmYXVsdDogUHJvcFR5cGVzLmFycmF5LFxuICAgIGFycmF5X2RlZmF1bHRfZW1wdHk6IFByb3BUeXBlcy5hcnJheSxcblxuICAgIG9iamVjdF9kZWZhdWx0OiBQcm9wVHlwZXMub2JqZWN0LFxuICAgIG9iamVjdF9kZWZhdWx0X2VtcHR5OiBQcm9wVHlwZXMub2JqZWN0LFxufTtcbiIsImltcG9ydCBSZWFjdCwge0NvbXBvbmVudH0gZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcbmltcG9ydCB7aXNOaWx9IGZyb20gJ3JhbWRhJztcblxuLyoqXG4gKiBUZXN0IGNvbXBvbmVudCB3aXRoIGFsbCBzdXBwb3J0ZWQgcHJvcHMgYnkgZGF6emxlci5cbiAqIEVhY2ggcHJvcCBhcmUgcmVuZGVyZWQgd2l0aCBhIHNlbGVjdG9yIGZvciBlYXN5IGFjY2Vzcy5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVGVzdENvbXBvbmVudCBleHRlbmRzIENvbXBvbmVudCB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBpZD17dGhpcy5wcm9wcy5pZH0+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJhcnJheVwiPlxuICAgICAgICAgICAgICAgICAgICB7dGhpcy5wcm9wcy5hcnJheV9wcm9wICYmXG4gICAgICAgICAgICAgICAgICAgICAgICBKU09OLnN0cmluZ2lmeSh0aGlzLnByb3BzLmFycmF5X3Byb3ApfVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiYm9vbFwiPlxuICAgICAgICAgICAgICAgICAgICB7aXNOaWwodGhpcy5wcm9wcy5ib29sX3Byb3ApXG4gICAgICAgICAgICAgICAgICAgICAgICA/ICcnXG4gICAgICAgICAgICAgICAgICAgICAgICA6IHRoaXMucHJvcHMuYm9vbF9wcm9wXG4gICAgICAgICAgICAgICAgICAgICAgICA/ICdUcnVlJ1xuICAgICAgICAgICAgICAgICAgICAgICAgOiAnRmFsc2UnfVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwibnVtYmVyXCI+e3RoaXMucHJvcHMubnVtYmVyX3Byb3B9PC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJvYmplY3RcIj5cbiAgICAgICAgICAgICAgICAgICAge3RoaXMucHJvcHMub2JqZWN0X3Byb3AgJiZcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHRoaXMucHJvcHMub2JqZWN0X3Byb3ApfVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwic3RyaW5nXCI+e3RoaXMucHJvcHMuc3RyaW5nX3Byb3B9PC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJzeW1ib2xcIj57dGhpcy5wcm9wcy5zeW1ib2xfcHJvcH08L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImVudW1cIj57dGhpcy5wcm9wcy5lbnVtX3Byb3B9PC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ1bmlvblwiPnt0aGlzLnByb3BzLnVuaW9uX3Byb3B9PC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJhcnJheV9vZlwiPlxuICAgICAgICAgICAgICAgICAgICB7dGhpcy5wcm9wcy5hcnJheV9vZl9wcm9wICYmXG4gICAgICAgICAgICAgICAgICAgICAgICBKU09OLnN0cmluZ2lmeSh0aGlzLnByb3BzLmFycmF5X29mX3Byb3ApfVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwib2JqZWN0X29mXCI+XG4gICAgICAgICAgICAgICAgICAgIHt0aGlzLnByb3BzLm9iamVjdF9vZl9wcm9wICYmXG4gICAgICAgICAgICAgICAgICAgICAgICBKU09OLnN0cmluZ2lmeSh0aGlzLnByb3BzLm9iamVjdF9vZl9wcm9wKX1cbiAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInNoYXBlXCI+XG4gICAgICAgICAgICAgICAgICAgIHt0aGlzLnByb3BzLnNoYXBlX3Byb3AgJiZcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHRoaXMucHJvcHMuc2hhcGVfcHJvcCl9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJyZXF1aXJlZF9zdHJpbmdcIj5cbiAgICAgICAgICAgICAgICAgICAge3RoaXMucHJvcHMucmVxdWlyZWRfc3RyaW5nfVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5UZXN0Q29tcG9uZW50LmRlZmF1bHRQcm9wcyA9IHtcbiAgICBzdHJpbmdfd2l0aF9kZWZhdWx0OiAnRm9vJyxcbn07XG5cblRlc3RDb21wb25lbnQucHJvcFR5cGVzID0ge1xuICAgIC8qKlxuICAgICAqIFRoZSBJRCB1c2VkIHRvIGlkZW50aWZ5IHRoaXMgY29tcG9uZW50IGluIHRoZSBET00uXG4gICAgICogTG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdCwgc2VkIGRvIGVpdXNtb2QgdGVtcG9yIGluY2lkaWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdWEuIFV0IGVuaW0gYWQgbWluaW0gdmVuaWFtLCBxdWlzIG5vc3RydWQgZXhlcmNpdGF0aW9uIHVsbGFtY28gbGFib3JpcyBuaXNpIHV0IGFsaXF1aXAgZXggZWEgY29tbW9kbyBjb25zZXF1YXQuIER1aXMgYXV0ZSBpcnVyZSBkb2xvciBpbiByZXByZWhlbmRlcml0IGluIHZvbHVwdGF0ZSB2ZWxpdCBlc3NlIGNpbGx1bSBkb2xvcmUgZXUgZnVnaWF0IG51bGxhIHBhcmlhdHVyLiBFeGNlcHRldXIgc2ludCBvY2NhZWNhdCBjdXBpZGF0YXQgbm9uIHByb2lkZW50LCBzdW50IGluIGN1bHBhIHF1aSBvZmZpY2lhIGRlc2VydW50IG1vbGxpdCBhbmltIGlkIGVzdCBsYWJvcnVtLlxuICAgICAqL1xuICAgIGlkOiBQcm9wVHlwZXMuc3RyaW5nLFxuXG4gICAgLyoqXG4gICAgICogQXJyYXkgcHJvcHMgd2l0aFxuICAgICAqL1xuICAgIGFycmF5X3Byb3A6IFByb3BUeXBlcy5hcnJheSxcbiAgICBib29sX3Byb3A6IFByb3BUeXBlcy5ib29sLFxuICAgIGZ1bmNfcHJvcDogUHJvcFR5cGVzLmZ1bmMsXG4gICAgbnVtYmVyX3Byb3A6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgb2JqZWN0X3Byb3A6IFByb3BUeXBlcy5vYmplY3QsXG4gICAgc3RyaW5nX3Byb3A6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgc3ltYm9sX3Byb3A6IFByb3BUeXBlcy5zeW1ib2wsXG4gICAgYW55X3Byb3A6IFByb3BUeXBlcy5hbnksXG5cbiAgICBzdHJpbmdfd2l0aF9kZWZhdWx0OiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIGVudW1fcHJvcDogUHJvcFR5cGVzLm9uZU9mKFsnTmV3cycsICdQaG90b3MnXSksXG5cbiAgICAvLyBBbiBvYmplY3QgdGhhdCBjb3VsZCBiZSBvbmUgb2YgbWFueSB0eXBlc1xuICAgIHVuaW9uX3Byb3A6IFByb3BUeXBlcy5vbmVPZlR5cGUoW1Byb3BUeXBlcy5zdHJpbmcsIFByb3BUeXBlcy5udW1iZXJdKSxcblxuICAgIC8vIEFuIGFycmF5IG9mIGEgY2VydGFpbiB0eXBlXG4gICAgYXJyYXlfb2ZfcHJvcDogUHJvcFR5cGVzLmFycmF5T2YoUHJvcFR5cGVzLm51bWJlciksXG5cbiAgICAvLyBBbiBvYmplY3Qgd2l0aCBwcm9wZXJ0eSB2YWx1ZXMgb2YgYSBjZXJ0YWluIHR5cGVcbiAgICBvYmplY3Rfb2ZfcHJvcDogUHJvcFR5cGVzLm9iamVjdE9mKFByb3BUeXBlcy5udW1iZXIpLFxuXG4gICAgLy8gQW4gb2JqZWN0IHRha2luZyBvbiBhIHBhcnRpY3VsYXIgc2hhcGVcbiAgICBzaGFwZV9wcm9wOiBQcm9wVHlwZXMuc2hhcGUoe1xuICAgICAgICBjb2xvcjogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAgICAgZm9udFNpemU6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgfSksXG4gICAgcmVxdWlyZWRfc3RyaW5nOiBQcm9wVHlwZXMuc3RyaW5nLmlzUmVxdWlyZWQsXG5cbiAgICAvLyBUaGVzZSBkb24ndCB3b3JrIGdvb2QuXG4gICAgbmVzdGVkX3Byb3A6IFByb3BUeXBlcy5zaGFwZSh7XG4gICAgICAgIHN0cmluZ19wcm9wOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgICAgICBuZXN0ZWRfc2hhcGU6IFByb3BUeXBlcy5zaGFwZSh7XG4gICAgICAgICAgICBuZXN0ZWRfYXJyYXk6IFByb3BUeXBlcy5hcnJheU9mKFxuICAgICAgICAgICAgICAgIFByb3BUeXBlcy5zaGFwZSh7XG4gICAgICAgICAgICAgICAgICAgIG5lc3RlZF9hcnJheV9zdHJpbmc6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgICAgICAgICAgICAgICAgIG5lc3RlZF9hcnJheV9zaGFwZTogUHJvcFR5cGVzLnNoYXBlKHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHByb3AxOiBQcm9wVHlwZXMubnVtYmVyLFxuICAgICAgICAgICAgICAgICAgICAgICAgcHJvcDI6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgICAgICAgICAgICAgICAgIH0pLFxuICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICApLFxuICAgICAgICAgICAgbmVzdGVkX3NoYXBlX3NoYXBlOiBQcm9wVHlwZXMuc2hhcGUoe1xuICAgICAgICAgICAgICAgIHByb3AzOiBQcm9wVHlwZXMubnVtYmVyLFxuICAgICAgICAgICAgICAgIHByb3A0OiBQcm9wVHlwZXMuYm9vbCxcbiAgICAgICAgICAgIH0pLFxuICAgICAgICB9KSxcbiAgICB9KSxcblxuICAgIGFycmF5X29mX2FycmF5OiBQcm9wVHlwZXMuYXJyYXlPZihQcm9wVHlwZXMuYXJyYXlPZihQcm9wVHlwZXMubnVtYmVyKSksXG5cbiAgICBjaGlsZHJlbjogUHJvcFR5cGVzLm5vZGUsXG4gICAgaWRlbnRpdHk6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgdXBkYXRlQXNwZWN0czogUHJvcFR5cGVzLmZ1bmMsXG59O1xuIiwiaW1wb3J0IFRlc3RDb21wb25lbnQgZnJvbSAnLi9jb21wb25lbnRzL1Rlc3RDb21wb25lbnQnO1xuaW1wb3J0IERlZmF1bHRQcm9wcyBmcm9tICcuL2NvbXBvbmVudHMvRGVmYXVsdFByb3BzJztcbmltcG9ydCBDb21wb25lbnRBc0FzcGVjdCBmcm9tICcuL2NvbXBvbmVudHMvQ29tcG9uZW50QXNBc3BlY3QnO1xuXG5leHBvcnQge1Rlc3RDb21wb25lbnQsIERlZmF1bHRQcm9wcywgQ29tcG9uZW50QXNBc3BlY3R9O1xuIiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187Il0sInNvdXJjZVJvb3QiOiIifQ==