"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
self["webpackHotUpdate_N_E"]("app/itinerary/[id]/page",{

/***/ "(app-pages-browser)/./src/app/itinerary/[id]/page.tsx":
/*!*****************************************!*\
  !*** ./src/app/itinerary/[id]/page.tsx ***!
  \*****************************************/
/***/ (function(module, __webpack_exports__, __webpack_require__) {

eval(__webpack_require__.ts("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": function() { return /* binding */ ItineraryPage; }\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"(app-pages-browser)/./node_modules/next/dist/compiled/react/jsx-dev-runtime.js\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"(app-pages-browser)/./node_modules/next/dist/compiled/react/index.js\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! __barrel_optimize__?names=Box,Container,Typography!=!@mui/material */ \"(app-pages-browser)/./node_modules/@mui/material/Container/Container.js\");\n/* harmony import */ var _barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! __barrel_optimize__?names=Box,Container,Typography!=!@mui/material */ \"(app-pages-browser)/./node_modules/@mui/material/Box/Box.js\");\n/* harmony import */ var _barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! __barrel_optimize__?names=Box,Container,Typography!=!@mui/material */ \"(app-pages-browser)/./node_modules/@mui/material/Typography/Typography.js\");\n/* harmony import */ var _components_Itinerary__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../components/Itinerary */ \"(app-pages-browser)/./src/components/Itinerary.tsx\");\n/* harmony import */ var _components_TravelInfoExtrationURLInput__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../components/TravelInfoExtrationURLInput */ \"(app-pages-browser)/./src/components/TravelInfoExtrationURLInput.tsx\");\n/* harmony import */ var _components_Map__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../components/Map */ \"(app-pages-browser)/./src/components/Map.tsx\");\n/* __next_internal_client_entry_do_not_use__ default auto */ \nvar _s = $RefreshSig$();\n\n\n\n\n\nconst dummyLocations = [\n    {\n        id: \"1\",\n        name: \"Eiffel Tower\",\n        address: \"Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France\",\n        category: \"attraction\",\n        coordinates: {\n            lat: 48.8584,\n            lng: 2.2945\n        },\n        business_hours: [\n            \"09:00-00:00\"\n        ],\n        rating: 4.7,\n        price_level: 2,\n        photos: [\n            \"eiffel-tower.jpg\"\n        ],\n        description: \"Iconic iron lattice tower on the Champ de Mars in Paris\",\n        tags: [\n            \"landmark\",\n            \"tourist attraction\",\n            \"observation deck\"\n        ],\n        created_at: \"2023-01-01T00:00:00Z\"\n    },\n    {\n        id: \"2\",\n        name: \"Louvre Museum\",\n        address: \"Rue de Rivoli, 75001 Paris, France\",\n        category: \"attraction\",\n        coordinates: {\n            lat: 48.8606,\n            lng: 2.3376\n        },\n        business_hours: [\n            \"09:00-18:00\"\n        ],\n        rating: 4.8,\n        price_level: 3,\n        description: \"World's largest art museum and historic monument\",\n        tags: [\n            \"art\",\n            \"history\",\n            \"museum\"\n        ],\n        created_at: \"2023-01-01T00:00:00Z\"\n    }\n];\nfunction ItineraryPage(param) {\n    let { params } = param;\n    _s();\n    const [locations, setLocations] = react__WEBPACK_IMPORTED_MODULE_1___default().useState([]);\n    const [mapInstance, setMapInstance] = react__WEBPACK_IMPORTED_MODULE_1___default().useState(null);\n    // Fetch locations data based on destination ID\n    //   React.useEffect(() => {\n    //     // Add API call to fetch locations for this destination\n    //   }, [params.id]);\n    react__WEBPACK_IMPORTED_MODULE_1___default().useEffect(()=>{\n        setLocations(dummyLocations);\n    }, []);\n    const handleMapLoad = (0,react__WEBPACK_IMPORTED_MODULE_1__.useCallback)((map)=>{\n        setMapInstance(map);\n    }, []);\n    const handleLocationClick = (0,react__WEBPACK_IMPORTED_MODULE_1__.useCallback)((location)=>{\n        if (!mapInstance) return;\n        mapInstance.panTo({\n            lat: location.coordinates.lat,\n            lng: location.coordinates.lng\n        });\n        mapInstance.setZoom(18);\n    }, [\n        mapInstance\n    ]);\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_5__[\"default\"], {\n        children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_6__[\"default\"], {\n            sx: {\n                my: 4\n            },\n            children: [\n                /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_7__[\"default\"], {\n                    variant: \"h4\",\n                    gutterBottom: true,\n                    children: \"Plan Your Trip\"\n                }, void 0, false, {\n                    fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n                    lineNumber: 67,\n                    columnNumber: 17\n                }, this),\n                /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_components_TravelInfoExtrationURLInput__WEBPACK_IMPORTED_MODULE_3__[\"default\"], {\n                    onLocationsUpdate: handleLocationsUpdate\n                }, void 0, false, {\n                    fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n                    lineNumber: 70,\n                    columnNumber: 17\n                }, this),\n                /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_6__[\"default\"], {\n                    sx: {\n                        display: \"flex\",\n                        gap: 2,\n                        mt: 2\n                    },\n                    children: [\n                        /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_6__[\"default\"], {\n                            sx: {\n                                width: \"40%\"\n                            },\n                            children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_components_Itinerary__WEBPACK_IMPORTED_MODULE_2__[\"default\"], {\n                                locations: locations,\n                                onLocationClick: handleLocationClick\n                            }, void 0, false, {\n                                fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n                                lineNumber: 75,\n                                columnNumber: 25\n                            }, this)\n                        }, void 0, false, {\n                            fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n                            lineNumber: 74,\n                            columnNumber: 21\n                        }, this),\n                        /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Container_Typography_mui_material__WEBPACK_IMPORTED_MODULE_6__[\"default\"], {\n                            sx: {\n                                width: \"60%\"\n                            },\n                            children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_components_Map__WEBPACK_IMPORTED_MODULE_4__[\"default\"], {\n                                locations: locations,\n                                onMapLoad: handleMapLoad\n                            }, void 0, false, {\n                                fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n                                lineNumber: 81,\n                                columnNumber: 25\n                            }, this)\n                        }, void 0, false, {\n                            fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n                            lineNumber: 80,\n                            columnNumber: 21\n                        }, this)\n                    ]\n                }, void 0, true, {\n                    fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n                    lineNumber: 73,\n                    columnNumber: 17\n                }, this)\n            ]\n        }, void 0, true, {\n            fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n            lineNumber: 66,\n            columnNumber: 13\n        }, this)\n    }, void 0, false, {\n        fileName: \"C:\\\\Users\\\\Vincent\\\\Projects\\\\Group-project\\\\frontend\\\\src\\\\app\\\\itinerary\\\\[id]\\\\page.tsx\",\n        lineNumber: 65,\n        columnNumber: 9\n    }, this);\n}\n_s(ItineraryPage, \"9qAxrYzlmQVhy8xD5sVHoctVVE8=\");\n_c = ItineraryPage;\nvar _c;\n$RefreshReg$(_c, \"ItineraryPage\");\n\n\n;\n    // Wrapped in an IIFE to avoid polluting the global scope\n    ;\n    (function () {\n        var _a, _b;\n        // Legacy CSS implementations will `eval` browser code in a Node.js context\n        // to extract CSS. For backwards compatibility, we need to check we're in a\n        // browser context before continuing.\n        if (typeof self !== 'undefined' &&\n            // AMP / No-JS mode does not inject these helpers:\n            '$RefreshHelpers$' in self) {\n            // @ts-ignore __webpack_module__ is global\n            var currentExports = module.exports;\n            // @ts-ignore __webpack_module__ is global\n            var prevSignature = (_b = (_a = module.hot.data) === null || _a === void 0 ? void 0 : _a.prevSignature) !== null && _b !== void 0 ? _b : null;\n            // This cannot happen in MainTemplate because the exports mismatch between\n            // templating and execution.\n            self.$RefreshHelpers$.registerExportsForReactRefresh(currentExports, module.id);\n            // A module can be accepted automatically based on its exports, e.g. when\n            // it is a Refresh Boundary.\n            if (self.$RefreshHelpers$.isReactRefreshBoundary(currentExports)) {\n                // Save the previous exports signature on update so we can compare the boundary\n                // signatures. We avoid saving exports themselves since it causes memory leaks (https://github.com/vercel/next.js/pull/53797)\n                module.hot.dispose(function (data) {\n                    data.prevSignature =\n                        self.$RefreshHelpers$.getRefreshBoundarySignature(currentExports);\n                });\n                // Unconditionally accept an update to this module, we'll check if it's\n                // still a Refresh Boundary later.\n                // @ts-ignore importMeta is replaced in the loader\n                module.hot.accept();\n                // This field is set when the previous version of this module was a\n                // Refresh Boundary, letting us know we need to check for invalidation or\n                // enqueue an update.\n                if (prevSignature !== null) {\n                    // A boundary can become ineligible if its exports are incompatible\n                    // with the previous exports.\n                    //\n                    // For example, if you add/remove/change exports, we'll want to\n                    // re-execute the importing modules, and force those components to\n                    // re-render. Similarly, if you convert a class component to a\n                    // function, we want to invalidate the boundary.\n                    if (self.$RefreshHelpers$.shouldInvalidateReactRefreshBoundary(prevSignature, self.$RefreshHelpers$.getRefreshBoundarySignature(currentExports))) {\n                        module.hot.invalidate();\n                    }\n                    else {\n                        self.$RefreshHelpers$.scheduleUpdate();\n                    }\n                }\n            }\n            else {\n                // Since we just executed the code for the module, it's possible that the\n                // new exports made it ineligible for being a boundary.\n                // We only care about the case when we were _previously_ a boundary,\n                // because we already accepted this update (accidental side effect).\n                var isNoLongerABoundary = prevSignature !== null;\n                if (isNoLongerABoundary) {\n                    module.hot.invalidate();\n                }\n            }\n        }\n    })();\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwcC1wYWdlcy1icm93c2VyKS8uL3NyYy9hcHAvaXRpbmVyYXJ5L1tpZF0vcGFnZS50c3giLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7O0FBRTJDO0FBQ2dCO0FBQ0w7QUFFb0M7QUFDdkM7QUFFbkQsTUFBTVEsaUJBQTZCO0lBQy9CO1FBQ0lDLElBQUk7UUFDSkMsTUFBTTtRQUNOQyxTQUFTO1FBQ1RDLFVBQVU7UUFDVkMsYUFBYTtZQUFFQyxLQUFLO1lBQVNDLEtBQUs7UUFBTztRQUN6Q0MsZ0JBQWdCO1lBQUM7U0FBYztRQUMvQkMsUUFBUTtRQUNSQyxhQUFhO1FBQ2JDLFFBQVE7WUFBQztTQUFtQjtRQUM1QkMsYUFBYTtRQUNiQyxNQUFNO1lBQUM7WUFBWTtZQUFzQjtTQUFtQjtRQUM1REMsWUFBWTtJQUNoQjtJQUNBO1FBQ0liLElBQUk7UUFDSkMsTUFBTTtRQUNOQyxTQUFTO1FBQ1RDLFVBQVU7UUFDVkMsYUFBYTtZQUFFQyxLQUFLO1lBQVNDLEtBQUs7UUFBTztRQUN6Q0MsZ0JBQWdCO1lBQUM7U0FBYztRQUMvQkMsUUFBUTtRQUNSQyxhQUFhO1FBQ2JFLGFBQWE7UUFDYkMsTUFBTTtZQUFDO1lBQU87WUFBVztTQUFTO1FBQ2xDQyxZQUFZO0lBQ2hCO0NBQ0g7QUFFYyxTQUFTQyxjQUFjLEtBQXNDO1FBQXRDLEVBQUVDLE1BQU0sRUFBOEIsR0FBdEM7O0lBQ2xDLE1BQU0sQ0FBQ0MsV0FBV0MsYUFBYSxHQUFHMUIscURBQWMsQ0FBYSxFQUFFO0lBQy9ELE1BQU0sQ0FBQzRCLGFBQWFDLGVBQWUsR0FBRzdCLHFEQUFjLENBQXlCO0lBRTdFLCtDQUErQztJQUNuRCw0QkFBNEI7SUFDNUIsOERBQThEO0lBQzlELHFCQUFxQjtJQUVqQkEsc0RBQWUsQ0FBQztRQUNaMEIsYUFBYWxCO0lBQ2pCLEdBQUcsRUFBRTtJQUVMLE1BQU11QixnQkFBZ0I5QixrREFBV0EsQ0FBQyxDQUFDK0I7UUFDL0JILGVBQWVHO0lBQ25CLEdBQUcsRUFBRTtJQUVMLE1BQU1DLHNCQUFzQmhDLGtEQUFXQSxDQUFDLENBQUNpQztRQUNyQyxJQUFJLENBQUNOLGFBQWE7UUFFbEJBLFlBQVlPLEtBQUssQ0FBQztZQUFFckIsS0FBS29CLFNBQVNyQixXQUFXLENBQUNDLEdBQUc7WUFBRUMsS0FBS21CLFNBQVNyQixXQUFXLENBQUNFLEdBQUc7UUFBQztRQUNqRmEsWUFBWVEsT0FBTyxDQUFDO0lBQ3hCLEdBQUc7UUFBQ1I7S0FBWTtJQUVoQixxQkFDSSw4REFBQ3pCLG9HQUFTQTtrQkFDTiw0RUFBQ0Qsb0dBQUdBO1lBQUNtQyxJQUFJO2dCQUFFQyxJQUFJO1lBQUU7OzhCQUNiLDhEQUFDbEMsb0dBQVVBO29CQUFDbUMsU0FBUTtvQkFBS0MsWUFBWTs4QkFBQzs7Ozs7OzhCQUd0Qyw4REFBQ2xDLCtFQUEyQkE7b0JBQ3hCbUMsbUJBQW1CQzs7Ozs7OzhCQUV2Qiw4REFBQ3hDLG9HQUFHQTtvQkFBQ21DLElBQUk7d0JBQUVNLFNBQVM7d0JBQVFDLEtBQUs7d0JBQUdDLElBQUk7b0JBQUU7O3NDQUN0Qyw4REFBQzNDLG9HQUFHQTs0QkFBQ21DLElBQUk7Z0NBQUVTLE9BQU87NEJBQU07c0NBQ3BCLDRFQUFDekMsNkRBQVNBO2dDQUNOb0IsV0FBV0E7Z0NBQ1hzQixpQkFBaUJkOzs7Ozs7Ozs7OztzQ0FHekIsOERBQUMvQixvR0FBR0E7NEJBQUNtQyxJQUFJO2dDQUFFUyxPQUFPOzRCQUFNO3NDQUNwQiw0RUFBQ3ZDLHVEQUFZQTtnQ0FDVGtCLFdBQVdBO2dDQUNYdUIsV0FBV2pCOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBT3ZDO0dBbER3QlI7S0FBQUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9fTl9FLy4vc3JjL2FwcC9pdGluZXJhcnkvW2lkXS9wYWdlLnRzeD82YjQzIl0sInNvdXJjZXNDb250ZW50IjpbIid1c2UgY2xpZW50JztcclxuXHJcbmltcG9ydCBSZWFjdCwgeyB1c2VDYWxsYmFjayB9IGZyb20gJ3JlYWN0JztcclxuaW1wb3J0IHsgQm94LCBDb250YWluZXIsIFR5cG9ncmFwaHkgfSBmcm9tICdAbXVpL21hdGVyaWFsJztcclxuaW1wb3J0IEl0aW5lcmFyeSBmcm9tICcuLi8uLi8uLi9jb21wb25lbnRzL0l0aW5lcmFyeSc7XHJcbmltcG9ydCB7IExvY2F0aW9uIH0gZnJvbSAnLi4vLi4vLi4vdHlwZXMvbG9jYXRpb24nO1xyXG5pbXBvcnQgVHJhdmVsSW5mb0V4dHJhdGlvblVSTElucHV0IGZyb20gJy4uLy4uLy4uL2NvbXBvbmVudHMvVHJhdmVsSW5mb0V4dHJhdGlvblVSTElucHV0JztcclxuaW1wb3J0IE1hcENvbXBvbmVudCBmcm9tIFwiLi4vLi4vLi4vY29tcG9uZW50cy9NYXBcIjtcclxuXHJcbmNvbnN0IGR1bW15TG9jYXRpb25zOiBMb2NhdGlvbltdID0gW1xyXG4gICAge1xyXG4gICAgICAgIGlkOiAnMScsXHJcbiAgICAgICAgbmFtZTogJ0VpZmZlbCBUb3dlcicsXHJcbiAgICAgICAgYWRkcmVzczogJ0NoYW1wIGRlIE1hcnMsIDUgQXZlbnVlIEFuYXRvbGUgRnJhbmNlLCA3NTAwNyBQYXJpcywgRnJhbmNlJyxcclxuICAgICAgICBjYXRlZ29yeTogJ2F0dHJhY3Rpb24nLFxyXG4gICAgICAgIGNvb3JkaW5hdGVzOiB7IGxhdDogNDguODU4NCwgbG5nOiAyLjI5NDUgfSxcclxuICAgICAgICBidXNpbmVzc19ob3VyczogWycwOTowMC0wMDowMCddLFxyXG4gICAgICAgIHJhdGluZzogNC43LFxyXG4gICAgICAgIHByaWNlX2xldmVsOiAyLFxyXG4gICAgICAgIHBob3RvczogWydlaWZmZWwtdG93ZXIuanBnJ10sXHJcbiAgICAgICAgZGVzY3JpcHRpb246ICdJY29uaWMgaXJvbiBsYXR0aWNlIHRvd2VyIG9uIHRoZSBDaGFtcCBkZSBNYXJzIGluIFBhcmlzJyxcclxuICAgICAgICB0YWdzOiBbJ2xhbmRtYXJrJywgJ3RvdXJpc3QgYXR0cmFjdGlvbicsICdvYnNlcnZhdGlvbiBkZWNrJ10sXHJcbiAgICAgICAgY3JlYXRlZF9hdDogJzIwMjMtMDEtMDFUMDA6MDA6MDBaJ1xyXG4gICAgfSxcclxuICAgIHtcclxuICAgICAgICBpZDogJzInLFxyXG4gICAgICAgIG5hbWU6ICdMb3V2cmUgTXVzZXVtJyxcclxuICAgICAgICBhZGRyZXNzOiAnUnVlIGRlIFJpdm9saSwgNzUwMDEgUGFyaXMsIEZyYW5jZScsXHJcbiAgICAgICAgY2F0ZWdvcnk6ICdhdHRyYWN0aW9uJyxcclxuICAgICAgICBjb29yZGluYXRlczogeyBsYXQ6IDQ4Ljg2MDYsIGxuZzogMi4zMzc2IH0sXHJcbiAgICAgICAgYnVzaW5lc3NfaG91cnM6IFsnMDk6MDAtMTg6MDAnXSxcclxuICAgICAgICByYXRpbmc6IDQuOCxcclxuICAgICAgICBwcmljZV9sZXZlbDogMyxcclxuICAgICAgICBkZXNjcmlwdGlvbjogJ1dvcmxkXFwncyBsYXJnZXN0IGFydCBtdXNldW0gYW5kIGhpc3RvcmljIG1vbnVtZW50JyxcclxuICAgICAgICB0YWdzOiBbJ2FydCcsICdoaXN0b3J5JywgJ211c2V1bSddLFxyXG4gICAgICAgIGNyZWF0ZWRfYXQ6ICcyMDIzLTAxLTAxVDAwOjAwOjAwWidcclxuICAgIH1cclxuXTtcclxuXHJcbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIEl0aW5lcmFyeVBhZ2UoeyBwYXJhbXMgfTogeyBwYXJhbXM6IHsgaWQ6IHN0cmluZyB9IH0pIHtcclxuICAgIGNvbnN0IFtsb2NhdGlvbnMsIHNldExvY2F0aW9uc10gPSBSZWFjdC51c2VTdGF0ZTxMb2NhdGlvbltdPihbXSk7XHJcbiAgICBjb25zdCBbbWFwSW5zdGFuY2UsIHNldE1hcEluc3RhbmNlXSA9IFJlYWN0LnVzZVN0YXRlPGdvb2dsZS5tYXBzLk1hcCB8IG51bGw+KG51bGwpO1xyXG5cclxuICAgIC8vIEZldGNoIGxvY2F0aW9ucyBkYXRhIGJhc2VkIG9uIGRlc3RpbmF0aW9uIElEXHJcbi8vICAgUmVhY3QudXNlRWZmZWN0KCgpID0+IHtcclxuLy8gICAgIC8vIEFkZCBBUEkgY2FsbCB0byBmZXRjaCBsb2NhdGlvbnMgZm9yIHRoaXMgZGVzdGluYXRpb25cclxuLy8gICB9LCBbcGFyYW1zLmlkXSk7XHJcblxyXG4gICAgUmVhY3QudXNlRWZmZWN0KCgpID0+IHtcclxuICAgICAgICBzZXRMb2NhdGlvbnMoZHVtbXlMb2NhdGlvbnMpO1xyXG4gICAgfSwgW10pO1xyXG5cclxuICAgIGNvbnN0IGhhbmRsZU1hcExvYWQgPSB1c2VDYWxsYmFjaygobWFwOiBnb29nbGUubWFwcy5NYXApID0+IHtcclxuICAgICAgICBzZXRNYXBJbnN0YW5jZShtYXApO1xyXG4gICAgfSwgW10pO1xyXG5cclxuICAgIGNvbnN0IGhhbmRsZUxvY2F0aW9uQ2xpY2sgPSB1c2VDYWxsYmFjaygobG9jYXRpb246IExvY2F0aW9uKSA9PiB7XHJcbiAgICAgICAgaWYgKCFtYXBJbnN0YW5jZSkgcmV0dXJuO1xyXG5cclxuICAgICAgICBtYXBJbnN0YW5jZS5wYW5Ubyh7IGxhdDogbG9jYXRpb24uY29vcmRpbmF0ZXMubGF0LCBsbmc6IGxvY2F0aW9uLmNvb3JkaW5hdGVzLmxuZyB9KTtcclxuICAgICAgICBtYXBJbnN0YW5jZS5zZXRab29tKDE4KTtcclxuICAgIH0sIFttYXBJbnN0YW5jZV0pO1xyXG4gICAgXHJcbiAgICByZXR1cm4gKFxyXG4gICAgICAgIDxDb250YWluZXI+XHJcbiAgICAgICAgICAgIDxCb3ggc3g9e3sgbXk6IDQgfX0+XHJcbiAgICAgICAgICAgICAgICA8VHlwb2dyYXBoeSB2YXJpYW50PVwiaDRcIiBndXR0ZXJCb3R0b20+XHJcbiAgICAgICAgICAgICAgICAgICAgUGxhbiBZb3VyIFRyaXBcclxuICAgICAgICAgICAgICAgIDwvVHlwb2dyYXBoeT5cclxuICAgICAgICAgICAgICAgIDxUcmF2ZWxJbmZvRXh0cmF0aW9uVVJMSW5wdXQgXHJcbiAgICAgICAgICAgICAgICAgICAgb25Mb2NhdGlvbnNVcGRhdGU9e2hhbmRsZUxvY2F0aW9uc1VwZGF0ZX1cclxuICAgICAgICAgICAgICAgIC8+XHJcbiAgICAgICAgICAgICAgICA8Qm94IHN4PXt7IGRpc3BsYXk6ICdmbGV4JywgZ2FwOiAyLCBtdDogMiB9fT5cclxuICAgICAgICAgICAgICAgICAgICA8Qm94IHN4PXt7IHdpZHRoOiAnNDAlJyB9fT5cclxuICAgICAgICAgICAgICAgICAgICAgICAgPEl0aW5lcmFyeSBcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGxvY2F0aW9ucz17bG9jYXRpb25zfSBcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9uTG9jYXRpb25DbGljaz17aGFuZGxlTG9jYXRpb25DbGlja31cclxuICAgICAgICAgICAgICAgICAgICAgICAgLz5cclxuICAgICAgICAgICAgICAgICAgICA8L0JveD5cclxuICAgICAgICAgICAgICAgICAgICA8Qm94IHN4PXt7IHdpZHRoOiAnNjAlJyB9fT5cclxuICAgICAgICAgICAgICAgICAgICAgICAgPE1hcENvbXBvbmVudCBcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGxvY2F0aW9ucz17bG9jYXRpb25zfSBcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9uTWFwTG9hZD17aGFuZGxlTWFwTG9hZH1cclxuICAgICAgICAgICAgICAgICAgICAgICAgLz5cclxuICAgICAgICAgICAgICAgICAgICA8L0JveD5cclxuICAgICAgICAgICAgICAgIDwvQm94PlxyXG4gICAgICAgICAgICA8L0JveD5cclxuICAgICAgICA8L0NvbnRhaW5lcj5cclxuICAgICk7XHJcbn1cclxuIl0sIm5hbWVzIjpbIlJlYWN0IiwidXNlQ2FsbGJhY2siLCJCb3giLCJDb250YWluZXIiLCJUeXBvZ3JhcGh5IiwiSXRpbmVyYXJ5IiwiVHJhdmVsSW5mb0V4dHJhdGlvblVSTElucHV0IiwiTWFwQ29tcG9uZW50IiwiZHVtbXlMb2NhdGlvbnMiLCJpZCIsIm5hbWUiLCJhZGRyZXNzIiwiY2F0ZWdvcnkiLCJjb29yZGluYXRlcyIsImxhdCIsImxuZyIsImJ1c2luZXNzX2hvdXJzIiwicmF0aW5nIiwicHJpY2VfbGV2ZWwiLCJwaG90b3MiLCJkZXNjcmlwdGlvbiIsInRhZ3MiLCJjcmVhdGVkX2F0IiwiSXRpbmVyYXJ5UGFnZSIsInBhcmFtcyIsImxvY2F0aW9ucyIsInNldExvY2F0aW9ucyIsInVzZVN0YXRlIiwibWFwSW5zdGFuY2UiLCJzZXRNYXBJbnN0YW5jZSIsInVzZUVmZmVjdCIsImhhbmRsZU1hcExvYWQiLCJtYXAiLCJoYW5kbGVMb2NhdGlvbkNsaWNrIiwibG9jYXRpb24iLCJwYW5UbyIsInNldFpvb20iLCJzeCIsIm15IiwidmFyaWFudCIsImd1dHRlckJvdHRvbSIsIm9uTG9jYXRpb25zVXBkYXRlIiwiaGFuZGxlTG9jYXRpb25zVXBkYXRlIiwiZGlzcGxheSIsImdhcCIsIm10Iiwid2lkdGgiLCJvbkxvY2F0aW9uQ2xpY2siLCJvbk1hcExvYWQiXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///(app-pages-browser)/./src/app/itinerary/[id]/page.tsx\n"));

/***/ })

});