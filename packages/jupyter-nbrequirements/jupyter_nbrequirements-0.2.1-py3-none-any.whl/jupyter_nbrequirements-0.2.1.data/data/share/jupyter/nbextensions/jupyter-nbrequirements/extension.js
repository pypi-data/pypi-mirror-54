define(function() { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
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
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/extension.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/extension.js":
/*!**************************!*\
  !*** ./src/extension.js ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/**\n * Jupyter NBRequirements.\n *\n * This file contains the javascript that is run when the notebook is loaded.\n * It contains some requirejs configuration and the `load_ipython_extension`\n * which is required for any notebook extension.\n *\n * @link   https://github.com/CermakM/jupyter-nbrequirements#readme\n * @file   This file loads the Jupyter magic extension for managing notebook requirements.\n * @author Marek Cermak <macermak@redhat.com>\n * @since  0.0.1\n */\n\n/* eslint-disable */\n\nconst __extension__ = \"jupyter_nbrequirements\"\n\n// Some static assets may be required by the custom widget javascript. The base\n// url for the notebook is not known at build time and is therefore computed\n// dynamically.\n__webpack_require__.p = document.querySelector( \"body\" ).getAttribute( 'data-base-url' ) + 'nbextensions/jupyter-nbrequirements/';\n\n/** Constants **/\n// Logging level\nwindow.DEFAULT_LOGGING_LEVEL = { value: 2, name: \"DEBUG\" }\n// Notification timeout in ms\nwindow.DEFAULT_NOTIFICATION_TIMEOUT = 30000\n// Resolution engine {pipenv, thoth}\nwindow.DEFAULT_RESOLUTION_ENGINE = \"thoth\"\n\n// Load the extension\nif ( window.require ) {\n    window.require.config( {\n        map: {\n            \"*\": {\n                \"nbrequirements\": \"nbextensions/jupyter-nbrequirements/index\"\n            }\n        }\n    } );\n    window.require( [ 'nbrequirements' ], () => console.log( \"Loaded extension: jupyter-nbrequirements\" ) )\n}\n\n// Export the required load_ipython_extension\nmodule.exports = {\n    load_ipython_extension: function () {// Autoload\n        // wait for both the kernel and the jupyter-require extension to be loaded\n        window.require( [\n            \"base/js/namespace\",\n            \"base/js/events\"\n        ], ( Jupyter, events ) => {\n            const options = {\n                silent: false,\n                // if there is an error, let user try to manually\n                // load the extension himself and finish the extension\n                // loading anyway\n                stop_on_error: true,\n                store_history: false\n            }\n\n            // Wait for the required extension to be loaded\n            events.one( \"extension_loaded.JupyterRequire\", () => {\n\n                console.info( \"Loading magic commands: [ '%dep', '%requirements', '%kernel' ]\" )\n\n                const cmd = \"%reload_ext \" + __extension__\n                Jupyter.notebook.kernel.execute( cmd, {}, options )\n\n            } )\n        } )\n    }\n};\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9zcmMvZXh0ZW5zaW9uLmpzLmpzIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vLy4vc3JjL2V4dGVuc2lvbi5qcz8xNWU4Il0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogSnVweXRlciBOQlJlcXVpcmVtZW50cy5cbiAqXG4gKiBUaGlzIGZpbGUgY29udGFpbnMgdGhlIGphdmFzY3JpcHQgdGhhdCBpcyBydW4gd2hlbiB0aGUgbm90ZWJvb2sgaXMgbG9hZGVkLlxuICogSXQgY29udGFpbnMgc29tZSByZXF1aXJlanMgY29uZmlndXJhdGlvbiBhbmQgdGhlIGBsb2FkX2lweXRob25fZXh0ZW5zaW9uYFxuICogd2hpY2ggaXMgcmVxdWlyZWQgZm9yIGFueSBub3RlYm9vayBleHRlbnNpb24uXG4gKlxuICogQGxpbmsgICBodHRwczovL2dpdGh1Yi5jb20vQ2VybWFrTS9qdXB5dGVyLW5icmVxdWlyZW1lbnRzI3JlYWRtZVxuICogQGZpbGUgICBUaGlzIGZpbGUgbG9hZHMgdGhlIEp1cHl0ZXIgbWFnaWMgZXh0ZW5zaW9uIGZvciBtYW5hZ2luZyBub3RlYm9vayByZXF1aXJlbWVudHMuXG4gKiBAYXV0aG9yIE1hcmVrIENlcm1hayA8bWFjZXJtYWtAcmVkaGF0LmNvbT5cbiAqIEBzaW5jZSAgMC4wLjFcbiAqL1xuXG4vKiBlc2xpbnQtZGlzYWJsZSAqL1xuXG5jb25zdCBfX2V4dGVuc2lvbl9fID0gXCJqdXB5dGVyX25icmVxdWlyZW1lbnRzXCJcblxuLy8gU29tZSBzdGF0aWMgYXNzZXRzIG1heSBiZSByZXF1aXJlZCBieSB0aGUgY3VzdG9tIHdpZGdldCBqYXZhc2NyaXB0LiBUaGUgYmFzZVxuLy8gdXJsIGZvciB0aGUgbm90ZWJvb2sgaXMgbm90IGtub3duIGF0IGJ1aWxkIHRpbWUgYW5kIGlzIHRoZXJlZm9yZSBjb21wdXRlZFxuLy8gZHluYW1pY2FsbHkuXG5fX3dlYnBhY2tfcHVibGljX3BhdGhfXyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoIFwiYm9keVwiICkuZ2V0QXR0cmlidXRlKCAnZGF0YS1iYXNlLXVybCcgKSArICduYmV4dGVuc2lvbnMvanVweXRlci1uYnJlcXVpcmVtZW50cy8nO1xuXG4vKiogQ29uc3RhbnRzICoqL1xuLy8gTG9nZ2luZyBsZXZlbFxud2luZG93LkRFRkFVTFRfTE9HR0lOR19MRVZFTCA9IHsgdmFsdWU6IDIsIG5hbWU6IFwiREVCVUdcIiB9XG4vLyBOb3RpZmljYXRpb24gdGltZW91dCBpbiBtc1xud2luZG93LkRFRkFVTFRfTk9USUZJQ0FUSU9OX1RJTUVPVVQgPSAzMDAwMFxuLy8gUmVzb2x1dGlvbiBlbmdpbmUge3BpcGVudiwgdGhvdGh9XG53aW5kb3cuREVGQVVMVF9SRVNPTFVUSU9OX0VOR0lORSA9IFwidGhvdGhcIlxuXG4vLyBMb2FkIHRoZSBleHRlbnNpb25cbmlmICggd2luZG93LnJlcXVpcmUgKSB7XG4gICAgd2luZG93LnJlcXVpcmUuY29uZmlnKCB7XG4gICAgICAgIG1hcDoge1xuICAgICAgICAgICAgXCIqXCI6IHtcbiAgICAgICAgICAgICAgICBcIm5icmVxdWlyZW1lbnRzXCI6IFwibmJleHRlbnNpb25zL2p1cHl0ZXItbmJyZXF1aXJlbWVudHMvaW5kZXhcIlxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfSApO1xuICAgIHdpbmRvdy5yZXF1aXJlKCBbICduYnJlcXVpcmVtZW50cycgXSwgKCkgPT4gY29uc29sZS5sb2coIFwiTG9hZGVkIGV4dGVuc2lvbjoganVweXRlci1uYnJlcXVpcmVtZW50c1wiICkgKVxufVxuXG4vLyBFeHBvcnQgdGhlIHJlcXVpcmVkIGxvYWRfaXB5dGhvbl9leHRlbnNpb25cbm1vZHVsZS5leHBvcnRzID0ge1xuICAgIGxvYWRfaXB5dGhvbl9leHRlbnNpb246IGZ1bmN0aW9uICgpIHsvLyBBdXRvbG9hZFxuICAgICAgICAvLyB3YWl0IGZvciBib3RoIHRoZSBrZXJuZWwgYW5kIHRoZSBqdXB5dGVyLXJlcXVpcmUgZXh0ZW5zaW9uIHRvIGJlIGxvYWRlZFxuICAgICAgICB3aW5kb3cucmVxdWlyZSggW1xuICAgICAgICAgICAgXCJiYXNlL2pzL25hbWVzcGFjZVwiLFxuICAgICAgICAgICAgXCJiYXNlL2pzL2V2ZW50c1wiXG4gICAgICAgIF0sICggSnVweXRlciwgZXZlbnRzICkgPT4ge1xuICAgICAgICAgICAgY29uc3Qgb3B0aW9ucyA9IHtcbiAgICAgICAgICAgICAgICBzaWxlbnQ6IGZhbHNlLFxuICAgICAgICAgICAgICAgIC8vIGlmIHRoZXJlIGlzIGFuIGVycm9yLCBsZXQgdXNlciB0cnkgdG8gbWFudWFsbHlcbiAgICAgICAgICAgICAgICAvLyBsb2FkIHRoZSBleHRlbnNpb24gaGltc2VsZiBhbmQgZmluaXNoIHRoZSBleHRlbnNpb25cbiAgICAgICAgICAgICAgICAvLyBsb2FkaW5nIGFueXdheVxuICAgICAgICAgICAgICAgIHN0b3Bfb25fZXJyb3I6IHRydWUsXG4gICAgICAgICAgICAgICAgc3RvcmVfaGlzdG9yeTogZmFsc2VcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgLy8gV2FpdCBmb3IgdGhlIHJlcXVpcmVkIGV4dGVuc2lvbiB0byBiZSBsb2FkZWRcbiAgICAgICAgICAgIGV2ZW50cy5vbmUoIFwiZXh0ZW5zaW9uX2xvYWRlZC5KdXB5dGVyUmVxdWlyZVwiLCAoKSA9PiB7XG5cbiAgICAgICAgICAgICAgICBjb25zb2xlLmluZm8oIFwiTG9hZGluZyBtYWdpYyBjb21tYW5kczogWyAnJWRlcCcsICclcmVxdWlyZW1lbnRzJywgJyVrZXJuZWwnIF1cIiApXG5cbiAgICAgICAgICAgICAgICBjb25zdCBjbWQgPSBcIiVyZWxvYWRfZXh0IFwiICsgX19leHRlbnNpb25fX1xuICAgICAgICAgICAgICAgIEp1cHl0ZXIubm90ZWJvb2sua2VybmVsLmV4ZWN1dGUoIGNtZCwge30sIG9wdGlvbnMgKVxuXG4gICAgICAgICAgICB9IClcbiAgICAgICAgfSApXG4gICAgfVxufTtcbiJdLCJtYXBwaW5ncyI6IkFBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTsiLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./src/extension.js\n");

/***/ })

/******/ })});;