(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"), require("react-dom"));
	else if(typeof define === 'function' && define.amd)
		define(["react", "react-dom"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_renderer"] = factory(require("react"), require("react-dom"));
	else
		root["dazzler_renderer"] = factory(root["React"], root["ReactDOM"]);
})(window, function(__WEBPACK_EXTERNAL_MODULE_react__, __WEBPACK_EXTERNAL_MODULE_react_dom__) {
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
/******/ 		"renderer": 0
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
/******/ 	deferredModules.push([1,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/renderer/js/components/Renderer.jsx":
/*!*************************************************!*\
  !*** ./src/renderer/js/components/Renderer.jsx ***!
  \*************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Renderer; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _Updater__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Updater */ "./src/renderer/js/components/Updater.jsx");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_2__);
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





var Renderer =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Renderer, _React$Component);

  function Renderer() {
    _classCallCheck(this, Renderer);

    return _possibleConstructorReturn(this, _getPrototypeOf(Renderer).apply(this, arguments));
  }

  _createClass(Renderer, [{
    key: "componentWillMount",
    value: function componentWillMount() {
      window.dazzler_base_url = this.props.baseUrl;
    }
  }, {
    key: "render",
    value: function render() {
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "dazzler-renderer"
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_Updater__WEBPACK_IMPORTED_MODULE_1__["default"], this.props));
    }
  }]);

  return Renderer;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Renderer.propTypes = {
  baseUrl: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.string.isRequired,
  ping: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.bool,
  ping_interval: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.number,
  retries: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.number
};

/***/ }),

/***/ "./src/renderer/js/components/Updater.jsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Updater.jsx ***!
  \************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Updater; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/* harmony import */ var _Wrapper__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./Wrapper */ "./src/renderer/js/components/Wrapper.jsx");
/* harmony import */ var _requests__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../requests */ "./src/renderer/js/requests.js");
/* harmony import */ var _commons_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../commons/js */ "./src/commons/js/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function _iterableToArrayLimit(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }








function isComponent(c) {
  return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(c) === 'Object' && c.hasOwnProperty('package') && c.hasOwnProperty('aspects') && c.hasOwnProperty('name') && c.hasOwnProperty('identity');
}

function hydrateProps(props, updateAspects, connect, disconnect) {
  var replace = {};
  Object.entries(props).forEach(function (_ref) {
    var _ref2 = _slicedToArray(_ref, 2),
        k = _ref2[0],
        v = _ref2[1];

    if (Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(v) === 'Array') {
      replace[k] = v.map(function (c) {
        if (!isComponent(c)) {
          // Mixing components and primitives
          return c;
        }

        var newProps = hydrateProps(c.aspects, updateAspects, connect, disconnect);

        if (!newProps.key) {
          newProps.key = c.identity;
        }

        return hydrateComponent(c.name, c["package"], c.identity, newProps, updateAspects, connect, disconnect);
      });
    } else if (isComponent(v)) {
      var newProps = hydrateProps(v.aspects, updateAspects, connect, disconnect);
      replace[k] = hydrateComponent(v.name, v["package"], v.identity, newProps, updateAspects, connect, disconnect);
    } else if (Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(v) === 'Object') {
      replace[k] = hydrateProps(v, updateAspects, connect, disconnect);
    }
  });
  return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["merge"])(props, replace);
}

function hydrateComponent(name, package_name, identity, props, updateAspects, connect, disconnect) {
  var pack = window[package_name];
  var element = react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(pack[name], props);
  return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_Wrapper__WEBPACK_IMPORTED_MODULE_3__["default"], {
    identity: identity,
    updateAspects: updateAspects,
    component: element,
    connect: connect,
    package_name: package_name,
    component_name: name,
    aspects: props,
    disconnect: disconnect,
    key: "wrapper-".concat(identity)
  });
}

function prepareProp(prop) {
  if (react__WEBPACK_IMPORTED_MODULE_0___default.a.isValidElement(prop)) {
    return {
      identity: prop.props.identity,
      aspects: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["map"])(prepareProp, Object(ramda__WEBPACK_IMPORTED_MODULE_2__["omit"])(['identity', 'updateAspects', '_name', '_package', 'aspects', 'key'], prop.props.aspects // You actually in the wrapper here.
      )),
      name: prop.props.component_name,
      "package": prop.props.package_name
    };
  }

  if (Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(prop) === 'Array') {
    return prop.map(prepareProp);
  }

  if (Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(prop) === 'Object') {
    return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["map"])(prepareProp, prop);
  }

  return prop;
}

var Updater =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Updater, _React$Component);

  function Updater(props) {
    var _this;

    _classCallCheck(this, Updater);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Updater).call(this, props));
    _this.state = {
      layout: false,
      ready: false,
      page: null,
      bindings: {},
      packages: [],
      requirements: []
    }; // The api url for the page is the same but a post.
    // Fetch bindings, packages & requirements

    _this.pageApi = Object(_requests__WEBPACK_IMPORTED_MODULE_4__["apiRequest"])(_this.getHeaders.bind(_assertThisInitialized(_this)), _this.refresh.bind(_assertThisInitialized(_this)), window.location.href); // All components get connected.

    _this.boundComponents = {};
    _this.ws = null;
    _this.updateAspects = _this.updateAspects.bind(_assertThisInitialized(_this));
    _this.connect = _this.connect.bind(_assertThisInitialized(_this));
    _this.disconnect = _this.disconnect.bind(_assertThisInitialized(_this));
    _this.onMessage = _this.onMessage.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Updater, [{
    key: "updateAspects",
    value: function updateAspects(identity, aspects) {
      var _this2 = this;

      return new Promise(function (resolve) {
        var bindings = Object.keys(aspects).map(function (key) {
          return _this2.state.bindings["".concat(identity, ".").concat(key)];
        }).filter(function (e) {
          return e;
        });

        if (!bindings) {
          return resolve(0);
        }

        bindings.forEach(function (binding) {
          return _this2.sendBinding(binding, aspects[binding.trigger.aspect]);
        });
        resolve();
      });
    }
  }, {
    key: "connect",
    value: function connect(identity, setAspects, getAspect) {
      this.boundComponents[identity] = {
        setAspects: setAspects,
        getAspect: getAspect
      };
    }
  }, {
    key: "disconnect",
    value: function disconnect(identity) {
      delete this.boundComponents[identity];
    }
  }, {
    key: "onMessage",
    value: function onMessage(response) {
      var _this3 = this;

      var data = JSON.parse(response.data);
      var identity = data.identity,
          kind = data.kind,
          payload = data.payload,
          storage = data.storage,
          request_id = data.request_id;
      var store;

      if (storage === 'session') {
        store = window.sessionStorage;
      } else {
        store = window.localStorage;
      }

      switch (kind) {
        case 'set-aspect':
          var component = this.boundComponents[identity];

          if (!component) {
            var error = "Component not found: ".concat(identity);
            this.ws.send(JSON.stringify({
              error: error,
              kind: 'error'
            }));
            console.error(error);
            return;
          }

          component.setAspects(hydrateProps(payload, this.updateAspects, this.connect, this.disconnect)).then(function () {
            Object.keys(payload).forEach(function (k) {
              var key = "".concat(identity, ".").concat(k);
              var binding = _this3.state.bindings[key];

              if (binding) {
                _this3.sendBinding(binding, component.getAspect(k));
              } // What about returned components ?
              // They get their Wrapper.

            });
          });
          break;

        case 'get-aspect':
          var aspect = data.aspect;
          var wanted = this.boundComponents[identity];

          if (!wanted) {
            this.ws.send(JSON.stringify({
              kind: kind,
              identity: identity,
              aspect: aspect,
              request_id: request_id,
              error: "Aspect not found ".concat(identity, ".").concat(aspect)
            }));
            return;
          }

          var value = wanted.getAspect(aspect);
          this.ws.send(JSON.stringify({
            kind: kind,
            identity: identity,
            aspect: aspect,
            value: prepareProp(value),
            request_id: request_id
          }));
          break;

        case 'set-storage':
          store.setItem(identity, JSON.stringify(payload));
          break;

        case 'get-storage':
          this.ws.send(JSON.stringify({
            kind: kind,
            identity: identity,
            request_id: request_id,
            value: JSON.parse(store.getItem(identity))
          }));
          break;

        case 'ping':
          // Just do nothing.
          break;
      }
    }
  }, {
    key: "sendBinding",
    value: function sendBinding(binding, value) {
      var _this4 = this;

      // Collect all values and send a binding payload
      var trigger = _objectSpread({}, binding.trigger, {
        value: prepareProp(value)
      });

      var states = binding.states.map(function (state) {
        return _objectSpread({}, state, {
          value: _this4.boundComponents[state.identity] && prepareProp(_this4.boundComponents[state.identity].getAspect(state.aspect))
        });
      });
      var payload = {
        trigger: trigger,
        states: states,
        kind: 'binding',
        page: this.state.page,
        key: binding.key
      };
      this.ws.send(JSON.stringify(payload));
    }
  }, {
    key: "loadRequirements",
    value: function loadRequirements(requirements, packages) {
      var _this5 = this;

      return new Promise(function (resolve, reject) {
        var loadings = []; // Load packages first.

        Object.keys(packages).forEach(function (pack_name) {
          var pack = packages[pack_name];
          loadings = loadings.concat(pack.requirements.map(_this5.loadRequirement));
        }); // Then load requirements so they can use packages
        // and override css.

        Promise.all(loadings).then(function () {
          var i = 0; // Load in order.

          var handler = function handler() {
            if (i < requirements.length) {
              _this5.loadRequirement(requirements[i]).then(function () {
                i++;
                handler();
              });
            } else {
              resolve();
            }
          };

          handler();
        })["catch"](reject);
      });
    }
  }, {
    key: "loadRequirement",
    value: function loadRequirement(requirement) {
      return new Promise(function (resolve, reject) {
        var url = requirement.url,
            kind = requirement.kind,
            meta = requirement.meta;
        var method;

        if (kind === 'js') {
          method = _commons_js__WEBPACK_IMPORTED_MODULE_5__["loadScript"];
        } else if (kind === 'css') {
          method = _commons_js__WEBPACK_IMPORTED_MODULE_5__["loadCss"];
        } else if (kind === 'map') {
          return resolve();
        } else {
          return reject({
            error: "Invalid requirement kind: ".concat(kind)
          });
        }

        method(url, meta).then(resolve)["catch"](reject);
      });
    }
  }, {
    key: "_connectWS",
    value: function _connectWS() {
      var _this6 = this;

      // Setup websocket for updates
      var tries = 0;

      var connexion = function connexion() {
        _this6.ws = new WebSocket("ws".concat(window.location.href.startsWith('https') ? 's' : '', "://").concat(_this6.props.baseUrl && _this6.props.baseUrl || window.location.host).concat(window.location.pathname, "/ws"));

        _this6.ws.addEventListener('message', _this6.onMessage);

        _this6.ws.onopen = function () {
          _this6.setState({
            ready: true
          });

          tries = 0;
        };

        _this6.ws.onclose = function () {
          var reconnect = function reconnect() {
            tries++;
            connexion();
          };

          if (tries < _this6.props.retries) {
            setTimeout(reconnect, 1000);
          }
        };
      };

      connexion();
    } // TODO implement or remove dependence on these functions.

  }, {
    key: "getHeaders",
    value: function getHeaders() {
      return {};
    }
  }, {
    key: "refresh",
    value: function refresh() {}
  }, {
    key: "componentWillMount",
    value: function componentWillMount() {
      var _this7 = this;

      this.pageApi('', {
        method: 'POST'
      }).then(function (response) {
        _this7.setState({
          page: response.page,
          layout: response.layout,
          bindings: response.bindings,
          packages: response.packages,
          requirements: response.requirements
        });

        _this7.loadRequirements(response.requirements, response.packages).then(function () {
          return _this7._connectWS();
        });
      });
    }
  }, {
    key: "render",
    value: function render() {
      var _this$state = this.state,
          layout = _this$state.layout,
          ready = _this$state.ready;
      if (!ready) return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", null, "Loading...");

      if (!isComponent(layout)) {
        throw new Error("Layout is not a component: ".concat(layout));
      }

      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "dazzler-rendered"
      }, hydrateComponent(layout.name, layout["package"], layout.identity, hydrateProps(layout.aspects, this.updateAspects, this.connect, this.disconnect), this.updateAspects, this.connect, this.disconnect));
    }
  }]);

  return Updater;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Updater.defaultProps = {};
Updater.propTypes = {
  baseUrl: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  ping: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  ping_interval: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  retries: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number
};

/***/ }),

/***/ "./src/renderer/js/components/Wrapper.jsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Wrapper.jsx ***!
  \************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Wrapper; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/* harmony import */ var _commons_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../commons/js */ "./src/commons/js/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





/**
 * Wraps components for aspects updating.
 */

var Wrapper =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Wrapper, _React$Component);

  function Wrapper(props) {
    var _this;

    _classCallCheck(this, Wrapper);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Wrapper).call(this, props));
    _this.state = {
      aspects: props.aspects || {},
      ready: false,
      initial: false
    };
    _this.setAspects = _this.setAspects.bind(_assertThisInitialized(_this));
    _this.getAspect = _this.getAspect.bind(_assertThisInitialized(_this));
    _this.updateAspects = _this.updateAspects.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Wrapper, [{
    key: "updateAspects",
    value: function updateAspects(aspects) {
      var _this2 = this;

      return this.setAspects(aspects).then(function () {
        return _this2.props.updateAspects(_this2.props.identity, aspects);
      });
    }
  }, {
    key: "setAspects",
    value: function setAspects(aspects) {
      var _this3 = this;

      return new Promise(function (resolve) {
        _this3.setState({
          aspects: _objectSpread({}, _this3.state.aspects, aspects)
        }, resolve);
      });
    }
  }, {
    key: "getAspect",
    value: function getAspect(aspect) {
      return this.state.aspects[aspect];
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      var _this4 = this;

      // Only update the component when mounted.
      // Otherwise gets a race condition with willUnmount
      this.props.connect(this.props.identity, this.setAspects, this.getAspect);

      if (!this.state.initial) {
        this.updateAspects(this.state.aspects).then(function () {
          return _this4.setState({
            ready: true,
            initial: true
          });
        });
      }
    }
  }, {
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      this.props.disconnect(this.props.identity);
    }
  }, {
    key: "render",
    value: function render() {
      var _this$props = this.props,
          component = _this$props.component,
          component_name = _this$props.component_name,
          package_name = _this$props.package_name;
      var _this$state = this.state,
          aspects = _this$state.aspects,
          ready = _this$state.ready;
      if (!ready) return null;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.cloneElement(component, _objectSpread({}, aspects, {
        updateAspects: this.updateAspects,
        identity: this.props.identity,
        class_name: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(["".concat(package_name.replace('_', '-').toLowerCase(), "-").concat(Object(_commons_js__WEBPACK_IMPORTED_MODULE_3__["camelToSpinal"])(component_name))], aspects.class_name ? aspects.class_name.split(' ') : []))
      }));
    }
  }]);

  return Wrapper;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Wrapper.propTypes = {
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired,
  component: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node.isRequired,
  connect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired,
  component_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  package_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  disconnect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired
};

/***/ }),

/***/ "./src/renderer/js/index.js":
/*!**********************************!*\
  !*** ./src/renderer/js/index.js ***!
  \**********************************/
/*! exports provided: Renderer, render */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dom */ "react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_Renderer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Renderer */ "./src/renderer/js/components/Renderer.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Renderer", function() { return _components_Renderer__WEBPACK_IMPORTED_MODULE_2__["default"]; });





function render(_ref, element) {
  var baseUrl = _ref.baseUrl,
      ping = _ref.ping,
      ping_interval = _ref.ping_interval,
      retries = _ref.retries;
  react_dom__WEBPACK_IMPORTED_MODULE_1___default.a.render(react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Renderer__WEBPACK_IMPORTED_MODULE_2__["default"], {
    baseUrl: baseUrl,
    ping: ping,
    ping_interval: ping_interval,
    retries: retries
  }), element);
}



/***/ }),

/***/ "./src/renderer/js/requests.js":
/*!*************************************!*\
  !*** ./src/renderer/js/requests.js ***!
  \*************************************/
/*! exports provided: JSONHEADERS, xhrRequest, apiRequest */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "JSONHEADERS", function() { return JSONHEADERS; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "xhrRequest", function() { return xhrRequest; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "apiRequest", function() { return apiRequest; });
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

/* eslint-disable no-magic-numbers */
var jsonPattern = /json/i;
/**
 * @typedef {Object} XhrOptions
 * @property {string} [method='GET']
 * @property {Object} [headers={}]
 * @property {string|Blob|ArrayBuffer|object|Array} [payload='']
 */

/**
 * @type {XhrOptions}
 */

var defaultXhrOptions = {
  method: 'GET',
  headers: {},
  payload: '',
  json: true
};
var JSONHEADERS = {
  'Content-Type': 'application/json'
};
/**
 * Xhr promise wrap.
 *
 * Fetch can't do put request, so xhr still useful.
 *
 * Auto parse json responses.
 * Cancellation: xhr.abort
 * @param {string} url
 * @param {XhrOptions} [options]
 * @return {Promise}
 */

function xhrRequest(url) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : defaultXhrOptions;
  return new Promise(function (resolve, reject) {
    var _defaultXhrOptions$op = _objectSpread({}, defaultXhrOptions, options),
        method = _defaultXhrOptions$op.method,
        headers = _defaultXhrOptions$op.headers,
        payload = _defaultXhrOptions$op.payload,
        json = _defaultXhrOptions$op.json;

    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    var head = json ? _objectSpread({}, JSONHEADERS, headers) : headers;
    Object.keys(head).forEach(function (k) {
      return xhr.setRequestHeader(k, head[k]);
    });

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status < 400) {
          var responseValue = xhr.response;

          if (jsonPattern.test(xhr.getResponseHeader('Content-Type'))) {
            responseValue = JSON.parse(xhr.responseText);
          }

          resolve(responseValue);
        } else {
          reject({
            error: 'RequestError',
            message: "XHR ".concat(url, " FAILED - STATUS: ").concat(xhr.status, " MESSAGE: ").concat(xhr.statusText),
            status: xhr.status,
            xhr: xhr
          });
        }
      }
    };

    xhr.onerror = function (err) {
      return reject(err);
    };

    xhr.send(json ? JSON.stringify(payload) : payload);
  });
}
/**
 * Auto get headers and refresh/retry.
 *
 * @param {function} getHeaders
 * @param {function} refresh
 * @param {string} baseUrl
 */

function apiRequest(getHeaders, refresh) {
  var baseUrl = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : '';
  return function () {
    var retried = false;
    var url = baseUrl + arguments[0];
    var options = arguments[1] || {};
    options.headers = _objectSpread({}, getHeaders(), options.headers);
    return new Promise(function (resolve, reject) {
      xhrRequest(url, options).then(resolve)["catch"](function (err) {
        if (err.status === 401 && !retried) {
          retried = true;
          refresh().then(function () {
            return xhrRequest(url, _objectSpread({}, options, {
              headers: _objectSpread({}, options.headers, getHeaders())
            })).then(resolve);
          })["catch"](reject);
        } else {
          reject(err);
        }
      });
    });
  };
}

/***/ }),

/***/ 1:
/*!****************************************!*\
  !*** multi ./src/renderer/js/index.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/renderer/js/index.js */"./src/renderer/js/index.js");


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ }),

/***/ "react-dom":
/*!***********************************************************************************************************************!*\
  !*** external {"commonjs":"react-dom","commonjs2":"react-dom","amd":"react-dom","umd":"react-dom","root":"ReactDOM"} ***!
  \***********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react_dom__;

/***/ })

/******/ });
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24iLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvcmVuZGVyZXIvanMvY29tcG9uZW50cy9SZW5kZXJlci5qc3giLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvcmVuZGVyZXIvanMvY29tcG9uZW50cy9VcGRhdGVyLmpzeCIsIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1dyYXBwZXIuanN4Iiwid2VicGFjazovL2RhenpsZXJfW25hbWVdLy4vc3JjL3JlbmRlcmVyL2pzL2luZGV4LmpzIiwid2VicGFjazovL2RhenpsZXJfW25hbWVdLy4vc3JjL3JlbmRlcmVyL2pzL3JlcXVlc3RzLmpzIiwid2VicGFjazovL2RhenpsZXJfW25hbWVdL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0iLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0LWRvbVwiLFwiY29tbW9uanMyXCI6XCJyZWFjdC1kb21cIixcImFtZFwiOlwicmVhY3QtZG9tXCIsXCJ1bWRcIjpcInJlYWN0LWRvbVwiLFwicm9vdFwiOlwiUmVhY3RET01cIn0iXSwibmFtZXMiOlsiUmVuZGVyZXIiLCJ3aW5kb3ciLCJkYXp6bGVyX2Jhc2VfdXJsIiwicHJvcHMiLCJiYXNlVXJsIiwiUmVhY3QiLCJDb21wb25lbnQiLCJwcm9wVHlwZXMiLCJQcm9wVHlwZXMiLCJzdHJpbmciLCJpc1JlcXVpcmVkIiwicGluZyIsImJvb2wiLCJwaW5nX2ludGVydmFsIiwibnVtYmVyIiwicmV0cmllcyIsImlzQ29tcG9uZW50IiwiYyIsInR5cGUiLCJoYXNPd25Qcm9wZXJ0eSIsImh5ZHJhdGVQcm9wcyIsInVwZGF0ZUFzcGVjdHMiLCJjb25uZWN0IiwiZGlzY29ubmVjdCIsInJlcGxhY2UiLCJPYmplY3QiLCJlbnRyaWVzIiwiZm9yRWFjaCIsImsiLCJ2IiwibWFwIiwibmV3UHJvcHMiLCJhc3BlY3RzIiwia2V5IiwiaWRlbnRpdHkiLCJoeWRyYXRlQ29tcG9uZW50IiwibmFtZSIsIm1lcmdlIiwicGFja2FnZV9uYW1lIiwicGFjayIsImVsZW1lbnQiLCJjcmVhdGVFbGVtZW50IiwicHJlcGFyZVByb3AiLCJwcm9wIiwiaXNWYWxpZEVsZW1lbnQiLCJvbWl0IiwiY29tcG9uZW50X25hbWUiLCJVcGRhdGVyIiwic3RhdGUiLCJsYXlvdXQiLCJyZWFkeSIsInBhZ2UiLCJiaW5kaW5ncyIsInBhY2thZ2VzIiwicmVxdWlyZW1lbnRzIiwicGFnZUFwaSIsImFwaVJlcXVlc3QiLCJnZXRIZWFkZXJzIiwiYmluZCIsInJlZnJlc2giLCJsb2NhdGlvbiIsImhyZWYiLCJib3VuZENvbXBvbmVudHMiLCJ3cyIsIm9uTWVzc2FnZSIsIlByb21pc2UiLCJyZXNvbHZlIiwia2V5cyIsImZpbHRlciIsImUiLCJiaW5kaW5nIiwic2VuZEJpbmRpbmciLCJ0cmlnZ2VyIiwiYXNwZWN0Iiwic2V0QXNwZWN0cyIsImdldEFzcGVjdCIsInJlc3BvbnNlIiwiZGF0YSIsIkpTT04iLCJwYXJzZSIsImtpbmQiLCJwYXlsb2FkIiwic3RvcmFnZSIsInJlcXVlc3RfaWQiLCJzdG9yZSIsInNlc3Npb25TdG9yYWdlIiwibG9jYWxTdG9yYWdlIiwiY29tcG9uZW50IiwiZXJyb3IiLCJzZW5kIiwic3RyaW5naWZ5IiwiY29uc29sZSIsInRoZW4iLCJ3YW50ZWQiLCJ2YWx1ZSIsInNldEl0ZW0iLCJnZXRJdGVtIiwic3RhdGVzIiwicmVqZWN0IiwibG9hZGluZ3MiLCJwYWNrX25hbWUiLCJjb25jYXQiLCJsb2FkUmVxdWlyZW1lbnQiLCJhbGwiLCJpIiwiaGFuZGxlciIsImxlbmd0aCIsInJlcXVpcmVtZW50IiwidXJsIiwibWV0YSIsIm1ldGhvZCIsImxvYWRTY3JpcHQiLCJsb2FkQ3NzIiwidHJpZXMiLCJjb25uZXhpb24iLCJXZWJTb2NrZXQiLCJzdGFydHNXaXRoIiwiaG9zdCIsInBhdGhuYW1lIiwiYWRkRXZlbnRMaXN0ZW5lciIsIm9ub3BlbiIsInNldFN0YXRlIiwib25jbG9zZSIsInJlY29ubmVjdCIsInNldFRpbWVvdXQiLCJsb2FkUmVxdWlyZW1lbnRzIiwiX2Nvbm5lY3RXUyIsIkVycm9yIiwiZGVmYXVsdFByb3BzIiwiV3JhcHBlciIsImluaXRpYWwiLCJjbG9uZUVsZW1lbnQiLCJjbGFzc19uYW1lIiwiam9pbiIsInRvTG93ZXJDYXNlIiwiY2FtZWxUb1NwaW5hbCIsInNwbGl0IiwiZnVuYyIsIm5vZGUiLCJyZW5kZXIiLCJSZWFjdERPTSIsImpzb25QYXR0ZXJuIiwiZGVmYXVsdFhock9wdGlvbnMiLCJoZWFkZXJzIiwianNvbiIsIkpTT05IRUFERVJTIiwieGhyUmVxdWVzdCIsIm9wdGlvbnMiLCJ4aHIiLCJYTUxIdHRwUmVxdWVzdCIsIm9wZW4iLCJoZWFkIiwic2V0UmVxdWVzdEhlYWRlciIsIm9ucmVhZHlzdGF0ZWNoYW5nZSIsInJlYWR5U3RhdGUiLCJET05FIiwic3RhdHVzIiwicmVzcG9uc2VWYWx1ZSIsInRlc3QiLCJnZXRSZXNwb25zZUhlYWRlciIsInJlc3BvbnNlVGV4dCIsIm1lc3NhZ2UiLCJzdGF0dXNUZXh0Iiwib25lcnJvciIsImVyciIsInJldHJpZWQiLCJhcmd1bWVudHMiXSwibWFwcGluZ3MiOiJBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLENBQUM7QUFDRCxPO0FDVkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxnQkFBUSxvQkFBb0I7QUFDNUI7QUFDQTtBQUNBO0FBQ0E7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QyxDQUFELENBQS9CO0FBQ0EsUUFBTW5CLE9BQU8sR0FBR21CLFNBQVMsQ0FBQyxDQUFELENBQVQsSUFBZ0IsRUFBaEM7QUFDQW5CLFdBQU8sQ0FBQ0osT0FBUixxQkFBc0J0RixVQUFVLEVBQWhDLEVBQXVDMEYsT0FBTyxDQUFDSixPQUEvQztBQUNBLFdBQU8sSUFBSTlFLE9BQUosQ0FBWSxVQUFDQyxPQUFELEVBQVVnQyxNQUFWLEVBQXFCO0FBQ3BDZ0QsZ0JBQVUsQ0FBQ3RDLEdBQUQsRUFBTXVDLE9BQU4sQ0FBVixDQUNLdkQsSUFETCxDQUNVMUIsT0FEVixXQUVXLFVBQUFrRyxHQUFHLEVBQUk7QUFDVixZQUFJQSxHQUFHLENBQUNSLE1BQUosS0FBZSxHQUFmLElBQXNCLENBQUNTLE9BQTNCLEVBQW9DO0FBQ2hDQSxpQkFBTyxHQUFHLElBQVY7QUFDQTFHLGlCQUFPLEdBQ0ZpQyxJQURMLENBQ1U7QUFBQSxtQkFDRnNELFVBQVUsQ0FBQ3RDLEdBQUQsb0JBQ0h1QyxPQURHO0FBRU5KLHFCQUFPLG9CQUNBSSxPQUFPLENBQUNKLE9BRFIsRUFFQXRGLFVBQVUsRUFGVjtBQUZELGVBQVYsQ0FNR21DLElBTkgsQ0FNUTFCLE9BTlIsQ0FERTtBQUFBLFdBRFYsV0FVV2dDLE1BVlg7QUFXSCxTQWJELE1BYU87QUFDSEEsZ0JBQU0sQ0FBQ2tFLEdBQUQsQ0FBTjtBQUNIO0FBQ0osT0FuQkw7QUFvQkgsS0FyQk0sQ0FBUDtBQXNCSCxHQTNCRDtBQTRCSCxDOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQzdHRCxtRDs7Ozs7Ozs7Ozs7QUNBQSx1RCIsImZpbGUiOiJkYXp6bGVyX3JlbmRlcmVyXzk0YmRkNTk2ZWRlMjE0M2I0ZTQ4LmpzIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIHdlYnBhY2tVbml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uKHJvb3QsIGZhY3RvcnkpIHtcblx0aWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnICYmIHR5cGVvZiBtb2R1bGUgPT09ICdvYmplY3QnKVxuXHRcdG1vZHVsZS5leHBvcnRzID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIiksIHJlcXVpcmUoXCJyZWFjdC1kb21cIikpO1xuXHRlbHNlIGlmKHR5cGVvZiBkZWZpbmUgPT09ICdmdW5jdGlvbicgJiYgZGVmaW5lLmFtZClcblx0XHRkZWZpbmUoW1wicmVhY3RcIiwgXCJyZWFjdC1kb21cIl0sIGZhY3RvcnkpO1xuXHRlbHNlIGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0Jylcblx0XHRleHBvcnRzW1wiZGF6emxlcl9yZW5kZXJlclwiXSA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpLCByZXF1aXJlKFwicmVhY3QtZG9tXCIpKTtcblx0ZWxzZVxuXHRcdHJvb3RbXCJkYXp6bGVyX3JlbmRlcmVyXCJdID0gZmFjdG9yeShyb290W1wiUmVhY3RcIl0sIHJvb3RbXCJSZWFjdERPTVwiXSk7XG59KSh3aW5kb3csIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXywgX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9kb21fXykge1xucmV0dXJuICIsIiBcdC8vIGluc3RhbGwgYSBKU09OUCBjYWxsYmFjayBmb3IgY2h1bmsgbG9hZGluZ1xuIFx0ZnVuY3Rpb24gd2VicGFja0pzb25wQ2FsbGJhY2soZGF0YSkge1xuIFx0XHR2YXIgY2h1bmtJZHMgPSBkYXRhWzBdO1xuIFx0XHR2YXIgbW9yZU1vZHVsZXMgPSBkYXRhWzFdO1xuIFx0XHR2YXIgZXhlY3V0ZU1vZHVsZXMgPSBkYXRhWzJdO1xuXG4gXHRcdC8vIGFkZCBcIm1vcmVNb2R1bGVzXCIgdG8gdGhlIG1vZHVsZXMgb2JqZWN0LFxuIFx0XHQvLyB0aGVuIGZsYWcgYWxsIFwiY2h1bmtJZHNcIiBhcyBsb2FkZWQgYW5kIGZpcmUgY2FsbGJhY2tcbiBcdFx0dmFyIG1vZHVsZUlkLCBjaHVua0lkLCBpID0gMCwgcmVzb2x2ZXMgPSBbXTtcbiBcdFx0Zm9yKDtpIDwgY2h1bmtJZHMubGVuZ3RoOyBpKyspIHtcbiBcdFx0XHRjaHVua0lkID0gY2h1bmtJZHNbaV07XG4gXHRcdFx0aWYoaW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRdKSB7XG4gXHRcdFx0XHRyZXNvbHZlcy5wdXNoKGluc3RhbGxlZENodW5rc1tjaHVua0lkXVswXSk7XG4gXHRcdFx0fVxuIFx0XHRcdGluc3RhbGxlZENodW5rc1tjaHVua0lkXSA9IDA7XG4gXHRcdH1cbiBcdFx0Zm9yKG1vZHVsZUlkIGluIG1vcmVNb2R1bGVzKSB7XG4gXHRcdFx0aWYoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG1vcmVNb2R1bGVzLCBtb2R1bGVJZCkpIHtcbiBcdFx0XHRcdG1vZHVsZXNbbW9kdWxlSWRdID0gbW9yZU1vZHVsZXNbbW9kdWxlSWRdO1xuIFx0XHRcdH1cbiBcdFx0fVxuIFx0XHRpZihwYXJlbnRKc29ucEZ1bmN0aW9uKSBwYXJlbnRKc29ucEZ1bmN0aW9uKGRhdGEpO1xuXG4gXHRcdHdoaWxlKHJlc29sdmVzLmxlbmd0aCkge1xuIFx0XHRcdHJlc29sdmVzLnNoaWZ0KCkoKTtcbiBcdFx0fVxuXG4gXHRcdC8vIGFkZCBlbnRyeSBtb2R1bGVzIGZyb20gbG9hZGVkIGNodW5rIHRvIGRlZmVycmVkIGxpc3RcbiBcdFx0ZGVmZXJyZWRNb2R1bGVzLnB1c2guYXBwbHkoZGVmZXJyZWRNb2R1bGVzLCBleGVjdXRlTW9kdWxlcyB8fCBbXSk7XG5cbiBcdFx0Ly8gcnVuIGRlZmVycmVkIG1vZHVsZXMgd2hlbiBhbGwgY2h1bmtzIHJlYWR5XG4gXHRcdHJldHVybiBjaGVja0RlZmVycmVkTW9kdWxlcygpO1xuIFx0fTtcbiBcdGZ1bmN0aW9uIGNoZWNrRGVmZXJyZWRNb2R1bGVzKCkge1xuIFx0XHR2YXIgcmVzdWx0O1xuIFx0XHRmb3IodmFyIGkgPSAwOyBpIDwgZGVmZXJyZWRNb2R1bGVzLmxlbmd0aDsgaSsrKSB7XG4gXHRcdFx0dmFyIGRlZmVycmVkTW9kdWxlID0gZGVmZXJyZWRNb2R1bGVzW2ldO1xuIFx0XHRcdHZhciBmdWxmaWxsZWQgPSB0cnVlO1xuIFx0XHRcdGZvcih2YXIgaiA9IDE7IGogPCBkZWZlcnJlZE1vZHVsZS5sZW5ndGg7IGorKykge1xuIFx0XHRcdFx0dmFyIGRlcElkID0gZGVmZXJyZWRNb2R1bGVbal07XG4gXHRcdFx0XHRpZihpbnN0YWxsZWRDaHVua3NbZGVwSWRdICE9PSAwKSBmdWxmaWxsZWQgPSBmYWxzZTtcbiBcdFx0XHR9XG4gXHRcdFx0aWYoZnVsZmlsbGVkKSB7XG4gXHRcdFx0XHRkZWZlcnJlZE1vZHVsZXMuc3BsaWNlKGktLSwgMSk7XG4gXHRcdFx0XHRyZXN1bHQgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKF9fd2VicGFja19yZXF1aXJlX18ucyA9IGRlZmVycmVkTW9kdWxlWzBdKTtcbiBcdFx0XHR9XG4gXHRcdH1cblxuIFx0XHRyZXR1cm4gcmVzdWx0O1xuIFx0fVxuXG4gXHQvLyBUaGUgbW9kdWxlIGNhY2hlXG4gXHR2YXIgaW5zdGFsbGVkTW9kdWxlcyA9IHt9O1xuXG4gXHQvLyBvYmplY3QgdG8gc3RvcmUgbG9hZGVkIGFuZCBsb2FkaW5nIGNodW5rc1xuIFx0Ly8gdW5kZWZpbmVkID0gY2h1bmsgbm90IGxvYWRlZCwgbnVsbCA9IGNodW5rIHByZWxvYWRlZC9wcmVmZXRjaGVkXG4gXHQvLyBQcm9taXNlID0gY2h1bmsgbG9hZGluZywgMCA9IGNodW5rIGxvYWRlZFxuIFx0dmFyIGluc3RhbGxlZENodW5rcyA9IHtcbiBcdFx0XCJyZW5kZXJlclwiOiAwXG4gXHR9O1xuXG4gXHR2YXIgZGVmZXJyZWRNb2R1bGVzID0gW107XG5cbiBcdC8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG4gXHRmdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cbiBcdFx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG4gXHRcdGlmKGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdKSB7XG4gXHRcdFx0cmV0dXJuIGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdLmV4cG9ydHM7XG4gXHRcdH1cbiBcdFx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcbiBcdFx0dmFyIG1vZHVsZSA9IGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdID0ge1xuIFx0XHRcdGk6IG1vZHVsZUlkLFxuIFx0XHRcdGw6IGZhbHNlLFxuIFx0XHRcdGV4cG9ydHM6IHt9XG4gXHRcdH07XG5cbiBcdFx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG4gXHRcdG1vZHVsZXNbbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG4gXHRcdC8vIEZsYWcgdGhlIG1vZHVsZSBhcyBsb2FkZWRcbiBcdFx0bW9kdWxlLmwgPSB0cnVlO1xuXG4gXHRcdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG4gXHRcdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbiBcdH1cblxuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZXMgb2JqZWN0IChfX3dlYnBhY2tfbW9kdWxlc19fKVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5tID0gbW9kdWxlcztcblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGUgY2FjaGVcbiBcdF9fd2VicGFja19yZXF1aXJlX18uYyA9IGluc3RhbGxlZE1vZHVsZXM7XG5cbiBcdC8vIGRlZmluZSBnZXR0ZXIgZnVuY3Rpb24gZm9yIGhhcm1vbnkgZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kID0gZnVuY3Rpb24oZXhwb3J0cywgbmFtZSwgZ2V0dGVyKSB7XG4gXHRcdGlmKCFfX3dlYnBhY2tfcmVxdWlyZV9fLm8oZXhwb3J0cywgbmFtZSkpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgbmFtZSwgeyBlbnVtZXJhYmxlOiB0cnVlLCBnZXQ6IGdldHRlciB9KTtcbiBcdFx0fVxuIFx0fTtcblxuIFx0Ly8gZGVmaW5lIF9fZXNNb2R1bGUgb24gZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yID0gZnVuY3Rpb24oZXhwb3J0cykge1xuIFx0XHRpZih0eXBlb2YgU3ltYm9sICE9PSAndW5kZWZpbmVkJyAmJiBTeW1ib2wudG9TdHJpbmdUYWcpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgU3ltYm9sLnRvU3RyaW5nVGFnLCB7IHZhbHVlOiAnTW9kdWxlJyB9KTtcbiBcdFx0fVxuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgJ19fZXNNb2R1bGUnLCB7IHZhbHVlOiB0cnVlIH0pO1xuIFx0fTtcblxuIFx0Ly8gY3JlYXRlIGEgZmFrZSBuYW1lc3BhY2Ugb2JqZWN0XG4gXHQvLyBtb2RlICYgMTogdmFsdWUgaXMgYSBtb2R1bGUgaWQsIHJlcXVpcmUgaXRcbiBcdC8vIG1vZGUgJiAyOiBtZXJnZSBhbGwgcHJvcGVydGllcyBvZiB2YWx1ZSBpbnRvIHRoZSBuc1xuIFx0Ly8gbW9kZSAmIDQ6IHJldHVybiB2YWx1ZSB3aGVuIGFscmVhZHkgbnMgb2JqZWN0XG4gXHQvLyBtb2RlICYgOHwxOiBiZWhhdmUgbGlrZSByZXF1aXJlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnQgPSBmdW5jdGlvbih2YWx1ZSwgbW9kZSkge1xuIFx0XHRpZihtb2RlICYgMSkgdmFsdWUgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKHZhbHVlKTtcbiBcdFx0aWYobW9kZSAmIDgpIHJldHVybiB2YWx1ZTtcbiBcdFx0aWYoKG1vZGUgJiA0KSAmJiB0eXBlb2YgdmFsdWUgPT09ICdvYmplY3QnICYmIHZhbHVlICYmIHZhbHVlLl9fZXNNb2R1bGUpIHJldHVybiB2YWx1ZTtcbiBcdFx0dmFyIG5zID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yKG5zKTtcbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KG5zLCAnZGVmYXVsdCcsIHsgZW51bWVyYWJsZTogdHJ1ZSwgdmFsdWU6IHZhbHVlIH0pO1xuIFx0XHRpZihtb2RlICYgMiAmJiB0eXBlb2YgdmFsdWUgIT0gJ3N0cmluZycpIGZvcih2YXIga2V5IGluIHZhbHVlKSBfX3dlYnBhY2tfcmVxdWlyZV9fLmQobnMsIGtleSwgZnVuY3Rpb24oa2V5KSB7IHJldHVybiB2YWx1ZVtrZXldOyB9LmJpbmQobnVsbCwga2V5KSk7XG4gXHRcdHJldHVybiBucztcbiBcdH07XG5cbiBcdC8vIGdldERlZmF1bHRFeHBvcnQgZnVuY3Rpb24gZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBub24taGFybW9ueSBtb2R1bGVzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm4gPSBmdW5jdGlvbihtb2R1bGUpIHtcbiBcdFx0dmFyIGdldHRlciA9IG1vZHVsZSAmJiBtb2R1bGUuX19lc01vZHVsZSA/XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0RGVmYXVsdCgpIHsgcmV0dXJuIG1vZHVsZVsnZGVmYXVsdCddOyB9IDpcbiBcdFx0XHRmdW5jdGlvbiBnZXRNb2R1bGVFeHBvcnRzKCkgeyByZXR1cm4gbW9kdWxlOyB9O1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQoZ2V0dGVyLCAnYScsIGdldHRlcik7XG4gXHRcdHJldHVybiBnZXR0ZXI7XG4gXHR9O1xuXG4gXHQvLyBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGxcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubyA9IGZ1bmN0aW9uKG9iamVjdCwgcHJvcGVydHkpIHsgcmV0dXJuIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChvYmplY3QsIHByb3BlcnR5KTsgfTtcblxuIFx0Ly8gX193ZWJwYWNrX3B1YmxpY19wYXRoX19cbiBcdF9fd2VicGFja19yZXF1aXJlX18ucCA9IFwiXCI7XG5cbiBcdHZhciBqc29ucEFycmF5ID0gd2luZG93W1wid2VicGFja0pzb25wZGF6emxlcl9uYW1lX1wiXSA9IHdpbmRvd1tcIndlYnBhY2tKc29ucGRhenpsZXJfbmFtZV9cIl0gfHwgW107XG4gXHR2YXIgb2xkSnNvbnBGdW5jdGlvbiA9IGpzb25wQXJyYXkucHVzaC5iaW5kKGpzb25wQXJyYXkpO1xuIFx0anNvbnBBcnJheS5wdXNoID0gd2VicGFja0pzb25wQ2FsbGJhY2s7XG4gXHRqc29ucEFycmF5ID0ganNvbnBBcnJheS5zbGljZSgpO1xuIFx0Zm9yKHZhciBpID0gMDsgaSA8IGpzb25wQXJyYXkubGVuZ3RoOyBpKyspIHdlYnBhY2tKc29ucENhbGxiYWNrKGpzb25wQXJyYXlbaV0pO1xuIFx0dmFyIHBhcmVudEpzb25wRnVuY3Rpb24gPSBvbGRKc29ucEZ1bmN0aW9uO1xuXG5cbiBcdC8vIGFkZCBlbnRyeSBtb2R1bGUgdG8gZGVmZXJyZWQgbGlzdFxuIFx0ZGVmZXJyZWRNb2R1bGVzLnB1c2goWzEsXCJjb21tb25zXCJdKTtcbiBcdC8vIHJ1biBkZWZlcnJlZCBtb2R1bGVzIHdoZW4gcmVhZHlcbiBcdHJldHVybiBjaGVja0RlZmVycmVkTW9kdWxlcygpO1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBVcGRhdGVyIGZyb20gJy4vVXBkYXRlcic7XG5pbXBvcnQgUHJvcFR5cGVzIGZyb20gJ3Byb3AtdHlwZXMnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBSZW5kZXJlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgY29tcG9uZW50V2lsbE1vdW50KCkge1xuICAgICAgICB3aW5kb3cuZGF6emxlcl9iYXNlX3VybCA9IHRoaXMucHJvcHMuYmFzZVVybDtcbiAgICB9XG5cbiAgICByZW5kZXIoKSB7XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItcmVuZGVyZXJcIj5cbiAgICAgICAgICAgICAgICA8VXBkYXRlciB7Li4udGhpcy5wcm9wc30gLz5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgIH1cbn1cblxuUmVuZGVyZXIucHJvcFR5cGVzID0ge1xuICAgIGJhc2VVcmw6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBwaW5nOiBQcm9wVHlwZXMuYm9vbCxcbiAgICBwaW5nX2ludGVydmFsOiBQcm9wVHlwZXMubnVtYmVyLFxuICAgIHJldHJpZXM6IFByb3BUeXBlcy5udW1iZXIsXG59O1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQge21lcmdlLCB0eXBlLCBvbWl0LCBtYXB9IGZyb20gJ3JhbWRhJztcbmltcG9ydCBXcmFwcGVyIGZyb20gJy4vV3JhcHBlcic7XG5pbXBvcnQge2FwaVJlcXVlc3R9IGZyb20gJy4uL3JlcXVlc3RzJztcbmltcG9ydCB7bG9hZENzcywgbG9hZFNjcmlwdH0gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcyc7XG5cbmZ1bmN0aW9uIGlzQ29tcG9uZW50KGMpIHtcbiAgICByZXR1cm4gKFxuICAgICAgICB0eXBlKGMpID09PSAnT2JqZWN0JyAmJlxuICAgICAgICAoYy5oYXNPd25Qcm9wZXJ0eSgncGFja2FnZScpICYmXG4gICAgICAgICAgICBjLmhhc093blByb3BlcnR5KCdhc3BlY3RzJykgJiZcbiAgICAgICAgICAgIGMuaGFzT3duUHJvcGVydHkoJ25hbWUnKSAmJlxuICAgICAgICAgICAgYy5oYXNPd25Qcm9wZXJ0eSgnaWRlbnRpdHknKSlcbiAgICApO1xufVxuXG5mdW5jdGlvbiBoeWRyYXRlUHJvcHMocHJvcHMsIHVwZGF0ZUFzcGVjdHMsIGNvbm5lY3QsIGRpc2Nvbm5lY3QpIHtcbiAgICBjb25zdCByZXBsYWNlID0ge307XG4gICAgT2JqZWN0LmVudHJpZXMocHJvcHMpLmZvckVhY2goKFtrLCB2XSkgPT4ge1xuICAgICAgICBpZiAodHlwZSh2KSA9PT0gJ0FycmF5Jykge1xuICAgICAgICAgICAgcmVwbGFjZVtrXSA9IHYubWFwKGMgPT4ge1xuICAgICAgICAgICAgICAgIGlmICghaXNDb21wb25lbnQoYykpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gTWl4aW5nIGNvbXBvbmVudHMgYW5kIHByaW1pdGl2ZXNcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGM7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGNvbnN0IG5ld1Byb3BzID0gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgICAgICBjLmFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGlmICghbmV3UHJvcHMua2V5KSB7XG4gICAgICAgICAgICAgICAgICAgIG5ld1Byb3BzLmtleSA9IGMuaWRlbnRpdHk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiBoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgICAgICAgICBjLm5hbWUsXG4gICAgICAgICAgICAgICAgICAgIGMucGFja2FnZSxcbiAgICAgICAgICAgICAgICAgICAgYy5pZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgbmV3UHJvcHMsXG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgIH0gZWxzZSBpZiAoaXNDb21wb25lbnQodikpIHtcbiAgICAgICAgICAgIGNvbnN0IG5ld1Byb3BzID0gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgIHYuYXNwZWN0cyxcbiAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgZGlzY29ubmVjdFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIHJlcGxhY2Vba10gPSBoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgICAgIHYubmFtZSxcbiAgICAgICAgICAgICAgICB2LnBhY2thZ2UsXG4gICAgICAgICAgICAgICAgdi5pZGVudGl0eSxcbiAgICAgICAgICAgICAgICBuZXdQcm9wcyxcbiAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgZGlzY29ubmVjdFxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSBlbHNlIGlmICh0eXBlKHYpID09PSAnT2JqZWN0Jykge1xuICAgICAgICAgICAgcmVwbGFjZVtrXSA9IGh5ZHJhdGVQcm9wcyh2LCB1cGRhdGVBc3BlY3RzLCBjb25uZWN0LCBkaXNjb25uZWN0KTtcbiAgICAgICAgfVxuICAgIH0pO1xuICAgIHJldHVybiBtZXJnZShwcm9wcywgcmVwbGFjZSk7XG59XG5cbmZ1bmN0aW9uIGh5ZHJhdGVDb21wb25lbnQoXG4gICAgbmFtZSxcbiAgICBwYWNrYWdlX25hbWUsXG4gICAgaWRlbnRpdHksXG4gICAgcHJvcHMsXG4gICAgdXBkYXRlQXNwZWN0cyxcbiAgICBjb25uZWN0LFxuICAgIGRpc2Nvbm5lY3Rcbikge1xuICAgIGNvbnN0IHBhY2sgPSB3aW5kb3dbcGFja2FnZV9uYW1lXTtcbiAgICBjb25zdCBlbGVtZW50ID0gUmVhY3QuY3JlYXRlRWxlbWVudChwYWNrW25hbWVdLCBwcm9wcyk7XG4gICAgcmV0dXJuIChcbiAgICAgICAgPFdyYXBwZXJcbiAgICAgICAgICAgIGlkZW50aXR5PXtpZGVudGl0eX1cbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHM9e3VwZGF0ZUFzcGVjdHN9XG4gICAgICAgICAgICBjb21wb25lbnQ9e2VsZW1lbnR9XG4gICAgICAgICAgICBjb25uZWN0PXtjb25uZWN0fVxuICAgICAgICAgICAgcGFja2FnZV9uYW1lPXtwYWNrYWdlX25hbWV9XG4gICAgICAgICAgICBjb21wb25lbnRfbmFtZT17bmFtZX1cbiAgICAgICAgICAgIGFzcGVjdHM9e3Byb3BzfVxuICAgICAgICAgICAgZGlzY29ubmVjdD17ZGlzY29ubmVjdH1cbiAgICAgICAgICAgIGtleT17YHdyYXBwZXItJHtpZGVudGl0eX1gfVxuICAgICAgICAvPlxuICAgICk7XG59XG5cbmZ1bmN0aW9uIHByZXBhcmVQcm9wKHByb3ApIHtcbiAgICBpZiAoUmVhY3QuaXNWYWxpZEVsZW1lbnQocHJvcCkpIHtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICAgIGlkZW50aXR5OiBwcm9wLnByb3BzLmlkZW50aXR5LFxuICAgICAgICAgICAgYXNwZWN0czogbWFwKFxuICAgICAgICAgICAgICAgIHByZXBhcmVQcm9wLFxuICAgICAgICAgICAgICAgIG9taXQoXG4gICAgICAgICAgICAgICAgICAgIFtcbiAgICAgICAgICAgICAgICAgICAgICAgICdpZGVudGl0eScsXG4gICAgICAgICAgICAgICAgICAgICAgICAndXBkYXRlQXNwZWN0cycsXG4gICAgICAgICAgICAgICAgICAgICAgICAnX25hbWUnLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ19wYWNrYWdlJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdhc3BlY3RzJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdrZXknLFxuICAgICAgICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgICAgICAgICBwcm9wLnByb3BzLmFzcGVjdHMgLy8gWW91IGFjdHVhbGx5IGluIHRoZSB3cmFwcGVyIGhlcmUuXG4gICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgKSxcbiAgICAgICAgICAgIG5hbWU6IHByb3AucHJvcHMuY29tcG9uZW50X25hbWUsXG4gICAgICAgICAgICBwYWNrYWdlOiBwcm9wLnByb3BzLnBhY2thZ2VfbmFtZSxcbiAgICAgICAgfTtcbiAgICB9XG4gICAgaWYgKHR5cGUocHJvcCkgPT09ICdBcnJheScpIHtcbiAgICAgICAgcmV0dXJuIHByb3AubWFwKHByZXBhcmVQcm9wKTtcbiAgICB9XG4gICAgaWYgKHR5cGUocHJvcCkgPT09ICdPYmplY3QnKSB7XG4gICAgICAgIHJldHVybiBtYXAocHJlcGFyZVByb3AsIHByb3ApO1xuICAgIH1cbiAgICByZXR1cm4gcHJvcDtcbn1cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVXBkYXRlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgbGF5b3V0OiBmYWxzZSxcbiAgICAgICAgICAgIHJlYWR5OiBmYWxzZSxcbiAgICAgICAgICAgIHBhZ2U6IG51bGwsXG4gICAgICAgICAgICBiaW5kaW5nczoge30sXG4gICAgICAgICAgICBwYWNrYWdlczogW10sXG4gICAgICAgICAgICByZXF1aXJlbWVudHM6IFtdLFxuICAgICAgICB9O1xuICAgICAgICAvLyBUaGUgYXBpIHVybCBmb3IgdGhlIHBhZ2UgaXMgdGhlIHNhbWUgYnV0IGEgcG9zdC5cbiAgICAgICAgLy8gRmV0Y2ggYmluZGluZ3MsIHBhY2thZ2VzICYgcmVxdWlyZW1lbnRzXG4gICAgICAgIHRoaXMucGFnZUFwaSA9IGFwaVJlcXVlc3QoXG4gICAgICAgICAgICB0aGlzLmdldEhlYWRlcnMuYmluZCh0aGlzKSxcbiAgICAgICAgICAgIHRoaXMucmVmcmVzaC5iaW5kKHRoaXMpLFxuICAgICAgICAgICAgd2luZG93LmxvY2F0aW9uLmhyZWZcbiAgICAgICAgKTtcbiAgICAgICAgLy8gQWxsIGNvbXBvbmVudHMgZ2V0IGNvbm5lY3RlZC5cbiAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHMgPSB7fTtcbiAgICAgICAgdGhpcy53cyA9IG51bGw7XG5cbiAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzID0gdGhpcy51cGRhdGVBc3BlY3RzLmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMuY29ubmVjdCA9IHRoaXMuY29ubmVjdC5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLmRpc2Nvbm5lY3QgPSB0aGlzLmRpc2Nvbm5lY3QuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5vbk1lc3NhZ2UgPSB0aGlzLm9uTWVzc2FnZS5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIHVwZGF0ZUFzcGVjdHMoaWRlbnRpdHksIGFzcGVjdHMpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKHJlc29sdmUgPT4ge1xuICAgICAgICAgICAgY29uc3QgYmluZGluZ3MgPSBPYmplY3Qua2V5cyhhc3BlY3RzKVxuICAgICAgICAgICAgICAgIC5tYXAoa2V5ID0+IHRoaXMuc3RhdGUuYmluZGluZ3NbYCR7aWRlbnRpdHl9LiR7a2V5fWBdKVxuICAgICAgICAgICAgICAgIC5maWx0ZXIoZSA9PiBlKTtcblxuICAgICAgICAgICAgaWYgKCFiaW5kaW5ncykge1xuICAgICAgICAgICAgICAgIHJldHVybiByZXNvbHZlKDApO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICBiaW5kaW5ncy5mb3JFYWNoKGJpbmRpbmcgPT5cbiAgICAgICAgICAgICAgICB0aGlzLnNlbmRCaW5kaW5nKGJpbmRpbmcsIGFzcGVjdHNbYmluZGluZy50cmlnZ2VyLmFzcGVjdF0pXG4gICAgICAgICAgICApO1xuICAgICAgICAgICAgcmVzb2x2ZSgpO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBjb25uZWN0KGlkZW50aXR5LCBzZXRBc3BlY3RzLCBnZXRBc3BlY3QpIHtcbiAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldID0ge1xuICAgICAgICAgICAgc2V0QXNwZWN0cyxcbiAgICAgICAgICAgIGdldEFzcGVjdCxcbiAgICAgICAgfTtcbiAgICB9XG5cbiAgICBkaXNjb25uZWN0KGlkZW50aXR5KSB7XG4gICAgICAgIGRlbGV0ZSB0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV07XG4gICAgfVxuXG4gICAgb25NZXNzYWdlKHJlc3BvbnNlKSB7XG4gICAgICAgIGNvbnN0IGRhdGEgPSBKU09OLnBhcnNlKHJlc3BvbnNlLmRhdGEpO1xuICAgICAgICBjb25zdCB7aWRlbnRpdHksIGtpbmQsIHBheWxvYWQsIHN0b3JhZ2UsIHJlcXVlc3RfaWR9ID0gZGF0YTtcbiAgICAgICAgbGV0IHN0b3JlO1xuICAgICAgICBpZiAoc3RvcmFnZSA9PT0gJ3Nlc3Npb24nKSB7XG4gICAgICAgICAgICBzdG9yZSA9IHdpbmRvdy5zZXNzaW9uU3RvcmFnZTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHN0b3JlID0gd2luZG93LmxvY2FsU3RvcmFnZTtcbiAgICAgICAgfVxuICAgICAgICBzd2l0Y2ggKGtpbmQpIHtcbiAgICAgICAgICAgIGNhc2UgJ3NldC1hc3BlY3QnOlxuICAgICAgICAgICAgICAgIGNvbnN0IGNvbXBvbmVudCA9IHRoaXMuYm91bmRDb21wb25lbnRzW2lkZW50aXR5XTtcbiAgICAgICAgICAgICAgICBpZiAoIWNvbXBvbmVudCkge1xuICAgICAgICAgICAgICAgICAgICBjb25zdCBlcnJvciA9IGBDb21wb25lbnQgbm90IGZvdW5kOiAke2lkZW50aXR5fWA7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChKU09OLnN0cmluZ2lmeSh7ZXJyb3IsIGtpbmQ6ICdlcnJvcid9KSk7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoZXJyb3IpO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICAgICAgY29tcG9uZW50XG4gICAgICAgICAgICAgICAgICAgIC5zZXRBc3BlY3RzKFxuICAgICAgICAgICAgICAgICAgICAgICAgaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBheWxvYWQsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuY29ubmVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBPYmplY3Qua2V5cyhwYXlsb2FkKS5mb3JFYWNoKGsgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbnN0IGtleSA9IGAke2lkZW50aXR5fS4ke2t9YDtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb25zdCBiaW5kaW5nID0gdGhpcy5zdGF0ZS5iaW5kaW5nc1trZXldO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIChiaW5kaW5nKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc2VuZEJpbmRpbmcoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBiaW5kaW5nLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY29tcG9uZW50LmdldEFzcGVjdChrKVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAvLyBXaGF0IGFib3V0IHJldHVybmVkIGNvbXBvbmVudHMgP1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIC8vIFRoZXkgZ2V0IHRoZWlyIFdyYXBwZXIuXG4gICAgICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdnZXQtYXNwZWN0JzpcbiAgICAgICAgICAgICAgICBjb25zdCB7YXNwZWN0fSA9IGRhdGE7XG4gICAgICAgICAgICAgICAgY29uc3Qgd2FudGVkID0gdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldO1xuICAgICAgICAgICAgICAgIGlmICghd2FudGVkKSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBraW5kLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVycm9yOiBgQXNwZWN0IG5vdCBmb3VuZCAke2lkZW50aXR5fS4ke2FzcGVjdH1gLFxuICAgICAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBjb25zdCB2YWx1ZSA9IHdhbnRlZC5nZXRBc3BlY3QoYXNwZWN0KTtcbiAgICAgICAgICAgICAgICB0aGlzLndzLnNlbmQoXG4gICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGtpbmQsXG4gICAgICAgICAgICAgICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBwcmVwYXJlUHJvcCh2YWx1ZSksXG4gICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdzZXQtc3RvcmFnZSc6XG4gICAgICAgICAgICAgICAgc3RvcmUuc2V0SXRlbShpZGVudGl0eSwgSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkpO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAnZ2V0LXN0b3JhZ2UnOlxuICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgICAgICAgICAgICAgICAga2luZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdF9pZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBKU09OLnBhcnNlKHN0b3JlLmdldEl0ZW0oaWRlbnRpdHkpKSxcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAncGluZyc6XG4gICAgICAgICAgICAgICAgLy8gSnVzdCBkbyBub3RoaW5nLlxuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgc2VuZEJpbmRpbmcoYmluZGluZywgdmFsdWUpIHtcbiAgICAgICAgLy8gQ29sbGVjdCBhbGwgdmFsdWVzIGFuZCBzZW5kIGEgYmluZGluZyBwYXlsb2FkXG4gICAgICAgIGNvbnN0IHRyaWdnZXIgPSB7XG4gICAgICAgICAgICAuLi5iaW5kaW5nLnRyaWdnZXIsXG4gICAgICAgICAgICB2YWx1ZTogcHJlcGFyZVByb3AodmFsdWUpLFxuICAgICAgICB9O1xuICAgICAgICBjb25zdCBzdGF0ZXMgPSBiaW5kaW5nLnN0YXRlcy5tYXAoc3RhdGUgPT4gKHtcbiAgICAgICAgICAgIC4uLnN0YXRlLFxuICAgICAgICAgICAgdmFsdWU6XG4gICAgICAgICAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHNbc3RhdGUuaWRlbnRpdHldICYmXG4gICAgICAgICAgICAgICAgcHJlcGFyZVByb3AoXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW3N0YXRlLmlkZW50aXR5XS5nZXRBc3BlY3Qoc3RhdGUuYXNwZWN0KVxuICAgICAgICAgICAgICAgICksXG4gICAgICAgIH0pKTtcblxuICAgICAgICBjb25zdCBwYXlsb2FkID0ge1xuICAgICAgICAgICAgdHJpZ2dlcixcbiAgICAgICAgICAgIHN0YXRlcyxcbiAgICAgICAgICAgIGtpbmQ6ICdiaW5kaW5nJyxcbiAgICAgICAgICAgIHBhZ2U6IHRoaXMuc3RhdGUucGFnZSxcbiAgICAgICAgICAgIGtleTogYmluZGluZy5rZXksXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMud3Muc2VuZChKU09OLnN0cmluZ2lmeShwYXlsb2FkKSk7XG4gICAgfVxuXG4gICAgbG9hZFJlcXVpcmVtZW50cyhyZXF1aXJlbWVudHMsIHBhY2thZ2VzKSB7XG4gICAgICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICAgICAgICBsZXQgbG9hZGluZ3MgPSBbXTtcbiAgICAgICAgICAgIC8vIExvYWQgcGFja2FnZXMgZmlyc3QuXG4gICAgICAgICAgICBPYmplY3Qua2V5cyhwYWNrYWdlcykuZm9yRWFjaChwYWNrX25hbWUgPT4ge1xuICAgICAgICAgICAgICAgIGNvbnN0IHBhY2sgPSBwYWNrYWdlc1twYWNrX25hbWVdO1xuICAgICAgICAgICAgICAgIGxvYWRpbmdzID0gbG9hZGluZ3MuY29uY2F0KFxuICAgICAgICAgICAgICAgICAgICBwYWNrLnJlcXVpcmVtZW50cy5tYXAodGhpcy5sb2FkUmVxdWlyZW1lbnQpXG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgLy8gVGhlbiBsb2FkIHJlcXVpcmVtZW50cyBzbyB0aGV5IGNhbiB1c2UgcGFja2FnZXNcbiAgICAgICAgICAgIC8vIGFuZCBvdmVycmlkZSBjc3MuXG4gICAgICAgICAgICBQcm9taXNlLmFsbChsb2FkaW5ncylcbiAgICAgICAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIGxldCBpID0gMDtcbiAgICAgICAgICAgICAgICAgICAgLy8gTG9hZCBpbiBvcmRlci5cbiAgICAgICAgICAgICAgICAgICAgY29uc3QgaGFuZGxlciA9ICgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChpIDwgcmVxdWlyZW1lbnRzLmxlbmd0aCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMubG9hZFJlcXVpcmVtZW50KHJlcXVpcmVtZW50c1tpXSkudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGkrKztcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaGFuZGxlcigpO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXNvbHZlKCk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIH07XG4gICAgICAgICAgICAgICAgICAgIGhhbmRsZXIoKTtcbiAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgIC5jYXRjaChyZWplY3QpO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBsb2FkUmVxdWlyZW1lbnQocmVxdWlyZW1lbnQpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgICAgICAgIGNvbnN0IHt1cmwsIGtpbmQsIG1ldGF9ID0gcmVxdWlyZW1lbnQ7XG4gICAgICAgICAgICBsZXQgbWV0aG9kO1xuICAgICAgICAgICAgaWYgKGtpbmQgPT09ICdqcycpIHtcbiAgICAgICAgICAgICAgICBtZXRob2QgPSBsb2FkU2NyaXB0O1xuICAgICAgICAgICAgfSBlbHNlIGlmIChraW5kID09PSAnY3NzJykge1xuICAgICAgICAgICAgICAgIG1ldGhvZCA9IGxvYWRDc3M7XG4gICAgICAgICAgICB9IGVsc2UgaWYgKGtpbmQgPT09ICdtYXAnKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHJlc29sdmUoKTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHJlamVjdCh7ZXJyb3I6IGBJbnZhbGlkIHJlcXVpcmVtZW50IGtpbmQ6ICR7a2luZH1gfSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBtZXRob2QodXJsLCBtZXRhKVxuICAgICAgICAgICAgICAgIC50aGVuKHJlc29sdmUpXG4gICAgICAgICAgICAgICAgLmNhdGNoKHJlamVjdCk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIF9jb25uZWN0V1MoKSB7XG4gICAgICAgIC8vIFNldHVwIHdlYnNvY2tldCBmb3IgdXBkYXRlc1xuICAgICAgICBsZXQgdHJpZXMgPSAwO1xuICAgICAgICBjb25zdCBjb25uZXhpb24gPSAoKSA9PiB7XG4gICAgICAgICAgICB0aGlzLndzID0gbmV3IFdlYlNvY2tldChcbiAgICAgICAgICAgICAgICBgd3Mke1xuICAgICAgICAgICAgICAgICAgICB3aW5kb3cubG9jYXRpb24uaHJlZi5zdGFydHNXaXRoKCdodHRwcycpID8gJ3MnIDogJydcbiAgICAgICAgICAgICAgICB9Oi8vJHsodGhpcy5wcm9wcy5iYXNlVXJsICYmIHRoaXMucHJvcHMuYmFzZVVybCkgfHxcbiAgICAgICAgICAgICAgICAgICAgd2luZG93LmxvY2F0aW9uLmhvc3R9JHt3aW5kb3cubG9jYXRpb24ucGF0aG5hbWV9L3dzYFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIHRoaXMud3MuYWRkRXZlbnRMaXN0ZW5lcignbWVzc2FnZScsIHRoaXMub25NZXNzYWdlKTtcbiAgICAgICAgICAgIHRoaXMud3Mub25vcGVuID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe3JlYWR5OiB0cnVlfSk7XG4gICAgICAgICAgICAgICAgdHJpZXMgPSAwO1xuICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIHRoaXMud3Mub25jbG9zZSA9ICgpID0+IHtcbiAgICAgICAgICAgICAgICBjb25zdCByZWNvbm5lY3QgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIHRyaWVzKys7XG4gICAgICAgICAgICAgICAgICAgIGNvbm5leGlvbigpO1xuICAgICAgICAgICAgICAgIH07XG4gICAgICAgICAgICAgICAgaWYgKHRyaWVzIDwgdGhpcy5wcm9wcy5yZXRyaWVzKSB7XG4gICAgICAgICAgICAgICAgICAgIHNldFRpbWVvdXQocmVjb25uZWN0LCAxMDAwKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9O1xuICAgICAgICB9O1xuICAgICAgICBjb25uZXhpb24oKTtcbiAgICB9XG5cbiAgICAvLyBUT0RPIGltcGxlbWVudCBvciByZW1vdmUgZGVwZW5kZW5jZSBvbiB0aGVzZSBmdW5jdGlvbnMuXG4gICAgZ2V0SGVhZGVycygpIHtcbiAgICAgICAgcmV0dXJuIHt9O1xuICAgIH1cbiAgICByZWZyZXNoKCkge31cblxuICAgIGNvbXBvbmVudFdpbGxNb3VudCgpIHtcbiAgICAgICAgdGhpcy5wYWdlQXBpKCcnLCB7bWV0aG9kOiAnUE9TVCd9KS50aGVuKHJlc3BvbnNlID0+IHtcbiAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICAgICAgIHBhZ2U6IHJlc3BvbnNlLnBhZ2UsXG4gICAgICAgICAgICAgICAgbGF5b3V0OiByZXNwb25zZS5sYXlvdXQsXG4gICAgICAgICAgICAgICAgYmluZGluZ3M6IHJlc3BvbnNlLmJpbmRpbmdzLFxuICAgICAgICAgICAgICAgIHBhY2thZ2VzOiByZXNwb25zZS5wYWNrYWdlcyxcbiAgICAgICAgICAgICAgICByZXF1aXJlbWVudHM6IHJlc3BvbnNlLnJlcXVpcmVtZW50cyxcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgdGhpcy5sb2FkUmVxdWlyZW1lbnRzKFxuICAgICAgICAgICAgICAgIHJlc3BvbnNlLnJlcXVpcmVtZW50cyxcbiAgICAgICAgICAgICAgICByZXNwb25zZS5wYWNrYWdlc1xuICAgICAgICAgICAgKS50aGVuKCgpID0+IHRoaXMuX2Nvbm5lY3RXUygpKTtcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7bGF5b3V0LCByZWFkeX0gPSB0aGlzLnN0YXRlO1xuICAgICAgICBpZiAoIXJlYWR5KSByZXR1cm4gPGRpdj5Mb2FkaW5nLi4uPC9kaXY+O1xuICAgICAgICBpZiAoIWlzQ29tcG9uZW50KGxheW91dCkpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcihgTGF5b3V0IGlzIG5vdCBhIGNvbXBvbmVudDogJHtsYXlvdXR9YCk7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJkYXp6bGVyLXJlbmRlcmVkXCI+XG4gICAgICAgICAgICAgICAge2h5ZHJhdGVDb21wb25lbnQoXG4gICAgICAgICAgICAgICAgICAgIGxheW91dC5uYW1lLFxuICAgICAgICAgICAgICAgICAgICBsYXlvdXQucGFja2FnZSxcbiAgICAgICAgICAgICAgICAgICAgbGF5b3V0LmlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICBoeWRyYXRlUHJvcHMoXG4gICAgICAgICAgICAgICAgICAgICAgICBsYXlvdXQuYXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuY29ubmVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuZGlzY29ubmVjdFxuICAgICAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY29ubmVjdCxcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5kaXNjb25uZWN0XG4gICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgIH1cbn1cblxuVXBkYXRlci5kZWZhdWx0UHJvcHMgPSB7fTtcblxuVXBkYXRlci5wcm9wVHlwZXMgPSB7XG4gICAgYmFzZVVybDogUHJvcFR5cGVzLnN0cmluZy5pc1JlcXVpcmVkLFxuICAgIHBpbmc6IFByb3BUeXBlcy5ib29sLFxuICAgIHBpbmdfaW50ZXJ2YWw6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgcmV0cmllczogUHJvcFR5cGVzLm51bWJlcixcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcbmltcG9ydCB7Y29uY2F0LCBqb2lufSBmcm9tICdyYW1kYSc7XG5pbXBvcnQge2NhbWVsVG9TcGluYWx9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMnO1xuXG4vKipcbiAqIFdyYXBzIGNvbXBvbmVudHMgZm9yIGFzcGVjdHMgdXBkYXRpbmcuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFdyYXBwZXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIGFzcGVjdHM6IHByb3BzLmFzcGVjdHMgfHwge30sXG4gICAgICAgICAgICByZWFkeTogZmFsc2UsXG4gICAgICAgICAgICBpbml0aWFsOiBmYWxzZSxcbiAgICAgICAgfTtcbiAgICAgICAgdGhpcy5zZXRBc3BlY3RzID0gdGhpcy5zZXRBc3BlY3RzLmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMuZ2V0QXNwZWN0ID0gdGhpcy5nZXRBc3BlY3QuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzID0gdGhpcy51cGRhdGVBc3BlY3RzLmJpbmQodGhpcyk7XG4gICAgfVxuXG4gICAgdXBkYXRlQXNwZWN0cyhhc3BlY3RzKSB7XG4gICAgICAgIHJldHVybiB0aGlzLnNldEFzcGVjdHMoYXNwZWN0cykudGhlbigoKSA9PlxuICAgICAgICAgICAgdGhpcy5wcm9wcy51cGRhdGVBc3BlY3RzKHRoaXMucHJvcHMuaWRlbnRpdHksIGFzcGVjdHMpXG4gICAgICAgICk7XG4gICAgfVxuXG4gICAgc2V0QXNwZWN0cyhhc3BlY3RzKSB7XG4gICAgICAgIHJldHVybiBuZXcgUHJvbWlzZShyZXNvbHZlID0+IHtcbiAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoXG4gICAgICAgICAgICAgICAge2FzcGVjdHM6IHsuLi50aGlzLnN0YXRlLmFzcGVjdHMsIC4uLmFzcGVjdHN9fSxcbiAgICAgICAgICAgICAgICByZXNvbHZlXG4gICAgICAgICAgICApO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBnZXRBc3BlY3QoYXNwZWN0KSB7XG4gICAgICAgIHJldHVybiB0aGlzLnN0YXRlLmFzcGVjdHNbYXNwZWN0XTtcbiAgICB9XG5cbiAgICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICAgICAgLy8gT25seSB1cGRhdGUgdGhlIGNvbXBvbmVudCB3aGVuIG1vdW50ZWQuXG4gICAgICAgIC8vIE90aGVyd2lzZSBnZXRzIGEgcmFjZSBjb25kaXRpb24gd2l0aCB3aWxsVW5tb3VudFxuICAgICAgICB0aGlzLnByb3BzLmNvbm5lY3QoXG4gICAgICAgICAgICB0aGlzLnByb3BzLmlkZW50aXR5LFxuICAgICAgICAgICAgdGhpcy5zZXRBc3BlY3RzLFxuICAgICAgICAgICAgdGhpcy5nZXRBc3BlY3RcbiAgICAgICAgKTtcbiAgICAgICAgaWYgKCF0aGlzLnN0YXRlLmluaXRpYWwpIHtcbiAgICAgICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyh0aGlzLnN0YXRlLmFzcGVjdHMpLnRoZW4oKCkgPT5cbiAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtyZWFkeTogdHJ1ZSwgaW5pdGlhbDogdHJ1ZX0pXG4gICAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgY29tcG9uZW50V2lsbFVubW91bnQoKSB7XG4gICAgICAgIHRoaXMucHJvcHMuZGlzY29ubmVjdCh0aGlzLnByb3BzLmlkZW50aXR5KTtcbiAgICB9XG5cbiAgICByZW5kZXIoKSB7XG4gICAgICAgIGNvbnN0IHtjb21wb25lbnQsIGNvbXBvbmVudF9uYW1lLCBwYWNrYWdlX25hbWV9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgY29uc3Qge2FzcGVjdHMsIHJlYWR5fSA9IHRoaXMuc3RhdGU7XG4gICAgICAgIGlmICghcmVhZHkpIHJldHVybiBudWxsO1xuXG4gICAgICAgIHJldHVybiBSZWFjdC5jbG9uZUVsZW1lbnQoY29tcG9uZW50LCB7XG4gICAgICAgICAgICAuLi5hc3BlY3RzLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0czogdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgaWRlbnRpdHk6IHRoaXMucHJvcHMuaWRlbnRpdHksXG4gICAgICAgICAgICBjbGFzc19uYW1lOiBqb2luKFxuICAgICAgICAgICAgICAgICcgJyxcbiAgICAgICAgICAgICAgICBjb25jYXQoXG4gICAgICAgICAgICAgICAgICAgIFtcbiAgICAgICAgICAgICAgICAgICAgICAgIGAke3BhY2thZ2VfbmFtZVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5yZXBsYWNlKCdfJywgJy0nKVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIC50b0xvd2VyQ2FzZSgpfS0ke2NhbWVsVG9TcGluYWwoY29tcG9uZW50X25hbWUpfWAsXG4gICAgICAgICAgICAgICAgICAgIF0sXG4gICAgICAgICAgICAgICAgICAgIGFzcGVjdHMuY2xhc3NfbmFtZSA/IGFzcGVjdHMuY2xhc3NfbmFtZS5zcGxpdCgnICcpIDogW11cbiAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICApLFxuICAgICAgICB9KTtcbiAgICB9XG59XG5cbldyYXBwZXIucHJvcFR5cGVzID0ge1xuICAgIGlkZW50aXR5OiBQcm9wVHlwZXMuc3RyaW5nLmlzUmVxdWlyZWQsXG4gICAgdXBkYXRlQXNwZWN0czogUHJvcFR5cGVzLmZ1bmMuaXNSZXF1aXJlZCxcbiAgICBjb21wb25lbnQ6IFByb3BUeXBlcy5ub2RlLmlzUmVxdWlyZWQsXG4gICAgY29ubmVjdDogUHJvcFR5cGVzLmZ1bmMuaXNSZXF1aXJlZCxcbiAgICBjb21wb25lbnRfbmFtZTogUHJvcFR5cGVzLnN0cmluZy5pc1JlcXVpcmVkLFxuICAgIHBhY2thZ2VfbmFtZTogUHJvcFR5cGVzLnN0cmluZy5pc1JlcXVpcmVkLFxuICAgIGRpc2Nvbm5lY3Q6IFByb3BUeXBlcy5mdW5jLmlzUmVxdWlyZWQsXG59O1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IFJlbmRlcmVyIGZyb20gJy4vY29tcG9uZW50cy9SZW5kZXJlcic7XG5cbmZ1bmN0aW9uIHJlbmRlcih7YmFzZVVybCwgcGluZywgcGluZ19pbnRlcnZhbCwgcmV0cmllc30sIGVsZW1lbnQpIHtcbiAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICAgIDxSZW5kZXJlclxuICAgICAgICAgICAgYmFzZVVybD17YmFzZVVybH1cbiAgICAgICAgICAgIHBpbmc9e3Bpbmd9XG4gICAgICAgICAgICBwaW5nX2ludGVydmFsPXtwaW5nX2ludGVydmFsfVxuICAgICAgICAgICAgcmV0cmllcz17cmV0cmllc31cbiAgICAgICAgLz4sXG4gICAgICAgIGVsZW1lbnRcbiAgICApO1xufVxuXG5leHBvcnQge1JlbmRlcmVyLCByZW5kZXJ9O1xuIiwiLyogZXNsaW50LWRpc2FibGUgbm8tbWFnaWMtbnVtYmVycyAqL1xuXG5jb25zdCBqc29uUGF0dGVybiA9IC9qc29uL2k7XG5cbi8qKlxuICogQHR5cGVkZWYge09iamVjdH0gWGhyT3B0aW9uc1xuICogQHByb3BlcnR5IHtzdHJpbmd9IFttZXRob2Q9J0dFVCddXG4gKiBAcHJvcGVydHkge09iamVjdH0gW2hlYWRlcnM9e31dXG4gKiBAcHJvcGVydHkge3N0cmluZ3xCbG9ifEFycmF5QnVmZmVyfG9iamVjdHxBcnJheX0gW3BheWxvYWQ9JyddXG4gKi9cblxuLyoqXG4gKiBAdHlwZSB7WGhyT3B0aW9uc31cbiAqL1xuY29uc3QgZGVmYXVsdFhock9wdGlvbnMgPSB7XG4gICAgbWV0aG9kOiAnR0VUJyxcbiAgICBoZWFkZXJzOiB7fSxcbiAgICBwYXlsb2FkOiAnJyxcbiAgICBqc29uOiB0cnVlLFxufTtcblxuZXhwb3J0IGNvbnN0IEpTT05IRUFERVJTID0ge1xuICAgICdDb250ZW50LVR5cGUnOiAnYXBwbGljYXRpb24vanNvbicsXG59O1xuXG4vKipcbiAqIFhociBwcm9taXNlIHdyYXAuXG4gKlxuICogRmV0Y2ggY2FuJ3QgZG8gcHV0IHJlcXVlc3QsIHNvIHhociBzdGlsbCB1c2VmdWwuXG4gKlxuICogQXV0byBwYXJzZSBqc29uIHJlc3BvbnNlcy5cbiAqIENhbmNlbGxhdGlvbjogeGhyLmFib3J0XG4gKiBAcGFyYW0ge3N0cmluZ30gdXJsXG4gKiBAcGFyYW0ge1hock9wdGlvbnN9IFtvcHRpb25zXVxuICogQHJldHVybiB7UHJvbWlzZX1cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHhoclJlcXVlc3QodXJsLCBvcHRpb25zID0gZGVmYXVsdFhock9wdGlvbnMpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7bWV0aG9kLCBoZWFkZXJzLCBwYXlsb2FkLCBqc29ufSA9IHtcbiAgICAgICAgICAgIC4uLmRlZmF1bHRYaHJPcHRpb25zLFxuICAgICAgICAgICAgLi4ub3B0aW9ucyxcbiAgICAgICAgfTtcbiAgICAgICAgY29uc3QgeGhyID0gbmV3IFhNTEh0dHBSZXF1ZXN0KCk7XG4gICAgICAgIHhoci5vcGVuKG1ldGhvZCwgdXJsKTtcbiAgICAgICAgY29uc3QgaGVhZCA9IGpzb24gPyB7Li4uSlNPTkhFQURFUlMsIC4uLmhlYWRlcnN9IDogaGVhZGVycztcbiAgICAgICAgT2JqZWN0LmtleXMoaGVhZCkuZm9yRWFjaChrID0+IHhoci5zZXRSZXF1ZXN0SGVhZGVyKGssIGhlYWRba10pKTtcbiAgICAgICAgeGhyLm9ucmVhZHlzdGF0ZWNoYW5nZSA9ICgpID0+IHtcbiAgICAgICAgICAgIGlmICh4aHIucmVhZHlTdGF0ZSA9PT0gWE1MSHR0cFJlcXVlc3QuRE9ORSkge1xuICAgICAgICAgICAgICAgIGlmICh4aHIuc3RhdHVzIDwgNDAwKSB7XG4gICAgICAgICAgICAgICAgICAgIGxldCByZXNwb25zZVZhbHVlID0geGhyLnJlc3BvbnNlO1xuICAgICAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICAgICBqc29uUGF0dGVybi50ZXN0KHhoci5nZXRSZXNwb25zZUhlYWRlcignQ29udGVudC1UeXBlJykpXG4gICAgICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2VWYWx1ZSA9IEpTT04ucGFyc2UoeGhyLnJlc3BvbnNlVGV4dCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgcmVzb2x2ZShyZXNwb25zZVZhbHVlKTtcbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICByZWplY3Qoe1xuICAgICAgICAgICAgICAgICAgICAgICAgZXJyb3I6ICdSZXF1ZXN0RXJyb3InLFxuICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZTogYFhIUiAke3VybH0gRkFJTEVEIC0gU1RBVFVTOiAke1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHhoci5zdGF0dXNcbiAgICAgICAgICAgICAgICAgICAgICAgIH0gTUVTU0FHRTogJHt4aHIuc3RhdHVzVGV4dH1gLFxuICAgICAgICAgICAgICAgICAgICAgICAgc3RhdHVzOiB4aHIuc3RhdHVzLFxuICAgICAgICAgICAgICAgICAgICAgICAgeGhyLFxuICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgICAgIHhoci5vbmVycm9yID0gZXJyID0+IHJlamVjdChlcnIpO1xuICAgICAgICB4aHIuc2VuZChqc29uID8gSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkgOiBwYXlsb2FkKTtcbiAgICB9KTtcbn1cblxuLyoqXG4gKiBBdXRvIGdldCBoZWFkZXJzIGFuZCByZWZyZXNoL3JldHJ5LlxuICpcbiAqIEBwYXJhbSB7ZnVuY3Rpb259IGdldEhlYWRlcnNcbiAqIEBwYXJhbSB7ZnVuY3Rpb259IHJlZnJlc2hcbiAqIEBwYXJhbSB7c3RyaW5nfSBiYXNlVXJsXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBhcGlSZXF1ZXN0KGdldEhlYWRlcnMsIHJlZnJlc2gsIGJhc2VVcmwgPSAnJykge1xuICAgIHJldHVybiBmdW5jdGlvbigpIHtcbiAgICAgICAgbGV0IHJldHJpZWQgPSBmYWxzZTtcbiAgICAgICAgY29uc3QgdXJsID0gYmFzZVVybCArIGFyZ3VtZW50c1swXTtcbiAgICAgICAgY29uc3Qgb3B0aW9ucyA9IGFyZ3VtZW50c1sxXSB8fCB7fTtcbiAgICAgICAgb3B0aW9ucy5oZWFkZXJzID0gey4uLmdldEhlYWRlcnMoKSwgLi4ub3B0aW9ucy5oZWFkZXJzfTtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgICAgICAgIHhoclJlcXVlc3QodXJsLCBvcHRpb25zKVxuICAgICAgICAgICAgICAgIC50aGVuKHJlc29sdmUpXG4gICAgICAgICAgICAgICAgLmNhdGNoKGVyciA9PiB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChlcnIuc3RhdHVzID09PSA0MDEgJiYgIXJldHJpZWQpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHJpZWQgPSB0cnVlO1xuICAgICAgICAgICAgICAgICAgICAgICAgcmVmcmVzaCgpXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLnRoZW4oKCkgPT5cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeGhyUmVxdWVzdCh1cmwsIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4uLm9wdGlvbnMsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLi4ub3B0aW9ucy5oZWFkZXJzLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4uLmdldEhlYWRlcnMoKSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pLnRoZW4ocmVzb2x2ZSlcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLmNhdGNoKHJlamVjdCk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZWplY3QoZXJyKTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICB9KTtcbiAgICB9O1xufVxuIiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187IiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X2RvbV9fOyJdLCJzb3VyY2VSb290IjoiIn0=