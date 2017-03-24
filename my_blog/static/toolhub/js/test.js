if (function (t, e) {
        "object" == typeof module && "object" == typeof module.exports ? module.exports = t.document ? e(t, !0) : function (t) {
            if (!t.document)throw new Error("jQuery requires a window with a document");
            return e(t)
        } : e(t)
    }("undefined" != typeof window ? window : this, function (t, e) {
        function n(t) {
            var e = t.length, n = oe.type(t);
            return "function" === n || oe.isWindow(t) ? !1 : 1 === t.nodeType && e ? !0 : "array" === n || 0 === e || "number" == typeof e && e > 0 && e - 1 in t
        }

        function i(t, e, n) {
            if (oe.isFunction(e))return oe.grep(t, function (t, i) {
                return !!e.call(t, i, t) !== n
            });
            if (e.nodeType)return oe.grep(t, function (t) {
                return t === e !== n
            });
            if ("string" == typeof e) {
                if (he.test(e))return oe.filter(e, t, n);
                e = oe.filter(e, t)
            }
            return oe.grep(t, function (t) {
                return oe.inArray(t, e) >= 0 !== n
            })
        }

        function o(t, e) {
            do t = t[e]; while (t && 1 !== t.nodeType);
            return t
        }

        function a(t) {
            var e = we[t] = {};
            return oe.each(t.match(be) || [], function (t, n) {
                e[n] = !0
            }), e
        }

        function r() {
            pe.addEventListener ? (pe.removeEventListener("DOMContentLoaded", s, !1), t.removeEventListener("load", s, !1)) : (pe.detachEvent("onreadystatechange", s), t.detachEvent("onload", s))
        }

        function s() {
            (pe.addEventListener || "load" === event.type || "complete" === pe.readyState) && (r(), oe.ready())
        }

        function l(t, e, n) {
            if (void 0 === n && 1 === t.nodeType) {
                var i = "data-" + e.replace(Te, "-$1").toLowerCase();
                if (n = t.getAttribute(i), "string" == typeof n) {
                    try {
                        n = "true" === n ? !0 : "false" === n ? !1 : "null" === n ? null : +n + "" === n ? +n : ke.test(n) ? oe.parseJSON(n) : n
                    } catch (o) {
                    }
                    oe.data(t, e, n)
                } else n = void 0
            }
            return n
        }

        function u(t) {
            var e;
            for (e in t)if (("data" !== e || !oe.isEmptyObject(t[e])) && "toJSON" !== e)return !1;
            return !0
        }

        function c(t, e, n, i) {
            if (oe.acceptData(t)) {
                var o, a, r = oe.expando, s = t.nodeType, l = s ? oe.cache : t, u = s ? t[r] : t[r] && r;
                if (u && l[u] && (i || l[u].data) || void 0 !== n || "string" != typeof e)return u || (u = s ? t[r] = Q.pop() || oe.guid++ : r), l[u] || (l[u] = s ? {} : {toJSON: oe.noop}), ("object" == typeof e || "function" == typeof e) && (i ? l[u] = oe.extend(l[u], e) : l[u].data = oe.extend(l[u].data, e)), a = l[u], i || (a.data || (a.data = {}), a = a.data), void 0 !== n && (a[oe.camelCase(e)] = n), "string" == typeof e ? (o = a[e], null == o && (o = a[oe.camelCase(e)])) : o = a, o
            }
        }

        function d(t, e, n) {
            if (oe.acceptData(t)) {
                var i, o, a = t.nodeType, r = a ? oe.cache : t, s = a ? t[oe.expando] : oe.expando;
                if (r[s]) {
                    if (e && (i = n ? r[s] : r[s].data)) {
                        oe.isArray(e) ? e = e.concat(oe.map(e, oe.camelCase)) : e in i ? e = [e] : (e = oe.camelCase(e), e = e in i ? [e] : e.split(" ")), o = e.length;
                        for (; o--;)delete i[e[o]];
                        if (n ? !u(i) : !oe.isEmptyObject(i))return
                    }
                    (n || (delete r[s].data, u(r[s]))) && (a ? oe.cleanData([t], !0) : ne.deleteExpando || r != r.window ? delete r[s] : r[s] = null)
                }
            }
        }

        function h() {
            return !0
        }

        function f() {
            return !1
        }

        function p() {
            try {
                return pe.activeElement
            } catch (t) {
            }
        }

        function m(t) {
            var e = Ie.split("|"), n = t.createDocumentFragment();
            if (n.createElement)for (; e.length;)n.createElement(e.pop());
            return n
        }

        function g(t, e) {
            var n, i, o = 0, a = typeof t.getElementsByTagName !== Ce ? t.getElementsByTagName(e || "*") : typeof t.querySelectorAll !== Ce ? t.querySelectorAll(e || "*") : void 0;
            if (!a)for (a = [], n = t.childNodes || t; null != (i = n[o]); o++)!e || oe.nodeName(i, e) ? a.push(i) : oe.merge(a, g(i, e));
            return void 0 === e || e && oe.nodeName(t, e) ? oe.merge([t], a) : a
        }

        function v(t) {
            Ne.test(t.type) && (t.defaultChecked = t.checked)
        }

        function y(t, e) {
            return oe.nodeName(t, "table") && oe.nodeName(11 !== e.nodeType ? e : e.firstChild, "tr") ? t.getElementsByTagName("tbody")[0] || t.appendChild(t.ownerDocument.createElement("tbody")) : t
        }

        function b(t) {
            return t.type = (null !== oe.find.attr(t, "type")) + "/" + t.type, t
        }

        function w(t) {
            var e = Xe.exec(t.type);
            return e ? t.type = e[1] : t.removeAttribute("type"), t
        }

        function x(t, e) {
            for (var n, i = 0; null != (n = t[i]); i++)oe._data(n, "globalEval", !e || oe._data(e[i], "globalEval"))
        }

        function _(t, e) {
            if (1 === e.nodeType && oe.hasData(t)) {
                var n, i, o, a = oe._data(t), r = oe._data(e, a), s = a.events;
                if (s) {
                    delete r.handle, r.events = {};
                    for (n in s)for (i = 0, o = s[n].length; o > i; i++)oe.event.add(e, n, s[n][i])
                }
                r.data && (r.data = oe.extend({}, r.data))
            }
        }

        function C(t, e) {
            var n, i, o;
            if (1 === e.nodeType) {
                if (n = e.nodeName.toLowerCase(), !ne.noCloneEvent && e[oe.expando]) {
                    o = oe._data(e);
                    for (i in o.events)oe.removeEvent(e, i, o.handle);
                    e.removeAttribute(oe.expando)
                }
                "script" === n && e.text !== t.text ? (b(e).text = t.text, w(e)) : "object" === n ? (e.parentNode && (e.outerHTML = t.outerHTML), ne.html5Clone && t.innerHTML && !oe.trim(e.innerHTML) && (e.innerHTML = t.innerHTML)) : "input" === n && Ne.test(t.type) ? (e.defaultChecked = e.checked = t.checked, e.value !== t.value && (e.value = t.value)) : "option" === n ? e.defaultSelected = e.selected = t.defaultSelected : ("input" === n || "textarea" === n) && (e.defaultValue = t.defaultValue)
            }
        }

        function k(e, n) {
            var i, o = oe(n.createElement(e)).appendTo(n.body), a = t.getDefaultComputedStyle && (i = t.getDefaultComputedStyle(o[0])) ? i.display : oe.css(o[0], "display");
            return o.detach(), a
        }

        function T(t) {
            var e = pe, n = Ke[t];
            return n || (n = k(t, e), "none" !== n && n || (Je = (Je || oe("<iframe frameborder='0' width='0' height='0'/>")).appendTo(e.documentElement), e = (Je[0].contentWindow || Je[0].contentDocument).document, e.write(), e.close(), n = k(t, e), Je.detach()), Ke[t] = n), n
        }

        function E(t, e) {
            return {
                get: function () {
                    var n = t();
                    if (null != n)return n ? void delete this.get : (this.get = e).apply(this, arguments)
                }
            }
        }

        function S(t, e) {
            if (e in t)return e;
            for (var n = e.charAt(0).toUpperCase() + e.slice(1), i = e, o = fn.length; o--;)if (e = fn[o] + n, e in t)return e;
            return i
        }

        function D(t, e) {
            for (var n, i, o, a = [], r = 0, s = t.length; s > r; r++)i = t[r], i.style && (a[r] = oe._data(i, "olddisplay"), n = i.style.display, e ? (a[r] || "none" !== n || (i.style.display = ""), "" === i.style.display && De(i) && (a[r] = oe._data(i, "olddisplay", T(i.nodeName)))) : (o = De(i), (n && "none" !== n || !o) && oe._data(i, "olddisplay", o ? n : oe.css(i, "display"))));
            for (r = 0; s > r; r++)i = t[r], i.style && (e && "none" !== i.style.display && "" !== i.style.display || (i.style.display = e ? a[r] || "" : "none"));
            return t
        }

        function j(t, e, n) {
            var i = un.exec(e);
            return i ? Math.max(0, i[1] - (n || 0)) + (i[2] || "px") : e
        }

        function N(t, e, n, i, o) {
            for (var a = n === (i ? "border" : "content") ? 4 : "width" === e ? 1 : 0, r = 0; 4 > a; a += 2)"margin" === n && (r += oe.css(t, n + Se[a], !0, o)), i ? ("content" === n && (r -= oe.css(t, "padding" + Se[a], !0, o)), "margin" !== n && (r -= oe.css(t, "border" + Se[a] + "Width", !0, o))) : (r += oe.css(t, "padding" + Se[a], !0, o), "padding" !== n && (r += oe.css(t, "border" + Se[a] + "Width", !0, o)));
            return r
        }

        function $(t, e, n) {
            var i = !0, o = "width" === e ? t.offsetWidth : t.offsetHeight, a = tn(t), r = ne.boxSizing && "border-box" === oe.css(t, "boxSizing", !1, a);
            if (0 >= o || null == o) {
                if (o = en(t, e, a), (0 > o || null == o) && (o = t.style[e]), on.test(o))return o;
                i = r && (ne.boxSizingReliable() || o === t.style[e]), o = parseFloat(o) || 0
            }
            return o + N(t, e, n || (r ? "border" : "content"), i, a) + "px"
        }

        function A(t, e, n, i, o) {
            return new A.prototype.init(t, e, n, i, o)
        }

        function F() {
            return setTimeout(function () {
                pn = void 0
            }), pn = oe.now()
        }

        function H(t, e) {
            var n, i = {height: t}, o = 0;
            for (e = e ? 1 : 0; 4 > o; o += 2 - e)n = Se[o], i["margin" + n] = i["padding" + n] = t;
            return e && (i.opacity = i.width = t), i
        }

        function P(t, e, n) {
            for (var i, o = (wn[e] || []).concat(wn["*"]), a = 0, r = o.length; r > a; a++)if (i = o[a].call(n, e, t))return i
        }

        function I(t, e, n) {
            var i, o, a, r, s, l, u, c, d = this, h = {}, f = t.style, p = t.nodeType && De(t), m = oe._data(t, "fxshow");
            n.queue || (s = oe._queueHooks(t, "fx"), null == s.unqueued && (s.unqueued = 0, l = s.empty.fire, s.empty.fire = function () {
                s.unqueued || l()
            }), s.unqueued++, d.always(function () {
                d.always(function () {
                    s.unqueued--, oe.queue(t, "fx").length || s.empty.fire()
                })
            })), 1 === t.nodeType && ("height" in e || "width" in e) && (n.overflow = [f.overflow, f.overflowX, f.overflowY], u = oe.css(t, "display"), c = "none" === u ? oe._data(t, "olddisplay") || T(t.nodeName) : u, "inline" === c && "none" === oe.css(t, "float") && (ne.inlineBlockNeedsLayout && "inline" !== T(t.nodeName) ? f.zoom = 1 : f.display = "inline-block")), n.overflow && (f.overflow = "hidden", ne.shrinkWrapBlocks() || d.always(function () {
                f.overflow = n.overflow[0], f.overflowX = n.overflow[1], f.overflowY = n.overflow[2]
            }));
            for (i in e)if (o = e[i], gn.exec(o)) {
                if (delete e[i], a = a || "toggle" === o, o === (p ? "hide" : "show")) {
                    if ("show" !== o || !m || void 0 === m[i])continue;
                    p = !0
                }
                h[i] = m && m[i] || oe.style(t, i)
            } else u = void 0;
            if (oe.isEmptyObject(h))"inline" === ("none" === u ? T(t.nodeName) : u) && (f.display = u); else {
                m ? "hidden" in m && (p = m.hidden) : m = oe._data(t, "fxshow", {}), a && (m.hidden = !p), p ? oe(t).show() : d.done(function () {
                    oe(t).hide()
                }), d.done(function () {
                    var e;
                    oe._removeData(t, "fxshow");
                    for (e in h)oe.style(t, e, h[e])
                });
                for (i in h)r = P(p ? m[i] : 0, i, d), i in m || (m[i] = r.start, p && (r.end = r.start, r.start = "width" === i || "height" === i ? 1 : 0))
            }
        }

        function L(t, e) {
            var n, i, o, a, r;
            for (n in t)if (i = oe.camelCase(n), o = e[i], a = t[n], oe.isArray(a) && (o = a[1], a = t[n] = a[0]), n !== i && (t[i] = a, delete t[n]), r = oe.cssHooks[i], r && "expand" in r) {
                a = r.expand(a), delete t[i];
                for (n in a)n in t || (t[n] = a[n], e[n] = o)
            } else e[i] = o
        }

        function O(t, e, n) {
            var i, o, a = 0, r = bn.length, s = oe.Deferred().always(function () {
                delete l.elem
            }), l = function () {
                if (o)return !1;
                for (var e = pn || F(), n = Math.max(0, u.startTime + u.duration - e), i = n / u.duration || 0, a = 1 - i, r = 0, l = u.tweens.length; l > r; r++)u.tweens[r].run(a);
                return s.notifyWith(t, [u, a, n]), 1 > a && l ? n : (s.resolveWith(t, [u]), !1)
            }, u = s.promise({
                elem: t,
                props: oe.extend({}, e),
                opts: oe.extend(!0, {specialEasing: {}}, n),
                originalProperties: e,
                originalOptions: n,
                startTime: pn || F(),
                duration: n.duration,
                tweens: [],
                createTween: function (e, n) {
                    var i = oe.Tween(t, u.opts, e, n, u.opts.specialEasing[e] || u.opts.easing);
                    return u.tweens.push(i), i
                },
                stop: function (e) {
                    var n = 0, i = e ? u.tweens.length : 0;
                    if (o)return this;
                    for (o = !0; i > n; n++)u.tweens[n].run(1);
                    return e ? s.resolveWith(t, [u, e]) : s.rejectWith(t, [u, e]), this
                }
            }), c = u.props;
            for (L(c, u.opts.specialEasing); r > a; a++)if (i = bn[a].call(u, t, c, u.opts))return i;
            return oe.map(c, P, u), oe.isFunction(u.opts.start) && u.opts.start.call(t, u), oe.fx.timer(oe.extend(l, {
                elem: t,
                anim: u,
                queue: u.opts.queue
            })), u.progress(u.opts.progress).done(u.opts.done, u.opts.complete).fail(u.opts.fail).always(u.opts.always)
        }

        function M(t) {
            return function (e, n) {
                "string" != typeof e && (n = e, e = "*");
                var i, o = 0, a = e.toLowerCase().match(be) || [];
                if (oe.isFunction(n))for (; i = a[o++];)"+" === i.charAt(0) ? (i = i.slice(1) || "*", (t[i] = t[i] || []).unshift(n)) : (t[i] = t[i] || []).push(n)
            }
        }

        function q(t, e, n, i) {
            function o(s) {
                var l;
                return a[s] = !0, oe.each(t[s] || [], function (t, s) {
                    var u = s(e, n, i);
                    return "string" != typeof u || r || a[u] ? r ? !(l = u) : void 0 : (e.dataTypes.unshift(u), o(u), !1)
                }), l
            }

            var a = {}, r = t === zn;
            return o(e.dataTypes[0]) || !a["*"] && o("*")
        }

        function W(t, e) {
            var n, i, o = oe.ajaxSettings.flatOptions || {};
            for (i in e)void 0 !== e[i] && ((o[i] ? t : n || (n = {}))[i] = e[i]);
            return n && oe.extend(!0, t, n), t
        }

        function R(t, e, n) {
            for (var i, o, a, r, s = t.contents, l = t.dataTypes; "*" === l[0];)l.shift(), void 0 === o && (o = t.mimeType || e.getResponseHeader("Content-Type"));
            if (o)for (r in s)if (s[r] && s[r].test(o)) {
                l.unshift(r);
                break
            }
            if (l[0] in n)a = l[0]; else {
                for (r in n) {
                    if (!l[0] || t.converters[r + " " + l[0]]) {
                        a = r;
                        break
                    }
                    i || (i = r)
                }
                a = a || i
            }
            return a ? (a !== l[0] && l.unshift(a), n[a]) : void 0
        }

        function B(t, e, n, i) {
            var o, a, r, s, l, u = {}, c = t.dataTypes.slice();
            if (c[1])for (r in t.converters)u[r.toLowerCase()] = t.converters[r];
            for (a = c.shift(); a;)if (t.responseFields[a] && (n[t.responseFields[a]] = e), !l && i && t.dataFilter && (e = t.dataFilter(e, t.dataType)), l = a, a = c.shift())if ("*" === a)a = l; else if ("*" !== l && l !== a) {
                if (r = u[l + " " + a] || u["* " + a], !r)for (o in u)if (s = o.split(" "), s[1] === a && (r = u[l + " " + s[0]] || u["* " + s[0]])) {
                    r === !0 ? r = u[o] : u[o] !== !0 && (a = s[0], c.unshift(s[1]));
                    break
                }
                if (r !== !0)if (r && t["throws"])e = r(e); else try {
                    e = r(e)
                } catch (d) {
                    return {state: "parsererror", error: r ? d : "No conversion from " + l + " to " + a}
                }
            }
            return {state: "success", data: e}
        }

        function z(t, e, n, i) {
            var o;
            if (oe.isArray(e))oe.each(e, function (e, o) {
                n || Qn.test(t) ? i(t, o) : z(t + "[" + ("object" == typeof o ? e : "") + "]", o, n, i)
            }); else if (n || "object" !== oe.type(e))i(t, e); else for (o in e)z(t + "[" + o + "]", e[o], n, i)
        }

        function U() {
            try {
                return new t.XMLHttpRequest
            } catch (e) {
            }
        }

        function G() {
            try {
                return new t.ActiveXObject("Microsoft.XMLHTTP")
            } catch (e) {
            }
        }

        function X(t) {
            return oe.isWindow(t) ? t : 9 === t.nodeType ? t.defaultView || t.parentWindow : !1
        }

        var Q = [], V = Q.slice, Y = Q.concat, Z = Q.push, J = Q.indexOf, K = {}, te = K.toString, ee = K.hasOwnProperty, ne = {}, ie = "1.11.1", oe = function (t, e) {
            return new oe.fn.init(t, e)
        }, ae = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, re = /^-ms-/, se = /-([\da-z])/gi, le = function (t, e) {
            return e.toUpperCase()
        };
        oe.fn = oe.prototype = {
            jquery: ie, constructor: oe, selector: "", length: 0, toArray: function () {
                return V.call(this)
            }, get: function (t) {
                return null != t ? 0 > t ? this[t + this.length] : this[t] : V.call(this)
            }, pushStack: function (t) {
                var e = oe.merge(this.constructor(), t);
                return e.prevObject = this, e.context = this.context, e
            }, each: function (t, e) {
                return oe.each(this, t, e)
            }, map: function (t) {
                return this.pushStack(oe.map(this, function (e, n) {
                    return t.call(e, n, e)
                }))
            }, slice: function () {
                return this.pushStack(V.apply(this, arguments))
            }, first: function () {
                return this.eq(0)
            }, last: function () {
                return this.eq(-1)
            }, eq: function (t) {
                var e = this.length, n = +t + (0 > t ? e : 0);
                return this.pushStack(n >= 0 && e > n ? [this[n]] : [])
            }, end: function () {
                return this.prevObject || this.constructor(null)
            }, push: Z, sort: Q.sort, splice: Q.splice
        }, oe.extend = oe.fn.extend = function () {
            var t, e, n, i, o, a, r = arguments[0] || {}, s = 1, l = arguments.length, u = !1;
            for ("boolean" == typeof r && (u = r, r = arguments[s] || {}, s++), "object" == typeof r || oe.isFunction(r) || (r = {}), s === l && (r = this, s--); l > s; s++)if (null != (o = arguments[s]))for (i in o)t = r[i], n = o[i], r !== n && (u && n && (oe.isPlainObject(n) || (e = oe.isArray(n))) ? (e ? (e = !1, a = t && oe.isArray(t) ? t : []) : a = t && oe.isPlainObject(t) ? t : {}, r[i] = oe.extend(u, a, n)) : void 0 !== n && (r[i] = n));
            return r
        }, oe.extend({
            expando: "jQuery" + (ie + Math.random()).replace(/\D/g, ""), isReady: !0, error: function (t) {
                throw new Error(t)
            }, noop: function () {
            }, isFunction: function (t) {
                return "function" === oe.type(t)
            }, isArray: Array.isArray || function (t) {
                return "array" === oe.type(t)
            }, isWindow: function (t) {
                return null != t && t == t.window
            }, isNumeric: function (t) {
                return !oe.isArray(t) && t - parseFloat(t) >= 0
            }, isEmptyObject: function (t) {
                var e;
                for (e in t)return !1;
                return !0
            }, isPlainObject: function (t) {
                var e;
                if (!t || "object" !== oe.type(t) || t.nodeType || oe.isWindow(t))return !1;
                try {
                    if (t.constructor && !ee.call(t, "constructor") && !ee.call(t.constructor.prototype, "isPrototypeOf"))return !1
                } catch (n) {
                    return !1
                }
                if (ne.ownLast)for (e in t)return ee.call(t, e);
                for (e in t);
                return void 0 === e || ee.call(t, e)
            }, type: function (t) {
                return null == t ? t + "" : "object" == typeof t || "function" == typeof t ? K[te.call(t)] || "object" : typeof t
            }, globalEval: function (e) {
                e && oe.trim(e) && (t.execScript || function (e) {
                    t.eval.call(t, e)
                })(e)
            }, camelCase: function (t) {
                return t.replace(re, "ms-").replace(se, le)
            }, nodeName: function (t, e) {
                return t.nodeName && t.nodeName.toLowerCase() === e.toLowerCase()
            }, each: function (t, e, i) {
                var o, a = 0, r = t.length, s = n(t);
                if (i) {
                    if (s)for (; r > a && (o = e.apply(t[a], i), o !== !1); a++); else for (a in t)if (o = e.apply(t[a], i), o === !1)break
                } else if (s)for (; r > a && (o = e.call(t[a], a, t[a]), o !== !1); a++); else for (a in t)if (o = e.call(t[a], a, t[a]), o === !1)break;
                return t
            }, trim: function (t) {
                return null == t ? "" : (t + "").replace(ae, "")
            }, makeArray: function (t, e) {
                var i = e || [];
                return null != t && (n(Object(t)) ? oe.merge(i, "string" == typeof t ? [t] : t) : Z.call(i, t)), i
            }, inArray: function (t, e, n) {
                var i;
                if (e) {
                    if (J)return J.call(e, t, n);
                    for (i = e.length, n = n ? 0 > n ? Math.max(0, i + n) : n : 0; i > n; n++)if (n in e && e[n] === t)return n
                }
                return -1
            }, merge: function (t, e) {
                for (var n = +e.length, i = 0, o = t.length; n > i;)t[o++] = e[i++];
                if (n !== n)for (; void 0 !== e[i];)t[o++] = e[i++];
                return t.length = o, t
            }, grep: function (t, e, n) {
                for (var i, o = [], a = 0, r = t.length, s = !n; r > a; a++)i = !e(t[a], a), i !== s && o.push(t[a]);
                return o
            }, map: function (t, e, i) {
                var o, a = 0, r = t.length, s = n(t), l = [];
                if (s)for (; r > a; a++)o = e(t[a], a, i), null != o && l.push(o); else for (a in t)o = e(t[a], a, i), null != o && l.push(o);
                return Y.apply([], l)
            }, guid: 1, proxy: function (t, e) {
                var n, i, o;
                return "string" == typeof e && (o = t[e], e = t, t = o), oe.isFunction(t) ? (n = V.call(arguments, 2), i = function () {
                    return t.apply(e || this, n.concat(V.call(arguments)))
                }, i.guid = t.guid = t.guid || oe.guid++, i) : void 0
            }, now: function () {
                return +new Date
            }, support: ne
        }), oe.each("Boolean Number String Function Array Date RegExp Object Error".split(" "), function (t, e) {
            K["[object " + e + "]"] = e.toLowerCase()
        });
        var ue = function (t) {
            function e(t, e, n, i) {
                var o, a, r, s, l, u, d, f, p, m;
                if ((e ? e.ownerDocument || e : q) !== A && $(e), e = e || A, n = n || [], !t || "string" != typeof t)return n;
                if (1 !== (s = e.nodeType) && 9 !== s)return [];
                if (H && !i) {
                    if (o = ye.exec(t))if (r = o[1]) {
                        if (9 === s) {
                            if (a = e.getElementById(r), !a || !a.parentNode)return n;
                            if (a.id === r)return n.push(a), n
                        } else if (e.ownerDocument && (a = e.ownerDocument.getElementById(r)) && O(e, a) && a.id === r)return n.push(a), n
                    } else {
                        if (o[2])return K.apply(n, e.getElementsByTagName(t)), n;
                        if ((r = o[3]) && x.getElementsByClassName && e.getElementsByClassName)return K.apply(n, e.getElementsByClassName(r)), n
                    }
                    if (x.qsa && (!P || !P.test(t))) {
                        if (f = d = M, p = e, m = 9 === s && t, 1 === s && "object" !== e.nodeName.toLowerCase()) {
                            for (u = T(t), (d = e.getAttribute("id")) ? f = d.replace(we, "\\$&") : e.setAttribute("id", f), f = "[id='" + f + "'] ", l = u.length; l--;)u[l] = f + h(u[l]);
                            p = be.test(t) && c(e.parentNode) || e, m = u.join(",")
                        }
                        if (m)try {
                            return K.apply(n, p.querySelectorAll(m)), n
                        } catch (g) {
                        } finally {
                            d || e.removeAttribute("id")
                        }
                    }
                }
                return S(t.replace(le, "$1"), e, n, i)
            }

            function n() {
                function t(n, i) {
                    return e.push(n + " ") > _.cacheLength && delete t[e.shift()], t[n + " "] = i
                }

                var e = [];
                return t
            }

            function i(t) {
                return t[M] = !0, t
            }

            function o(t) {
                var e = A.createElement("div");
                try {
                    return !!t(e)
                } catch (n) {
                    return !1
                } finally {
                    e.parentNode && e.parentNode.removeChild(e), e = null
                }
            }

            function a(t, e) {
                for (var n = t.split("|"), i = t.length; i--;)_.attrHandle[n[i]] = e
            }

            function r(t, e) {
                var n = e && t, i = n && 1 === t.nodeType && 1 === e.nodeType && (~e.sourceIndex || Q) - (~t.sourceIndex || Q);
                if (i)return i;
                if (n)for (; n = n.nextSibling;)if (n === e)return -1;
                return t ? 1 : -1
            }

            function s(t) {
                return function (e) {
                    var n = e.nodeName.toLowerCase();
                    return "input" === n && e.type === t
                }
            }

            function l(t) {
                return function (e) {
                    var n = e.nodeName.toLowerCase();
                    return ("input" === n || "button" === n) && e.type === t
                }
            }

            function u(t) {
                return i(function (e) {
                    return e = +e, i(function (n, i) {
                        for (var o, a = t([], n.length, e), r = a.length; r--;)n[o = a[r]] && (n[o] = !(i[o] = n[o]))
                    })
                })
            }

            function c(t) {
                return t && typeof t.getElementsByTagName !== X && t
            }

            function d() {
            }

            function h(t) {
                for (var e = 0, n = t.length, i = ""; n > e; e++)i += t[e].value;
                return i
            }

            function f(t, e, n) {
                var i = e.dir, o = n && "parentNode" === i, a = R++;
                return e.first ? function (e, n, a) {
                    for (; e = e[i];)if (1 === e.nodeType || o)return t(e, n, a)
                } : function (e, n, r) {
                    var s, l, u = [W, a];
                    if (r) {
                        for (; e = e[i];)if ((1 === e.nodeType || o) && t(e, n, r))return !0
                    } else for (; e = e[i];)if (1 === e.nodeType || o) {
                        if (l = e[M] || (e[M] = {}), (s = l[i]) && s[0] === W && s[1] === a)return u[2] = s[2];
                        if (l[i] = u, u[2] = t(e, n, r))return !0
                    }
                }
            }

            function p(t) {
                return t.length > 1 ? function (e, n, i) {
                    for (var o = t.length; o--;)if (!t[o](e, n, i))return !1;
                    return !0
                } : t[0]
            }

            function m(t, n, i) {
                for (var o = 0, a = n.length; a > o; o++)e(t, n[o], i);
                return i
            }

            function g(t, e, n, i, o) {
                for (var a, r = [], s = 0, l = t.length, u = null != e; l > s; s++)(a = t[s]) && (!n || n(a, i, o)) && (r.push(a), u && e.push(s));
                return r
            }

            function v(t, e, n, o, a, r) {
                return o && !o[M] && (o = v(o)), a && !a[M] && (a = v(a, r)), i(function (i, r, s, l) {
                    var u, c, d, h = [], f = [], p = r.length, v = i || m(e || "*", s.nodeType ? [s] : s, []), y = !t || !i && e ? v : g(v, h, t, s, l), b = n ? a || (i ? t : p || o) ? [] : r : y;
                    if (n && n(y, b, s, l), o)for (u = g(b, f), o(u, [], s, l), c = u.length; c--;)(d = u[c]) && (b[f[c]] = !(y[f[c]] = d));
                    if (i) {
                        if (a || t) {
                            if (a) {
                                for (u = [], c = b.length; c--;)(d = b[c]) && u.push(y[c] = d);
                                a(null, b = [], u, l)
                            }
                            for (c = b.length; c--;)(d = b[c]) && (u = a ? ee.call(i, d) : h[c]) > -1 && (i[u] = !(r[u] = d))
                        }
                    } else b = g(b === r ? b.splice(p, b.length) : b), a ? a(null, r, b, l) : K.apply(r, b)
                })
            }

            function y(t) {
                for (var e, n, i, o = t.length, a = _.relative[t[0].type], r = a || _.relative[" "], s = a ? 1 : 0, l = f(function (t) {
                    return t === e
                }, r, !0), u = f(function (t) {
                    return ee.call(e, t) > -1
                }, r, !0), c = [function (t, n, i) {
                    return !a && (i || n !== D) || ((e = n).nodeType ? l(t, n, i) : u(t, n, i))
                }]; o > s; s++)if (n = _.relative[t[s].type])c = [f(p(c), n)]; else {
                    if (n = _.filter[t[s].type].apply(null, t[s].matches), n[M]) {
                        for (i = ++s; o > i && !_.relative[t[i].type]; i++);
                        return v(s > 1 && p(c), s > 1 && h(t.slice(0, s - 1).concat({value: " " === t[s - 2].type ? "*" : ""})).replace(le, "$1"), n, i > s && y(t.slice(s, i)), o > i && y(t = t.slice(i)), o > i && h(t))
                    }
                    c.push(n)
                }
                return p(c)
            }

            function b(t, n) {
                var o = n.length > 0, a = t.length > 0, r = function (i, r, s, l, u) {
                    var c, d, h, f = 0, p = "0", m = i && [], v = [], y = D, b = i || a && _.find.TAG("*", u), w = W += null == y ? 1 : Math.random() || .1, x = b.length;
                    for (u && (D = r !== A && r); p !== x && null != (c = b[p]); p++) {
                        if (a && c) {
                            for (d = 0; h = t[d++];)if (h(c, r, s)) {
                                l.push(c);
                                break
                            }
                            u && (W = w)
                        }
                        o && ((c = !h && c) && f--, i && m.push(c))
                    }
                    if (f += p, o && p !== f) {
                        for (d = 0; h = n[d++];)h(m, v, r, s);
                        if (i) {
                            if (f > 0)for (; p--;)m[p] || v[p] || (v[p] = Z.call(l));
                            v = g(v)
                        }
                        K.apply(l, v), u && !i && v.length > 0 && f + n.length > 1 && e.uniqueSort(l)
                    }
                    return u && (W = w, D = y), m
                };
                return o ? i(r) : r
            }

            var w, x, _, C, k, T, E, S, D, j, N, $, A, F, H, P, I, L, O, M = "sizzle" + -new Date, q = t.document, W = 0, R = 0, B = n(), z = n(), U = n(), G = function (t, e) {
                return t === e && (N = !0), 0
            }, X = "undefined", Q = 1 << 31, V = {}.hasOwnProperty, Y = [], Z = Y.pop, J = Y.push, K = Y.push, te = Y.slice, ee = Y.indexOf || function (t) {
                    for (var e = 0, n = this.length; n > e; e++)if (this[e] === t)return e;
                    return -1
                }, ne = "checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped", ie = "[\\x20\\t\\r\\n\\f]", oe = "(?:\\\\.|[\\w-]|[^\\x00-\\xa0])+", ae = oe.replace("w", "w#"), re = "\\[" + ie + "*(" + oe + ")(?:" + ie + "*([*^$|!~]?=)" + ie + "*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|(" + ae + "))|)" + ie + "*\\]", se = ":(" + oe + ")(?:\\((('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|((?:\\\\.|[^\\\\()[\\]]|" + re + ")*)|.*)\\)|)", le = new RegExp("^" + ie + "+|((?:^|[^\\\\])(?:\\\\.)*)" + ie + "+$", "g"), ue = new RegExp("^" + ie + "*," + ie + "*"), ce = new RegExp("^" + ie + "*([>+~]|" + ie + ")" + ie + "*"), de = new RegExp("=" + ie + "*([^\\]'\"]*?)" + ie + "*\\]", "g"), he = new RegExp(se), fe = new RegExp("^" + ae + "$"), pe = {
                ID: new RegExp("^#(" + oe + ")"),
                CLASS: new RegExp("^\\.(" + oe + ")"),
                TAG: new RegExp("^(" + oe.replace("w", "w*") + ")"),
                ATTR: new RegExp("^" + re),
                PSEUDO: new RegExp("^" + se),
                CHILD: new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" + ie + "*(even|odd|(([+-]|)(\\d*)n|)" + ie + "*(?:([+-]|)" + ie + "*(\\d+)|))" + ie + "*\\)|)", "i"),
                bool: new RegExp("^(?:" + ne + ")$", "i"),
                needsContext: new RegExp("^" + ie + "*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + ie + "*((?:-\\d)?\\d*)" + ie + "*\\)|)(?=[^-]|$)", "i")
            }, me = /^(?:input|select|textarea|button)$/i, ge = /^h\d$/i, ve = /^[^{]+\{\s*\[native \w/, ye = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/, be = /[+~]/, we = /'|\\/g, xe = new RegExp("\\\\([\\da-f]{1,6}" + ie + "?|(" + ie + ")|.)", "ig"), _e = function (t, e, n) {
                var i = "0x" + e - 65536;
                return i !== i || n ? e : 0 > i ? String.fromCharCode(i + 65536) : String.fromCharCode(i >> 10 | 55296, 1023 & i | 56320)
            };
            try {
                K.apply(Y = te.call(q.childNodes), q.childNodes), Y[q.childNodes.length].nodeType
            } catch (Ce) {
                K = {
                    apply: Y.length ? function (t, e) {
                        J.apply(t, te.call(e))
                    } : function (t, e) {
                        for (var n = t.length, i = 0; t[n++] = e[i++];);
                        t.length = n - 1
                    }
                }
            }
            x = e.support = {}, k = e.isXML = function (t) {
                var e = t && (t.ownerDocument || t).documentElement;
                return e ? "HTML" !== e.nodeName : !1
            }, $ = e.setDocument = function (t) {
                var e, n = t ? t.ownerDocument || t : q, i = n.defaultView;
                return n !== A && 9 === n.nodeType && n.documentElement ? (A = n, F = n.documentElement, H = !k(n), i && i !== i.top && (i.addEventListener ? i.addEventListener("unload", function () {
                    $()
                }, !1) : i.attachEvent && i.attachEvent("onunload", function () {
                    $()
                })), x.attributes = o(function (t) {
                    return t.className = "i", !t.getAttribute("className")
                }), x.getElementsByTagName = o(function (t) {
                    return t.appendChild(n.createComment("")), !t.getElementsByTagName("*").length
                }), x.getElementsByClassName = ve.test(n.getElementsByClassName) && o(function (t) {
                        return t.innerHTML = "<div class='a'></div><div class='a i'></div>", t.firstChild.className = "i", 2 === t.getElementsByClassName("i").length
                    }), x.getById = o(function (t) {
                    return F.appendChild(t).id = M, !n.getElementsByName || !n.getElementsByName(M).length
                }), x.getById ? (_.find.ID = function (t, e) {
                    if (typeof e.getElementById !== X && H) {
                        var n = e.getElementById(t);
                        return n && n.parentNode ? [n] : []
                    }
                }, _.filter.ID = function (t) {
                    var e = t.replace(xe, _e);
                    return function (t) {
                        return t.getAttribute("id") === e
                    }
                }) : (delete _.find.ID, _.filter.ID = function (t) {
                    var e = t.replace(xe, _e);
                    return function (t) {
                        var n = typeof t.getAttributeNode !== X && t.getAttributeNode("id");
                        return n && n.value === e
                    }
                }), _.find.TAG = x.getElementsByTagName ? function (t, e) {
                    return typeof e.getElementsByTagName !== X ? e.getElementsByTagName(t) : void 0
                } : function (t, e) {
                    var n, i = [], o = 0, a = e.getElementsByTagName(t);
                    if ("*" === t) {
                        for (; n = a[o++];)1 === n.nodeType && i.push(n);
                        return i
                    }
                    return a
                }, _.find.CLASS = x.getElementsByClassName && function (t, e) {
                        return typeof e.getElementsByClassName !== X && H ? e.getElementsByClassName(t) : void 0
                    }, I = [], P = [], (x.qsa = ve.test(n.querySelectorAll)) && (o(function (t) {
                    t.innerHTML = "<select msallowclip=''><option selected=''></option></select>", t.querySelectorAll("[msallowclip^='']").length && P.push("[*^$]=" + ie + "*(?:''|\"\")"), t.querySelectorAll("[selected]").length || P.push("\\[" + ie + "*(?:value|" + ne + ")"), t.querySelectorAll(":checked").length || P.push(":checked")
                }), o(function (t) {
                    var e = n.createElement("input");
                    e.setAttribute("type", "hidden"), t.appendChild(e).setAttribute("name", "D"), t.querySelectorAll("[name=d]").length && P.push("name" + ie + "*[*^$|!~]?="), t.querySelectorAll(":enabled").length || P.push(":enabled", ":disabled"), t.querySelectorAll("*,:x"), P.push(",.*:")
                })), (x.matchesSelector = ve.test(L = F.matches || F.webkitMatchesSelector || F.mozMatchesSelector || F.oMatchesSelector || F.msMatchesSelector)) && o(function (t) {
                    x.disconnectedMatch = L.call(t, "div"), L.call(t, "[s!='']:x"), I.push("!=", se)
                }), P = P.length && new RegExp(P.join("|")), I = I.length && new RegExp(I.join("|")), e = ve.test(F.compareDocumentPosition), O = e || ve.test(F.contains) ? function (t, e) {
                    var n = 9 === t.nodeType ? t.documentElement : t, i = e && e.parentNode;
                    return t === i || !(!i || 1 !== i.nodeType || !(n.contains ? n.contains(i) : t.compareDocumentPosition && 16 & t.compareDocumentPosition(i)))
                } : function (t, e) {
                    if (e)for (; e = e.parentNode;)if (e === t)return !0;
                    return !1
                }, G = e ? function (t, e) {
                    if (t === e)return N = !0, 0;
                    var i = !t.compareDocumentPosition - !e.compareDocumentPosition;
                    return i ? i : (i = (t.ownerDocument || t) === (e.ownerDocument || e) ? t.compareDocumentPosition(e) : 1, 1 & i || !x.sortDetached && e.compareDocumentPosition(t) === i ? t === n || t.ownerDocument === q && O(q, t) ? -1 : e === n || e.ownerDocument === q && O(q, e) ? 1 : j ? ee.call(j, t) - ee.call(j, e) : 0 : 4 & i ? -1 : 1)
                } : function (t, e) {
                    if (t === e)return N = !0, 0;
                    var i, o = 0, a = t.parentNode, s = e.parentNode, l = [t], u = [e];
                    if (!a || !s)return t === n ? -1 : e === n ? 1 : a ? -1 : s ? 1 : j ? ee.call(j, t) - ee.call(j, e) : 0;
                    if (a === s)return r(t, e);
                    for (i = t; i = i.parentNode;)l.unshift(i);
                    for (i = e; i = i.parentNode;)u.unshift(i);
                    for (; l[o] === u[o];)o++;
                    return o ? r(l[o], u[o]) : l[o] === q ? -1 : u[o] === q ? 1 : 0
                }, n) : A
            }, e.matches = function (t, n) {
                return e(t, null, null, n)
            }, e.matchesSelector = function (t, n) {
                if ((t.ownerDocument || t) !== A && $(t), n = n.replace(de, "='$1']"), !(!x.matchesSelector || !H || I && I.test(n) || P && P.test(n)))try {
                    var i = L.call(t, n);
                    if (i || x.disconnectedMatch || t.document && 11 !== t.document.nodeType)return i
                } catch (o) {
                }
                return e(n, A, null, [t]).length > 0
            }, e.contains = function (t, e) {
                return (t.ownerDocument || t) !== A && $(t), O(t, e)
            }, e.attr = function (t, e) {
                (t.ownerDocument || t) !== A && $(t);
                var n = _.attrHandle[e.toLowerCase()], i = n && V.call(_.attrHandle, e.toLowerCase()) ? n(t, e, !H) : void 0;
                return void 0 !== i ? i : x.attributes || !H ? t.getAttribute(e) : (i = t.getAttributeNode(e)) && i.specified ? i.value : null
            }, e.error = function (t) {
                throw new Error("Syntax error, unrecognized expression: " + t)
            }, e.uniqueSort = function (t) {
                var e, n = [], i = 0, o = 0;
                if (N = !x.detectDuplicates, j = !x.sortStable && t.slice(0), t.sort(G), N) {
                    for (; e = t[o++];)e === t[o] && (i = n.push(o));
                    for (; i--;)t.splice(n[i], 1)
                }
                return j = null, t
            }, C = e.getText = function (t) {
                var e, n = "", i = 0, o = t.nodeType;
                if (o) {
                    if (1 === o || 9 === o || 11 === o) {
                        if ("string" == typeof t.textContent)return t.textContent;
                        for (t = t.firstChild; t; t = t.nextSibling)n += C(t)
                    } else if (3 === o || 4 === o)return t.nodeValue
                } else for (; e = t[i++];)n += C(e);
                return n
            }, _ = e.selectors = {
                cacheLength: 50,
                createPseudo: i,
                match: pe,
                attrHandle: {},
                find: {},
                relative: {
                    ">": {dir: "parentNode", first: !0},
                    " ": {dir: "parentNode"},
                    "+": {dir: "previousSibling", first: !0},
                    "~": {dir: "previousSibling"}
                },
                preFilter: {
                    ATTR: function (t) {
                        return t[1] = t[1].replace(xe, _e), t[3] = (t[3] || t[4] || t[5] || "").replace(xe, _e), "~=" === t[2] && (t[3] = " " + t[3] + " "), t.slice(0, 4)
                    }, CHILD: function (t) {
                        return t[1] = t[1].toLowerCase(), "nth" === t[1].slice(0, 3) ? (t[3] || e.error(t[0]), t[4] = +(t[4] ? t[5] + (t[6] || 1) : 2 * ("even" === t[3] || "odd" === t[3])), t[5] = +(t[7] + t[8] || "odd" === t[3])) : t[3] && e.error(t[0]), t
                    }, PSEUDO: function (t) {
                        var e, n = !t[6] && t[2];
                        return pe.CHILD.test(t[0]) ? null : (t[3] ? t[2] = t[4] || t[5] || "" : n && he.test(n) && (e = T(n, !0)) && (e = n.indexOf(")", n.length - e) - n.length) && (t[0] = t[0].slice(0, e), t[2] = n.slice(0, e)), t.slice(0, 3))
                    }
                },
                filter: {
                    TAG: function (t) {
                        var e = t.replace(xe, _e).toLowerCase();
                        return "*" === t ? function () {
                            return !0
                        } : function (t) {
                            return t.nodeName && t.nodeName.toLowerCase() === e
                        }
                    }, CLASS: function (t) {
                        var e = B[t + " "];
                        return e || (e = new RegExp("(^|" + ie + ")" + t + "(" + ie + "|$)")) && B(t, function (t) {
                                return e.test("string" == typeof t.className && t.className || typeof t.getAttribute !== X && t.getAttribute("class") || "")
                            })
                    }, ATTR: function (t, n, i) {
                        return function (o) {
                            var a = e.attr(o, t);
                            return null == a ? "!=" === n : n ? (a += "", "=" === n ? a === i : "!=" === n ? a !== i : "^=" === n ? i && 0 === a.indexOf(i) : "*=" === n ? i && a.indexOf(i) > -1 : "$=" === n ? i && a.slice(-i.length) === i : "~=" === n ? (" " + a + " ").indexOf(i) > -1 : "|=" === n ? a === i || a.slice(0, i.length + 1) === i + "-" : !1) : !0
                        }
                    }, CHILD: function (t, e, n, i, o) {
                        var a = "nth" !== t.slice(0, 3), r = "last" !== t.slice(-4), s = "of-type" === e;
                        return 1 === i && 0 === o ? function (t) {
                            return !!t.parentNode
                        } : function (e, n, l) {
                            var u, c, d, h, f, p, m = a !== r ? "nextSibling" : "previousSibling", g = e.parentNode, v = s && e.nodeName.toLowerCase(), y = !l && !s;
                            if (g) {
                                if (a) {
                                    for (; m;) {
                                        for (d = e; d = d[m];)if (s ? d.nodeName.toLowerCase() === v : 1 === d.nodeType)return !1;
                                        p = m = "only" === t && !p && "nextSibling"
                                    }
                                    return !0
                                }
                                if (p = [r ? g.firstChild : g.lastChild], r && y) {
                                    for (c = g[M] || (g[M] = {}), u = c[t] || [], f = u[0] === W && u[1], h = u[0] === W && u[2], d = f && g.childNodes[f]; d = ++f && d && d[m] || (h = f = 0) || p.pop();)if (1 === d.nodeType && ++h && d === e) {
                                        c[t] = [W, f, h];
                                        break
                                    }
                                } else if (y && (u = (e[M] || (e[M] = {}))[t]) && u[0] === W)h = u[1]; else for (; (d = ++f && d && d[m] || (h = f = 0) || p.pop()) && ((s ? d.nodeName.toLowerCase() !== v : 1 !== d.nodeType) || !++h || (y && ((d[M] || (d[M] = {}))[t] = [W, h]), d !== e)););
                                return h -= o, h === i || h % i === 0 && h / i >= 0
                            }
                        }
                    }, PSEUDO: function (t, n) {
                        var o, a = _.pseudos[t] || _.setFilters[t.toLowerCase()] || e.error("unsupported pseudo: " + t);
                        return a[M] ? a(n) : a.length > 1 ? (o = [t, t, "", n], _.setFilters.hasOwnProperty(t.toLowerCase()) ? i(function (t, e) {
                            for (var i, o = a(t, n), r = o.length; r--;)i = ee.call(t, o[r]), t[i] = !(e[i] = o[r])
                        }) : function (t) {
                            return a(t, 0, o)
                        }) : a
                    }
                },
                pseudos: {
                    not: i(function (t) {
                        var e = [], n = [], o = E(t.replace(le, "$1"));
                        return o[M] ? i(function (t, e, n, i) {
                            for (var a, r = o(t, null, i, []), s = t.length; s--;)(a = r[s]) && (t[s] = !(e[s] = a))
                        }) : function (t, i, a) {
                            return e[0] = t, o(e, null, a, n), !n.pop()
                        }
                    }), has: i(function (t) {
                        return function (n) {
                            return e(t, n).length > 0
                        }
                    }), contains: i(function (t) {
                        return function (e) {
                            return (e.textContent || e.innerText || C(e)).indexOf(t) > -1
                        }
                    }), lang: i(function (t) {
                        return fe.test(t || "") || e.error("unsupported lang: " + t), t = t.replace(xe, _e).toLowerCase(), function (e) {
                            var n;
                            do if (n = H ? e.lang : e.getAttribute("xml:lang") || e.getAttribute("lang"))return n = n.toLowerCase(), n === t || 0 === n.indexOf(t + "-"); while ((e = e.parentNode) && 1 === e.nodeType);
                            return !1
                        }
                    }), target: function (e) {
                        var n = t.location && t.location.hash;
                        return n && n.slice(1) === e.id
                    }, root: function (t) {
                        return t === F
                    }, focus: function (t) {
                        return t === A.activeElement && (!A.hasFocus || A.hasFocus()) && !!(t.type || t.href || ~t.tabIndex)
                    }, enabled: function (t) {
                        return t.disabled === !1
                    }, disabled: function (t) {
                        return t.disabled === !0
                    }, checked: function (t) {
                        var e = t.nodeName.toLowerCase();
                        return "input" === e && !!t.checked || "option" === e && !!t.selected
                    }, selected: function (t) {
                        return t.parentNode && t.parentNode.selectedIndex, t.selected === !0
                    }, empty: function (t) {
                        for (t = t.firstChild; t; t = t.nextSibling)if (t.nodeType < 6)return !1;
                        return !0
                    }, parent: function (t) {
                        return !_.pseudos.empty(t)
                    }, header: function (t) {
                        return ge.test(t.nodeName)
                    }, input: function (t) {
                        return me.test(t.nodeName)
                    }, button: function (t) {
                        var e = t.nodeName.toLowerCase();
                        return "input" === e && "button" === t.type || "button" === e
                    }, text: function (t) {
                        var e;
                        return "input" === t.nodeName.toLowerCase() && "text" === t.type && (null == (e = t.getAttribute("type")) || "text" === e.toLowerCase())
                    }, first: u(function () {
                        return [0]
                    }), last: u(function (t, e) {
                        return [e - 1]
                    }), eq: u(function (t, e, n) {
                        return [0 > n ? n + e : n]
                    }), even: u(function (t, e) {
                        for (var n = 0; e > n; n += 2)t.push(n);
                        return t
                    }), odd: u(function (t, e) {
                        for (var n = 1; e > n; n += 2)t.push(n);
                        return t
                    }), lt: u(function (t, e, n) {
                        for (var i = 0 > n ? n + e : n; --i >= 0;)t.push(i);
                        return t
                    }), gt: u(function (t, e, n) {
                        for (var i = 0 > n ? n + e : n; ++i < e;)t.push(i);
                        return t
                    })
                }
            }, _.pseudos.nth = _.pseudos.eq;
            for (w in{radio: !0, checkbox: !0, file: !0, password: !0, image: !0})_.pseudos[w] = s(w);
            for (w in{submit: !0, reset: !0})_.pseudos[w] = l(w);
            return d.prototype = _.filters = _.pseudos, _.setFilters = new d, T = e.tokenize = function (t, n) {
                var i, o, a, r, s, l, u, c = z[t + " "];
                if (c)return n ? 0 : c.slice(0);
                for (s = t, l = [], u = _.preFilter; s;) {
                    (!i || (o = ue.exec(s))) && (o && (s = s.slice(o[0].length) || s), l.push(a = [])), i = !1, (o = ce.exec(s)) && (i = o.shift(), a.push({
                        value: i,
                        type: o[0].replace(le, " ")
                    }), s = s.slice(i.length));
                    for (r in _.filter)!(o = pe[r].exec(s)) || u[r] && !(o = u[r](o)) || (i = o.shift(), a.push({
                        value: i,
                        type: r,
                        matches: o
                    }), s = s.slice(i.length));
                    if (!i)break
                }
                return n ? s.length : s ? e.error(t) : z(t, l).slice(0)
            }, E = e.compile = function (t, e) {
                var n, i = [], o = [], a = U[t + " "];
                if (!a) {
                    for (e || (e = T(t)), n = e.length; n--;)a = y(e[n]), a[M] ? i.push(a) : o.push(a);
                    a = U(t, b(o, i)), a.selector = t
                }
                return a
            }, S = e.select = function (t, e, n, i) {
                var o, a, r, s, l, u = "function" == typeof t && t, d = !i && T(t = u.selector || t);
                if (n = n || [], 1 === d.length) {
                    if (a = d[0] = d[0].slice(0), a.length > 2 && "ID" === (r = a[0]).type && x.getById && 9 === e.nodeType && H && _.relative[a[1].type]) {
                        if (e = (_.find.ID(r.matches[0].replace(xe, _e), e) || [])[0], !e)return n;
                        u && (e = e.parentNode), t = t.slice(a.shift().value.length)
                    }
                    for (o = pe.needsContext.test(t) ? 0 : a.length; o-- && (r = a[o], !_.relative[s = r.type]);)if ((l = _.find[s]) && (i = l(r.matches[0].replace(xe, _e), be.test(a[0].type) && c(e.parentNode) || e))) {
                        if (a.splice(o, 1), t = i.length && h(a), !t)return K.apply(n, i), n;
                        break
                    }
                }
                return (u || E(t, d))(i, e, !H, n, be.test(t) && c(e.parentNode) || e), n
            }, x.sortStable = M.split("").sort(G).join("") === M, x.detectDuplicates = !!N, $(), x.sortDetached = o(function (t) {
                return 1 & t.compareDocumentPosition(A.createElement("div"))
            }), o(function (t) {
                return t.innerHTML = "<a href='#'></a>", "#" === t.firstChild.getAttribute("href")
            }) || a("type|href|height|width", function (t, e, n) {
                return n ? void 0 : t.getAttribute(e, "type" === e.toLowerCase() ? 1 : 2)
            }), x.attributes && o(function (t) {
                return t.innerHTML = "<input/>", t.firstChild.setAttribute("value", ""), "" === t.firstChild.getAttribute("value")
            }) || a("value", function (t, e, n) {
                return n || "input" !== t.nodeName.toLowerCase() ? void 0 : t.defaultValue
            }), o(function (t) {
                return null == t.getAttribute("disabled")
            }) || a(ne, function (t, e, n) {
                var i;
                return n ? void 0 : t[e] === !0 ? e.toLowerCase() : (i = t.getAttributeNode(e)) && i.specified ? i.value : null
            }), e
        }(t);
        oe.find = ue, oe.expr = ue.selectors, oe.expr[":"] = oe.expr.pseudos, oe.unique = ue.uniqueSort, oe.text = ue.getText, oe.isXMLDoc = ue.isXML, oe.contains = ue.contains;
        var ce = oe.expr.match.needsContext, de = /^<(\w+)\s*\/?>(?:<\/\1>|)$/, he = /^.[^:#\[\.,]*$/;
        oe.filter = function (t, e, n) {
            var i = e[0];
            return n && (t = ":not(" + t + ")"), 1 === e.length && 1 === i.nodeType ? oe.find.matchesSelector(i, t) ? [i] : [] : oe.find.matches(t, oe.grep(e, function (t) {
                return 1 === t.nodeType
            }))
        }, oe.fn.extend({
            find: function (t) {
                var e, n = [], i = this, o = i.length;
                if ("string" != typeof t)return this.pushStack(oe(t).filter(function () {
                    for (e = 0; o > e; e++)if (oe.contains(i[e], this))return !0
                }));
                for (e = 0; o > e; e++)oe.find(t, i[e], n);
                return n = this.pushStack(o > 1 ? oe.unique(n) : n), n.selector = this.selector ? this.selector + " " + t : t, n
            }, filter: function (t) {
                return this.pushStack(i(this, t || [], !1))
            }, not: function (t) {
                return this.pushStack(i(this, t || [], !0))
            }, is: function (t) {
                return !!i(this, "string" == typeof t && ce.test(t) ? oe(t) : t || [], !1).length
            }
        });
        var fe, pe = t.document, me = /^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]*))$/, ge = oe.fn.init = function (t, e) {
            var n, i;
            if (!t)return this;
            if ("string" == typeof t) {
                if (n = "<" === t.charAt(0) && ">" === t.charAt(t.length - 1) && t.length >= 3 ? [null, t, null] : me.exec(t), !n || !n[1] && e)return !e || e.jquery ? (e || fe).find(t) : this.constructor(e).find(t);
                if (n[1]) {
                    if (e = e instanceof oe ? e[0] : e, oe.merge(this, oe.parseHTML(n[1], e && e.nodeType ? e.ownerDocument || e : pe, !0)), de.test(n[1]) && oe.isPlainObject(e))for (n in e)oe.isFunction(this[n]) ? this[n](e[n]) : this.attr(n, e[n]);
                    return this
                }
                if (i = pe.getElementById(n[2]), i && i.parentNode) {
                    if (i.id !== n[2])return fe.find(t);
                    this.length = 1, this[0] = i
                }
                return this.context = pe, this.selector = t, this
            }
            return t.nodeType ? (this.context = this[0] = t, this.length = 1, this) : oe.isFunction(t) ? "undefined" != typeof fe.ready ? fe.ready(t) : t(oe) : (void 0 !== t.selector && (this.selector = t.selector, this.context = t.context), oe.makeArray(t, this))
        };
        ge.prototype = oe.fn, fe = oe(pe);
        var ve = /^(?:parents|prev(?:Until|All))/, ye = {children: !0, contents: !0, next: !0, prev: !0};
        oe.extend({
            dir: function (t, e, n) {
                for (var i = [], o = t[e]; o && 9 !== o.nodeType && (void 0 === n || 1 !== o.nodeType || !oe(o).is(n));)1 === o.nodeType && i.push(o), o = o[e];
                return i
            }, sibling: function (t, e) {
                for (var n = []; t; t = t.nextSibling)1 === t.nodeType && t !== e && n.push(t);
                return n
            }
        }), oe.fn.extend({
            has: function (t) {
                var e, n = oe(t, this), i = n.length;
                return this.filter(function () {
                    for (e = 0; i > e; e++)if (oe.contains(this, n[e]))return !0
                })
            }, closest: function (t, e) {
                for (var n, i = 0, o = this.length, a = [], r = ce.test(t) || "string" != typeof t ? oe(t, e || this.context) : 0; o > i; i++)for (n = this[i]; n && n !== e; n = n.parentNode)if (n.nodeType < 11 && (r ? r.index(n) > -1 : 1 === n.nodeType && oe.find.matchesSelector(n, t))) {
                    a.push(n);
                    break
                }
                return this.pushStack(a.length > 1 ? oe.unique(a) : a)
            }, index: function (t) {
                return t ? "string" == typeof t ? oe.inArray(this[0], oe(t)) : oe.inArray(t.jquery ? t[0] : t, this) : this[0] && this[0].parentNode ? this.first().prevAll().length : -1
            }, add: function (t, e) {
                return this.pushStack(oe.unique(oe.merge(this.get(), oe(t, e))))
            }, addBack: function (t) {
                return this.add(null == t ? this.prevObject : this.prevObject.filter(t))
            }
        }), oe.each({
            parent: function (t) {
                var e = t.parentNode;
                return e && 11 !== e.nodeType ? e : null
            }, parents: function (t) {
                return oe.dir(t, "parentNode")
            }, parentsUntil: function (t, e, n) {
                return oe.dir(t, "parentNode", n)
            }, next: function (t) {
                return o(t, "nextSibling")
            }, prev: function (t) {
                return o(t, "previousSibling")
            }, nextAll: function (t) {
                return oe.dir(t, "nextSibling")
            }, prevAll: function (t) {
                return oe.dir(t, "previousSibling")
            }, nextUntil: function (t, e, n) {
                return oe.dir(t, "nextSibling", n)
            }, prevUntil: function (t, e, n) {
                return oe.dir(t, "previousSibling", n)
            }, siblings: function (t) {
                return oe.sibling((t.parentNode || {}).firstChild, t)
            }, children: function (t) {
                return oe.sibling(t.firstChild)
            }, contents: function (t) {
                return oe.nodeName(t, "iframe") ? t.contentDocument || t.contentWindow.document : oe.merge([], t.childNodes)
            }
        }, function (t, e) {
            oe.fn[t] = function (n, i) {
                var o = oe.map(this, e, n);
                return "Until" !== t.slice(-5) && (i = n), i && "string" == typeof i && (o = oe.filter(i, o)), this.length > 1 && (ye[t] || (o = oe.unique(o)), ve.test(t) && (o = o.reverse())), this.pushStack(o)
            }
        });
        var be = /\S+/g, we = {};
        oe.Callbacks = function (t) {
            t = "string" == typeof t ? we[t] || a(t) : oe.extend({}, t);
            var e, n, i, o, r, s, l = [], u = !t.once && [], c = function (a) {
                for (n = t.memory && a, i = !0, r = s || 0, s = 0, o = l.length, e = !0; l && o > r; r++)if (l[r].apply(a[0], a[1]) === !1 && t.stopOnFalse) {
                    n = !1;
                    break
                }
                e = !1, l && (u ? u.length && c(u.shift()) : n ? l = [] : d.disable())
            }, d = {
                add: function () {
                    if (l) {
                        var i = l.length;
                        !function a(e) {
                            oe.each(e, function (e, n) {
                                var i = oe.type(n);
                                "function" === i ? t.unique && d.has(n) || l.push(n) : n && n.length && "string" !== i && a(n)
                            })
                        }(arguments), e ? o = l.length : n && (s = i, c(n))
                    }
                    return this
                }, remove: function () {
                    return l && oe.each(arguments, function (t, n) {
                        for (var i; (i = oe.inArray(n, l, i)) > -1;)l.splice(i, 1), e && (o >= i && o--, r >= i && r--)
                    }), this
                }, has: function (t) {
                    return t ? oe.inArray(t, l) > -1 : !(!l || !l.length)
                }, empty: function () {
                    return l = [], o = 0, this
                }, disable: function () {
                    return l = u = n = void 0, this
                }, disabled: function () {
                    return !l
                }, lock: function () {
                    return u = void 0, n || d.disable(), this
                }, locked: function () {
                    return !u
                }, fireWith: function (t, n) {
                    return !l || i && !u || (n = n || [], n = [t, n.slice ? n.slice() : n], e ? u.push(n) : c(n)), this
                }, fire: function () {
                    return d.fireWith(this, arguments), this
                }, fired: function () {
                    return !!i
                }
            };
            return d
        }, oe.extend({
            Deferred: function (t) {
                var e = [["resolve", "done", oe.Callbacks("once memory"), "resolved"], ["reject", "fail", oe.Callbacks("once memory"), "rejected"], ["notify", "progress", oe.Callbacks("memory")]], n = "pending", i = {
                    state: function () {
                        return n
                    }, always: function () {
                        return o.done(arguments).fail(arguments), this
                    }, then: function () {
                        var t = arguments;
                        return oe.Deferred(function (n) {
                            oe.each(e, function (e, a) {
                                var r = oe.isFunction(t[e]) && t[e];
                                o[a[1]](function () {
                                    var t = r && r.apply(this, arguments);
                                    t && oe.isFunction(t.promise) ? t.promise().done(n.resolve).fail(n.reject).progress(n.notify) : n[a[0] + "With"](this === i ? n.promise() : this, r ? [t] : arguments)
                                })
                            }), t = null
                        }).promise()
                    }, promise: function (t) {
                        return null != t ? oe.extend(t, i) : i
                    }
                }, o = {};
                return i.pipe = i.then, oe.each(e, function (t, a) {
                    var r = a[2], s = a[3];
                    i[a[1]] = r.add, s && r.add(function () {
                        n = s
                    }, e[1 ^ t][2].disable, e[2][2].lock), o[a[0]] = function () {
                        return o[a[0] + "With"](this === o ? i : this, arguments), this
                    }, o[a[0] + "With"] = r.fireWith
                }), i.promise(o), t && t.call(o, o), o
            }, when: function (t) {
                var e, n, i, o = 0, a = V.call(arguments), r = a.length, s = 1 !== r || t && oe.isFunction(t.promise) ? r : 0, l = 1 === s ? t : oe.Deferred(), u = function (t, n, i) {
                    return function (o) {
                        n[t] = this, i[t] = arguments.length > 1 ? V.call(arguments) : o, i === e ? l.notifyWith(n, i) : --s || l.resolveWith(n, i)
                    }
                };
                if (r > 1)for (e = new Array(r), n = new Array(r), i = new Array(r); r > o; o++)a[o] && oe.isFunction(a[o].promise) ? a[o].promise().done(u(o, i, a)).fail(l.reject).progress(u(o, n, e)) : --s;
                return s || l.resolveWith(i, a), l.promise()
            }
        });
        var xe;
        oe.fn.ready = function (t) {
            return oe.ready.promise().done(t), this
        }, oe.extend({
            isReady: !1, readyWait: 1, holdReady: function (t) {
                t ? oe.readyWait++ : oe.ready(!0)
            }, ready: function (t) {
                if (t === !0 ? !--oe.readyWait : !oe.isReady) {
                    if (!pe.body)return setTimeout(oe.ready);
                    oe.isReady = !0, t !== !0 && --oe.readyWait > 0 || (xe.resolveWith(pe, [oe]), oe.fn.triggerHandler && (oe(pe).triggerHandler("ready"), oe(pe).off("ready")))
                }
            }
        }), oe.ready.promise = function (e) {
            if (!xe)if (xe = oe.Deferred(), "complete" === pe.readyState)setTimeout(oe.ready); else if (pe.addEventListener)pe.addEventListener("DOMContentLoaded", s, !1), t.addEventListener("load", s, !1); else {
                pe.attachEvent("onreadystatechange", s), t.attachEvent("onload", s);
                var n = !1;
                try {
                    n = null == t.frameElement && pe.documentElement
                } catch (i) {
                }
                n && n.doScroll && !function o() {
                    if (!oe.isReady) {
                        try {
                            n.doScroll("left")
                        } catch (t) {
                            return setTimeout(o, 50)
                        }
                        r(), oe.ready()
                    }
                }()
            }
            return xe.promise(e)
        };
        var _e, Ce = "undefined";
        for (_e in oe(ne))break;
        ne.ownLast = "0" !== _e, ne.inlineBlockNeedsLayout = !1, oe(function () {
            var t, e, n, i;
            n = pe.getElementsByTagName("body")[0], n && n.style && (e = pe.createElement("div"), i = pe.createElement("div"), i.style.cssText = "position:absolute;border:0;width:0;height:0;top:0;left:-9999px", n.appendChild(i).appendChild(e), typeof e.style.zoom !== Ce && (e.style.cssText = "display:inline;margin:0;border:0;padding:1px;width:1px;zoom:1", ne.inlineBlockNeedsLayout = t = 3 === e.offsetWidth, t && (n.style.zoom = 1)), n.removeChild(i))
        }), function () {
            var t = pe.createElement("div");
            if (null == ne.deleteExpando) {
                ne.deleteExpando = !0;
                try {
                    delete t.test
                } catch (e) {
                    ne.deleteExpando = !1
                }
            }
            t = null
        }(), oe.acceptData = function (t) {
            var e = oe.noData[(t.nodeName + " ").toLowerCase()], n = +t.nodeType || 1;
            return 1 !== n && 9 !== n ? !1 : !e || e !== !0 && t.getAttribute("classid") === e
        };
        var ke = /^(?:\{[\w\W]*\}|\[[\w\W]*\])$/, Te = /([A-Z])/g;
        oe.extend({
            cache: {},
            noData: {"applet ": !0, "embed ": !0, "object ": "clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"},
            hasData: function (t) {
                return t = t.nodeType ? oe.cache[t[oe.expando]] : t[oe.expando], !!t && !u(t)
            },
            data: function (t, e, n) {
                return c(t, e, n)
            },
            removeData: function (t, e) {
                return d(t, e)
            },
            _data: function (t, e, n) {
                return c(t, e, n, !0)
            },
            _removeData: function (t, e) {
                return d(t, e, !0)
            }
        }), oe.fn.extend({
            data: function (t, e) {
                var n, i, o, a = this[0], r = a && a.attributes;
                if (void 0 === t) {
                    if (this.length && (o = oe.data(a), 1 === a.nodeType && !oe._data(a, "parsedAttrs"))) {
                        for (n = r.length; n--;)r[n] && (i = r[n].name, 0 === i.indexOf("data-") && (i = oe.camelCase(i.slice(5)), l(a, i, o[i])));
                        oe._data(a, "parsedAttrs", !0)
                    }
                    return o
                }
                return "object" == typeof t ? this.each(function () {
                    oe.data(this, t)
                }) : arguments.length > 1 ? this.each(function () {
                    oe.data(this, t, e)
                }) : a ? l(a, t, oe.data(a, t)) : void 0
            }, removeData: function (t) {
                return this.each(function () {
                    oe.removeData(this, t)
                })
            }
        }), oe.extend({
            queue: function (t, e, n) {
                var i;
                return t ? (e = (e || "fx") + "queue", i = oe._data(t, e), n && (!i || oe.isArray(n) ? i = oe._data(t, e, oe.makeArray(n)) : i.push(n)), i || []) : void 0
            }, dequeue: function (t, e) {
                e = e || "fx";
                var n = oe.queue(t, e), i = n.length, o = n.shift(), a = oe._queueHooks(t, e), r = function () {
                    oe.dequeue(t, e)
                };
                "inprogress" === o && (o = n.shift(), i--), o && ("fx" === e && n.unshift("inprogress"), delete a.stop, o.call(t, r, a)), !i && a && a.empty.fire()
            }, _queueHooks: function (t, e) {
                var n = e + "queueHooks";
                return oe._data(t, n) || oe._data(t, n, {
                        empty: oe.Callbacks("once memory").add(function () {
                            oe._removeData(t, e + "queue"), oe._removeData(t, n)
                        })
                    })
            }
        }), oe.fn.extend({
            queue: function (t, e) {
                var n = 2;
                return "string" != typeof t && (e = t, t = "fx", n--), arguments.length < n ? oe.queue(this[0], t) : void 0 === e ? this : this.each(function () {
                    var n = oe.queue(this, t, e);
                    oe._queueHooks(this, t), "fx" === t && "inprogress" !== n[0] && oe.dequeue(this, t)
                })
            }, dequeue: function (t) {
                return this.each(function () {
                    oe.dequeue(this, t)
                })
            }, clearQueue: function (t) {
                return this.queue(t || "fx", [])
            }, promise: function (t, e) {
                var n, i = 1, o = oe.Deferred(), a = this, r = this.length, s = function () {
                    --i || o.resolveWith(a, [a])
                };
                for ("string" != typeof t && (e = t, t = void 0), t = t || "fx"; r--;)n = oe._data(a[r], t + "queueHooks"), n && n.empty && (i++, n.empty.add(s));
                return s(), o.promise(e)
            }
        });
        var Ee = /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source, Se = ["Top", "Right", "Bottom", "Left"], De = function (t, e) {
            return t = e || t, "none" === oe.css(t, "display") || !oe.contains(t.ownerDocument, t)
        }, je = oe.access = function (t, e, n, i, o, a, r) {
            var s = 0, l = t.length, u = null == n;
            if ("object" === oe.type(n)) {
                o = !0;
                for (s in n)oe.access(t, e, s, n[s], !0, a, r)
            } else if (void 0 !== i && (o = !0, oe.isFunction(i) || (r = !0), u && (r ? (e.call(t, i), e = null) : (u = e, e = function (t, e, n) {
                    return u.call(oe(t), n)
                })), e))for (; l > s; s++)e(t[s], n, r ? i : i.call(t[s], s, e(t[s], n)));
            return o ? t : u ? e.call(t) : l ? e(t[0], n) : a
        }, Ne = /^(?:checkbox|radio)$/i;
        !function () {
            var t = pe.createElement("input"), e = pe.createElement("div"), n = pe.createDocumentFragment();
            if (e.innerHTML = "  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>", ne.leadingWhitespace = 3 === e.firstChild.nodeType, ne.tbody = !e.getElementsByTagName("tbody").length, ne.htmlSerialize = !!e.getElementsByTagName("link").length, ne.html5Clone = "<:nav></:nav>" !== pe.createElement("nav").cloneNode(!0).outerHTML, t.type = "checkbox", t.checked = !0, n.appendChild(t), ne.appendChecked = t.checked, e.innerHTML = "<textarea>x</textarea>", ne.noCloneChecked = !!e.cloneNode(!0).lastChild.defaultValue, n.appendChild(e), e.innerHTML = "<input type='radio' checked='checked' name='t'/>", ne.checkClone = e.cloneNode(!0).cloneNode(!0).lastChild.checked, ne.noCloneEvent = !0, e.attachEvent && (e.attachEvent("onclick", function () {
                    ne.noCloneEvent = !1
                }), e.cloneNode(!0).click()), null == ne.deleteExpando) {
                ne.deleteExpando = !0;
                try {
                    delete e.test
                } catch (i) {
                    ne.deleteExpando = !1
                }
            }
        }(), function () {
            var e, n, i = pe.createElement("div");
            for (e in{
                submit: !0,
                change: !0,
                focusin: !0
            })n = "on" + e, (ne[e + "Bubbles"] = n in t) || (i.setAttribute(n, "t"), ne[e + "Bubbles"] = i.attributes[n].expando === !1);
            i = null
        }();
        var $e = /^(?:input|select|textarea)$/i, Ae = /^key/, Fe = /^(?:mouse|pointer|contextmenu)|click/, He = /^(?:focusinfocus|focusoutblur)$/, Pe = /^([^.]*)(?:\.(.+)|)$/;
        oe.event = {
            global: {},
            add: function (t, e, n, i, o) {
                var a, r, s, l, u, c, d, h, f, p, m, g = oe._data(t);
                if (g) {
                    for (n.handler && (l = n, n = l.handler, o = l.selector), n.guid || (n.guid = oe.guid++), (r = g.events) || (r = g.events = {}), (c = g.handle) || (c = g.handle = function (t) {
                        return typeof oe === Ce || t && oe.event.triggered === t.type ? void 0 : oe.event.dispatch.apply(c.elem, arguments)
                    }, c.elem = t), e = (e || "").match(be) || [""], s = e.length; s--;)a = Pe.exec(e[s]) || [], f = m = a[1], p = (a[2] || "").split(".").sort(), f && (u = oe.event.special[f] || {}, f = (o ? u.delegateType : u.bindType) || f, u = oe.event.special[f] || {}, d = oe.extend({
                        type: f,
                        origType: m,
                        data: i,
                        handler: n,
                        guid: n.guid,
                        selector: o,
                        needsContext: o && oe.expr.match.needsContext.test(o),
                        namespace: p.join(".")
                    }, l), (h = r[f]) || (h = r[f] = [], h.delegateCount = 0, u.setup && u.setup.call(t, i, p, c) !== !1 || (t.addEventListener ? t.addEventListener(f, c, !1) : t.attachEvent && t.attachEvent("on" + f, c))), u.add && (u.add.call(t, d), d.handler.guid || (d.handler.guid = n.guid)), o ? h.splice(h.delegateCount++, 0, d) : h.push(d), oe.event.global[f] = !0);
                    t = null
                }
            },
            remove: function (t, e, n, i, o) {
                var a, r, s, l, u, c, d, h, f, p, m, g = oe.hasData(t) && oe._data(t);
                if (g && (c = g.events)) {
                    for (e = (e || "").match(be) || [""], u = e.length; u--;)if (s = Pe.exec(e[u]) || [], f = m = s[1], p = (s[2] || "").split(".").sort(), f) {
                        for (d = oe.event.special[f] || {}, f = (i ? d.delegateType : d.bindType) || f, h = c[f] || [], s = s[2] && new RegExp("(^|\\.)" + p.join("\\.(?:.*\\.|)") + "(\\.|$)"), l = a = h.length; a--;)r = h[a], !o && m !== r.origType || n && n.guid !== r.guid || s && !s.test(r.namespace) || i && i !== r.selector && ("**" !== i || !r.selector) || (h.splice(a, 1), r.selector && h.delegateCount--, d.remove && d.remove.call(t, r));
                        l && !h.length && (d.teardown && d.teardown.call(t, p, g.handle) !== !1 || oe.removeEvent(t, f, g.handle), delete c[f])
                    } else for (f in c)oe.event.remove(t, f + e[u], n, i, !0);
                    oe.isEmptyObject(c) && (delete g.handle, oe._removeData(t, "events"))
                }
            },
            trigger: function (e, n, i, o) {
                var a, r, s, l, u, c, d, h = [i || pe], f = ee.call(e, "type") ? e.type : e, p = ee.call(e, "namespace") ? e.namespace.split(".") : [];
                if (s = c = i = i || pe, 3 !== i.nodeType && 8 !== i.nodeType && !He.test(f + oe.event.triggered) && (f.indexOf(".") >= 0 && (p = f.split("."), f = p.shift(), p.sort()), r = f.indexOf(":") < 0 && "on" + f, e = e[oe.expando] ? e : new oe.Event(f, "object" == typeof e && e), e.isTrigger = o ? 2 : 3, e.namespace = p.join("."), e.namespace_re = e.namespace ? new RegExp("(^|\\.)" + p.join("\\.(?:.*\\.|)") + "(\\.|$)") : null, e.result = void 0, e.target || (e.target = i), n = null == n ? [e] : oe.makeArray(n, [e]), u = oe.event.special[f] || {}, o || !u.trigger || u.trigger.apply(i, n) !== !1)) {
                    if (!o && !u.noBubble && !oe.isWindow(i)) {
                        for (l = u.delegateType || f, He.test(l + f) || (s = s.parentNode); s; s = s.parentNode)h.push(s), c = s;
                        c === (i.ownerDocument || pe) && h.push(c.defaultView || c.parentWindow || t)
                    }
                    for (d = 0; (s = h[d++]) && !e.isPropagationStopped();)e.type = d > 1 ? l : u.bindType || f, a = (oe._data(s, "events") || {})[e.type] && oe._data(s, "handle"), a && a.apply(s, n), a = r && s[r], a && a.apply && oe.acceptData(s) && (e.result = a.apply(s, n), e.result === !1 && e.preventDefault());
                    if (e.type = f, !o && !e.isDefaultPrevented() && (!u._default || u._default.apply(h.pop(), n) === !1) && oe.acceptData(i) && r && i[f] && !oe.isWindow(i)) {
                        c = i[r], c && (i[r] = null), oe.event.triggered = f;
                        try {
                            i[f]()
                        } catch (m) {
                        }
                        oe.event.triggered = void 0, c && (i[r] = c)
                    }
                    return e.result
                }
            },
            dispatch: function (t) {
                t = oe.event.fix(t);
                var e, n, i, o, a, r = [], s = V.call(arguments), l = (oe._data(this, "events") || {})[t.type] || [], u = oe.event.special[t.type] || {};
                if (s[0] = t, t.delegateTarget = this, !u.preDispatch || u.preDispatch.call(this, t) !== !1) {
                    for (r = oe.event.handlers.call(this, t, l), e = 0; (o = r[e++]) && !t.isPropagationStopped();)for (t.currentTarget = o.elem, a = 0; (i = o.handlers[a++]) && !t.isImmediatePropagationStopped();)(!t.namespace_re || t.namespace_re.test(i.namespace)) && (t.handleObj = i, t.data = i.data, n = ((oe.event.special[i.origType] || {}).handle || i.handler).apply(o.elem, s), void 0 !== n && (t.result = n) === !1 && (t.preventDefault(), t.stopPropagation()));
                    return u.postDispatch && u.postDispatch.call(this, t), t.result
                }
            },
            handlers: function (t, e) {
                var n, i, o, a, r = [], s = e.delegateCount, l = t.target;
                if (s && l.nodeType && (!t.button || "click" !== t.type))for (; l != this; l = l.parentNode || this)if (1 === l.nodeType && (l.disabled !== !0 || "click" !== t.type)) {
                    for (o = [], a = 0; s > a; a++)i = e[a], n = i.selector + " ", void 0 === o[n] && (o[n] = i.needsContext ? oe(n, this).index(l) >= 0 : oe.find(n, this, null, [l]).length), o[n] && o.push(i);
                    o.length && r.push({elem: l, handlers: o})
                }
                return s < e.length && r.push({elem: this, handlers: e.slice(s)}), r
            },
            fix: function (t) {
                if (t[oe.expando])return t;
                var e, n, i, o = t.type, a = t, r = this.fixHooks[o];
                for (r || (this.fixHooks[o] = r = Fe.test(o) ? this.mouseHooks : Ae.test(o) ? this.keyHooks : {}), i = r.props ? this.props.concat(r.props) : this.props, t = new oe.Event(a), e = i.length; e--;)n = i[e], t[n] = a[n];
                return t.target || (t.target = a.srcElement || pe), 3 === t.target.nodeType && (t.target = t.target.parentNode), t.metaKey = !!t.metaKey, r.filter ? r.filter(t, a) : t
            },
            props: "altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),
            fixHooks: {},
            keyHooks: {
                props: "char charCode key keyCode".split(" "), filter: function (t, e) {
                    return null == t.which && (t.which = null != e.charCode ? e.charCode : e.keyCode), t
                }
            },
            mouseHooks: {
                props: "button buttons clientX clientY fromElement offsetX offsetY pageX pageY screenX screenY toElement".split(" "),
                filter: function (t, e) {
                    var n, i, o, a = e.button, r = e.fromElement;
                    return null == t.pageX && null != e.clientX && (i = t.target.ownerDocument || pe, o = i.documentElement, n = i.body, t.pageX = e.clientX + (o && o.scrollLeft || n && n.scrollLeft || 0) - (o && o.clientLeft || n && n.clientLeft || 0), t.pageY = e.clientY + (o && o.scrollTop || n && n.scrollTop || 0) - (o && o.clientTop || n && n.clientTop || 0)), !t.relatedTarget && r && (t.relatedTarget = r === t.target ? e.toElement : r), t.which || void 0 === a || (t.which = 1 & a ? 1 : 2 & a ? 3 : 4 & a ? 2 : 0), t
                }
            },
            special: {
                load: {noBubble: !0}, focus: {
                    trigger: function () {
                        if (this !== p() && this.focus)try {
                            return this.focus(), !1
                        } catch (t) {
                        }
                    }, delegateType: "focusin"
                }, blur: {
                    trigger: function () {
                        return this === p() && this.blur ? (this.blur(), !1) : void 0
                    }, delegateType: "focusout"
                }, click: {
                    trigger: function () {
                        return oe.nodeName(this, "input") && "checkbox" === this.type && this.click ? (this.click(), !1) : void 0
                    }, _default: function (t) {
                        return oe.nodeName(t.target, "a")
                    }
                }, beforeunload: {
                    postDispatch: function (t) {
                        void 0 !== t.result && t.originalEvent && (t.originalEvent.returnValue = t.result)
                    }
                }
            },
            simulate: function (t, e, n, i) {
                var o = oe.extend(new oe.Event, n, {type: t, isSimulated: !0, originalEvent: {}});
                i ? oe.event.trigger(o, null, e) : oe.event.dispatch.call(e, o), o.isDefaultPrevented() && n.preventDefault()
            }
        }, oe.removeEvent = pe.removeEventListener ? function (t, e, n) {
            t.removeEventListener && t.removeEventListener(e, n, !1)
        } : function (t, e, n) {
            var i = "on" + e;
            t.detachEvent && (typeof t[i] === Ce && (t[i] = null), t.detachEvent(i, n))
        }, oe.Event = function (t, e) {
            return this instanceof oe.Event ? (t && t.type ? (this.originalEvent = t, this.type = t.type, this.isDefaultPrevented = t.defaultPrevented || void 0 === t.defaultPrevented && t.returnValue === !1 ? h : f) : this.type = t, e && oe.extend(this, e), this.timeStamp = t && t.timeStamp || oe.now(), void(this[oe.expando] = !0)) : new oe.Event(t, e)
        }, oe.Event.prototype = {
            isDefaultPrevented: f,
            isPropagationStopped: f,
            isImmediatePropagationStopped: f,
            preventDefault: function () {
                var t = this.originalEvent;
                this.isDefaultPrevented = h, t && (t.preventDefault ? t.preventDefault() : t.returnValue = !1)
            },
            stopPropagation: function () {
                var t = this.originalEvent;
                this.isPropagationStopped = h, t && (t.stopPropagation && t.stopPropagation(), t.cancelBubble = !0)
            },
            stopImmediatePropagation: function () {
                var t = this.originalEvent;
                this.isImmediatePropagationStopped = h, t && t.stopImmediatePropagation && t.stopImmediatePropagation(), this.stopPropagation()
            }
        }, oe.each({
            mouseenter: "mouseover",
            mouseleave: "mouseout",
            pointerenter: "pointerover",
            pointerleave: "pointerout"
        }, function (t, e) {
            oe.event.special[t] = {
                delegateType: e, bindType: e, handle: function (t) {
                    var n, i = this, o = t.relatedTarget, a = t.handleObj;
                    return (!o || o !== i && !oe.contains(i, o)) && (t.type = a.origType, n = a.handler.apply(this, arguments), t.type = e), n
                }
            }
        }), ne.submitBubbles || (oe.event.special.submit = {
            setup: function () {
                return oe.nodeName(this, "form") ? !1 : void oe.event.add(this, "click._submit keypress._submit", function (t) {
                    var e = t.target, n = oe.nodeName(e, "input") || oe.nodeName(e, "button") ? e.form : void 0;
                    n && !oe._data(n, "submitBubbles") && (oe.event.add(n, "submit._submit", function (t) {
                        t._submit_bubble = !0
                    }), oe._data(n, "submitBubbles", !0))
                })
            }, postDispatch: function (t) {
                t._submit_bubble && (delete t._submit_bubble, this.parentNode && !t.isTrigger && oe.event.simulate("submit", this.parentNode, t, !0))
            }, teardown: function () {
                return oe.nodeName(this, "form") ? !1 : void oe.event.remove(this, "._submit")
            }
        }), ne.changeBubbles || (oe.event.special.change = {
            setup: function () {
                return $e.test(this.nodeName) ? (("checkbox" === this.type || "radio" === this.type) && (oe.event.add(this, "propertychange._change", function (t) {
                    "checked" === t.originalEvent.propertyName && (this._just_changed = !0)
                }), oe.event.add(this, "click._change", function (t) {
                    this._just_changed && !t.isTrigger && (this._just_changed = !1), oe.event.simulate("change", this, t, !0)
                })), !1) : void oe.event.add(this, "beforeactivate._change", function (t) {
                    var e = t.target;
                    $e.test(e.nodeName) && !oe._data(e, "changeBubbles") && (oe.event.add(e, "change._change", function (t) {
                        !this.parentNode || t.isSimulated || t.isTrigger || oe.event.simulate("change", this.parentNode, t, !0)
                    }), oe._data(e, "changeBubbles", !0))
                })
            }, handle: function (t) {
                var e = t.target;
                return this !== e || t.isSimulated || t.isTrigger || "radio" !== e.type && "checkbox" !== e.type ? t.handleObj.handler.apply(this, arguments) : void 0
            }, teardown: function () {
                return oe.event.remove(this, "._change"), !$e.test(this.nodeName)
            }
        }), ne.focusinBubbles || oe.each({focus: "focusin", blur: "focusout"}, function (t, e) {
            var n = function (t) {
                oe.event.simulate(e, t.target, oe.event.fix(t), !0)
            };
            oe.event.special[e] = {
                setup: function () {
                    var i = this.ownerDocument || this, o = oe._data(i, e);
                    o || i.addEventListener(t, n, !0), oe._data(i, e, (o || 0) + 1)
                }, teardown: function () {
                    var i = this.ownerDocument || this, o = oe._data(i, e) - 1;
                    o ? oe._data(i, e, o) : (i.removeEventListener(t, n, !0), oe._removeData(i, e))
                }
            }
        }), oe.fn.extend({
            on: function (t, e, n, i, o) {
                var a, r;
                if ("object" == typeof t) {
                    "string" != typeof e && (n = n || e, e = void 0);
                    for (a in t)this.on(a, e, n, t[a], o);
                    return this
                }
                if (null == n && null == i ? (i = e, n = e = void 0) : null == i && ("string" == typeof e ? (i = n, n = void 0) : (i = n, n = e, e = void 0)), i === !1)i = f; else if (!i)return this;
                return 1 === o && (r = i, i = function (t) {
                    return oe().off(t), r.apply(this, arguments)
                }, i.guid = r.guid || (r.guid = oe.guid++)), this.each(function () {
                    oe.event.add(this, t, i, n, e)
                })
            }, one: function (t, e, n, i) {
                return this.on(t, e, n, i, 1)
            }, off: function (t, e, n) {
                var i, o;
                if (t && t.preventDefault && t.handleObj)return i = t.handleObj, oe(t.delegateTarget).off(i.namespace ? i.origType + "." + i.namespace : i.origType, i.selector, i.handler), this;
                if ("object" == typeof t) {
                    for (o in t)this.off(o, e, t[o]);
                    return this
                }
                return (e === !1 || "function" == typeof e) && (n = e, e = void 0), n === !1 && (n = f), this.each(function () {
                    oe.event.remove(this, t, n, e)
                })
            }, trigger: function (t, e) {
                return this.each(function () {
                    oe.event.trigger(t, e, this)
                })
            }, triggerHandler: function (t, e) {
                var n = this[0];
                return n ? oe.event.trigger(t, e, n, !0) : void 0
            }
        });
        var Ie = "abbr|article|aside|audio|bdi|canvas|data|datalist|details|figcaption|figure|footer|header|hgroup|mark|meter|nav|output|progress|section|summary|time|video", Le = / jQuery\d+="(?:null|\d+)"/g, Oe = new RegExp("<(?:" + Ie + ")[\\s/>]", "i"), Me = /^\s+/, qe = /<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi, We = /<([\w:]+)/, Re = /<tbody/i, Be = /<|&#?\w+;/, ze = /<(?:script|style|link)/i, Ue = /checked\s*(?:[^=]|=\s*.checked.)/i, Ge = /^$|\/(?:java|ecma)script/i, Xe = /^true\/(.*)/, Qe = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g, Ve = {
            option: [1, "<select multiple='multiple'>", "</select>"],
            legend: [1, "<fieldset>", "</fieldset>"],
            area: [1, "<map>", "</map>"],
            param: [1, "<object>", "</object>"],
            thead: [1, "<table>", "</table>"],
            tr: [2, "<table><tbody>", "</tbody></table>"],
            col: [2, "<table><tbody></tbody><colgroup>", "</colgroup></table>"],
            td: [3, "<table><tbody><tr>", "</tr></tbody></table>"],
            _default: ne.htmlSerialize ? [0, "", ""] : [1, "X<div>", "</div>"]
        }, Ye = m(pe), Ze = Ye.appendChild(pe.createElement("div"));
        Ve.optgroup = Ve.option, Ve.tbody = Ve.tfoot = Ve.colgroup = Ve.caption = Ve.thead, Ve.th = Ve.td, oe.extend({
            clone: function (t, e, n) {
                var i, o, a, r, s, l = oe.contains(t.ownerDocument, t);
                if (ne.html5Clone || oe.isXMLDoc(t) || !Oe.test("<" + t.nodeName + ">") ? a = t.cloneNode(!0) : (Ze.innerHTML = t.outerHTML, Ze.removeChild(a = Ze.firstChild)), !(ne.noCloneEvent && ne.noCloneChecked || 1 !== t.nodeType && 11 !== t.nodeType || oe.isXMLDoc(t)))for (i = g(a), s = g(t), r = 0; null != (o = s[r]); ++r)i[r] && C(o, i[r]);
                if (e)if (n)for (s = s || g(t), i = i || g(a), r = 0; null != (o = s[r]); r++)_(o, i[r]); else _(t, a);
                return i = g(a, "script"), i.length > 0 && x(i, !l && g(t, "script")), i = s = o = null, a
            }, buildFragment: function (t, e, n, i) {
                for (var o, a, r, s, l, u, c, d = t.length, h = m(e), f = [], p = 0; d > p; p++)if (a = t[p], a || 0 === a)if ("object" === oe.type(a))oe.merge(f, a.nodeType ? [a] : a); else if (Be.test(a)) {
                    for (s = s || h.appendChild(e.createElement("div")), l = (We.exec(a) || ["", ""])[1].toLowerCase(), c = Ve[l] || Ve._default, s.innerHTML = c[1] + a.replace(qe, "<$1></$2>") + c[2], o = c[0]; o--;)s = s.lastChild;
                    if (!ne.leadingWhitespace && Me.test(a) && f.push(e.createTextNode(Me.exec(a)[0])), !ne.tbody)for (a = "table" !== l || Re.test(a) ? "<table>" !== c[1] || Re.test(a) ? 0 : s : s.firstChild, o = a && a.childNodes.length; o--;)oe.nodeName(u = a.childNodes[o], "tbody") && !u.childNodes.length && a.removeChild(u);
                    for (oe.merge(f, s.childNodes), s.textContent = ""; s.firstChild;)s.removeChild(s.firstChild);
                    s = h.lastChild
                } else f.push(e.createTextNode(a));
                for (s && h.removeChild(s), ne.appendChecked || oe.grep(g(f, "input"), v), p = 0; a = f[p++];)if ((!i || -1 === oe.inArray(a, i)) && (r = oe.contains(a.ownerDocument, a), s = g(h.appendChild(a), "script"), r && x(s), n))for (o = 0; a = s[o++];)Ge.test(a.type || "") && n.push(a);
                return s = null, h
            }, cleanData: function (t, e) {
                for (var n, i, o, a, r = 0, s = oe.expando, l = oe.cache, u = ne.deleteExpando, c = oe.event.special; null != (n = t[r]); r++)if ((e || oe.acceptData(n)) && (o = n[s], a = o && l[o])) {
                    if (a.events)for (i in a.events)c[i] ? oe.event.remove(n, i) : oe.removeEvent(n, i, a.handle);
                    l[o] && (delete l[o], u ? delete n[s] : typeof n.removeAttribute !== Ce ? n.removeAttribute(s) : n[s] = null, Q.push(o))
                }
            }
        }), oe.fn.extend({
            text: function (t) {
                return je(this, function (t) {
                    return void 0 === t ? oe.text(this) : this.empty().append((this[0] && this[0].ownerDocument || pe).createTextNode(t))
                }, null, t, arguments.length)
            }, append: function () {
                return this.domManip(arguments, function (t) {
                    if (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) {
                        var e = y(this, t);
                        e.appendChild(t)
                    }
                })
            }, prepend: function () {
                return this.domManip(arguments, function (t) {
                    if (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) {
                        var e = y(this, t);
                        e.insertBefore(t, e.firstChild)
                    }
                })
            }, before: function () {
                return this.domManip(arguments, function (t) {
                    this.parentNode && this.parentNode.insertBefore(t, this)
                })
            }, after: function () {
                return this.domManip(arguments, function (t) {
                    this.parentNode && this.parentNode.insertBefore(t, this.nextSibling)
                })
            }, remove: function (t, e) {
                for (var n, i = t ? oe.filter(t, this) : this, o = 0; null != (n = i[o]); o++)e || 1 !== n.nodeType || oe.cleanData(g(n)), n.parentNode && (e && oe.contains(n.ownerDocument, n) && x(g(n, "script")), n.parentNode.removeChild(n));
                return this
            }, empty: function () {
                for (var t, e = 0; null != (t = this[e]); e++) {
                    for (1 === t.nodeType && oe.cleanData(g(t, !1)); t.firstChild;)t.removeChild(t.firstChild);
                    t.options && oe.nodeName(t, "select") && (t.options.length = 0)
                }
                return this
            }, clone: function (t, e) {
                return t = null == t ? !1 : t, e = null == e ? t : e, this.map(function () {
                    return oe.clone(this, t, e)
                })
            }, html: function (t) {
                return je(this, function (t) {
                    var e = this[0] || {}, n = 0, i = this.length;
                    if (void 0 === t)return 1 === e.nodeType ? e.innerHTML.replace(Le, "") : void 0;
                    if (!("string" != typeof t || ze.test(t) || !ne.htmlSerialize && Oe.test(t) || !ne.leadingWhitespace && Me.test(t) || Ve[(We.exec(t) || ["", ""])[1].toLowerCase()])) {
                        t = t.replace(qe, "<$1></$2>");
                        try {
                            for (; i > n; n++)e = this[n] || {}, 1 === e.nodeType && (oe.cleanData(g(e, !1)), e.innerHTML = t);
                            e = 0
                        } catch (o) {
                        }
                    }
                    e && this.empty().append(t)
                }, null, t, arguments.length)
            }, replaceWith: function () {
                var t = arguments[0];
                return this.domManip(arguments, function (e) {
                    t = this.parentNode, oe.cleanData(g(this)), t && t.replaceChild(e, this)
                }), t && (t.length || t.nodeType) ? this : this.remove()
            }, detach: function (t) {
                return this.remove(t, !0)
            }, domManip: function (t, e) {
                t = Y.apply([], t);
                var n, i, o, a, r, s, l = 0, u = this.length, c = this, d = u - 1, h = t[0], f = oe.isFunction(h);
                if (f || u > 1 && "string" == typeof h && !ne.checkClone && Ue.test(h))return this.each(function (n) {
                    var i = c.eq(n);
                    f && (t[0] = h.call(this, n, i.html())), i.domManip(t, e)
                });
                if (u && (s = oe.buildFragment(t, this[0].ownerDocument, !1, this), n = s.firstChild, 1 === s.childNodes.length && (s = n), n)) {
                    for (a = oe.map(g(s, "script"), b), o = a.length; u > l; l++)i = s, l !== d && (i = oe.clone(i, !0, !0), o && oe.merge(a, g(i, "script"))), e.call(this[l], i, l);
                    if (o)for (r = a[a.length - 1].ownerDocument, oe.map(a, w), l = 0; o > l; l++)i = a[l], Ge.test(i.type || "") && !oe._data(i, "globalEval") && oe.contains(r, i) && (i.src ? oe._evalUrl && oe._evalUrl(i.src) : oe.globalEval((i.text || i.textContent || i.innerHTML || "").replace(Qe, "")));
                    s = n = null
                }
                return this
            }
        }), oe.each({
            appendTo: "append",
            prependTo: "prepend",
            insertBefore: "before",
            insertAfter: "after",
            replaceAll: "replaceWith"
        }, function (t, e) {
            oe.fn[t] = function (t) {
                for (var n, i = 0, o = [], a = oe(t), r = a.length - 1; r >= i; i++)n = i === r ? this : this.clone(!0), oe(a[i])[e](n), Z.apply(o, n.get());
                return this.pushStack(o)
            }
        });
        var Je, Ke = {};
        !function () {
            var t;
            ne.shrinkWrapBlocks = function () {
                if (null != t)return t;
                t = !1;
                var e, n, i;
                return n = pe.getElementsByTagName("body")[0], n && n.style ? (e = pe.createElement("div"), i = pe.createElement("div"), i.style.cssText = "position:absolute;border:0;width:0;height:0;top:0;left:-9999px", n.appendChild(i).appendChild(e), typeof e.style.zoom !== Ce && (e.style.cssText = "-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box;display:block;margin:0;border:0;padding:1px;width:1px;zoom:1", e.appendChild(pe.createElement("div")).style.width = "5px", t = 3 !== e.offsetWidth), n.removeChild(i), t) : void 0
            }
        }();
        var tn, en, nn = /^margin/, on = new RegExp("^(" + Ee + ")(?!px)[a-z%]+$", "i"), an = /^(top|right|bottom|left)$/;
        t.getComputedStyle ? (tn = function (t) {
            return t.ownerDocument.defaultView.getComputedStyle(t, null)
        }, en = function (t, e, n) {
            var i, o, a, r, s = t.style;
            return n = n || tn(t), r = n ? n.getPropertyValue(e) || n[e] : void 0, n && ("" !== r || oe.contains(t.ownerDocument, t) || (r = oe.style(t, e)), on.test(r) && nn.test(e) && (i = s.width, o = s.minWidth, a = s.maxWidth, s.minWidth = s.maxWidth = s.width = r, r = n.width, s.width = i, s.minWidth = o, s.maxWidth = a)), void 0 === r ? r : r + ""
        }) : pe.documentElement.currentStyle && (tn = function (t) {
            return t.currentStyle
        }, en = function (t, e, n) {
            var i, o, a, r, s = t.style;
            return n = n || tn(t), r = n ? n[e] : void 0, null == r && s && s[e] && (r = s[e]), on.test(r) && !an.test(e) && (i = s.left, o = t.runtimeStyle, a = o && o.left, a && (o.left = t.currentStyle.left), s.left = "fontSize" === e ? "1em" : r, r = s.pixelLeft + "px", s.left = i, a && (o.left = a)), void 0 === r ? r : r + "" || "auto"
        }), function () {
            function e() {
                var e, n, i, o;
                n = pe.getElementsByTagName("body")[0], n && n.style && (e = pe.createElement("div"), i = pe.createElement("div"), i.style.cssText = "position:absolute;border:0;width:0;height:0;top:0;left:-9999px", n.appendChild(i).appendChild(e), e.style.cssText = "-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;display:block;margin-top:1%;top:1%;border:1px;padding:1px;width:4px;position:absolute", a = r = !1, l = !0, t.getComputedStyle && (a = "1%" !== (t.getComputedStyle(e, null) || {}).top, r = "4px" === (t.getComputedStyle(e, null) || {width: "4px"}).width, o = e.appendChild(pe.createElement("div")), o.style.cssText = e.style.cssText = "-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box;display:block;margin:0;border:0;padding:0", o.style.marginRight = o.style.width = "0", e.style.width = "1px", l = !parseFloat((t.getComputedStyle(o, null) || {}).marginRight)), e.innerHTML = "<table><tr><td></td><td>t</td></tr></table>", o = e.getElementsByTagName("td"), o[0].style.cssText = "margin:0;border:0;padding:0;display:none", s = 0 === o[0].offsetHeight, s && (o[0].style.display = "", o[1].style.display = "none", s = 0 === o[0].offsetHeight), n.removeChild(i))
            }

            var n, i, o, a, r, s, l;
            n = pe.createElement("div"), n.innerHTML = "  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>", o = n.getElementsByTagName("a")[0], i = o && o.style, i && (i.cssText = "float:left;opacity:.5", ne.opacity = "0.5" === i.opacity, ne.cssFloat = !!i.cssFloat, n.style.backgroundClip = "content-box", n.cloneNode(!0).style.backgroundClip = "", ne.clearCloneStyle = "content-box" === n.style.backgroundClip, ne.boxSizing = "" === i.boxSizing || "" === i.MozBoxSizing || "" === i.WebkitBoxSizing, oe.extend(ne, {
                reliableHiddenOffsets: function () {
                    return null == s && e(), s
                }, boxSizingReliable: function () {
                    return null == r && e(), r
                }, pixelPosition: function () {
                    return null == a && e(), a
                }, reliableMarginRight: function () {
                    return null == l && e(), l
                }
            }))
        }(), oe.swap = function (t, e, n, i) {
            var o, a, r = {};
            for (a in e)r[a] = t.style[a], t.style[a] = e[a];
            o = n.apply(t, i || []);
            for (a in e)t.style[a] = r[a];
            return o
        };
        var rn = /alpha\([^)]*\)/i, sn = /opacity\s*=\s*([^)]*)/, ln = /^(none|table(?!-c[ea]).+)/, un = new RegExp("^(" + Ee + ")(.*)$", "i"), cn = new RegExp("^([+-])=(" + Ee + ")", "i"), dn = {
            position: "absolute",
            visibility: "hidden",
            display: "block"
        }, hn = {letterSpacing: "0", fontWeight: "400"}, fn = ["Webkit", "O", "Moz", "ms"];
        oe.extend({
            cssHooks: {
                opacity: {
                    get: function (t, e) {
                        if (e) {
                            var n = en(t, "opacity");
                            return "" === n ? "1" : n
                        }
                    }
                }
            },
            cssNumber: {
                columnCount: !0,
                fillOpacity: !0,
                flexGrow: !0,
                flexShrink: !0,
                fontWeight: !0,
                lineHeight: !0,
                opacity: !0,
                order: !0,
                orphans: !0,
                widows: !0,
                zIndex: !0,
                zoom: !0
            },
            cssProps: {"float": ne.cssFloat ? "cssFloat" : "styleFloat"},
            style: function (t, e, n, i) {
                if (t && 3 !== t.nodeType && 8 !== t.nodeType && t.style) {
                    var o, a, r, s = oe.camelCase(e), l = t.style;
                    if (e = oe.cssProps[s] || (oe.cssProps[s] = S(l, s)), r = oe.cssHooks[e] || oe.cssHooks[s], void 0 === n)return r && "get" in r && void 0 !== (o = r.get(t, !1, i)) ? o : l[e];
                    if (a = typeof n, "string" === a && (o = cn.exec(n)) && (n = (o[1] + 1) * o[2] + parseFloat(oe.css(t, e)), a = "number"), null != n && n === n && ("number" !== a || oe.cssNumber[s] || (n += "px"), ne.clearCloneStyle || "" !== n || 0 !== e.indexOf("background") || (l[e] = "inherit"), !(r && "set" in r && void 0 === (n = r.set(t, n, i)))))try {
                        l[e] = n
                    } catch (u) {
                    }
                }
            },
            css: function (t, e, n, i) {
                var o, a, r, s = oe.camelCase(e);
                return e = oe.cssProps[s] || (oe.cssProps[s] = S(t.style, s)), r = oe.cssHooks[e] || oe.cssHooks[s], r && "get" in r && (a = r.get(t, !0, n)), void 0 === a && (a = en(t, e, i)), "normal" === a && e in hn && (a = hn[e]), "" === n || n ? (o = parseFloat(a), n === !0 || oe.isNumeric(o) ? o || 0 : a) : a
            }
        }), oe.each(["height", "width"], function (t, e) {
            oe.cssHooks[e] = {
                get: function (t, n, i) {
                    return n ? ln.test(oe.css(t, "display")) && 0 === t.offsetWidth ? oe.swap(t, dn, function () {
                        return $(t, e, i)
                    }) : $(t, e, i) : void 0
                }, set: function (t, n, i) {
                    var o = i && tn(t);
                    return j(t, n, i ? N(t, e, i, ne.boxSizing && "border-box" === oe.css(t, "boxSizing", !1, o), o) : 0)
                }
            }
        }), ne.opacity || (oe.cssHooks.opacity = {
            get: function (t, e) {
                return sn.test((e && t.currentStyle ? t.currentStyle.filter : t.style.filter) || "") ? .01 * parseFloat(RegExp.$1) + "" : e ? "1" : ""
            }, set: function (t, e) {
                var n = t.style, i = t.currentStyle, o = oe.isNumeric(e) ? "alpha(opacity=" + 100 * e + ")" : "", a = i && i.filter || n.filter || "";
                n.zoom = 1, (e >= 1 || "" === e) && "" === oe.trim(a.replace(rn, "")) && n.removeAttribute && (n.removeAttribute("filter"), "" === e || i && !i.filter) || (n.filter = rn.test(a) ? a.replace(rn, o) : a + " " + o)
            }
        }), oe.cssHooks.marginRight = E(ne.reliableMarginRight, function (t, e) {
            return e ? oe.swap(t, {display: "inline-block"}, en, [t, "marginRight"]) : void 0
        }), oe.each({margin: "", padding: "", border: "Width"}, function (t, e) {
            oe.cssHooks[t + e] = {
                expand: function (n) {
                    for (var i = 0, o = {}, a = "string" == typeof n ? n.split(" ") : [n]; 4 > i; i++)o[t + Se[i] + e] = a[i] || a[i - 2] || a[0];
                    return o
                }
            }, nn.test(t) || (oe.cssHooks[t + e].set = j)
        }), oe.fn.extend({
            css: function (t, e) {
                return je(this, function (t, e, n) {
                    var i, o, a = {}, r = 0;
                    if (oe.isArray(e)) {
                        for (i = tn(t), o = e.length; o > r; r++)a[e[r]] = oe.css(t, e[r], !1, i);
                        return a
                    }
                    return void 0 !== n ? oe.style(t, e, n) : oe.css(t, e)
                }, t, e, arguments.length > 1)
            }, show: function () {
                return D(this, !0)
            }, hide: function () {
                return D(this)
            }, toggle: function (t) {
                return "boolean" == typeof t ? t ? this.show() : this.hide() : this.each(function () {
                    De(this) ? oe(this).show() : oe(this).hide()
                })
            }
        }), oe.Tween = A, A.prototype = {
            constructor: A, init: function (t, e, n, i, o, a) {
                this.elem = t, this.prop = n, this.easing = o || "swing", this.options = e, this.start = this.now = this.cur(), this.end = i, this.unit = a || (oe.cssNumber[n] ? "" : "px")
            }, cur: function () {
                var t = A.propHooks[this.prop];
                return t && t.get ? t.get(this) : A.propHooks._default.get(this)
            }, run: function (t) {
                var e, n = A.propHooks[this.prop];
                return this.pos = e = this.options.duration ? oe.easing[this.easing](t, this.options.duration * t, 0, 1, this.options.duration) : t, this.now = (this.end - this.start) * e + this.start, this.options.step && this.options.step.call(this.elem, this.now, this), n && n.set ? n.set(this) : A.propHooks._default.set(this), this
            }
        }, A.prototype.init.prototype = A.prototype, A.propHooks = {
            _default: {
                get: function (t) {
                    var e;
                    return null == t.elem[t.prop] || t.elem.style && null != t.elem.style[t.prop] ? (e = oe.css(t.elem, t.prop, ""), e && "auto" !== e ? e : 0) : t.elem[t.prop]
                }, set: function (t) {
                    oe.fx.step[t.prop] ? oe.fx.step[t.prop](t) : t.elem.style && (null != t.elem.style[oe.cssProps[t.prop]] || oe.cssHooks[t.prop]) ? oe.style(t.elem, t.prop, t.now + t.unit) : t.elem[t.prop] = t.now
                }
            }
        }, A.propHooks.scrollTop = A.propHooks.scrollLeft = {
            set: function (t) {
                t.elem.nodeType && t.elem.parentNode && (t.elem[t.prop] = t.now)
            }
        }, oe.easing = {
            linear: function (t) {
                return t
            }, swing: function (t) {
                return .5 - Math.cos(t * Math.PI) / 2
            }
        }, oe.fx = A.prototype.init, oe.fx.step = {};
        var pn, mn, gn = /^(?:toggle|show|hide)$/, vn = new RegExp("^(?:([+-])=|)(" + Ee + ")([a-z%]*)$", "i"), yn = /queueHooks$/, bn = [I], wn = {
            "*": [function (t, e) {
                var n = this.createTween(t, e), i = n.cur(), o = vn.exec(e), a = o && o[3] || (oe.cssNumber[t] ? "" : "px"), r = (oe.cssNumber[t] || "px" !== a && +i) && vn.exec(oe.css(n.elem, t)), s = 1, l = 20;
                if (r && r[3] !== a) {
                    a = a || r[3], o = o || [], r = +i || 1;
                    do s = s || ".5", r /= s, oe.style(n.elem, t, r + a); while (s !== (s = n.cur() / i) && 1 !== s && --l)
                }
                return o && (r = n.start = +r || +i || 0, n.unit = a, n.end = o[1] ? r + (o[1] + 1) * o[2] : +o[2]), n
            }]
        };
        oe.Animation = oe.extend(O, {
            tweener: function (t, e) {
                oe.isFunction(t) ? (e = t, t = ["*"]) : t = t.split(" ");
                for (var n, i = 0, o = t.length; o > i; i++)n = t[i], wn[n] = wn[n] || [], wn[n].unshift(e)
            }, prefilter: function (t, e) {
                e ? bn.unshift(t) : bn.push(t)
            }
        }), oe.speed = function (t, e, n) {
            var i = t && "object" == typeof t ? oe.extend({}, t) : {
                complete: n || !n && e || oe.isFunction(t) && t,
                duration: t,
                easing: n && e || e && !oe.isFunction(e) && e
            };
            return i.duration = oe.fx.off ? 0 : "number" == typeof i.duration ? i.duration : i.duration in oe.fx.speeds ? oe.fx.speeds[i.duration] : oe.fx.speeds._default, (null == i.queue || i.queue === !0) && (i.queue = "fx"), i.old = i.complete, i.complete = function () {
                oe.isFunction(i.old) && i.old.call(this), i.queue && oe.dequeue(this, i.queue)
            }, i
        }, oe.fn.extend({
            fadeTo: function (t, e, n, i) {
                return this.filter(De).css("opacity", 0).show().end().animate({opacity: e}, t, n, i)
            }, animate: function (t, e, n, i) {
                var o = oe.isEmptyObject(t), a = oe.speed(e, n, i), r = function () {
                    var e = O(this, oe.extend({}, t), a);
                    (o || oe._data(this, "finish")) && e.stop(!0)
                };
                return r.finish = r, o || a.queue === !1 ? this.each(r) : this.queue(a.queue, r)
            }, stop: function (t, e, n) {
                var i = function (t) {
                    var e = t.stop;
                    delete t.stop, e(n)
                };
                return "string" != typeof t && (n = e, e = t, t = void 0), e && t !== !1 && this.queue(t || "fx", []), this.each(function () {
                    var e = !0, o = null != t && t + "queueHooks", a = oe.timers, r = oe._data(this);
                    if (o)r[o] && r[o].stop && i(r[o]); else for (o in r)r[o] && r[o].stop && yn.test(o) && i(r[o]);
                    for (o = a.length; o--;)a[o].elem !== this || null != t && a[o].queue !== t || (a[o].anim.stop(n), e = !1, a.splice(o, 1));
                    (e || !n) && oe.dequeue(this, t)
                })
            }, finish: function (t) {
                return t !== !1 && (t = t || "fx"), this.each(function () {
                    var e, n = oe._data(this), i = n[t + "queue"], o = n[t + "queueHooks"], a = oe.timers, r = i ? i.length : 0;
                    for (n.finish = !0, oe.queue(this, t, []), o && o.stop && o.stop.call(this, !0), e = a.length; e--;)a[e].elem === this && a[e].queue === t && (a[e].anim.stop(!0), a.splice(e, 1));
                    for (e = 0; r > e; e++)i[e] && i[e].finish && i[e].finish.call(this);
                    delete n.finish
                })
            }
        }), oe.each(["toggle", "show", "hide"], function (t, e) {
            var n = oe.fn[e];
            oe.fn[e] = function (t, i, o) {
                return null == t || "boolean" == typeof t ? n.apply(this, arguments) : this.animate(H(e, !0), t, i, o)
            }
        }), oe.each({
            slideDown: H("show"),
            slideUp: H("hide"),
            slideToggle: H("toggle"),
            fadeIn: {opacity: "show"},
            fadeOut: {opacity: "hide"},
            fadeToggle: {opacity: "toggle"}
        }, function (t, e) {
            oe.fn[t] = function (t, n, i) {
                return this.animate(e, t, n, i)
            }
        }), oe.timers = [], oe.fx.tick = function () {
            var t, e = oe.timers, n = 0;
            for (pn = oe.now(); n < e.length; n++)t = e[n], t() || e[n] !== t || e.splice(n--, 1);
            e.length || oe.fx.stop(), pn = void 0
        }, oe.fx.timer = function (t) {
            oe.timers.push(t), t() ? oe.fx.start() : oe.timers.pop()
        }, oe.fx.interval = 13, oe.fx.start = function () {
            mn || (mn = setInterval(oe.fx.tick, oe.fx.interval))
        }, oe.fx.stop = function () {
            clearInterval(mn), mn = null
        }, oe.fx.speeds = {slow: 600, fast: 200, _default: 400}, oe.fn.delay = function (t, e) {
            return t = oe.fx ? oe.fx.speeds[t] || t : t, e = e || "fx", this.queue(e, function (e, n) {
                var i = setTimeout(e, t);
                n.stop = function () {
                    clearTimeout(i)
                }
            })
        }, function () {
            var t, e, n, i, o;
            e = pe.createElement("div"), e.setAttribute("className", "t"), e.innerHTML = "  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>", i = e.getElementsByTagName("a")[0], n = pe.createElement("select"), o = n.appendChild(pe.createElement("option")), t = e.getElementsByTagName("input")[0], i.style.cssText = "top:1px", ne.getSetAttribute = "t" !== e.className, ne.style = /top/.test(i.getAttribute("style")), ne.hrefNormalized = "/a" === i.getAttribute("href"), ne.checkOn = !!t.value, ne.optSelected = o.selected, ne.enctype = !!pe.createElement("form").enctype, n.disabled = !0, ne.optDisabled = !o.disabled, t = pe.createElement("input"), t.setAttribute("value", ""), ne.input = "" === t.getAttribute("value"), t.value = "t", t.setAttribute("type", "radio"), ne.radioValue = "t" === t.value
        }();
        var xn = /\r/g;
        oe.fn.extend({
            val: function (t) {
                var e, n, i, o = this[0];
                {
                    if (arguments.length)return i = oe.isFunction(t), this.each(function (n) {
                        var o;
                        1 === this.nodeType && (o = i ? t.call(this, n, oe(this).val()) : t, null == o ? o = "" : "number" == typeof o ? o += "" : oe.isArray(o) && (o = oe.map(o, function (t) {
                            return null == t ? "" : t + ""
                        })), e = oe.valHooks[this.type] || oe.valHooks[this.nodeName.toLowerCase()], e && "set" in e && void 0 !== e.set(this, o, "value") || (this.value = o))
                    });
                    if (o)return e = oe.valHooks[o.type] || oe.valHooks[o.nodeName.toLowerCase()], e && "get" in e && void 0 !== (n = e.get(o, "value")) ? n : (n = o.value, "string" == typeof n ? n.replace(xn, "") : null == n ? "" : n)
                }
            }
        }), oe.extend({
            valHooks: {
                option: {
                    get: function (t) {
                        var e = oe.find.attr(t, "value");
                        return null != e ? e : oe.trim(oe.text(t))
                    }
                }, select: {
                    get: function (t) {
                        for (var e, n, i = t.options, o = t.selectedIndex, a = "select-one" === t.type || 0 > o, r = a ? null : [], s = a ? o + 1 : i.length, l = 0 > o ? s : a ? o : 0; s > l; l++)if (n = i[l], !(!n.selected && l !== o || (ne.optDisabled ? n.disabled : null !== n.getAttribute("disabled")) || n.parentNode.disabled && oe.nodeName(n.parentNode, "optgroup"))) {
                            if (e = oe(n).val(), a)return e;
                            r.push(e)
                        }
                        return r
                    }, set: function (t, e) {
                        for (var n, i, o = t.options, a = oe.makeArray(e), r = o.length; r--;)if (i = o[r], oe.inArray(oe.valHooks.option.get(i), a) >= 0)try {
                            i.selected = n = !0
                        } catch (s) {
                            i.scrollHeight
                        } else i.selected = !1;
                        return n || (t.selectedIndex = -1), o
                    }
                }
            }
        }), oe.each(["radio", "checkbox"], function () {
            oe.valHooks[this] = {
                set: function (t, e) {
                    return oe.isArray(e) ? t.checked = oe.inArray(oe(t).val(), e) >= 0 : void 0
                }
            }, ne.checkOn || (oe.valHooks[this].get = function (t) {
                return null === t.getAttribute("value") ? "on" : t.value
            })
        });
        var _n, Cn, kn = oe.expr.attrHandle, Tn = /^(?:checked|selected)$/i, En = ne.getSetAttribute, Sn = ne.input;
        oe.fn.extend({
            attr: function (t, e) {
                return je(this, oe.attr, t, e, arguments.length > 1)
            }, removeAttr: function (t) {
                return this.each(function () {
                    oe.removeAttr(this, t)
                })
            }
        }), oe.extend({
            attr: function (t, e, n) {
                var i, o, a = t.nodeType;
                if (t && 3 !== a && 8 !== a && 2 !== a)return typeof t.getAttribute === Ce ? oe.prop(t, e, n) : (1 === a && oe.isXMLDoc(t) || (e = e.toLowerCase(), i = oe.attrHooks[e] || (oe.expr.match.bool.test(e) ? Cn : _n)), void 0 === n ? i && "get" in i && null !== (o = i.get(t, e)) ? o : (o = oe.find.attr(t, e), null == o ? void 0 : o) : null !== n ? i && "set" in i && void 0 !== (o = i.set(t, n, e)) ? o : (t.setAttribute(e, n + ""), n) : void oe.removeAttr(t, e))
            }, removeAttr: function (t, e) {
                var n, i, o = 0, a = e && e.match(be);
                if (a && 1 === t.nodeType)for (; n = a[o++];)i = oe.propFix[n] || n, oe.expr.match.bool.test(n) ? Sn && En || !Tn.test(n) ? t[i] = !1 : t[oe.camelCase("default-" + n)] = t[i] = !1 : oe.attr(t, n, ""), t.removeAttribute(En ? n : i)
            }, attrHooks: {
                type: {
                    set: function (t, e) {
                        if (!ne.radioValue && "radio" === e && oe.nodeName(t, "input")) {
                            var n = t.value;
                            return t.setAttribute("type", e), n && (t.value = n), e
                        }
                    }
                }
            }
        }), Cn = {
            set: function (t, e, n) {
                return e === !1 ? oe.removeAttr(t, n) : Sn && En || !Tn.test(n) ? t.setAttribute(!En && oe.propFix[n] || n, n) : t[oe.camelCase("default-" + n)] = t[n] = !0, n
            }
        }, oe.each(oe.expr.match.bool.source.match(/\w+/g), function (t, e) {
            var n = kn[e] || oe.find.attr;
            kn[e] = Sn && En || !Tn.test(e) ? function (t, e, i) {
                var o, a;
                return i || (a = kn[e], kn[e] = o, o = null != n(t, e, i) ? e.toLowerCase() : null, kn[e] = a), o
            } : function (t, e, n) {
                return n ? void 0 : t[oe.camelCase("default-" + e)] ? e.toLowerCase() : null
            }
        }), Sn && En || (oe.attrHooks.value = {
            set: function (t, e, n) {
                return oe.nodeName(t, "input") ? void(t.defaultValue = e) : _n && _n.set(t, e, n)
            }
        }), En || (_n = {
            set: function (t, e, n) {
                var i = t.getAttributeNode(n);
                return i || t.setAttributeNode(i = t.ownerDocument.createAttribute(n)), i.value = e += "", "value" === n || e === t.getAttribute(n) ? e : void 0
            }
        }, kn.id = kn.name = kn.coords = function (t, e, n) {
            var i;
            return n ? void 0 : (i = t.getAttributeNode(e)) && "" !== i.value ? i.value : null
        }, oe.valHooks.button = {
            get: function (t, e) {
                var n = t.getAttributeNode(e);
                return n && n.specified ? n.value : void 0
            }, set: _n.set
        }, oe.attrHooks.contenteditable = {
            set: function (t, e, n) {
                _n.set(t, "" === e ? !1 : e, n)
            }
        }, oe.each(["width", "height"], function (t, e) {
            oe.attrHooks[e] = {
                set: function (t, n) {
                    return "" === n ? (t.setAttribute(e, "auto"), n) : void 0
                }
            }
        })), ne.style || (oe.attrHooks.style = {
            get: function (t) {
                return t.style.cssText || void 0
            }, set: function (t, e) {
                return t.style.cssText = e + ""
            }
        });
        var Dn = /^(?:input|select|textarea|button|object)$/i, jn = /^(?:a|area)$/i;
        oe.fn.extend({
            prop: function (t, e) {
                return je(this, oe.prop, t, e, arguments.length > 1)
            }, removeProp: function (t) {
                return t = oe.propFix[t] || t, this.each(function () {
                    try {
                        this[t] = void 0, delete this[t]
                    } catch (e) {
                    }
                })
            }
        }), oe.extend({
            propFix: {"for": "htmlFor", "class": "className"}, prop: function (t, e, n) {
                var i, o, a, r = t.nodeType;
                if (t && 3 !== r && 8 !== r && 2 !== r)return a = 1 !== r || !oe.isXMLDoc(t), a && (e = oe.propFix[e] || e, o = oe.propHooks[e]), void 0 !== n ? o && "set" in o && void 0 !== (i = o.set(t, n, e)) ? i : t[e] = n : o && "get" in o && null !== (i = o.get(t, e)) ? i : t[e]
            }, propHooks: {
                tabIndex: {
                    get: function (t) {
                        var e = oe.find.attr(t, "tabindex");
                        return e ? parseInt(e, 10) : Dn.test(t.nodeName) || jn.test(t.nodeName) && t.href ? 0 : -1
                    }
                }
            }
        }), ne.hrefNormalized || oe.each(["href", "src"], function (t, e) {
            oe.propHooks[e] = {
                get: function (t) {
                    return t.getAttribute(e, 4)
                }
            }
        }), ne.optSelected || (oe.propHooks.selected = {
            get: function (t) {
                var e = t.parentNode;
                return e && (e.selectedIndex, e.parentNode && e.parentNode.selectedIndex), null
            }
        }), oe.each(["tabIndex", "readOnly", "maxLength", "cellSpacing", "cellPadding", "rowSpan", "colSpan", "useMap", "frameBorder", "contentEditable"], function () {
            oe.propFix[this.toLowerCase()] = this
        }), ne.enctype || (oe.propFix.enctype = "encoding");
        var Nn = /[\t\r\n\f]/g;
        oe.fn.extend({
            addClass: function (t) {
                var e, n, i, o, a, r, s = 0, l = this.length, u = "string" == typeof t && t;
                if (oe.isFunction(t))return this.each(function (e) {
                    oe(this).addClass(t.call(this, e, this.className))
                });
                if (u)for (e = (t || "").match(be) || []; l > s; s++)if (n = this[s], i = 1 === n.nodeType && (n.className ? (" " + n.className + " ").replace(Nn, " ") : " ")) {
                    for (a = 0; o = e[a++];)i.indexOf(" " + o + " ") < 0 && (i += o + " ");
                    r = oe.trim(i), n.className !== r && (n.className = r)
                }
                return this
            }, removeClass: function (t) {
                var e, n, i, o, a, r, s = 0, l = this.length, u = 0 === arguments.length || "string" == typeof t && t;
                if (oe.isFunction(t))return this.each(function (e) {
                    oe(this).removeClass(t.call(this, e, this.className))
                });
                if (u)for (e = (t || "").match(be) || []; l > s; s++)if (n = this[s], i = 1 === n.nodeType && (n.className ? (" " + n.className + " ").replace(Nn, " ") : "")) {
                    for (a = 0; o = e[a++];)for (; i.indexOf(" " + o + " ") >= 0;)i = i.replace(" " + o + " ", " ");
                    r = t ? oe.trim(i) : "", n.className !== r && (n.className = r)
                }
                return this
            }, toggleClass: function (t, e) {
                var n = typeof t;
                return "boolean" == typeof e && "string" === n ? e ? this.addClass(t) : this.removeClass(t) : this.each(oe.isFunction(t) ? function (n) {
                    oe(this).toggleClass(t.call(this, n, this.className, e), e)
                } : function () {
                    if ("string" === n)for (var e, i = 0, o = oe(this), a = t.match(be) || []; e = a[i++];)o.hasClass(e) ? o.removeClass(e) : o.addClass(e); else(n === Ce || "boolean" === n) && (this.className && oe._data(this, "__className__", this.className), this.className = this.className || t === !1 ? "" : oe._data(this, "__className__") || "")
                })
            }, hasClass: function (t) {
                for (var e = " " + t + " ", n = 0, i = this.length; i > n; n++)if (1 === this[n].nodeType && (" " + this[n].className + " ").replace(Nn, " ").indexOf(e) >= 0)return !0;
                return !1
            }
        }), oe.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error contextmenu".split(" "), function (t, e) {
            oe.fn[e] = function (t, n) {
                return arguments.length > 0 ? this.on(e, null, t, n) : this.trigger(e)
            }
        }), oe.fn.extend({
            hover: function (t, e) {
                return this.mouseenter(t).mouseleave(e || t)
            }, bind: function (t, e, n) {
                return this.on(t, null, e, n)
            }, unbind: function (t, e) {
                return this.off(t, null, e)
            }, delegate: function (t, e, n, i) {
                return this.on(e, t, n, i)
            }, undelegate: function (t, e, n) {
                return 1 === arguments.length ? this.off(t, "**") : this.off(e, t || "**", n)
            }
        });
        var $n = oe.now(), An = /\?/, Fn = /(,)|(\[|{)|(}|])|"(?:[^"\\\r\n]|\\["\\\/bfnrt]|\\u[\da-fA-F]{4})*"\s*:?|true|false|null|-?(?!0\d)\d+(?:\.\d+|)(?:[eE][+-]?\d+|)/g;
        oe.parseJSON = function (e) {
            if (t.JSON && t.JSON.parse)return t.JSON.parse(e + "");
            var n, i = null, o = oe.trim(e + "");
            return o && !oe.trim(o.replace(Fn, function (t, e, o, a) {
                return n && e && (i = 0), 0 === i ? t : (n = o || e, i += !a - !o, "")
            })) ? Function("return " + o)() : oe.error("Invalid JSON: " + e)
        }, oe.parseXML = function (e) {
            var n, i;
            if (!e || "string" != typeof e)return null;
            try {
                t.DOMParser ? (i = new DOMParser, n = i.parseFromString(e, "text/xml")) : (n = new ActiveXObject("Microsoft.XMLDOM"), n.async = "false", n.loadXML(e))
            } catch (o) {
                n = void 0
            }
            return n && n.documentElement && !n.getElementsByTagName("parsererror").length || oe.error("Invalid XML: " + e), n
        };
        var Hn, Pn, In = /#.*$/, Ln = /([?&])_=[^&]*/, On = /^(.*?):[ \t]*([^\r\n]*)\r?$/gm, Mn = /^(?:about|app|app-storage|.+-extension|file|res|widget):$/, qn = /^(?:GET|HEAD)$/, Wn = /^\/\//, Rn = /^([\w.+-]+:)(?:\/\/(?:[^\/?#]*@|)([^\/?#:]*)(?::(\d+)|)|)/, Bn = {}, zn = {}, Un = "*/".concat("*");
        try {
            Pn = location.href
        } catch (Gn) {
            Pn = pe.createElement("a"), Pn.href = "", Pn = Pn.href
        }
        Hn = Rn.exec(Pn.toLowerCase()) || [], oe.extend({
            active: 0,
            lastModified: {},
            etag: {},
            ajaxSettings: {
                url: Pn,
                type: "GET",
                isLocal: Mn.test(Hn[1]),
                global: !0,
                processData: !0,
                async: !0,
                contentType: "application/x-www-form-urlencoded; charset=UTF-8",
                accepts: {
                    "*": Un,
                    text: "text/plain",
                    html: "text/html",
                    xml: "application/xml, text/xml",
                    json: "application/json, text/javascript"
                },
                contents: {xml: /xml/, html: /html/, json: /json/},
                responseFields: {xml: "responseXML", text: "responseText", json: "responseJSON"},
                converters: {"* text": String, "text html": !0, "text json": oe.parseJSON, "text xml": oe.parseXML},
                flatOptions: {url: !0, context: !0}
            },
            ajaxSetup: function (t, e) {
                return e ? W(W(t, oe.ajaxSettings), e) : W(oe.ajaxSettings, t)
            },
            ajaxPrefilter: M(Bn),
            ajaxTransport: M(zn),
            ajax: function (t, e) {
                function n(t, e, n, i) {
                    var o, c, v, y, w, _ = e;
                    2 !== b && (b = 2, s && clearTimeout(s), u = void 0, r = i || "", x.readyState = t > 0 ? 4 : 0, o = t >= 200 && 300 > t || 304 === t, n && (y = R(d, x, n)), y = B(d, y, x, o), o ? (d.ifModified && (w = x.getResponseHeader("Last-Modified"), w && (oe.lastModified[a] = w), w = x.getResponseHeader("etag"), w && (oe.etag[a] = w)), 204 === t || "HEAD" === d.type ? _ = "nocontent" : 304 === t ? _ = "notmodified" : (_ = y.state, c = y.data, v = y.error, o = !v)) : (v = _, (t || !_) && (_ = "error", 0 > t && (t = 0))), x.status = t, x.statusText = (e || _) + "", o ? p.resolveWith(h, [c, _, x]) : p.rejectWith(h, [x, _, v]), x.statusCode(g), g = void 0, l && f.trigger(o ? "ajaxSuccess" : "ajaxError", [x, d, o ? c : v]), m.fireWith(h, [x, _]), l && (f.trigger("ajaxComplete", [x, d]), --oe.active || oe.event.trigger("ajaxStop")))
                }

                "object" == typeof t && (e = t, t = void 0), e = e || {};
                var i, o, a, r, s, l, u, c, d = oe.ajaxSetup({}, e), h = d.context || d, f = d.context && (h.nodeType || h.jquery) ? oe(h) : oe.event, p = oe.Deferred(), m = oe.Callbacks("once memory"), g = d.statusCode || {}, v = {}, y = {}, b = 0, w = "canceled", x = {
                    readyState: 0,
                    getResponseHeader: function (t) {
                        var e;
                        if (2 === b) {
                            if (!c)for (c = {}; e = On.exec(r);)c[e[1].toLowerCase()] = e[2];
                            e = c[t.toLowerCase()]
                        }
                        return null == e ? null : e
                    },
                    getAllResponseHeaders: function () {
                        return 2 === b ? r : null
                    },
                    setRequestHeader: function (t, e) {
                        var n = t.toLowerCase();
                        return b || (t = y[n] = y[n] || t, v[t] = e), this
                    },
                    overrideMimeType: function (t) {
                        return b || (d.mimeType = t), this
                    },
                    statusCode: function (t) {
                        var e;
                        if (t)if (2 > b)for (e in t)g[e] = [g[e], t[e]]; else x.always(t[x.status]);
                        return this
                    },
                    abort: function (t) {
                        var e = t || w;
                        return u && u.abort(e), n(0, e), this
                    }
                };
                if (p.promise(x).complete = m.add, x.success = x.done, x.error = x.fail, d.url = ((t || d.url || Pn) + "").replace(In, "").replace(Wn, Hn[1] + "//"), d.type = e.method || e.type || d.method || d.type, d.dataTypes = oe.trim(d.dataType || "*").toLowerCase().match(be) || [""], null == d.crossDomain && (i = Rn.exec(d.url.toLowerCase()), d.crossDomain = !(!i || i[1] === Hn[1] && i[2] === Hn[2] && (i[3] || ("http:" === i[1] ? "80" : "443")) === (Hn[3] || ("http:" === Hn[1] ? "80" : "443")))), d.data && d.processData && "string" != typeof d.data && (d.data = oe.param(d.data, d.traditional)), q(Bn, d, e, x), 2 === b)return x;
                l = d.global, l && 0 === oe.active++ && oe.event.trigger("ajaxStart"), d.type = d.type.toUpperCase(), d.hasContent = !qn.test(d.type), a = d.url, d.hasContent || (d.data && (a = d.url += (An.test(a) ? "&" : "?") + d.data, delete d.data), d.cache === !1 && (d.url = Ln.test(a) ? a.replace(Ln, "$1_=" + $n++) : a + (An.test(a) ? "&" : "?") + "_=" + $n++)), d.ifModified && (oe.lastModified[a] && x.setRequestHeader("If-Modified-Since", oe.lastModified[a]), oe.etag[a] && x.setRequestHeader("If-None-Match", oe.etag[a])), (d.data && d.hasContent && d.contentType !== !1 || e.contentType) && x.setRequestHeader("Content-Type", d.contentType), x.setRequestHeader("Accept", d.dataTypes[0] && d.accepts[d.dataTypes[0]] ? d.accepts[d.dataTypes[0]] + ("*" !== d.dataTypes[0] ? ", " + Un + "; q=0.01" : "") : d.accepts["*"]);
                for (o in d.headers)x.setRequestHeader(o, d.headers[o]);
                if (d.beforeSend && (d.beforeSend.call(h, x, d) === !1 || 2 === b))return x.abort();
                w = "abort";
                for (o in{success: 1, error: 1, complete: 1})x[o](d[o]);
                if (u = q(zn, d, e, x)) {
                    x.readyState = 1, l && f.trigger("ajaxSend", [x, d]), d.async && d.timeout > 0 && (s = setTimeout(function () {
                        x.abort("timeout")
                    }, d.timeout));
                    try {
                        b = 1, u.send(v, n)
                    } catch (_) {
                        if (!(2 > b))throw _;
                        n(-1, _)
                    }
                } else n(-1, "No Transport");
                return x
            },
            getJSON: function (t, e, n) {
                return oe.get(t, e, n, "json")
            },
            getScript: function (t, e) {
                return oe.get(t, void 0, e, "script")
            }
        }), oe.each(["get", "post"], function (t, e) {
            oe[e] = function (t, n, i, o) {
                return oe.isFunction(n) && (o = o || i, i = n, n = void 0), oe.ajax({
                    url: t,
                    type: e,
                    dataType: o,
                    data: n,
                    success: i
                })
            }
        }), oe.each(["ajaxStart", "ajaxStop", "ajaxComplete", "ajaxError", "ajaxSuccess", "ajaxSend"], function (t, e) {
            oe.fn[e] = function (t) {
                return this.on(e, t)
            }
        }), oe._evalUrl = function (t) {
            return oe.ajax({url: t, type: "GET", dataType: "script", async: !1, global: !1, "throws": !0})
        }, oe.fn.extend({
            wrapAll: function (t) {
                if (oe.isFunction(t))return this.each(function (e) {
                    oe(this).wrapAll(t.call(this, e))
                });
                if (this[0]) {
                    var e = oe(t, this[0].ownerDocument).eq(0).clone(!0);
                    this[0].parentNode && e.insertBefore(this[0]), e.map(function () {
                        for (var t = this; t.firstChild && 1 === t.firstChild.nodeType;)t = t.firstChild;
                        return t
                    }).append(this)
                }
                return this
            }, wrapInner: function (t) {
                return this.each(oe.isFunction(t) ? function (e) {
                    oe(this).wrapInner(t.call(this, e))
                } : function () {
                    var e = oe(this), n = e.contents();
                    n.length ? n.wrapAll(t) : e.append(t)
                })
            }, wrap: function (t) {
                var e = oe.isFunction(t);
                return this.each(function (n) {
                    oe(this).wrapAll(e ? t.call(this, n) : t)
                })
            }, unwrap: function () {
                return this.parent().each(function () {
                    oe.nodeName(this, "body") || oe(this).replaceWith(this.childNodes)
                }).end()
            }
        }), oe.expr.filters.hidden = function (t) {
            return t.offsetWidth <= 0 && t.offsetHeight <= 0 || !ne.reliableHiddenOffsets() && "none" === (t.style && t.style.display || oe.css(t, "display"))
        }, oe.expr.filters.visible = function (t) {
            return !oe.expr.filters.hidden(t)
        };
        var Xn = /%20/g, Qn = /\[\]$/, Vn = /\r?\n/g, Yn = /^(?:submit|button|image|reset|file)$/i, Zn = /^(?:input|select|textarea|keygen)/i;
        oe.param = function (t, e) {
            var n, i = [], o = function (t, e) {
                e = oe.isFunction(e) ? e() : null == e ? "" : e, i[i.length] = encodeURIComponent(t) + "=" + encodeURIComponent(e)
            };
            if (void 0 === e && (e = oe.ajaxSettings && oe.ajaxSettings.traditional), oe.isArray(t) || t.jquery && !oe.isPlainObject(t))oe.each(t, function () {
                o(this.name, this.value)
            }); else for (n in t)z(n, t[n], e, o);
            return i.join("&").replace(Xn, "+")
        }, oe.fn.extend({
            serialize: function () {
                return oe.param(this.serializeArray())
            }, serializeArray: function () {
                return this.map(function () {
                    var t = oe.prop(this, "elements");
                    return t ? oe.makeArray(t) : this
                }).filter(function () {
                    var t = this.type;
                    return this.name && !oe(this).is(":disabled") && Zn.test(this.nodeName) && !Yn.test(t) && (this.checked || !Ne.test(t))
                }).map(function (t, e) {
                    var n = oe(this).val();
                    return null == n ? null : oe.isArray(n) ? oe.map(n, function (t) {
                        return {name: e.name, value: t.replace(Vn, "\r\n")}
                    }) : {name: e.name, value: n.replace(Vn, "\r\n")}
                }).get()
            }
        }), oe.ajaxSettings.xhr = void 0 !== t.ActiveXObject ? function () {
            return !this.isLocal && /^(get|post|head|put|delete|options)$/i.test(this.type) && U() || G()
        } : U;
        var Jn = 0, Kn = {}, ti = oe.ajaxSettings.xhr();
        t.ActiveXObject && oe(t).on("unload", function () {
            for (var t in Kn)Kn[t](void 0, !0)
        }), ne.cors = !!ti && "withCredentials" in ti, ti = ne.ajax = !!ti, ti && oe.ajaxTransport(function (t) {
            if (!t.crossDomain || ne.cors) {
                var e;
                return {
                    send: function (n, i) {
                        var o, a = t.xhr(), r = ++Jn;
                        if (a.open(t.type, t.url, t.async, t.username, t.password), t.xhrFields)for (o in t.xhrFields)a[o] = t.xhrFields[o];
                        t.mimeType && a.overrideMimeType && a.overrideMimeType(t.mimeType), t.crossDomain || n["X-Requested-With"] || (n["X-Requested-With"] = "XMLHttpRequest");
                        for (o in n)void 0 !== n[o] && a.setRequestHeader(o, n[o] + "");
                        a.send(t.hasContent && t.data || null), e = function (n, o) {
                            var s, l, u;
                            if (e && (o || 4 === a.readyState))if (delete Kn[r], e = void 0, a.onreadystatechange = oe.noop, o)4 !== a.readyState && a.abort(); else {
                                u = {}, s = a.status, "string" == typeof a.responseText && (u.text = a.responseText);
                                try {
                                    l = a.statusText
                                } catch (c) {
                                    l = ""
                                }
                                s || !t.isLocal || t.crossDomain ? 1223 === s && (s = 204) : s = u.text ? 200 : 404
                            }
                            u && i(s, l, u, a.getAllResponseHeaders())
                        }, t.async ? 4 === a.readyState ? setTimeout(e) : a.onreadystatechange = Kn[r] = e : e()
                    }, abort: function () {
                        e && e(void 0, !0)
                    }
                }
            }
        }), oe.ajaxSetup({
            accepts: {script: "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},
            contents: {script: /(?:java|ecma)script/},
            converters: {
                "text script": function (t) {
                    return oe.globalEval(t), t
                }
            }
        }), oe.ajaxPrefilter("script", function (t) {
            void 0 === t.cache && (t.cache = !1), t.crossDomain && (t.type = "GET", t.global = !1)
        }), oe.ajaxTransport("script", function (t) {
            if (t.crossDomain) {
                var e, n = pe.head || oe("head")[0] || pe.documentElement;
                return {
                    send: function (i, o) {
                        e = pe.createElement("script"), e.async = !0, t.scriptCharset && (e.charset = t.scriptCharset), e.src = t.url, e.onload = e.onreadystatechange = function (t, n) {
                            (n || !e.readyState || /loaded|complete/.test(e.readyState)) && (e.onload = e.onreadystatechange = null, e.parentNode && e.parentNode.removeChild(e), e = null, n || o(200, "success"))
                        }, n.insertBefore(e, n.firstChild)
                    }, abort: function () {
                        e && e.onload(void 0, !0)
                    }
                }
            }
        });
        var ei = [], ni = /(=)\?(?=&|$)|\?\?/;
        oe.ajaxSetup({
            jsonp: "callback", jsonpCallback: function () {
                var t = ei.pop() || oe.expando + "_" + $n++;
                return this[t] = !0, t
            }
        }), oe.ajaxPrefilter("json jsonp", function (e, n, i) {
            var o, a, r, s = e.jsonp !== !1 && (ni.test(e.url) ? "url" : "string" == typeof e.data && !(e.contentType || "").indexOf("application/x-www-form-urlencoded") && ni.test(e.data) && "data");
            return s || "jsonp" === e.dataTypes[0] ? (o = e.jsonpCallback = oe.isFunction(e.jsonpCallback) ? e.jsonpCallback() : e.jsonpCallback, s ? e[s] = e[s].replace(ni, "$1" + o) : e.jsonp !== !1 && (e.url += (An.test(e.url) ? "&" : "?") + e.jsonp + "=" + o), e.converters["script json"] = function () {
                return r || oe.error(o + " was not called"), r[0]
            }, e.dataTypes[0] = "json", a = t[o], t[o] = function () {
                r = arguments
            }, i.always(function () {
                t[o] = a, e[o] && (e.jsonpCallback = n.jsonpCallback, ei.push(o)), r && oe.isFunction(a) && a(r[0]), r = a = void 0
            }), "script") : void 0
        }), oe.parseHTML = function (t, e, n) {
            if (!t || "string" != typeof t)return null;
            "boolean" == typeof e && (n = e, e = !1), e = e || pe;
            var i = de.exec(t), o = !n && [];
            return i ? [e.createElement(i[1])] : (i = oe.buildFragment([t], e, o), o && o.length && oe(o).remove(), oe.merge([], i.childNodes))
        };
        var ii = oe.fn.load;
        oe.fn.load = function (t, e, n) {
            if ("string" != typeof t && ii)return ii.apply(this, arguments);
            var i, o, a, r = this, s = t.indexOf(" ");
            return s >= 0 && (i = oe.trim(t.slice(s, t.length)), t = t.slice(0, s)), oe.isFunction(e) ? (n = e, e = void 0) : e && "object" == typeof e && (a = "POST"), r.length > 0 && oe.ajax({
                url: t,
                type: a,
                dataType: "html",
                data: e
            }).done(function (t) {
                o = arguments, r.html(i ? oe("<div>").append(oe.parseHTML(t)).find(i) : t)
            }).complete(n && function (t, e) {
                    r.each(n, o || [t.responseText, e, t])
                }), this
        }, oe.expr.filters.animated = function (t) {
            return oe.grep(oe.timers, function (e) {
                return t === e.elem
            }).length
        };
        var oi = t.document.documentElement;
        oe.offset = {
            setOffset: function (t, e, n) {
                var i, o, a, r, s, l, u, c = oe.css(t, "position"), d = oe(t), h = {};
                "static" === c && (t.style.position = "relative"), s = d.offset(), a = oe.css(t, "top"), l = oe.css(t, "left"), u = ("absolute" === c || "fixed" === c) && oe.inArray("auto", [a, l]) > -1, u ? (i = d.position(), r = i.top, o = i.left) : (r = parseFloat(a) || 0, o = parseFloat(l) || 0), oe.isFunction(e) && (e = e.call(t, n, s)), null != e.top && (h.top = e.top - s.top + r), null != e.left && (h.left = e.left - s.left + o), "using" in e ? e.using.call(t, h) : d.css(h)
            }
        }, oe.fn.extend({
            offset: function (t) {
                if (arguments.length)return void 0 === t ? this : this.each(function (e) {
                    oe.offset.setOffset(this, t, e)
                });
                var e, n, i = {top: 0, left: 0}, o = this[0], a = o && o.ownerDocument;
                if (a)return e = a.documentElement, oe.contains(e, o) ? (typeof o.getBoundingClientRect !== Ce && (i = o.getBoundingClientRect()), n = X(a), {
                    top: i.top + (n.pageYOffset || e.scrollTop) - (e.clientTop || 0),
                    left: i.left + (n.pageXOffset || e.scrollLeft) - (e.clientLeft || 0)
                }) : i
            }, position: function () {
                if (this[0]) {
                    var t, e, n = {top: 0, left: 0}, i = this[0];
                    return "fixed" === oe.css(i, "position") ? e = i.getBoundingClientRect() : (t = this.offsetParent(), e = this.offset(), oe.nodeName(t[0], "html") || (n = t.offset()), n.top += oe.css(t[0], "borderTopWidth", !0), n.left += oe.css(t[0], "borderLeftWidth", !0)), {
                        top: e.top - n.top - oe.css(i, "marginTop", !0),
                        left: e.left - n.left - oe.css(i, "marginLeft", !0)
                    }
                }
            }, offsetParent: function () {
                return this.map(function () {
                    for (var t = this.offsetParent || oi; t && !oe.nodeName(t, "html") && "static" === oe.css(t, "position");)t = t.offsetParent;
                    return t || oi
                })
            }
        }), oe.each({scrollLeft: "pageXOffset", scrollTop: "pageYOffset"}, function (t, e) {
            var n = /Y/.test(e);
            oe.fn[t] = function (i) {
                return je(this, function (t, i, o) {
                    var a = X(t);
                    return void 0 === o ? a ? e in a ? a[e] : a.document.documentElement[i] : t[i] : void(a ? a.scrollTo(n ? oe(a).scrollLeft() : o, n ? o : oe(a).scrollTop()) : t[i] = o)
                }, t, i, arguments.length, null)
            }
        }), oe.each(["top", "left"], function (t, e) {
            oe.cssHooks[e] = E(ne.pixelPosition, function (t, n) {
                return n ? (n = en(t, e), on.test(n) ? oe(t).position()[e] + "px" : n) : void 0
            })
        }), oe.each({Height: "height", Width: "width"}, function (t, e) {
            oe.each({padding: "inner" + t, content: e, "": "outer" + t}, function (n, i) {
                oe.fn[i] = function (i, o) {
                    var a = arguments.length && (n || "boolean" != typeof i), r = n || (i === !0 || o === !0 ? "margin" : "border");
                    return je(this, function (e, n, i) {
                        var o;
                        return oe.isWindow(e) ? e.document.documentElement["client" + t] : 9 === e.nodeType ? (o = e.documentElement, Math.max(e.body["scroll" + t], o["scroll" + t], e.body["offset" + t], o["offset" + t], o["client" + t])) : void 0 === i ? oe.css(e, n, r) : oe.style(e, n, i, r)
                    }, e, a ? i : void 0, a, null)
                }
            })
        }), oe.fn.size = function () {
            return this.length
        }, oe.fn.andSelf = oe.fn.addBack, "function" == typeof define && define.amd && define("jquery", [], function () {
            return oe
        });
        var ai = t.jQuery, ri = t.$;
        return oe.noConflict = function (e) {
            return t.$ === oe && (t.$ = ri), e && t.jQuery === oe && (t.jQuery = ai), oe
        }, typeof e === Ce && (t.jQuery = t.$ = oe), oe
    }), function (t, e) {
        t.rails !== e && t.error("jquery-ujs has already been loaded!");
        var n, i = t(document);
        t.rails = n = {
            linkClickSelector: "a[data-confirm], a[data-method], a[data-remote], a[data-disable-with], a[data-disable]",
            buttonClickSelector: "button[data-remote]:not(form button), button[data-confirm]:not(form button)",
            inputChangeSelector: "select[data-remote], input[data-remote], textarea[data-remote]",
            formSubmitSelector: "form",
            formInputClickSelector: "form input[type=submit], form input[type=image], form button[type=submit], form button:not([type]), input[type=submit][form], input[type=image][form], button[type=submit][form], button[form]:not([type])",
            disableSelector: "input[data-disable-with]:enabled, button[data-disable-with]:enabled, textarea[data-disable-with]:enabled, input[data-disable]:enabled, button[data-disable]:enabled, textarea[data-disable]:enabled",
            enableSelector: "input[data-disable-with]:disabled, button[data-disable-with]:disabled, textarea[data-disable-with]:disabled, input[data-disable]:disabled, button[data-disable]:disabled, textarea[data-disable]:disabled",
            requiredInputSelector: "input[name][required]:not([disabled]),textarea[name][required]:not([disabled])",
            fileInputSelector: "input[type=file]",
            linkDisableSelector: "a[data-disable-with], a[data-disable]",
            buttonDisableSelector: "button[data-remote][data-disable-with], button[data-remote][data-disable]",
            CSRFProtection: function (e) {
                var n = t('meta[name="csrf-token"]').attr("content");
                n && e.setRequestHeader("X-CSRF-Token", n)
            },
            refreshCSRFTokens: function () {
                var e = t("meta[name=csrf-token]").attr("content"), n = t("meta[name=csrf-param]").attr("content");
                t('form input[name="' + n + '"]').val(e)
            },
            fire: function (e, n, i) {
                var o = t.Event(n);
                return e.trigger(o, i), o.result !== !1
            },
            confirm: function (t) {
                return confirm(t)
            },
            ajax: function (e) {
                return t.ajax(e)
            },
            href: function (t) {
                return t.attr("href")
            },
            handleRemote: function (i) {
                var o, a, r, s, l, u, c, d;
                if (n.fire(i, "ajax:before")) {
                    if (s = i.data("cross-domain"), l = s === e ? null : s, u = i.data("with-credentials") || null, c = i.data("type") || t.ajaxSettings && t.ajaxSettings.dataType, i.is("form")) {
                        o = i.attr("method"), a = i.attr("action"), r = i.serializeArray();
                        var h = i.data("ujs:submit-button");
                        h && (r.push(h), i.data("ujs:submit-button", null))
                    } else i.is(n.inputChangeSelector) ? (o = i.data("method"), a = i.data("url"), r = i.serialize(), i.data("params") && (r = r + "&" + i.data("params"))) : i.is(n.buttonClickSelector) ? (o = i.data("method") || "get", a = i.data("url"), r = i.serialize(), i.data("params") && (r = r + "&" + i.data("params"))) : (o = i.data("method"), a = n.href(i), r = i.data("params") || null);
                    return d = {
                        type: o || "GET", data: r, dataType: c, beforeSend: function (t, o) {
                            return o.dataType === e && t.setRequestHeader("accept", "*/*;q=0.5, " + o.accepts.script), n.fire(i, "ajax:beforeSend", [t, o]) ? void i.trigger("ajax:send", t) : !1
                        }, success: function (t, e, n) {
                            i.trigger("ajax:success", [t, e, n])
                        }, complete: function (t, e) {
                            i.trigger("ajax:complete", [t, e])
                        }, error: function (t, e, n) {
                            i.trigger("ajax:error", [t, e, n])
                        }, crossDomain: l
                    }, u && (d.xhrFields = {withCredentials: u}), a && (d.url = a), n.ajax(d)
                }
                return !1
            },
            handleMethod: function (i) {
                var o = n.href(i), a = i.data("method"), r = i.attr("target"), s = t("meta[name=csrf-token]").attr("content"), l = t("meta[name=csrf-param]").attr("content"), u = t('<form method="post" action="' + o + '"></form>'), c = '<input name="_method" value="' + a + '" type="hidden" />';
                l !== e && s !== e && (c += '<input name="' + l + '" value="' + s + '" type="hidden" />'), r && u.attr("target", r), u.hide().append(c).appendTo("body"), u.submit()
            },
            formElements: function (e, n) {
                return e.is("form") ? t(e[0].elements).filter(n) : e.find(n)
            },
            disableFormElements: function (e) {
                n.formElements(e, n.disableSelector).each(function () {
                    n.disableFormElement(t(this))
                })
            },
            disableFormElement: function (t) {
                var n, i;
                n = t.is("button") ? "html" : "val", i = t.data("disable-with"), t.data("ujs:enable-with", t[n]()), i !== e && t[n](i), t.prop("disabled", !0)
            },
            enableFormElements: function (e) {
                n.formElements(e, n.enableSelector).each(function () {
                    n.enableFormElement(t(this))
                })
            },
            enableFormElement: function (t) {
                var e = t.is("button") ? "html" : "val";
                t.data("ujs:enable-with") && t[e](t.data("ujs:enable-with")), t.prop("disabled", !1)
            },
            allowAction: function (t) {
                var e, i = t.data("confirm"), o = !1;
                return i ? (n.fire(t, "confirm") && (o = n.confirm(i), e = n.fire(t, "confirm:complete", [o])), o && e) : !0
            },
            blankInputs: function (e, n, i) {
                var o, a, r = t(), s = n || "input,textarea", l = e.find(s);
                return l.each(function () {
                    if (o = t(this), a = o.is("input[type=checkbox],input[type=radio]") ? o.is(":checked") : o.val(), !a == !i) {
                        if (o.is("input[type=radio]") && l.filter('input[type=radio]:checked[name="' + o.attr("name") + '"]').length)return !0;
                        r = r.add(o)
                    }
                }), r.length ? r : !1
            },
            nonBlankInputs: function (t, e) {
                return n.blankInputs(t, e, !0)
            },
            stopEverything: function (e) {
                return t(e.target).trigger("ujs:everythingStopped"), e.stopImmediatePropagation(), !1
            },
            disableElement: function (t) {
                var i = t.data("disable-with");
                t.data("ujs:enable-with", t.html()), i !== e && t.html(i), t.bind("click.railsDisable", function (t) {
                    return n.stopEverything(t)
                })
            },
            enableElement: function (t) {
                t.data("ujs:enable-with") !== e && (t.html(t.data("ujs:enable-with")), t.removeData("ujs:enable-with")), t.unbind("click.railsDisable")
            }
        }, n.fire(i, "rails:attachBindings") && (t.ajaxPrefilter(function (t, e, i) {
            t.crossDomain || n.CSRFProtection(i)
        }), i.delegate(n.linkDisableSelector, "ajax:complete", function () {
            n.enableElement(t(this))
        }), i.delegate(n.buttonDisableSelector, "ajax:complete", function () {
            n.enableFormElement(t(this))
        }), i.delegate(n.linkClickSelector, "click.rails", function (i) {
            var o = t(this), a = o.data("method"), r = o.data("params"), s = i.metaKey || i.ctrlKey;
            if (!n.allowAction(o))return n.stopEverything(i);
            if (!s && o.is(n.linkDisableSelector) && n.disableElement(o), o.data("remote") !== e) {
                if (s && (!a || "GET" === a) && !r)return !0;
                var l = n.handleRemote(o);
                return l === !1 ? n.enableElement(o) : l.error(function () {
                    n.enableElement(o)
                }), !1
            }
            return o.data("method") ? (n.handleMethod(o), !1) : void 0
        }), i.delegate(n.buttonClickSelector, "click.rails", function (e) {
            var i = t(this);
            if (!n.allowAction(i))return n.stopEverything(e);
            i.is(n.buttonDisableSelector) && n.disableFormElement(i);
            var o = n.handleRemote(i);
            return o === !1 ? n.enableFormElement(i) : o.error(function () {
                n.enableFormElement(i)
            }), !1
        }), i.delegate(n.inputChangeSelector, "change.rails", function (e) {
            var i = t(this);
            return n.allowAction(i) ? (n.handleRemote(i), !1) : n.stopEverything(e)
        }), i.delegate(n.formSubmitSelector, "submit.rails", function (i) {
            var o, a, r = t(this), s = r.data("remote") !== e;
            if (!n.allowAction(r))return n.stopEverything(i);
            if (r.attr("novalidate") == e && (o = n.blankInputs(r, n.requiredInputSelector), o && n.fire(r, "ajax:aborted:required", [o])))return n.stopEverything(i);
            if (s) {
                if (a = n.nonBlankInputs(r, n.fileInputSelector)) {
                    setTimeout(function () {
                        n.disableFormElements(r)
                    }, 13);
                    var l = n.fire(r, "ajax:aborted:file", [a]);
                    return l || setTimeout(function () {
                        n.enableFormElements(r)
                    }, 13), l
                }
                return n.handleRemote(r), !1
            }
            setTimeout(function () {
                n.disableFormElements(r)
            }, 13)
        }), i.delegate(n.formInputClickSelector, "click.rails", function (e) {
            var i = t(this);
            if (!n.allowAction(i))return n.stopEverything(e);
            var o = i.attr("name"), a = o ? {name: o, value: i.val()} : null;
            i.closest("form").data("ujs:submit-button", a)
        }), i.delegate(n.formSubmitSelector, "ajax:send.rails", function (e) {
            this == e.target && n.disableFormElements(t(this))
        }), i.delegate(n.formSubmitSelector, "ajax:complete.rails", function (e) {
            this == e.target && n.enableFormElements(t(this))
        }), t(function () {
            n.refreshCSRFTokens()
        }))
    }(jQuery), !function (t) {
        "use strict";
        var e = function (e, n) {
            this.$element = t(e), this.options = t.extend({}, t.fn.button.defaults, n)
        };
        e.prototype = {
            constructor: e, setState: function (t) {
                var e = "disabled", n = this.$element, i = n.data(), o = n.is("input") ? "val" : "html";
                t += "Text", i.resetText || n.data("resetText", n[o]()), n[o](i[t] || this.options[t]), setTimeout(function () {
                    "loadingText" == t ? n.addClass(e).attr(e, e) : n.removeClass(e).removeAttr(e)
                }, 0)
            }, toggle: function () {
                var t = this.$element.parent('[data-toggle="buttons-radio"]');
                t && t.find(".active").removeClass("active"), this.$element.toggleClass("active")
            }
        }, t.fn.button = function (n) {
            return this.each(function () {
                var i = t(this), o = i.data("button"), a = "object" == typeof n && n;
                o || i.data("button", o = new e(this, a)), "toggle" == n ? o.toggle() : n && o.setState(n)
            })
        }, t.fn.button.defaults = {loadingText: "loading..."}, t.fn.button.Constructor = e, t(function () {
            t("body").on("click.button.data-api", "[data-toggle^=button]", function (e) {
                var n = t(e.target);
                n.hasClass("btn") || (n = n.closest(".btn")), n.button("toggle")
            })
        })
    }(window.jQuery), !function (t) {
        "use strict";
        function e(e) {
            var i = this.$element.hasClass("fade") ? "fade" : "";
            if (this.isShown && this.options.backdrop) {
                var o = t.support.transition && i;
                this.$backdrop = t('<div class="modal-backdrop ' + i + '" />').appendTo(document.body), "static" != this.options.backdrop && this.$backdrop.click(t.proxy(this.hide, this)), o && this.$backdrop[0].offsetWidth, this.$backdrop.addClass("in"), o ? this.$backdrop.one(t.support.transition.end, e) : e()
            } else!this.isShown && this.$backdrop ? (this.$backdrop.removeClass("in"), t.support.transition && this.$element.hasClass("fade") ? this.$backdrop.one(t.support.transition.end, t.proxy(n, this)) : n.call(this)) : e && e()
        }

        function n() {
            this.$backdrop.remove(), this.$backdrop = null
        }

        function i() {
            var e = this;
            this.isShown && this.options.keyboard ? t(document).on("keyup.dismiss.modal", function (t) {
                27 == t.which && e.hide()
            }) : this.isShown || t(document).off("keyup.dismiss.modal")
        }

        var o = function (e, n) {
            this.options = n, this.$element = t(e).delegate('[data-dismiss="modal"]', "click.dismiss.modal", t.proxy(this.hide, this))
        };
        o.prototype = {
            constructor: o, toggle: function () {
                return this[this.isShown ? "hide" : "show"]()
            }, show: function () {
                var n = this;
                this.isShown || (t("body").addClass("modal-open"), this.isShown = !0, this.$element.trigger("show"), i.call(this), e.call(this, function () {
                    var e = t.support.transition && n.$element.hasClass("fade");
                    !n.$element.parent().length && n.$element.appendTo(document.body), n.$element.show(), e && n.$element[0].offsetWidth, n.$element.addClass("in"), e ? n.$element.one(t.support.transition.end, function () {
                        n.$element.trigger("shown")
                    }) : n.$element.trigger("shown")
                }))
            }, hide: function (e) {
                if (e && e.preventDefault(), this.isShown) {
                    this.isShown = !1, t("body").removeClass("modal-open"), i.call(this), this.$element.trigger("hide").removeClass("in")
                }
            }
        }, t.fn.modal = function (e) {
            return this.each(function () {
                var n = t(this), i = n.data("modal"), a = t.extend({}, t.fn.modal.defaults, n.data(), "object" == typeof e && e);
                i || n.data("modal", i = new o(this, a)), "string" == typeof e ? i[e]() : a.show && i.show()
            })
        }, t.fn.modal.defaults = {backdrop: !0, keyboard: !0, show: !0}, t.fn.modal.Constructor = o, t(function () {
            t("body").on("click.modal.data-api", '[data-toggle="modal"]', function (e) {
                var n, i = t(this), o = t(i.attr("data-target") || (n = i.attr("href")) && n.replace(/.*(?=#[^\s]+$)/, "")), a = o.data("modal") ? "toggle" : t.extend({}, o.data(), i.data());
                e.preventDefault(), o.modal(a)
            })
        })
    }(window.jQuery), function (t, e) {
        function n(e, n) {
            var o, a, r, s = e.nodeName.toLowerCase();
            return "area" === s ? (o = e.parentNode, a = o.name, e.href && a && "map" === o.nodeName.toLowerCase() ? (r = t("img[usemap=#" + a + "]")[0], !!r && i(r)) : !1) : (/input|select|textarea|button|object/.test(s) ? !e.disabled : "a" === s ? e.href || n : n) && i(e)
        }

        function i(e) {
            return t.expr.filters.visible(e) && !t(e).parents().addBack().filter(function () {
                    return "hidden" === t.css(this, "visibility")
                }).length
        }

        var o = 0, a = /^ui-id-\d+$/;
        t.ui = t.ui || {}, t.extend(t.ui, {
            version: "1.10.3",
            keyCode: {
                BACKSPACE: 8,
                COMMA: 188,
                DELETE: 46,
                DOWN: 40,
                END: 35,
                ENTER: 13,
                ESCAPE: 27,
                HOME: 36,
                LEFT: 37,
                NUMPAD_ADD: 107,
                NUMPAD_DECIMAL: 110,
                NUMPAD_DIVIDE: 111,
                NUMPAD_ENTER: 108,
                NUMPAD_MULTIPLY: 106,
                NUMPAD_SUBTRACT: 109,
                PAGE_DOWN: 34,
                PAGE_UP: 33,
                PERIOD: 190,
                RIGHT: 39,
                SPACE: 32,
                TAB: 9,
                UP: 38
            }
        }), t.fn.extend({
            focus: function (e) {
                return function (n, i) {
                    return "number" == typeof n ? this.each(function () {
                        var e = this;
                        setTimeout(function () {
                            t(e).focus(), i && i.call(e)
                        }, n)
                    }) : e.apply(this, arguments)
                }
            }(t.fn.focus), scrollParent: function () {
                var e;
                return e = t.ui.ie && /(static|relative)/.test(this.css("position")) || /absolute/.test(this.css("position")) ? this.parents().filter(function () {
                    return /(relative|absolute|fixed)/.test(t.css(this, "position")) && /(auto|scroll)/.test(t.css(this, "overflow") + t.css(this, "overflow-y") + t.css(this, "overflow-x"))
                }).eq(0) : this.parents().filter(function () {
                    return /(auto|scroll)/.test(t.css(this, "overflow") + t.css(this, "overflow-y") + t.css(this, "overflow-x"))
                }).eq(0), /fixed/.test(this.css("position")) || !e.length ? t(document) : e
            }, zIndex: function (n) {
                if (n !== e)return this.css("zIndex", n);
                if (this.length)for (var i, o, a = t(this[0]); a.length && a[0] !== document;) {
                    if (i = a.css("position"), ("absolute" === i || "relative" === i || "fixed" === i) && (o = parseInt(a.css("zIndex"), 10), !isNaN(o) && 0 !== o))return o;
                    a = a.parent()
                }
                return 0
            }, uniqueId: function () {
                return this.each(function () {
                    this.id || (this.id = "ui-id-" + ++o)
                })
            }, removeUniqueId: function () {
                return this.each(function () {
                    a.test(this.id) && t(this).removeAttr("id")
                })
            }
        }), t.extend(t.expr[":"], {
            data: t.expr.createPseudo ? t.expr.createPseudo(function (e) {
                return function (n) {
                    return !!t.data(n, e)
                }
            }) : function (e, n, i) {
                return !!t.data(e, i[3])
            }, focusable: function (e) {
                return n(e, !isNaN(t.attr(e, "tabindex")))
            }, tabbable: function (e) {
                var i = t.attr(e, "tabindex"), o = isNaN(i);
                return (o || i >= 0) && n(e, !o)
            }
        }), t("<a>").outerWidth(1).jquery || t.each(["Width", "Height"], function (n, i) {
            function o(e, n, i, o) {
                return t.each(a, function () {
                    n -= parseFloat(t.css(e, "padding" + this)) || 0, i && (n -= parseFloat(t.css(e, "border" + this + "Width")) || 0), o && (n -= parseFloat(t.css(e, "margin" + this)) || 0)
                }), n
            }

            var a = "Width" === i ? ["Left", "Right"] : ["Top", "Bottom"], r = i.toLowerCase(), s = {
                innerWidth: t.fn.innerWidth,
                innerHeight: t.fn.innerHeight,
                outerWidth: t.fn.outerWidth,
                outerHeight: t.fn.outerHeight
            };
            t.fn["inner" + i] = function (n) {
                return n === e ? s["inner" + i].call(this) : this.each(function () {
                    t(this).css(r, o(this, n) + "px")
                })
            }, t.fn["outer" + i] = function (e, n) {
                return "number" != typeof e ? s["outer" + i].call(this, e) : this.each(function () {
                    t(this).css(r, o(this, e, !0, n) + "px")
                })
            }
        }), t.fn.addBack || (t.fn.addBack = function (t) {
            return this.add(null == t ? this.prevObject : this.prevObject.filter(t))
        }), t("<a>").data("a-b", "a").removeData("a-b").data("a-b") && (t.fn.removeData = function (e) {
            return function (n) {
                return arguments.length ? e.call(this, t.camelCase(n)) : e.call(this)
            }
        }(t.fn.removeData)), t.ui.ie = !!/msie [\w.]+/.exec(navigator.userAgent.toLowerCase()), t.support.selectstart = "onselectstart" in document.createElement("div"), t.fn.extend({
            disableSelection: function () {
                return this.bind((t.support.selectstart ? "selectstart" : "mousedown") + ".ui-disableSelection", function (t) {
                    t.preventDefault()
                })
            }, enableSelection: function () {
                return this.unbind(".ui-disableSelection")
            }
        }), t.extend(t.ui, {
            plugin: {
                add: function (e, n, i) {
                    var o, a = t.ui[e].prototype;
                    for (o in i)a.plugins[o] = a.plugins[o] || [], a.plugins[o].push([n, i[o]])
                }, call: function (t, e, n) {
                    var i, o = t.plugins[e];
                    if (o && t.element[0].parentNode && 11 !== t.element[0].parentNode.nodeType)for (i = 0; o.length > i; i++)t.options[o[i][0]] && o[i][1].apply(t.element, n)
                }
            }, hasScroll: function (e, n) {
                if ("hidden" === t(e).css("overflow"))return !1;
                var i = n && "left" === n ? "scrollLeft" : "scrollTop", o = !1;
                return e[i] > 0 ? !0 : (e[i] = 1, o = e[i] > 0, e[i] = 0, o)
            }
        })
    }(jQuery), function (t, e) {
        var n = 0, i = Array.prototype.slice, o = t.cleanData;
        t.cleanData = function (e) {
            for (var n, i = 0; null != (n = e[i]); i++)try {
                t(n).triggerHandler("remove")
            } catch (a) {
            }
            o(e)
        }, t.widget = function (n, i, o) {
            var a, r, s, l, u = {}, c = n.split(".")[0];
            n = n.split(".")[1], a = c + "-" + n, o || (o = i, i = t.Widget), t.expr[":"][a.toLowerCase()] = function (e) {
                return !!t.data(e, a)
            }, t[c] = t[c] || {}, r = t[c][n], s = t[c][n] = function (t, n) {
                return this._createWidget ? (arguments.length && this._createWidget(t, n), e) : new s(t, n)
            }, t.extend(s, r, {
                version: o.version,
                _proto: t.extend({}, o),
                _childConstructors: []
            }), l = new i, l.options = t.widget.extend({}, l.options), t.each(o, function (n, o) {
                return t.isFunction(o) ? (u[n] = function () {
                    var t = function () {
                        return i.prototype[n].apply(this, arguments)
                    }, e = function (t) {
                        return i.prototype[n].apply(this, t)
                    };
                    return function () {
                        var n, i = this._super, a = this._superApply;
                        return this._super = t, this._superApply = e, n = o.apply(this, arguments), this._super = i, this._superApply = a, n
                    }
                }(), e) : (u[n] = o, e)
            }), s.prototype = t.widget.extend(l, {widgetEventPrefix: r ? l.widgetEventPrefix : n}, u, {
                constructor: s,
                namespace: c,
                widgetName: n,
                widgetFullName: a
            }), r ? (t.each(r._childConstructors, function (e, n) {
                var i = n.prototype;
                t.widget(i.namespace + "." + i.widgetName, s, n._proto)
            }), delete r._childConstructors) : i._childConstructors.push(s), t.widget.bridge(n, s)
        }, t.widget.extend = function (n) {
            for (var o, a, r = i.call(arguments, 1), s = 0, l = r.length; l > s; s++)for (o in r[s])a = r[s][o], r[s].hasOwnProperty(o) && a !== e && (n[o] = t.isPlainObject(a) ? t.isPlainObject(n[o]) ? t.widget.extend({}, n[o], a) : t.widget.extend({}, a) : a);
            return n
        }, t.widget.bridge = function (n, o) {
            var a = o.prototype.widgetFullName || n;
            t.fn[n] = function (r) {
                var s = "string" == typeof r, l = i.call(arguments, 1), u = this;
                return r = !s && l.length ? t.widget.extend.apply(null, [r].concat(l)) : r, this.each(s ? function () {
                    var i, o = t.data(this, a);
                    return o ? t.isFunction(o[r]) && "_" !== r.charAt(0) ? (i = o[r].apply(o, l), i !== o && i !== e ? (u = i && i.jquery ? u.pushStack(i.get()) : i, !1) : e) : t.error("no such method '" + r + "' for " + n + " widget instance") : t.error("cannot call methods on " + n + " prior to initialization; attempted to call method '" + r + "'")
                } : function () {
                    var e = t.data(this, a);
                    e ? e.option(r || {})._init() : t.data(this, a, new o(r, this))
                }), u
            }
        }, t.Widget = function () {
        }, t.Widget._childConstructors = [], t.Widget.prototype = {
            widgetName: "widget",
            widgetEventPrefix: "",
            defaultElement: "<div>",
            options: {disabled: !1, create: null},
            _createWidget: function (e, i) {
                i = t(i || this.defaultElement || this)[0], this.element = t(i), this.uuid = n++, this.eventNamespace = "." + this.widgetName + this.uuid, this.options = t.widget.extend({}, this.options, this._getCreateOptions(), e), this.bindings = t(), this.hoverable = t(), this.focusable = t(), i !== this && (t.data(i, this.widgetFullName, this), this._on(!0, this.element, {
                    remove: function (t) {
                        t.target === i && this.destroy()
                    }
                }), this.document = t(i.style ? i.ownerDocument : i.document || i), this.window = t(this.document[0].defaultView || this.document[0].parentWindow)), this._create(), this._trigger("create", null, this._getCreateEventData()), this._init()
            },
            _getCreateOptions: t.noop,
            _getCreateEventData: t.noop,
            _create: t.noop,
            _init: t.noop,
            destroy: function () {
                this._destroy(), this.element.unbind(this.eventNamespace).removeData(this.widgetName).removeData(this.widgetFullName).removeData(t.camelCase(this.widgetFullName)), this.widget().unbind(this.eventNamespace).removeAttr("aria-disabled").removeClass(this.widgetFullName + "-disabled ui-state-disabled"), this.bindings.unbind(this.eventNamespace), this.hoverable.removeClass("ui-state-hover"), this.focusable.removeClass("ui-state-focus")
            },
            _destroy: t.noop,
            widget: function () {
                return this.element
            },
            option: function (n, i) {
                var o, a, r, s = n;
                if (0 === arguments.length)return t.widget.extend({}, this.options);
                if ("string" == typeof n)if (s = {}, o = n.split("."), n = o.shift(), o.length) {
                    for (a = s[n] = t.widget.extend({}, this.options[n]), r = 0; o.length - 1 > r; r++)a[o[r]] = a[o[r]] || {}, a = a[o[r]];
                    if (n = o.pop(), i === e)return a[n] === e ? null : a[n];
                    a[n] = i
                } else {
                    if (i === e)return this.options[n] === e ? null : this.options[n];
                    s[n] = i
                }
                return this._setOptions(s), this
            },
            _setOptions: function (t) {
                var e;
                for (e in t)this._setOption(e, t[e]);
                return this
            },
            _setOption: function (t, e) {
                return this.options[t] = e, "disabled" === t && (this.widget().toggleClass(this.widgetFullName + "-disabled ui-state-disabled", !!e).attr("aria-disabled", e), this.hoverable.removeClass("ui-state-hover"), this.focusable.removeClass("ui-state-focus")), this
            },
            enable: function () {
                return this._setOption("disabled", !1)
            },
            disable: function () {
                return this._setOption("disabled", !0)
            },
            _on: function (n, i, o) {
                var a, r = this;
                "boolean" != typeof n && (o = i, i = n, n = !1), o ? (i = a = t(i), this.bindings = this.bindings.add(i)) : (o = i, i = this.element, a = this.widget()), t.each(o, function (o, s) {
                    function l() {
                        return n || r.options.disabled !== !0 && !t(this).hasClass("ui-state-disabled") ? ("string" == typeof s ? r[s] : s).apply(r, arguments) : e
                    }

                    "string" != typeof s && (l.guid = s.guid = s.guid || l.guid || t.guid++);
                    var u = o.match(/^(\w+)\s*(.*)$/), c = u[1] + r.eventNamespace, d = u[2];
                    d ? a.delegate(d, c, l) : i.bind(c, l)
                })
            },
            _off: function (t, e) {
                e = (e || "").split(" ").join(this.eventNamespace + " ") + this.eventNamespace, t.unbind(e).undelegate(e)
            },
            _delay: function (t, e) {
                function n() {
                    return ("string" == typeof t ? i[t] : t).apply(i, arguments)
                }

                var i = this;
                return setTimeout(n, e || 0)
            },
            _hoverable: function (e) {
                this.hoverable = this.hoverable.add(e), this._on(e, {
                    mouseenter: function (e) {
                        t(e.currentTarget).addClass("ui-state-hover")
                    }, mouseleave: function (e) {
                        t(e.currentTarget).removeClass("ui-state-hover")
                    }
                })
            },
            _focusable: function (e) {
                this.focusable = this.focusable.add(e), this._on(e, {
                    focusin: function (e) {
                        t(e.currentTarget).addClass("ui-state-focus")
                    }, focusout: function (e) {
                        t(e.currentTarget).removeClass("ui-state-focus")
                    }
                })
            },
            _trigger: function (e, n, i) {
                var o, a, r = this.options[e];
                if (i = i || {}, n = t.Event(n), n.type = (e === this.widgetEventPrefix ? e : this.widgetEventPrefix + e).toLowerCase(), n.target = this.element[0], a = n.originalEvent)for (o in a)o in n || (n[o] = a[o]);
                return this.element.trigger(n, i), !(t.isFunction(r) && r.apply(this.element[0], [n].concat(i)) === !1 || n.isDefaultPrevented())
            }
        }, t.each({show: "fadeIn", hide: "fadeOut"}, function (e, n) {
            t.Widget.prototype["_" + e] = function (i, o, a) {
                "string" == typeof o && (o = {effect: o});
                var r, s = o ? o === !0 || "number" == typeof o ? n : o.effect || n : e;
                o = o || {}, "number" == typeof o && (o = {duration: o}), r = !t.isEmptyObject(o), o.complete = a, o.delay && i.delay(o.delay), r && t.effects && t.effects.effect[s] ? i[e](o) : s !== e && i[s] ? i[s](o.duration, o.easing, a) : i.queue(function (n) {
                    t(this)[e](), a && a.call(i[0]), n()
                })
            }
        })
    }(jQuery), function (t) {
        var e = !1;
        t(document).mouseup(function () {
            e = !1
        }), t.widget("ui.mouse", {
            version: "1.10.3",
            options: {cancel: "input,textarea,button,select,option", distance: 1, delay: 0},
            _mouseInit: function () {
                var e = this;
                this.element.bind("mousedown." + this.widgetName, function (t) {
                    return e._mouseDown(t)
                }).bind("click." + this.widgetName, function (n) {
                    return !0 === t.data(n.target, e.widgetName + ".preventClickEvent") ? (t.removeData(n.target, e.widgetName + ".preventClickEvent"), n.stopImmediatePropagation(), !1) : void 0
                }), this.started = !1
            },
            _mouseDestroy: function () {
                this.element.unbind("." + this.widgetName), this._mouseMoveDelegate && t(document).unbind("mousemove." + this.widgetName, this._mouseMoveDelegate).unbind("mouseup." + this.widgetName, this._mouseUpDelegate)
            },
            _mouseDown: function (n) {
                if (!e) {
                    this._mouseStarted && this._mouseUp(n), this._mouseDownEvent = n;
                    var i = this, o = 1 === n.which, a = "string" == typeof this.options.cancel && n.target.nodeName ? t(n.target).closest(this.options.cancel).length : !1;
                    return o && !a && this._mouseCapture(n) ? (this.mouseDelayMet = !this.options.delay, this.mouseDelayMet || (this._mouseDelayTimer = setTimeout(function () {
                        i.mouseDelayMet = !0
                    }, this.options.delay)), this._mouseDistanceMet(n) && this._mouseDelayMet(n) && (this._mouseStarted = this._mouseStart(n) !== !1, !this._mouseStarted) ? (n.preventDefault(), !0) : (!0 === t.data(n.target, this.widgetName + ".preventClickEvent") && t.removeData(n.target, this.widgetName + ".preventClickEvent"), this._mouseMoveDelegate = function (t) {
                        return i._mouseMove(t)
                    }, this._mouseUpDelegate = function (t) {
                        return i._mouseUp(t)
                    }, t(document).bind("mousemove." + this.widgetName, this._mouseMoveDelegate).bind("mouseup." + this.widgetName, this._mouseUpDelegate), n.preventDefault(), e = !0, !0)) : !0
                }
            },
            _mouseMove: function (e) {
                return t.ui.ie && (!document.documentMode || 9 > document.documentMode) && !e.button ? this._mouseUp(e) : this._mouseStarted ? (this._mouseDrag(e), e.preventDefault()) : (this._mouseDistanceMet(e) && this._mouseDelayMet(e) && (this._mouseStarted = this._mouseStart(this._mouseDownEvent, e) !== !1, this._mouseStarted ? this._mouseDrag(e) : this._mouseUp(e)), !this._mouseStarted)
            },
            _mouseUp: function (e) {
                return t(document).unbind("mousemove." + this.widgetName, this._mouseMoveDelegate).unbind("mouseup." + this.widgetName, this._mouseUpDelegate), this._mouseStarted && (this._mouseStarted = !1, e.target === this._mouseDownEvent.target && t.data(e.target, this.widgetName + ".preventClickEvent", !0), this._mouseStop(e)), !1
            },
            _mouseDistanceMet: function (t) {
                return Math.max(Math.abs(this._mouseDownEvent.pageX - t.pageX), Math.abs(this._mouseDownEvent.pageY - t.pageY)) >= this.options.distance
            },
            _mouseDelayMet: function () {
                return this.mouseDelayMet
            },
            _mouseStart: function () {
            },
            _mouseDrag: function () {
            },
            _mouseStop: function () {
            },
            _mouseCapture: function () {
                return !0
            }
        })
    }(jQuery), function (t, e) {
        function n(t, e, n) {
            return [parseFloat(t[0]) * (f.test(t[0]) ? e / 100 : 1), parseFloat(t[1]) * (f.test(t[1]) ? n / 100 : 1)]
        }

        function i(e, n) {
            return parseInt(t.css(e, n), 10) || 0
        }

        function o(e) {
            var n = e[0];
            return 9 === n.nodeType ? {
                width: e.width(),
                height: e.height(),
                offset: {top: 0, left: 0}
            } : t.isWindow(n) ? {
                width: e.width(),
                height: e.height(),
                offset: {top: e.scrollTop(), left: e.scrollLeft()}
            } : n.preventDefault ? {
                width: 0,
                height: 0,
                offset: {top: n.pageY, left: n.pageX}
            } : {width: e.outerWidth(), height: e.outerHeight(), offset: e.offset()}
        }

        t.ui = t.ui || {};
        var a, r = Math.max, s = Math.abs, l = Math.round, u = /left|center|right/, c = /top|center|bottom/, d = /[\+\-]\d+(\.[\d]+)?%?/, h = /^\w+/, f = /%$/, p = t.fn.position;
        t.position = {
            scrollbarWidth: function () {
                if (a !== e)return a;
                var n, i, o = t("<div style='display:block;width:50px;height:50px;overflow:hidden;'><div style='height:100px;width:auto;'></div></div>"), r = o.children()[0];
                return t("body").append(o), n = r.offsetWidth, o.css("overflow", "scroll"), i = r.offsetWidth, n === i && (i = o[0].clientWidth), o.remove(), a = n - i
            }, getScrollInfo: function (e) {
                var n = e.isWindow ? "" : e.element.css("overflow-x"), i = e.isWindow ? "" : e.element.css("overflow-y"), o = "scroll" === n || "auto" === n && e.width < e.element[0].scrollWidth, a = "scroll" === i || "auto" === i && e.height < e.element[0].scrollHeight;
                return {width: a ? t.position.scrollbarWidth() : 0, height: o ? t.position.scrollbarWidth() : 0}
            }, getWithinInfo: function (e) {
                var n = t(e || window), i = t.isWindow(n[0]);
                return {
                    element: n,
                    isWindow: i,
                    offset: n.offset() || {left: 0, top: 0},
                    scrollLeft: n.scrollLeft(),
                    scrollTop: n.scrollTop(),
                    width: i ? n.width() : n.outerWidth(),
                    height: i ? n.height() : n.outerHeight()
                }
            }
        }, t.fn.position = function (e) {
            if (!e || !e.of)return p.apply(this, arguments);
            e = t.extend({}, e);
            var a, f, m, g, v, y, b = t(e.of), w = t.position.getWithinInfo(e.within), x = t.position.getScrollInfo(w), _ = (e.collision || "flip").split(" "), C = {};
            return y = o(b), b[0].preventDefault && (e.at = "left top"), f = y.width, m = y.height, g = y.offset, v = t.extend({}, g), t.each(["my", "at"], function () {
                var t, n, i = (e[this] || "").split(" ");
                1 === i.length && (i = u.test(i[0]) ? i.concat(["center"]) : c.test(i[0]) ? ["center"].concat(i) : ["center", "center"]), i[0] = u.test(i[0]) ? i[0] : "center", i[1] = c.test(i[1]) ? i[1] : "center", t = d.exec(i[0]), n = d.exec(i[1]), C[this] = [t ? t[0] : 0, n ? n[0] : 0], e[this] = [h.exec(i[0])[0], h.exec(i[1])[0]]
            }), 1 === _.length && (_[1] = _[0]), "right" === e.at[0] ? v.left += f : "center" === e.at[0] && (v.left += f / 2), "bottom" === e.at[1] ? v.top += m : "center" === e.at[1] && (v.top += m / 2), a = n(C.at, f, m), v.left += a[0], v.top += a[1], this.each(function () {
                var o, u, c = t(this), d = c.outerWidth(), h = c.outerHeight(), p = i(this, "marginLeft"), y = i(this, "marginTop"), k = d + p + i(this, "marginRight") + x.width, T = h + y + i(this, "marginBottom") + x.height, E = t.extend({}, v), S = n(C.my, c.outerWidth(), c.outerHeight());
                "right" === e.my[0] ? E.left -= d : "center" === e.my[0] && (E.left -= d / 2), "bottom" === e.my[1] ? E.top -= h : "center" === e.my[1] && (E.top -= h / 2), E.left += S[0], E.top += S[1], t.support.offsetFractions || (E.left = l(E.left), E.top = l(E.top)), o = {
                    marginLeft: p,
                    marginTop: y
                }, t.each(["left", "top"], function (n, i) {
                    t.ui.position[_[n]] && t.ui.position[_[n]][i](E, {
                        targetWidth: f,
                        targetHeight: m,
                        elemWidth: d,
                        elemHeight: h,
                        collisionPosition: o,
                        collisionWidth: k,
                        collisionHeight: T,
                        offset: [a[0] + S[0], a[1] + S[1]],
                        my: e.my,
                        at: e.at,
                        within: w,
                        elem: c
                    })
                }), e.using && (u = function (t) {
                    var n = g.left - E.left, i = n + f - d, o = g.top - E.top, a = o + m - h, l = {
                        target: {
                            element: b,
                            left: g.left,
                            top: g.top,
                            width: f,
                            height: m
                        },
                        element: {element: c, left: E.left, top: E.top, width: d, height: h},
                        horizontal: 0 > i ? "left" : n > 0 ? "right" : "center",
                        vertical: 0 > a ? "top" : o > 0 ? "bottom" : "middle"
                    };
                    d > f && f > s(n + i) && (l.horizontal = "center"), h > m && m > s(o + a) && (l.vertical = "middle"), l.important = r(s(n), s(i)) > r(s(o), s(a)) ? "horizontal" : "vertical", e.using.call(this, t, l)
                }), c.offset(t.extend(E, {using: u}))
            })
        }, t.ui.position = {
            fit: {
                left: function (t, e) {
                    var n, i = e.within, o = i.isWindow ? i.scrollLeft : i.offset.left, a = i.width, s = t.left - e.collisionPosition.marginLeft, l = o - s, u = s + e.collisionWidth - a - o;
                    e.collisionWidth > a ? l > 0 && 0 >= u ? (n = t.left + l + e.collisionWidth - a - o, t.left += l - n) : t.left = u > 0 && 0 >= l ? o : l > u ? o + a - e.collisionWidth : o : l > 0 ? t.left += l : u > 0 ? t.left -= u : t.left = r(t.left - s, t.left)
                }, top: function (t, e) {
                    var n, i = e.within, o = i.isWindow ? i.scrollTop : i.offset.top, a = e.within.height, s = t.top - e.collisionPosition.marginTop, l = o - s, u = s + e.collisionHeight - a - o;
                    e.collisionHeight > a ? l > 0 && 0 >= u ? (n = t.top + l + e.collisionHeight - a - o, t.top += l - n) : t.top = u > 0 && 0 >= l ? o : l > u ? o + a - e.collisionHeight : o : l > 0 ? t.top += l : u > 0 ? t.top -= u : t.top = r(t.top - s, t.top)
                }
            }, flip: {
                left: function (t, e) {
                    var n, i, o = e.within, a = o.offset.left + o.scrollLeft, r = o.width, l = o.isWindow ? o.scrollLeft : o.offset.left, u = t.left - e.collisionPosition.marginLeft, c = u - l, d = u + e.collisionWidth - r - l, h = "left" === e.my[0] ? -e.elemWidth : "right" === e.my[0] ? e.elemWidth : 0, f = "left" === e.at[0] ? e.targetWidth : "right" === e.at[0] ? -e.targetWidth : 0, p = -2 * e.offset[0];
                    0 > c ? (n = t.left + h + f + p + e.collisionWidth - r - a, (0 > n || s(c) > n) && (t.left += h + f + p)) : d > 0 && (i = t.left - e.collisionPosition.marginLeft + h + f + p - l, (i > 0 || d > s(i)) && (t.left += h + f + p))
                }, top: function (t, e) {
                    var n, i, o = e.within, a = o.offset.top + o.scrollTop, r = o.height, l = o.isWindow ? o.scrollTop : o.offset.top, u = t.top - e.collisionPosition.marginTop, c = u - l, d = u + e.collisionHeight - r - l, h = "top" === e.my[1], f = h ? -e.elemHeight : "bottom" === e.my[1] ? e.elemHeight : 0, p = "top" === e.at[1] ? e.targetHeight : "bottom" === e.at[1] ? -e.targetHeight : 0, m = -2 * e.offset[1];
                    0 > c ? (i = t.top + f + p + m + e.collisionHeight - r - a, t.top + f + p + m > c && (0 > i || s(c) > i) && (t.top += f + p + m)) : d > 0 && (n = t.top - e.collisionPosition.marginTop + f + p + m - l, t.top + f + p + m > d && (n > 0 || d > s(n)) && (t.top += f + p + m))
                }
            }, flipfit: {
                left: function () {
                    t.ui.position.flip.left.apply(this, arguments), t.ui.position.fit.left.apply(this, arguments)
                }, top: function () {
                    t.ui.position.flip.top.apply(this, arguments), t.ui.position.fit.top.apply(this, arguments)
                }
            }
        }, function () {
            var e, n, i, o, a, r = document.getElementsByTagName("body")[0], s = document.createElement("div");
            e = document.createElement(r ? "div" : "body"), i = {
                visibility: "hidden",
                width: 0,
                height: 0,
                border: 0,
                margin: 0,
                background: "none"
            }, r && t.extend(i, {position: "absolute", left: "-1000px", top: "-1000px"});
            for (a in i)e.style[a] = i[a];
            e.appendChild(s), n = r || document.documentElement, n.insertBefore(e, n.firstChild), s.style.cssText = "position: absolute; left: 10.7432222px;", o = t(s).offset().left, t.support.offsetFractions = o > 10 && 11 > o, e.innerHTML = "", n.removeChild(e)
        }()
    }(jQuery), function (t) {
        var e = 5;
        t.widget("ui.slider", t.ui.mouse, {
            version: "1.10.3",
            widgetEventPrefix: "slide",
            options: {
                animate: !1,
                distance: 0,
                max: 100,
                min: 0,
                orientation: "horizontal",
                range: !1,
                step: 1,
                value: 0,
                values: null,
                change: null,
                slide: null,
                start: null,
                stop: null
            },
            _create: function () {
                this._keySliding = !1, this._mouseSliding = !1, this._animateOff = !0, this._handleIndex = null, this._detectOrientation(), this._mouseInit(), this.element.addClass("ui-slider ui-slider-" + this.orientation + " ui-widget ui-widget-content ui-corner-all"), this._refresh(), this._setOption("disabled", this.options.disabled), this._animateOff = !1
            },
            _refresh: function () {
                this._createRange(), this._createHandles(), this._setupEvents(), this._refreshValue()
            },
            _createHandles: function () {
                var e, n, i = this.options, o = this.element.find(".ui-slider-handle").addClass("ui-state-default ui-corner-all"), a = "<a class='ui-slider-handle ui-state-default ui-corner-all' href='#'></a>", r = [];
                for (n = i.values && i.values.length || 1, o.length > n && (o.slice(n).remove(), o = o.slice(0, n)), e = o.length; n > e; e++)r.push(a);
                this.handles = o.add(t(r.join("")).appendTo(this.element)), this.handle = this.handles.eq(0), this.handles.each(function (e) {
                    t(this).data("ui-slider-handle-index", e)
                })
            },
            _createRange: function () {
                var e = this.options, n = "";
                e.range ? (e.range === !0 && (e.values ? e.values.length && 2 !== e.values.length ? e.values = [e.values[0], e.values[0]] : t.isArray(e.values) && (e.values = e.values.slice(0)) : e.values = [this._valueMin(), this._valueMin()]), this.range && this.range.length ? this.range.removeClass("ui-slider-range-min ui-slider-range-max").css({
                    left: "",
                    bottom: ""
                }) : (this.range = t("<div></div>").appendTo(this.element), n = "ui-slider-range ui-widget-header ui-corner-all"), this.range.addClass(n + ("min" === e.range || "max" === e.range ? " ui-slider-range-" + e.range : ""))) : this.range = t([])
            },
            _setupEvents: function () {
                var t = this.handles.add(this.range).filter("a");
                this._off(t), this._on(t, this._handleEvents), this._hoverable(t), this._focusable(t)
            },
            _destroy: function () {
                this.handles.remove(), this.range.remove(), this.element.removeClass("ui-slider ui-slider-horizontal ui-slider-vertical ui-widget ui-widget-content ui-corner-all"), this._mouseDestroy()
            },
            _mouseCapture: function (e) {
                var n, i, o, a, r, s, l, u, c = this, d = this.options;
                return d.disabled ? !1 : (this.elementSize = {
                    width: this.element.outerWidth(),
                    height: this.element.outerHeight()
                }, this.elementOffset = this.element.offset(), n = {
                    x: e.pageX,
                    y: e.pageY
                }, i = this._normValueFromMouse(n), o = this._valueMax() - this._valueMin() + 1, this.handles.each(function (e) {
                    var n = Math.abs(i - c.values(e));
                    (o > n || o === n && (e === c._lastChangedValue || c.values(e) === d.min)) && (o = n, a = t(this), r = e)
                }), s = this._start(e, r), s === !1 ? !1 : (this._mouseSliding = !0, this._handleIndex = r, a.addClass("ui-state-active").focus(), l = a.offset(), u = !t(e.target).parents().addBack().is(".ui-slider-handle"), this._clickOffset = u ? {
                    left: 0,
                    top: 0
                } : {
                    left: e.pageX - l.left - a.width() / 2,
                    top: e.pageY - l.top - a.height() / 2 - (parseInt(a.css("borderTopWidth"), 10) || 0) - (parseInt(a.css("borderBottomWidth"), 10) || 0) + (parseInt(a.css("marginTop"), 10) || 0)
                }, this.handles.hasClass("ui-state-hover") || this._slide(e, r, i), this._animateOff = !0, !0))
            },
            _mouseStart: function () {
                return !0
            },
            _mouseDrag: function (t) {
                var e = {x: t.pageX, y: t.pageY}, n = this._normValueFromMouse(e);
                return this._slide(t, this._handleIndex, n), !1
            },
            _mouseStop: function (t) {
                return this.handles.removeClass("ui-state-active"), this._mouseSliding = !1, this._stop(t, this._handleIndex), this._change(t, this._handleIndex), this._handleIndex = null, this._clickOffset = null, this._animateOff = !1, !1
            },
            _detectOrientation: function () {
                this.orientation = "vertical" === this.options.orientation ? "vertical" : "horizontal"
            },
            _normValueFromMouse: function (t) {
                var e, n, i, o, a;
                return "horizontal" === this.orientation ? (e = this.elementSize.width, n = t.x - this.elementOffset.left - (this._clickOffset ? this._clickOffset.left : 0)) : (e = this.elementSize.height, n = t.y - this.elementOffset.top - (this._clickOffset ? this._clickOffset.top : 0)), i = n / e, i > 1 && (i = 1), 0 > i && (i = 0), "vertical" === this.orientation && (i = 1 - i), o = this._valueMax() - this._valueMin(), a = this._valueMin() + i * o, this._trimAlignValue(a)
            },
            _start: function (t, e) {
                var n = {handle: this.handles[e], value: this.value()};
                return this.options.values && this.options.values.length && (n.value = this.values(e), n.values = this.values()), this._trigger("start", t, n)
            },
            _slide: function (t, e, n) {
                var i, o, a;
                this.options.values && this.options.values.length ? (i = this.values(e ? 0 : 1), 2 === this.options.values.length && this.options.range === !0 && (0 === e && n > i || 1 === e && i > n) && (n = i), n !== this.values(e) && (o = this.values(), o[e] = n, a = this._trigger("slide", t, {
                    handle: this.handles[e],
                    value: n,
                    values: o
                }), i = this.values(e ? 0 : 1), a !== !1 && this.values(e, n, !0))) : n !== this.value() && (a = this._trigger("slide", t, {
                    handle: this.handles[e],
                    value: n
                }), a !== !1 && this.value(n))
            },
            _stop: function (t, e) {
                var n = {handle: this.handles[e], value: this.value()};
                this.options.values && this.options.values.length && (n.value = this.values(e), n.values = this.values()), this._trigger("stop", t, n)
            },
            _change: function (t, e) {
                if (!this._keySliding && !this._mouseSliding) {
                    var n = {handle: this.handles[e], value: this.value()};
                    this.options.values && this.options.values.length && (n.value = this.values(e), n.values = this.values()), this._lastChangedValue = e, this._trigger("change", t, n)
                }
            },
            value: function (t) {
                return arguments.length ? (this.options.value = this._trimAlignValue(t), this._refreshValue(), void this._change(null, 0)) : this._value()
            },
            values: function (e, n) {
                var i, o, a;
                if (arguments.length > 1)return this.options.values[e] = this._trimAlignValue(n), this._refreshValue(), void this._change(null, e);
                if (!arguments.length)return this._values();
                if (!t.isArray(arguments[0]))return this.options.values && this.options.values.length ? this._values(e) : this.value();
                for (i = this.options.values, o = arguments[0], a = 0; i.length > a; a += 1)i[a] = this._trimAlignValue(o[a]), this._change(null, a);
                this._refreshValue()
            },
            _setOption: function (e, n) {
                var i, o = 0;
                switch ("range" === e && this.options.range === !0 && ("min" === n ? (this.options.value = this._values(0), this.options.values = null) : "max" === n && (this.options.value = this._values(this.options.values.length - 1), this.options.values = null)), t.isArray(this.options.values) && (o = this.options.values.length), t.Widget.prototype._setOption.apply(this, arguments), e) {
                    case"orientation":
                        this._detectOrientation(), this.element.removeClass("ui-slider-horizontal ui-slider-vertical").addClass("ui-slider-" + this.orientation), this._refreshValue();
                        break;
                    case"value":
                        this._animateOff = !0, this._refreshValue(), this._change(null, 0), this._animateOff = !1;
                        break;
                    case"values":
                        for (this._animateOff = !0, this._refreshValue(), i = 0; o > i; i += 1)this._change(null, i);
                        this._animateOff = !1;
                        break;
                    case"min":
                    case"max":
                        this._animateOff = !0, this._refreshValue(), this._animateOff = !1;
                        break;
                    case"range":
                        this._animateOff = !0, this._refresh(), this._animateOff = !1
                }
            },
            _value: function () {
                var t = this.options.value;
                return t = this._trimAlignValue(t)
            },
            _values: function (t) {
                var e, n, i;
                if (arguments.length)return e = this.options.values[t], e = this._trimAlignValue(e);
                if (this.options.values && this.options.values.length) {
                    for (n = this.options.values.slice(), i = 0; n.length > i; i += 1)n[i] = this._trimAlignValue(n[i]);
                    return n
                }
                return []
            },
            _trimAlignValue: function (t) {
                if (this._valueMin() >= t)return this._valueMin();
                if (t >= this._valueMax())return this._valueMax();
                var e = this.options.step > 0 ? this.options.step : 1, n = (t - this._valueMin()) % e, i = t - n;
                return 2 * Math.abs(n) >= e && (i += n > 0 ? e : -e), parseFloat(i.toFixed(5))
            },
            _valueMin: function () {
                return this.options.min
            },
            _valueMax: function () {
                return this.options.max
            },
            _refreshValue: function () {
                var e, n, i, o, a, r = this.options.range, s = this.options, l = this, u = this._animateOff ? !1 : s.animate, c = {};
                this.options.values && this.options.values.length ? this.handles.each(function (i) {
                    n = 100 * ((l.values(i) - l._valueMin()) / (l._valueMax() - l._valueMin())), c["horizontal" === l.orientation ? "left" : "bottom"] = n + "%", t(this).stop(1, 1)[u ? "animate" : "css"](c, s.animate), l.options.range === !0 && ("horizontal" === l.orientation ? (0 === i && l.range.stop(1, 1)[u ? "animate" : "css"]({left: n + "%"}, s.animate), 1 === i && l.range[u ? "animate" : "css"]({width: n - e + "%"}, {
                        queue: !1,
                        duration: s.animate
                    })) : (0 === i && l.range.stop(1, 1)[u ? "animate" : "css"]({bottom: n + "%"}, s.animate), 1 === i && l.range[u ? "animate" : "css"]({height: n - e + "%"}, {
                        queue: !1,
                        duration: s.animate
                    }))), e = n
                }) : (i = this.value(), o = this._valueMin(), a = this._valueMax(), n = a !== o ? 100 * ((i - o) / (a - o)) : 0, c["horizontal" === this.orientation ? "left" : "bottom"] = n + "%", this.handle.stop(1, 1)[u ? "animate" : "css"](c, s.animate), "min" === r && "horizontal" === this.orientation && this.range.stop(1, 1)[u ? "animate" : "css"]({width: n + "%"}, s.animate), "max" === r && "horizontal" === this.orientation && this.range[u ? "animate" : "css"]({width: 100 - n + "%"}, {
                    queue: !1,
                    duration: s.animate
                }), "min" === r && "vertical" === this.orientation && this.range.stop(1, 1)[u ? "animate" : "css"]({height: n + "%"}, s.animate), "max" === r && "vertical" === this.orientation && this.range[u ? "animate" : "css"]({height: 100 - n + "%"}, {
                    queue: !1,
                    duration: s.animate
                }))
            },
            _handleEvents: {
                keydown: function (n) {
                    var i, o, a, r, s = t(n.target).data("ui-slider-handle-index");
                    switch (n.keyCode) {
                        case t.ui.keyCode.HOME:
                        case t.ui.keyCode.END:
                        case t.ui.keyCode.PAGE_UP:
                        case t.ui.keyCode.PAGE_DOWN:
                        case t.ui.keyCode.UP:
                        case t.ui.keyCode.RIGHT:
                        case t.ui.keyCode.DOWN:
                        case t.ui.keyCode.LEFT:
                            if (n.preventDefault(), !this._keySliding && (this._keySliding = !0, t(n.target).addClass("ui-state-active"), i = this._start(n, s), i === !1))return
                    }
                    switch (r = this.options.step, o = a = this.options.values && this.options.values.length ? this.values(s) : this.value(), n.keyCode) {
                        case t.ui.keyCode.HOME:
                            a = this._valueMin();
                            break;
                        case t.ui.keyCode.END:
                            a = this._valueMax();
                            break;
                        case t.ui.keyCode.PAGE_UP:
                            a = this._trimAlignValue(o + (this._valueMax() - this._valueMin()) / e);
                            break;
                        case t.ui.keyCode.PAGE_DOWN:
                            a = this._trimAlignValue(o - (this._valueMax() - this._valueMin()) / e);
                            break;
                        case t.ui.keyCode.UP:
                        case t.ui.keyCode.RIGHT:
                            if (o === this._valueMax())return;
                            a = this._trimAlignValue(o + r);
                            break;
                        case t.ui.keyCode.DOWN:
                        case t.ui.keyCode.LEFT:
                            if (o === this._valueMin())return;
                            a = this._trimAlignValue(o - r)
                    }
                    this._slide(n, s, a)
                }, click: function (t) {
                    t.preventDefault()
                }, keyup: function (e) {
                    var n = t(e.target).data("ui-slider-handle-index");
                    this._keySliding && (this._keySliding = !1, this._stop(e, n), this._change(e, n), t(e.target).removeClass("ui-state-active"))
                }
            }
        })
    }(jQuery), function (t) {
        function e(e, n) {
            var i = (e.attr("aria-describedby") || "").split(/\s+/);
            i.push(n), e.data("ui-tooltip-id", n).attr("aria-describedby", t.trim(i.join(" ")))
        }

        function n(e) {
            var n = e.data("ui-tooltip-id"), i = (e.attr("aria-describedby") || "").split(/\s+/), o = t.inArray(n, i);
            -1 !== o && i.splice(o, 1), e.removeData("ui-tooltip-id"), i = t.trim(i.join(" ")), i ? e.attr("aria-describedby", i) : e.removeAttr("aria-describedby")
        }

        var i = 0;
        t.widget("ui.tooltip", {
            version: "1.10.3", options: {
                content: function () {
                    var e = t(this).attr("title") || "";
                    return t("<a>").text(e).html()
                },
                hide: !0,
                items: "[title]:not([disabled])",
                position: {my: "left top+15", at: "left bottom", collision: "flipfit flip"},
                show: !0,
                tooltipClass: null,
                track: !1,
                close: null,
                open: null
            }, _create: function () {
                this._on({
                    mouseover: "open",
                    focusin: "open"
                }), this.tooltips = {}, this.parents = {}, this.options.disabled && this._disable()
            }, _setOption: function (e, n) {
                var i = this;
                return "disabled" === e ? (this[n ? "_disable" : "_enable"](), void(this.options[e] = n)) : (this._super(e, n), void("content" === e && t.each(this.tooltips, function (t, e) {
                    i._updateContent(e)
                })))
            }, _disable: function () {
                var e = this;
                t.each(this.tooltips, function (n, i) {
                    var o = t.Event("blur");
                    o.target = o.currentTarget = i[0], e.close(o, !0)
                }), this.element.find(this.options.items).addBack().each(function () {
                    var e = t(this);
                    e.is("[title]") && e.data("ui-tooltip-title", e.attr("title")).attr("title", "")
                })
            }, _enable: function () {
                this.element.find(this.options.items).addBack().each(function () {
                    var e = t(this);
                    e.data("ui-tooltip-title") && e.attr("title", e.data("ui-tooltip-title"))
                })
            }, open: function (e) {
                var n = this, i = t(e ? e.target : this.element).closest(this.options.items);
                i.length && !i.data("ui-tooltip-id") && (i.attr("title") && i.data("ui-tooltip-title", i.attr("title")), i.data("ui-tooltip-open", !0), e && "mouseover" === e.type && i.parents().each(function () {
                    var e, i = t(this);
                    i.data("ui-tooltip-open") && (e = t.Event("blur"), e.target = e.currentTarget = this, n.close(e, !0)), i.attr("title") && (i.uniqueId(), n.parents[this.id] = {
                        element: this,
                        title: i.attr("title")
                    }, i.attr("title", ""))
                }), this._updateContent(i, e))
            }, _updateContent: function (t, e) {
                var n, i = this.options.content, o = this, a = e ? e.type : null;
                return "string" == typeof i ? this._open(e, t, i) : (n = i.call(t[0], function (n) {
                    t.data("ui-tooltip-open") && o._delay(function () {
                        e && (e.type = a), this._open(e, t, n)
                    })
                }), void(n && this._open(e, t, n)))
            }, _open: function (n, i, o) {
                function a(t) {
                    u.of = t, r.is(":hidden") || r.position(u)
                }

                var r, s, l, u = t.extend({}, this.options.position);
                if (o) {
                    if (r = this._find(i), r.length)return void r.find(".ui-tooltip-content").html(o);
                    i.is("[title]") && (n && "mouseover" === n.type ? i.attr("title", "") : i.removeAttr("title")), r = this._tooltip(i), e(i, r.attr("id")), r.find(".ui-tooltip-content").html(o), this.options.track && n && /^mouse/.test(n.type) ? (this._on(this.document, {mousemove: a}), a(n)) : r.position(t.extend({of: i}, this.options.position)), r.hide(), this._show(r, this.options.show), this.options.show && this.options.show.delay && (l = this.delayedShow = setInterval(function () {
                        r.is(":visible") && (a(u.of), clearInterval(l))
                    }, t.fx.interval)), this._trigger("open", n, {tooltip: r}), s = {
                        keyup: function (e) {
                            if (e.keyCode === t.ui.keyCode.ESCAPE) {
                                var n = t.Event(e);
                                n.currentTarget = i[0], this.close(n, !0)
                            }
                        }, remove: function () {
                            this._removeTooltip(r)
                        }
                    }, n && "mouseover" !== n.type || (s.mouseleave = "close"), n && "focusin" !== n.type || (s.focusout = "close"), this._on(!0, i, s)
                }
            }, close: function (e) {
                var i = this, o = t(e ? e.currentTarget : this.element), a = this._find(o);
                this.closing || (clearInterval(this.delayedShow), o.data("ui-tooltip-title") && o.attr("title", o.data("ui-tooltip-title")), n(o), a.stop(!0), this._hide(a, this.options.hide, function () {
                    i._removeTooltip(t(this))
                }), o.removeData("ui-tooltip-open"), this._off(o, "mouseleave focusout keyup"), o[0] !== this.element[0] && this._off(o, "remove"), this._off(this.document, "mousemove"), e && "mouseleave" === e.type && t.each(this.parents, function (e, n) {
                    t(n.element).attr("title", n.title), delete i.parents[e]
                }), this.closing = !0, this._trigger("close", e, {tooltip: a}), this.closing = !1)
            }, _tooltip: function (e) {
                var n = "ui-tooltip-" + i++, o = t("<div>").attr({
                    id: n,
                    role: "tooltip"
                }).addClass("ui-tooltip ui-widget ui-corner-all ui-widget-content " + (this.options.tooltipClass || ""));
                return t("<div>").addClass("ui-tooltip-content").appendTo(o), o.appendTo(this.document[0].body), this.tooltips[n] = e, o
            }, _find: function (e) {
                var n = e.data("ui-tooltip-id");
                return n ? t("#" + n) : t()
            }, _removeTooltip: function (t) {
                t.remove(), delete this.tooltips[t.attr("id")]
            }, _destroy: function () {
                var e = this;
                t.each(this.tooltips, function (n, i) {
                    var o = t.Event("blur");
                    o.target = o.currentTarget = i[0], e.close(o, !0), t("#" + n).remove(), i.data("ui-tooltip-title") && (i.attr("title", i.data("ui-tooltip-title")), i.removeData("ui-tooltip-title"))
                })
            }
        })
    }(jQuery), function (t, e) {
        var n = "ui-effects-";
        t.effects = {effect: {}}, function (t, e) {
            function n(t, e, n) {
                var i = d[e.type] || {};
                return null == t ? n || !e.def ? null : e.def : (t = i.floor ? ~~t : parseFloat(t), isNaN(t) ? e.def : i.mod ? (t + i.mod) % i.mod : 0 > t ? 0 : t > i.max ? i.max : t)
            }

            function i(n) {
                var i = u(), o = i._rgba = [];
                return n = n.toLowerCase(), p(l, function (t, a) {
                    var r, s = a.re.exec(n), l = s && a.parse(s), u = a.space || "rgba";
                    return l ? (r = i[u](l), i[c[u].cache] = r[c[u].cache], o = i._rgba = r._rgba, !1) : e
                }), o.length ? ("0,0,0,0" === o.join() && t.extend(o, a.transparent), i) : a[n]
            }

            function o(t, e, n) {
                return n = (n + 1) % 1, 1 > 6 * n ? t + 6 * (e - t) * n : 1 > 2 * n ? e : 2 > 3 * n ? t + 6 * (e - t) * (2 / 3 - n) : t
            }

            var a, r = "backgroundColor borderBottomColor borderLeftColor borderRightColor borderTopColor color columnRuleColor outlineColor textDecorationColor textEmphasisColor", s = /^([\-+])=\s*(\d+\.?\d*)/, l = [{
                re: /rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
                parse: function (t) {
                    return [t[1], t[2], t[3], t[4]]
                }
            }, {
                re: /rgba?\(\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
                parse: function (t) {
                    return [2.55 * t[1], 2.55 * t[2], 2.55 * t[3], t[4]]
                }
            }, {
                re: /#([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})/, parse: function (t) {
                    return [parseInt(t[1], 16), parseInt(t[2], 16), parseInt(t[3], 16)]
                }
            }, {
                re: /#([a-f0-9])([a-f0-9])([a-f0-9])/, parse: function (t) {
                    return [parseInt(t[1] + t[1], 16), parseInt(t[2] + t[2], 16), parseInt(t[3] + t[3], 16)]
                }
            }, {
                re: /hsla?\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
                space: "hsla",
                parse: function (t) {
                    return [t[1], t[2] / 100, t[3] / 100, t[4]]
                }
            }], u = t.Color = function (e, n, i, o) {
                return new t.Color.fn.parse(e, n, i, o)
            }, c = {
                rgba: {
                    props: {
                        red: {idx: 0, type: "byte"},
                        green: {idx: 1, type: "byte"},
                        blue: {idx: 2, type: "byte"}
                    }
                },
                hsla: {
                    props: {
                        hue: {idx: 0, type: "degrees"},
                        saturation: {idx: 1, type: "percent"},
                        lightness: {idx: 2, type: "percent"}
                    }
                }
            }, d = {
                "byte": {floor: !0, max: 255},
                percent: {max: 1},
                degrees: {mod: 360, floor: !0}
            }, h = u.support = {}, f = t("<p>")[0], p = t.each;
            f.style.cssText = "background-color:rgba(1,1,1,.5)", h.rgba = f.style.backgroundColor.indexOf("rgba") > -1, p(c, function (t, e) {
                e.cache = "_" + t, e.props.alpha = {idx: 3, type: "percent", def: 1}
            }), u.fn = t.extend(u.prototype, {
                parse: function (o, r, s, l) {
                    if (o === e)return this._rgba = [null, null, null, null], this;
                    (o.jquery || o.nodeType) && (o = t(o).css(r), r = e);
                    var d = this, h = t.type(o), f = this._rgba = [];
                    return r !== e && (o = [o, r, s, l], h = "array"), "string" === h ? this.parse(i(o) || a._default) : "array" === h ? (p(c.rgba.props, function (t, e) {
                        f[e.idx] = n(o[e.idx], e)
                    }), this) : "object" === h ? (o instanceof u ? p(c, function (t, e) {
                        o[e.cache] && (d[e.cache] = o[e.cache].slice())
                    }) : p(c, function (e, i) {
                        var a = i.cache;
                        p(i.props, function (t, e) {
                            if (!d[a] && i.to) {
                                if ("alpha" === t || null == o[t])return;
                                d[a] = i.to(d._rgba)
                            }
                            d[a][e.idx] = n(o[t], e, !0)
                        }), d[a] && 0 > t.inArray(null, d[a].slice(0, 3)) && (d[a][3] = 1, i.from && (d._rgba = i.from(d[a])))
                    }), this) : e
                }, is: function (t) {
                    var n = u(t), i = !0, o = this;
                    return p(c, function (t, a) {
                        var r, s = n[a.cache];
                        return s && (r = o[a.cache] || a.to && a.to(o._rgba) || [], p(a.props, function (t, n) {
                            return null != s[n.idx] ? i = s[n.idx] === r[n.idx] : e
                        })), i
                    }), i
                }, _space: function () {
                    var t = [], e = this;
                    return p(c, function (n, i) {
                        e[i.cache] && t.push(n)
                    }), t.pop()
                }, transition: function (t, e) {
                    var i = u(t), o = i._space(), a = c[o], r = 0 === this.alpha() ? u("transparent") : this, s = r[a.cache] || a.to(r._rgba), l = s.slice();
                    return i = i[a.cache], p(a.props, function (t, o) {
                        var a = o.idx, r = s[a], u = i[a], c = d[o.type] || {};
                        null !== u && (null === r ? l[a] = u : (c.mod && (u - r > c.mod / 2 ? r += c.mod : r - u > c.mod / 2 && (r -= c.mod)), l[a] = n((u - r) * e + r, o)))
                    }), this[o](l)
                }, blend: function (e) {
                    if (1 === this._rgba[3])return this;
                    var n = this._rgba.slice(), i = n.pop(), o = u(e)._rgba;
                    return u(t.map(n, function (t, e) {
                        return (1 - i) * o[e] + i * t
                    }))
                }, toRgbaString: function () {
                    var e = "rgba(", n = t.map(this._rgba, function (t, e) {
                        return null == t ? e > 2 ? 1 : 0 : t
                    });
                    return 1 === n[3] && (n.pop(), e = "rgb("), e + n.join() + ")"
                }, toHslaString: function () {
                    var e = "hsla(", n = t.map(this.hsla(), function (t, e) {
                        return null == t && (t = e > 2 ? 1 : 0), e && 3 > e && (t = Math.round(100 * t) + "%"), t
                    });
                    return 1 === n[3] && (n.pop(), e = "hsl("), e + n.join() + ")"
                }, toHexString: function (e) {
                    var n = this._rgba.slice(), i = n.pop();
                    return e && n.push(~~(255 * i)), "#" + t.map(n, function (t) {
                        return t = (t || 0).toString(16), 1 === t.length ? "0" + t : t
                    }).join("")
                }, toString: function () {
                    return 0 === this._rgba[3] ? "transparent" : this.toRgbaString()
                }
            }), u.fn.parse.prototype = u.fn, c.hsla.to = function (t) {
                if (null == t[0] || null == t[1] || null == t[2])return [null, null, null, t[3]];
                var e, n, i = t[0] / 255, o = t[1] / 255, a = t[2] / 255, r = t[3], s = Math.max(i, o, a), l = Math.min(i, o, a), u = s - l, c = s + l, d = .5 * c;
                return e = l === s ? 0 : i === s ? 60 * (o - a) / u + 360 : o === s ? 60 * (a - i) / u + 120 : 60 * (i - o) / u + 240, n = 0 === u ? 0 : .5 >= d ? u / c : u / (2 - c), [Math.round(e) % 360, n, d, null == r ? 1 : r]
            }, c.hsla.from = function (t) {
                if (null == t[0] || null == t[1] || null == t[2])return [null, null, null, t[3]];
                var e = t[0] / 360, n = t[1], i = t[2], a = t[3], r = .5 >= i ? i * (1 + n) : i + n - i * n, s = 2 * i - r;
                return [Math.round(255 * o(s, r, e + 1 / 3)), Math.round(255 * o(s, r, e)), Math.round(255 * o(s, r, e - 1 / 3)), a]
            }, p(c, function (i, o) {
                var a = o.props, r = o.cache, l = o.to, c = o.from;
                u.fn[i] = function (i) {
                    if (l && !this[r] && (this[r] = l(this._rgba)), i === e)return this[r].slice();
                    var o, s = t.type(i), d = "array" === s || "object" === s ? i : arguments, h = this[r].slice();
                    return p(a, function (t, e) {
                        var i = d["object" === s ? t : e.idx];
                        null == i && (i = h[e.idx]), h[e.idx] = n(i, e)
                    }), c ? (o = u(c(h)), o[r] = h, o) : u(h)
                }, p(a, function (e, n) {
                    u.fn[e] || (u.fn[e] = function (o) {
                        var a, r = t.type(o), l = "alpha" === e ? this._hsla ? "hsla" : "rgba" : i, u = this[l](), c = u[n.idx];
                        return "undefined" === r ? c : ("function" === r && (o = o.call(this, c), r = t.type(o)), null == o && n.empty ? this : ("string" === r && (a = s.exec(o), a && (o = c + parseFloat(a[2]) * ("+" === a[1] ? 1 : -1))), u[n.idx] = o, this[l](u)))
                    })
                })
            }), u.hook = function (e) {
                var n = e.split(" ");
                p(n, function (e, n) {
                    t.cssHooks[n] = {
                        set: function (e, o) {
                            var a, r, s = "";
                            if ("transparent" !== o && ("string" !== t.type(o) || (a = i(o)))) {
                                if (o = u(a || o), !h.rgba && 1 !== o._rgba[3]) {
                                    for (r = "backgroundColor" === n ? e.parentNode : e; ("" === s || "transparent" === s) && r && r.style;)try {
                                        s = t.css(r, "backgroundColor"), r = r.parentNode
                                    } catch (l) {
                                    }
                                    o = o.blend(s && "transparent" !== s ? s : "_default")
                                }
                                o = o.toRgbaString()
                            }
                            try {
                                e.style[n] = o
                            } catch (l) {
                            }
                        }
                    }, t.fx.step[n] = function (e) {
                        e.colorInit || (e.start = u(e.elem, n), e.end = u(e.end), e.colorInit = !0), t.cssHooks[n].set(e.elem, e.start.transition(e.end, e.pos))
                    }
                })
            }, u.hook(r), t.cssHooks.borderColor = {
                expand: function (t) {
                    var e = {};
                    return p(["Top", "Right", "Bottom", "Left"], function (n, i) {
                        e["border" + i + "Color"] = t
                    }), e
                }
            }, a = t.Color.names = {
                aqua: "#00ffff",
                black: "#000000",
                blue: "#0000ff",
                fuchsia: "#ff00ff",
                gray: "#808080",
                green: "#008000",
                lime: "#00ff00",
                maroon: "#800000",
                navy: "#000080",
                olive: "#808000",
                purple: "#800080",
                red: "#ff0000",
                silver: "#c0c0c0",
                teal: "#008080",
                white: "#ffffff",
                yellow: "#ffff00",
                transparent: [null, null, null, 0],
                _default: "#ffffff"
            }
        }(jQuery), function () {
            function n(e) {
                var n, i, o = e.ownerDocument.defaultView ? e.ownerDocument.defaultView.getComputedStyle(e, null) : e.currentStyle, a = {};
                if (o && o.length && o[0] && o[o[0]])for (i = o.length; i--;)n = o[i], "string" == typeof o[n] && (a[t.camelCase(n)] = o[n]); else for (n in o)"string" == typeof o[n] && (a[n] = o[n]);
                return a
            }

            function i(e, n) {
                var i, o, r = {};
                for (i in n)o = n[i], e[i] !== o && (a[i] || (t.fx.step[i] || !isNaN(parseFloat(o))) && (r[i] = o));
                return r
            }

            var o = ["add", "remove", "toggle"], a = {
                border: 1,
                borderBottom: 1,
                borderColor: 1,
                borderLeft: 1,
                borderRight: 1,
                borderTop: 1,
                borderWidth: 1,
                margin: 1,
                padding: 1
            };
            t.each(["borderLeftStyle", "borderRightStyle", "borderBottomStyle", "borderTopStyle"], function (e, n) {
                t.fx.step[n] = function (t) {
                    ("none" !== t.end && !t.setAttr || 1 === t.pos && !t.setAttr) && (jQuery.style(t.elem, n, t.end), t.setAttr = !0)
                }
            }), t.fn.addBack || (t.fn.addBack = function (t) {
                return this.add(null == t ? this.prevObject : this.prevObject.filter(t))
            }), t.effects.animateClass = function (e, a, r, s) {
                var l = t.speed(a, r, s);
                return this.queue(function () {
                    var a, r = t(this), s = r.attr("class") || "", u = l.children ? r.find("*").addBack() : r;
                    u = u.map(function () {
                        var e = t(this);
                        return {el: e, start: n(this)}
                    }), a = function () {
                        t.each(o, function (t, n) {
                            e[n] && r[n + "Class"](e[n])
                        })
                    }, a(), u = u.map(function () {
                        return this.end = n(this.el[0]), this.diff = i(this.start, this.end), this
                    }), r.attr("class", s), u = u.map(function () {
                        var e = this, n = t.Deferred(), i = t.extend({}, l, {
                            queue: !1, complete: function () {
                                n.resolve(e)
                            }
                        });
                        return this.el.animate(this.diff, i), n.promise()
                    }), t.when.apply(t, u.get()).done(function () {
                        a(), t.each(arguments, function () {
                            var e = this.el;
                            t.each(this.diff, function (t) {
                                e.css(t, "")
                            })
                        }), l.complete.call(r[0])
                    })
                })
            }, t.fn.extend({
                addClass: function (e) {
                    return function (n, i, o, a) {
                        return i ? t.effects.animateClass.call(this, {add: n}, i, o, a) : e.apply(this, arguments)
                    }
                }(t.fn.addClass), removeClass: function (e) {
                    return function (n, i, o, a) {
                        return arguments.length > 1 ? t.effects.animateClass.call(this, {remove: n}, i, o, a) : e.apply(this, arguments)
                    }
                }(t.fn.removeClass), toggleClass: function (n) {
                    return function (i, o, a, r, s) {
                        return "boolean" == typeof o || o === e ? a ? t.effects.animateClass.call(this, o ? {add: i} : {remove: i}, a, r, s) : n.apply(this, arguments) : t.effects.animateClass.call(this, {toggle: i}, o, a, r)
                    }
                }(t.fn.toggleClass), switchClass: function (e, n, i, o, a) {
                    return t.effects.animateClass.call(this, {add: n, remove: e}, i, o, a)
                }
            })
        }(), function () {
            function i(e, n, i, o) {
                return t.isPlainObject(e) && (n = e, e = e.effect), e = {effect: e}, null == n && (n = {}), t.isFunction(n) && (o = n, i = null, n = {}), ("number" == typeof n || t.fx.speeds[n]) && (o = i, i = n, n = {}), t.isFunction(i) && (o = i, i = null), n && t.extend(e, n), i = i || n.duration, e.duration = t.fx.off ? 0 : "number" == typeof i ? i : i in t.fx.speeds ? t.fx.speeds[i] : t.fx.speeds._default, e.complete = o || n.complete, e
            }

            function o(e) {
                return !e || "number" == typeof e || t.fx.speeds[e] ? !0 : "string" != typeof e || t.effects.effect[e] ? t.isFunction(e) ? !0 : "object" != typeof e || e.effect ? !1 : !0 : !0
            }

            t.extend(t.effects, {
                version: "1.10.3", save: function (t, e) {
                    for (var i = 0; e.length > i; i++)null !== e[i] && t.data(n + e[i], t[0].style[e[i]])
                }, restore: function (t, i) {
                    var o, a;
                    for (a = 0; i.length > a; a++)null !== i[a] && (o = t.data(n + i[a]), o === e && (o = ""), t.css(i[a], o))
                }, setMode: function (t, e) {
                    return "toggle" === e && (e = t.is(":hidden") ? "show" : "hide"), e
                }, getBaseline: function (t, e) {
                    var n, i;
                    switch (t[0]) {
                        case"top":
                            n = 0;
                            break;
                        case"middle":
                            n = .5;
                            break;
                        case"bottom":
                            n = 1;
                            break;
                        default:
                            n = t[0] / e.height
                    }
                    switch (t[1]) {
                        case"left":
                            i = 0;
                            break;
                        case"center":
                            i = .5;
                            break;
                        case"right":
                            i = 1;
                            break;
                        default:
                            i = t[1] / e.width
                    }
                    return {x: i, y: n}
                }, createWrapper: function (e) {
                    if (e.parent().is(".ui-effects-wrapper"))return e.parent();
                    var n = {
                        width: e.outerWidth(!0),
                        height: e.outerHeight(!0),
                        "float": e.css("float")
                    }, i = t("<div></div>").addClass("ui-effects-wrapper").css({
                        fontSize: "100%",
                        background: "transparent",
                        border: "none",
                        margin: 0,
                        padding: 0
                    }), o = {width: e.width(), height: e.height()}, a = document.activeElement;
                    try {
                        a.id
                    } catch (r) {
                        a = document.body
                    }
                    return e.wrap(i), (e[0] === a || t.contains(e[0], a)) && t(a).focus(), i = e.parent(), "static" === e.css("position") ? (i.css({position: "relative"}), e.css({position: "relative"})) : (t.extend(n, {
                        position: e.css("position"),
                        zIndex: e.css("z-index")
                    }), t.each(["top", "left", "bottom", "right"], function (t, i) {
                        n[i] = e.css(i), isNaN(parseInt(n[i], 10)) && (n[i] = "auto")
                    }), e.css({
                        position: "relative",
                        top: 0,
                        left: 0,
                        right: "auto",
                        bottom: "auto"
                    })), e.css(o), i.css(n).show()
                }, removeWrapper: function (e) {
                    var n = document.activeElement;
                    return e.parent().is(".ui-effects-wrapper") && (e.parent().replaceWith(e), (e[0] === n || t.contains(e[0], n)) && t(n).focus()), e
                }, setTransition: function (e, n, i, o) {
                    return o = o || {}, t.each(n, function (t, n) {
                        var a = e.cssUnit(n);
                        a[0] > 0 && (o[n] = a[0] * i + a[1])
                    }), o
                }
            }), t.fn.extend({
                effect: function () {
                    function e(e) {
                        function i() {
                            t.isFunction(a) && a.call(o[0]), t.isFunction(e) && e()
                        }

                        var o = t(this), a = n.complete, s = n.mode;
                        (o.is(":hidden") ? "hide" === s : "show" === s) ? (o[s](), i()) : r.call(o[0], n, i)
                    }

                    var n = i.apply(this, arguments), o = n.mode, a = n.queue, r = t.effects.effect[n.effect];
                    return t.fx.off || !r ? o ? this[o](n.duration, n.complete) : this.each(function () {
                        n.complete && n.complete.call(this)
                    }) : a === !1 ? this.each(e) : this.queue(a || "fx", e)
                }, show: function (t) {
                    return function (e) {
                        if (o(e))return t.apply(this, arguments);
                        var n = i.apply(this, arguments);
                        return n.mode = "show", this.effect.call(this, n)
                    }
                }(t.fn.show), hide: function (t) {
                    return function (e) {
                        if (o(e))return t.apply(this, arguments);
                        var n = i.apply(this, arguments);
                        return n.mode = "hide", this.effect.call(this, n)
                    }
                }(t.fn.hide), toggle: function (t) {
                    return function (e) {
                        if (o(e) || "boolean" == typeof e)return t.apply(this, arguments);
                        var n = i.apply(this, arguments);
                        return n.mode = "toggle", this.effect.call(this, n)
                    }
                }(t.fn.toggle), cssUnit: function (e) {
                    var n = this.css(e), i = [];
                    return t.each(["em", "px", "%", "pt"], function (t, e) {
                        n.indexOf(e) > 0 && (i = [parseFloat(n), e])
                    }), i
                }
            })
        }(), function () {
            var e = {};
            t.each(["Quad", "Cubic", "Quart", "Quint", "Expo"], function (t, n) {
                e[n] = function (e) {
                    return Math.pow(e, t + 2)
                }
            }), t.extend(e, {
                Sine: function (t) {
                    return 1 - Math.cos(t * Math.PI / 2)
                }, Circ: function (t) {
                    return 1 - Math.sqrt(1 - t * t)
                }, Elastic: function (t) {
                    return 0 === t || 1 === t ? t : -Math.pow(2, 8 * (t - 1)) * Math.sin((80 * (t - 1) - 7.5) * Math.PI / 15)
                }, Back: function (t) {
                    return t * t * (3 * t - 2)
                }, Bounce: function (t) {
                    for (var e, n = 4; ((e = Math.pow(2, --n)) - 1) / 11 > t;);
                    return 1 / Math.pow(4, 3 - n) - 7.5625 * Math.pow((3 * e - 2) / 22 - t, 2)
                }
            }), t.each(e, function (e, n) {
                t.easing["easeIn" + e] = n, t.easing["easeOut" + e] = function (t) {
                    return 1 - n(1 - t)
                }, t.easing["easeInOut" + e] = function (t) {
                    return .5 > t ? n(2 * t) / 2 : 1 - n(-2 * t + 2) / 2
                }
            })
        }()
    }(jQuery), function (t) {
        function e(t, e) {
            if (!(t.originalEvent.touches.length > 1)) {
                t.preventDefault();
                var n = t.originalEvent.changedTouches[0], i = document.createEvent("MouseEvents");
                i.initMouseEvent(e, !0, !0, window, 1, n.screenX, n.screenY, n.clientX, n.clientY, !1, !1, !1, !1, 0, null), t.target.dispatchEvent(i)
            }
        }

        if (t.support.touch = "ontouchend" in document, t.support.touch) {
            var n, i = t.ui.mouse.prototype, o = i._mouseInit;
            i._touchStart = function (t) {
                var i = this;
                !n && i._mouseCapture(t.originalEvent.changedTouches[0]) && (n = !0, i._touchMoved = !1, e(t, "mouseover"), e(t, "mousemove"), e(t, "mousedown"))
            }, i._touchMove = function (t) {
                n && (this._touchMoved = !0, e(t, "mousemove"))
            }, i._touchEnd = function (t) {
                n && (e(t, "mouseup"), e(t, "mouseout"), this._touchMoved || e(t, "click"), n = !1)
            }, i._mouseInit = function () {
                var e = this;
                e.element.bind("touchstart", t.proxy(e, "_touchStart")).bind("touchmove", t.proxy(e, "_touchMove")).bind("touchend", t.proxy(e, "_touchEnd")), o.call(e)
            }
        }
    }(jQuery), "undefined" == typeof jQuery)throw new Error("Bootstrap requires jQuery");
+function (t) {
    "use strict";
    function e() {
        var t = document.createElement("bootstrap"), e = {
            WebkitTransition: "webkitTransitionEnd",
            MozTransition: "transitionend",
            OTransition: "oTransitionEnd otransitionend",
            transition: "transitionend"
        };
        for (var n in e)if (void 0 !== t.style[n])return {end: e[n]}
    }

    t.fn.emulateTransitionEnd = function (e) {
        var n = !1, i = this;
        t(this).one(t.support.transition.end, function () {
            n = !0
        });
        var o = function () {
            n || t(i).trigger(t.support.transition.end)
        };
        return setTimeout(o, e), this
    }, t(function () {
        t.support.transition = e()
    })
}(window.jQuery), +function (t) {
    "use strict";
    var e = '[data-dismiss="alert"]', n = function (n) {
        t(n).on("click", e, this.close)
    };
    n.prototype.close = function (e) {
        function n() {
            a.trigger("closed.bs.alert").remove()
        }

        var i = t(this), o = i.attr("data-target");
        o || (o = i.attr("href"), o = o && o.replace(/.*(?=#[^\s]*$)/, ""));
        var a = t(o);
        e && e.preventDefault(), a.length || (a = i.hasClass("alert") ? i : i.parent()), a.trigger(e = t.Event("close.bs.alert")), e.isDefaultPrevented() || (a.removeClass("in"), t.support.transition && a.hasClass("fade") ? a.one(t.support.transition.end, n).emulateTransitionEnd(150) : n())
    };
    var i = t.fn.alert;
    t.fn.alert = function (e) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.alert");
            o || i.data("bs.alert", o = new n(this)), "string" == typeof e && o[e].call(i)
        })
    }, t.fn.alert.Constructor = n, t.fn.alert.noConflict = function () {
        return t.fn.alert = i, this
    }, t(document).on("click.bs.alert.data-api", e, n.prototype.close)
}(window.jQuery), +function (t) {
    "use strict";
    var e = function (n, i) {
        this.$element = t(n), this.options = t.extend({}, e.DEFAULTS, i)
    };
    e.DEFAULTS = {loadingText: "loading..."}, e.prototype.setState = function (t) {
        var e = "disabled", n = this.$element, i = n.is("input") ? "val" : "html", o = n.data();
        t += "Text", o.resetText || n.data("resetText", n[i]()), n[i](o[t] || this.options[t]), setTimeout(function () {
            "loadingText" == t ? n.addClass(e).attr(e, e) : n.removeClass(e).removeAttr(e)
        }, 0)
    }, e.prototype.toggle = function () {
        var t = this.$element.closest('[data-toggle="buttons"]');
        if (t.length) {
            var e = this.$element.find("input").prop("checked", !this.$element.hasClass("active")).trigger("change");
            "radio" === e.prop("type") && t.find(".active").removeClass("active")
        }
        this.$element.toggleClass("active")
    };
    var n = t.fn.button;
    t.fn.button = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.button"), a = "object" == typeof n && n;
            o || i.data("bs.button", o = new e(this, a)), "toggle" == n ? o.toggle() : n && o.setState(n)
        })
    }, t.fn.button.Constructor = e, t.fn.button.noConflict = function () {
        return t.fn.button = n, this
    }, t(document).on("click.bs.button.data-api", "[data-toggle^=button]", function (e) {
        var n = t(e.target);
        n.hasClass("btn") || (n = n.closest(".btn")), n.button("toggle"), e.preventDefault()
    })
}(window.jQuery), +function (t) {
    "use strict";
    var e = function (e, n) {
        this.$element = t(e), this.$indicators = this.$element.find(".carousel-indicators"), this.options = n, this.paused = this.sliding = this.interval = this.$active = this.$items = null, "hover" == this.options.pause && this.$element.on("mouseenter", t.proxy(this.pause, this)).on("mouseleave", t.proxy(this.cycle, this))
    };
    e.DEFAULTS = {interval: 5e3, pause: "hover", wrap: !0}, e.prototype.cycle = function (e) {
        return e || (this.paused = !1), this.interval && clearInterval(this.interval), this.options.interval && !this.paused && (this.interval = setInterval(t.proxy(this.next, this), this.options.interval)), this
    }, e.prototype.getActiveIndex = function () {
        return this.$active = this.$element.find(".item.active"), this.$items = this.$active.parent().children(), this.$items.index(this.$active)
    }, e.prototype.to = function (e) {
        var n = this, i = this.getActiveIndex();
        return e > this.$items.length - 1 || 0 > e ? void 0 : this.sliding ? this.$element.one("slid", function () {
            n.to(e)
        }) : i == e ? this.pause().cycle() : this.slide(e > i ? "next" : "prev", t(this.$items[e]))
    }, e.prototype.pause = function (e) {
        return e || (this.paused = !0), this.$element.find(".next, .prev").length && t.support.transition.end && (this.$element.trigger(t.support.transition.end), this.cycle(!0)), this.interval = clearInterval(this.interval), this
    }, e.prototype.next = function () {
        return this.sliding ? void 0 : this.slide("next")
    }, e.prototype.prev = function () {
        return this.sliding ? void 0 : this.slide("prev")
    }, e.prototype.slide = function (e, n) {
        var i = this.$element.find(".item.active"), o = n || i[e](), a = this.interval, r = "next" == e ? "left" : "right", s = "next" == e ? "first" : "last", l = this;
        if (!o.length) {
            if (!this.options.wrap)return;
            o = this.$element.find(".item")[s]()
        }
        this.sliding = !0, a && this.pause();
        var u = t.Event("slide.bs.carousel", {relatedTarget: o[0], direction: r});
        if (!o.hasClass("active")) {
            if (this.$indicators.length && (this.$indicators.find(".active").removeClass("active"), this.$element.one("slid", function () {
                    var e = t(l.$indicators.children()[l.getActiveIndex()]);
                    e && e.addClass("active")
                })), t.support.transition && this.$element.hasClass("slide")) {
                if (this.$element.trigger(u), u.isDefaultPrevented())return;
                o.addClass(e), o[0].offsetWidth, i.addClass(r), o.addClass(r), i.one(t.support.transition.end, function () {
                    o.removeClass([e, r].join(" ")).addClass("active"), i.removeClass(["active", r].join(" ")), l.sliding = !1, setTimeout(function () {
                        l.$element.trigger("slid")
                    }, 0)
                }).emulateTransitionEnd(600)
            } else {
                if (this.$element.trigger(u), u.isDefaultPrevented())return;
                i.removeClass("active"), o.addClass("active"), this.sliding = !1, this.$element.trigger("slid")
            }
            return a && this.cycle(), this
        }
    };
    var n = t.fn.carousel;
    t.fn.carousel = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.carousel"), a = t.extend({}, e.DEFAULTS, i.data(), "object" == typeof n && n), r = "string" == typeof n ? n : a.slide;
            o || i.data("bs.carousel", o = new e(this, a)), "number" == typeof n ? o.to(n) : r ? o[r]() : a.interval && o.pause().cycle()
        })
    }, t.fn.carousel.Constructor = e, t.fn.carousel.noConflict = function () {
        return t.fn.carousel = n, this
    }, t(document).on("click.bs.carousel.data-api", "[data-slide], [data-slide-to]", function (e) {
        var n, i = t(this), o = t(i.attr("data-target") || (n = i.attr("href")) && n.replace(/.*(?=#[^\s]+$)/, "")), a = t.extend({}, o.data(), i.data()), r = i.attr("data-slide-to");
        r && (a.interval = !1), o.carousel(a), (r = i.attr("data-slide-to")) && o.data("bs.carousel").to(r), e.preventDefault()
    }), t(window).on("load", function () {
        t('[data-ride="carousel"]').each(function () {
            var e = t(this);
            e.carousel(e.data())
        })
    })
}(window.jQuery), +function (t) {
    "use strict";
    var e = function (n, i) {
        this.$element = t(n), this.options = t.extend({}, e.DEFAULTS, i), this.transitioning = null, this.options.parent && (this.$parent = t(this.options.parent)), this.options.toggle && this.toggle()
    };
    e.DEFAULTS = {toggle: !0}, e.prototype.dimension = function () {
        var t = this.$element.hasClass("width");
        return t ? "width" : "height"
    }, e.prototype.show = function () {
        if (!this.transitioning && !this.$element.hasClass("in")) {
            var e = t.Event("show.bs.collapse");
            if (this.$element.trigger(e), !e.isDefaultPrevented()) {
                var n = this.$parent && this.$parent.find("> .panel > .in");
                if (n && n.length) {
                    var i = n.data("bs.collapse");
                    if (i && i.transitioning)return;
                    n.collapse("hide"), i || n.data("bs.collapse", null)
                }
                var o = this.dimension();
                this.$element.removeClass("collapse").addClass("collapsing")[o](0), this.transitioning = 1;
                var a = function () {
                    this.$element.removeClass("collapsing").addClass("in")[o]("auto"), this.transitioning = 0, this.$element.trigger("shown.bs.collapse")
                };
                if (!t.support.transition)return a.call(this);
                var r = t.camelCase(["scroll", o].join("-"));
                this.$element.one(t.support.transition.end, t.proxy(a, this)).emulateTransitionEnd(350)[o](this.$element[0][r])
            }
        }
    }, e.prototype.hide = function () {
        if (!this.transitioning && this.$element.hasClass("in")) {
            var e = t.Event("hide.bs.collapse");
            if (this.$element.trigger(e), !e.isDefaultPrevented()) {
                var n = this.dimension();
                this.$element[n](this.$element[n]())[0].offsetHeight, this.$element.addClass("collapsing").removeClass("collapse").removeClass("in"), this.transitioning = 1;
                var i = function () {
                    this.transitioning = 0, this.$element.trigger("hidden.bs.collapse").removeClass("collapsing").addClass("collapse")
                };
                return t.support.transition ? void this.$element[n](0).one(t.support.transition.end, t.proxy(i, this)).emulateTransitionEnd(350) : i.call(this)
            }
        }
    }, e.prototype.toggle = function () {
        this[this.$element.hasClass("in") ? "hide" : "show"]()
    };
    var n = t.fn.collapse;
    t.fn.collapse = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.collapse"), a = t.extend({}, e.DEFAULTS, i.data(), "object" == typeof n && n);
            o || i.data("bs.collapse", o = new e(this, a)), "string" == typeof n && o[n]()
        })
    }, t.fn.collapse.Constructor = e, t.fn.collapse.noConflict = function () {
        return t.fn.collapse = n, this
    }, t(document).on("click.bs.collapse.data-api", "[data-toggle=collapse]", function (e) {
        var n, i = t(this), o = i.attr("data-target") || e.preventDefault() || (n = i.attr("href")) && n.replace(/.*(?=#[^\s]+$)/, ""), a = t(o), r = a.data("bs.collapse"), s = r ? "toggle" : i.data(), l = i.attr("data-parent"), u = l && t(l);
        r && r.transitioning || (u && u.find('[data-toggle=collapse][data-parent="' + l + '"]').not(i).addClass("collapsed"), i[a.hasClass("in") ? "addClass" : "removeClass"]("collapsed")), a.collapse(s)
    })
}(window.jQuery), +function (t) {
    "use strict";
    function e() {
        t(i).remove(), t(o).each(function (e) {
            var i = n(t(this));
            i.hasClass("open") && (i.trigger(e = t.Event("hide.bs.dropdown")), e.isDefaultPrevented() || i.removeClass("open").trigger("hidden.bs.dropdown"))
        })
    }

    function n(e) {
        var n = e.attr("data-target");
        n || (n = e.attr("href"), n = n && /#/.test(n) && n.replace(/.*(?=#[^\s]*$)/, ""));
        var i = n && t(n);
        return i && i.length ? i : e.parent()
    }

    var i = ".dropdown-backdrop", o = "[data-toggle=dropdown]", a = function (e) {
        t(e).on("click.bs.dropdown", this.toggle)
    };
    a.prototype.toggle = function (i) {
        var o = t(this);
        if (!o.is(".disabled, :disabled")) {
            var a = n(o), r = a.hasClass("open");
            if (e(), !r) {
                if ("ontouchstart" in document.documentElement && !a.closest(".navbar-nav").length && t('<div class="dropdown-backdrop"/>').insertAfter(t(this)).on("click", e), a.trigger(i = t.Event("show.bs.dropdown")), i.isDefaultPrevented())return;
                a.toggleClass("open").trigger("shown.bs.dropdown"), o.focus()
            }
            return !1
        }
    }, a.prototype.keydown = function (e) {
        if (/(38|40|27)/.test(e.keyCode)) {
            var i = t(this);
            if (e.preventDefault(), e.stopPropagation(), !i.is(".disabled, :disabled")) {
                var a = n(i), r = a.hasClass("open");
                if (!r || r && 27 == e.keyCode)return 27 == e.which && a.find(o).focus(), i.click();
                var s = t("[role=menu] li:not(.divider):visible a", a);
                if (s.length) {
                    var l = s.index(s.filter(":focus"));
                    38 == e.keyCode && l > 0 && l--, 40 == e.keyCode && l < s.length - 1 && l++, ~l || (l = 0), s.eq(l).focus()
                }
            }
        }
    };
    var r = t.fn.dropdown;
    t.fn.dropdown = function (e) {
        return this.each(function () {
            var n = t(this), i = n.data("dropdown");
            i || n.data("dropdown", i = new a(this)), "string" == typeof e && i[e].call(n)
        })
    }, t.fn.dropdown.Constructor = a, t.fn.dropdown.noConflict = function () {
        return t.fn.dropdown = r, this
    }, t(document).on("click.bs.dropdown.data-api", e).on("click.bs.dropdown.data-api", ".dropdown form", function (t) {
        t.stopPropagation()
    }).on("click.bs.dropdown.data-api", o, a.prototype.toggle).on("keydown.bs.dropdown.data-api", o + ", [role=menu]", a.prototype.keydown)
}(window.jQuery), +function (t) {
    "use strict";
    var e = function (e, n) {
        this.options = n, this.$element = t(e), this.$backdrop = this.isShown = null, this.options.remote && this.$element.load(this.options.remote)
    };
    e.DEFAULTS = {backdrop: !0, keyboard: !0, show: !0}, e.prototype.toggle = function (t) {
        return this[this.isShown ? "hide" : "show"](t)
    }, e.prototype.show = function (e) {
        var n = this, i = t.Event("show.bs.modal", {relatedTarget: e});
        this.$element.trigger(i), this.isShown || i.isDefaultPrevented() || (this.isShown = !0, this.escape(), this.$element.on("click.dismiss.modal", '[data-dismiss="modal"]', t.proxy(this.hide, this)), this.backdrop(function () {
            var i = t.support.transition && n.$element.hasClass("fade");
            n.$element.parent().length || n.$element.appendTo(document.body), n.$element.show(), i && n.$element[0].offsetWidth, n.$element.addClass("in").attr("aria-hidden", !1), n.enforceFocus();
            var o = t.Event("shown.bs.modal", {relatedTarget: e});
            i ? n.$element.find(".modal-dialog").one(t.support.transition.end, function () {
                n.$element.focus().trigger(o)
            }).emulateTransitionEnd(300) : n.$element.focus().trigger(o)
        }))
    }, e.prototype.hide = function (e) {
        e && e.preventDefault(), e = t.Event("hide.bs.modal"), this.$element.trigger(e), this.isShown && !e.isDefaultPrevented() && (this.isShown = !1, this.escape(), t(document).off("focusin.bs.modal"), this.$element.removeClass("in").attr("aria-hidden", !0).off("click.dismiss.modal"), t.support.transition && this.$element.hasClass("fade") ? this.$element.one(t.support.transition.end, t.proxy(this.hideModal, this)).emulateTransitionEnd(300) : this.hideModal())
    }, e.prototype.enforceFocus = function () {
        t(document).off("focusin.bs.modal").on("focusin.bs.modal", t.proxy(function (t) {
            this.$element[0] === t.target || this.$element.has(t.target).length || this.$element.focus()
        }, this))
    }, e.prototype.escape = function () {
        this.isShown && this.options.keyboard ? this.$element.on("keyup.dismiss.bs.modal", t.proxy(function (t) {
            27 == t.which && this.hide()
        }, this)) : this.isShown || this.$element.off("keyup.dismiss.bs.modal")
    }, e.prototype.hideModal = function () {
        var t = this;
        this.$element.hide(), this.backdrop(function () {
            t.removeBackdrop(), t.$element.trigger("hidden.bs.modal")
        })
    }, e.prototype.removeBackdrop = function () {
        this.$backdrop && this.$backdrop.remove(), this.$backdrop = null
    }, e.prototype.backdrop = function (e) {
        var n = this.$element.hasClass("fade") ? "fade" : "";
        if (this.isShown && this.options.backdrop) {
            var i = t.support.transition && n;
            if (this.$backdrop = t('<div class="modal-backdrop ' + n + '" />').appendTo(document.body), this.$element.on("click.dismiss.modal", t.proxy(function (t) {
                    t.target === t.currentTarget && ("static" == this.options.backdrop ? this.$element[0].focus.call(this.$element[0]) : this.hide.call(this))
                }, this)), i && this.$backdrop[0].offsetWidth, this.$backdrop.addClass("in"), !e)return;
            i ? this.$backdrop.one(t.support.transition.end, e).emulateTransitionEnd(150) : e()
        } else!this.isShown && this.$backdrop ? (this.$backdrop.removeClass("in"), t.support.transition && this.$element.hasClass("fade") ? this.$backdrop.one(t.support.transition.end, e).emulateTransitionEnd(150) : e()) : e && e()
    };
    var n = t.fn.modal;
    t.fn.modal = function (n, i) {
        return this.each(function () {
            var o = t(this), a = o.data("bs.modal"), r = t.extend({}, e.DEFAULTS, o.data(), "object" == typeof n && n);
            a || o.data("bs.modal", a = new e(this, r)), "string" == typeof n ? a[n](i) : r.show && a.show(i)
        })
    }, t.fn.modal.Constructor = e, t.fn.modal.noConflict = function () {
        return t.fn.modal = n, this
    }, t(document).on("click.bs.modal.data-api", '[data-toggle="modal"]', function (e) {
        var n = t(this), i = n.attr("href"), o = t(n.attr("data-target") || i && i.replace(/.*(?=#[^\s]+$)/, "")), a = o.data("modal") ? "toggle" : t.extend({remote: !/#/.test(i) && i}, o.data(), n.data());
        e.preventDefault(), o.modal(a, this).one("hide", function () {
            n.is(":visible") && n.focus()
        })
    }), t(document).on("show.bs.modal", ".modal", function () {
        t(document.body).addClass("modal-open")
    }).on("hidden.bs.modal", ".modal", function () {
        t(document.body).removeClass("modal-open")
    })
}(window.jQuery), +function (t) {
    "use strict";
    var e = function (t, e) {
        this.type = this.options = this.enabled = this.timeout = this.hoverState = this.$element = null, this.init("tooltip", t, e)
    };
    e.DEFAULTS = {
        animation: !0,
        placement: "top",
        selector: !1,
        template: '<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
        trigger: "hover focus",
        title: "",
        delay: 0,
        html: !1,
        container: !1
    }, e.prototype.init = function (e, n, i) {
        this.enabled = !0, this.type = e, this.$element = t(n), this.options = this.getOptions(i);
        for (var o = this.options.trigger.split(" "), a = o.length; a--;) {
            var r = o[a];
            if ("click" == r)this.$element.on("click." + this.type, this.options.selector, t.proxy(this.toggle, this)); else if ("manual" != r) {
                var s = "hover" == r ? "mouseenter" : "focus", l = "hover" == r ? "mouseleave" : "blur";
                this.$element.on(s + "." + this.type, this.options.selector, t.proxy(this.enter, this)), this.$element.on(l + "." + this.type, this.options.selector, t.proxy(this.leave, this))
            }
        }
        this.options.selector ? this._options = t.extend({}, this.options, {
            trigger: "manual",
            selector: ""
        }) : this.fixTitle()
    }, e.prototype.getDefaults = function () {
        return e.DEFAULTS
    }, e.prototype.getOptions = function (e) {
        return e = t.extend({}, this.getDefaults(), this.$element.data(), e), e.delay && "number" == typeof e.delay && (e.delay = {
            show: e.delay,
            hide: e.delay
        }), e
    }, e.prototype.getDelegateOptions = function () {
        var e = {}, n = this.getDefaults();
        return this._options && t.each(this._options, function (t, i) {
            n[t] != i && (e[t] = i)
        }), e
    }, e.prototype.enter = function (e) {
        var n = e instanceof this.constructor ? e : t(e.currentTarget)[this.type](this.getDelegateOptions()).data("bs." + this.type);
        return clearTimeout(n.timeout), n.hoverState = "in", n.options.delay && n.options.delay.show ? void(n.timeout = setTimeout(function () {
            "in" == n.hoverState && n.show()
        }, n.options.delay.show)) : n.show()
    }, e.prototype.leave = function (e) {
        var n = e instanceof this.constructor ? e : t(e.currentTarget)[this.type](this.getDelegateOptions()).data("bs." + this.type);
        return clearTimeout(n.timeout), n.hoverState = "out", n.options.delay && n.options.delay.hide ? void(n.timeout = setTimeout(function () {
            "out" == n.hoverState && n.hide()
        }, n.options.delay.hide)) : n.hide()
    }, e.prototype.show = function () {
        var e = t.Event("show.bs." + this.type);
        if (this.hasContent() && this.enabled) {
            if (this.$element.trigger(e), e.isDefaultPrevented())return;
            var n = this.tip();
            this.setContent(), this.options.animation && n.addClass("fade");
            var i = "function" == typeof this.options.placement ? this.options.placement.call(this, n[0], this.$element[0]) : this.options.placement, o = /\s?auto?\s?/i, a = o.test(i);
            a && (i = i.replace(o, "") || "top"), n.detach().css({
                top: 0,
                left: 0,
                display: "block"
            }).addClass(i), this.options.container ? n.appendTo(this.options.container) : n.insertAfter(this.$element);
            var r = this.getPosition(), s = n[0].offsetWidth, l = n[0].offsetHeight;
            if (a) {
                var u = this.$element.parent(), c = i, d = document.documentElement.scrollTop || document.body.scrollTop, h = "body" == this.options.container ? window.innerWidth : u.outerWidth(), f = "body" == this.options.container ? window.innerHeight : u.outerHeight(), p = "body" == this.options.container ? 0 : u.offset().left;
                i = "bottom" == i && r.top + r.height + l - d > f ? "top" : "top" == i && r.top - d - l < 0 ? "bottom" : "right" == i && r.right + s > h ? "left" : "left" == i && r.left - s < p ? "right" : i, n.removeClass(c).addClass(i)
            }
            var m = this.getCalculatedOffset(i, r, s, l);
            this.applyPlacement(m, i), this.$element.trigger("shown.bs." + this.type)
        }
    }, e.prototype.applyPlacement = function (t, e) {
        var n, i = this.tip(), o = i[0].offsetWidth, a = i[0].offsetHeight, r = parseInt(i.css("margin-top"), 10), s = parseInt(i.css("margin-left"), 10);
        isNaN(r) && (r = 0), isNaN(s) && (s = 0), t.top = t.top + r, t.left = t.left + s, i.offset(t).addClass("in");
        var l = i[0].offsetWidth, u = i[0].offsetHeight;
        if ("top" == e && u != a && (n = !0, t.top = t.top + a - u), /bottom|top/.test(e)) {
            var c = 0;
            t.left < 0 && (c = -2 * t.left, t.left = 0, i.offset(t), l = i[0].offsetWidth, u = i[0].offsetHeight), this.replaceArrow(c - o + l, l, "left")
        } else this.replaceArrow(u - a, u, "top");
        n && i.offset(t)
    }, e.prototype.replaceArrow = function (t, e, n) {
        this.arrow().css(n, t ? 50 * (1 - t / e) + "%" : "")
    }, e.prototype.setContent = function () {
        var t = this.tip(), e = this.getTitle();
        t.find(".tooltip-inner")[this.options.html ? "html" : "text"](e), t.removeClass("fade in top bottom left right")
    }, e.prototype.hide = function () {
        function e() {
            "in" != n.hoverState && i.detach()
        }

        var n = this, i = this.tip(), o = t.Event("hide.bs." + this.type);
        return this.$element.trigger(o), o.isDefaultPrevented() ? void 0 : (i.removeClass("in"), t.support.transition && this.$tip.hasClass("fade") ? i.one(t.support.transition.end, e).emulateTransitionEnd(150) : e(), this.$element.trigger("hidden.bs." + this.type), this)
    }, e.prototype.fixTitle = function () {
        var t = this.$element;
        (t.attr("title") || "string" != typeof t.attr("data-original-title")) && t.attr("data-original-title", t.attr("title") || "").attr("title", "")
    }, e.prototype.hasContent = function () {
        return this.getTitle()
    }, e.prototype.getPosition = function () {
        var e = this.$element[0];
        return t.extend({}, "function" == typeof e.getBoundingClientRect ? e.getBoundingClientRect() : {
            width: e.offsetWidth,
            height: e.offsetHeight
        }, this.$element.offset())
    }, e.prototype.getCalculatedOffset = function (t, e, n, i) {
        return "bottom" == t ? {
            top: e.top + e.height,
            left: e.left + e.width / 2 - n / 2
        } : "top" == t ? {
            top: e.top - i,
            left: e.left + e.width / 2 - n / 2
        } : "left" == t ? {top: e.top + e.height / 2 - i / 2, left: e.left - n} : {
            top: e.top + e.height / 2 - i / 2,
            left: e.left + e.width
        }
    }, e.prototype.getTitle = function () {
        var t, e = this.$element, n = this.options;
        return t = e.attr("data-original-title") || ("function" == typeof n.title ? n.title.call(e[0]) : n.title)
    }, e.prototype.tip = function () {
        return this.$tip = this.$tip || t(this.options.template)
    }, e.prototype.arrow = function () {
        return this.$arrow = this.$arrow || this.tip().find(".tooltip-arrow")
    }, e.prototype.validate = function () {
        this.$element[0].parentNode || (this.hide(), this.$element = null, this.options = null)
    }, e.prototype.enable = function () {
        this.enabled = !0
    }, e.prototype.disable = function () {
        this.enabled = !1
    }, e.prototype.toggleEnabled = function () {
        this.enabled = !this.enabled
    }, e.prototype.toggle = function (e) {
        var n = e ? t(e.currentTarget)[this.type](this.getDelegateOptions()).data("bs." + this.type) : this;
        n.tip().hasClass("in") ? n.leave(n) : n.enter(n)
    }, e.prototype.destroy = function () {
        this.hide().$element.off("." + this.type).removeData("bs." + this.type)
    };
    var n = t.fn.tooltip;
    t.fn.tooltip = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.tooltip"), a = "object" == typeof n && n;
            o || i.data("bs.tooltip", o = new e(this, a)), "string" == typeof n && o[n]()
        })
    }, t.fn.tooltip.Constructor = e, t.fn.tooltip.noConflict = function () {
        return t.fn.tooltip = n, this
    }
}(window.jQuery), +function (t) {
    "use strict";
    var e = function (t, e) {
        this.init("popover", t, e)
    };
    if (!t.fn.tooltip)throw new Error("Popover requires tooltip.js");
    e.DEFAULTS = t.extend({}, t.fn.tooltip.Constructor.DEFAULTS, {
        placement: "right",
        trigger: "click",
        content: "",
        template: '<div class="popover"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
    }), e.prototype = t.extend({}, t.fn.tooltip.Constructor.prototype), e.prototype.constructor = e, e.prototype.getDefaults = function () {
        return e.DEFAULTS
    }, e.prototype.setContent = function () {
        var t = this.tip(), e = this.getTitle(), n = this.getContent();
        t.find(".popover-title")[this.options.html ? "html" : "text"](e), t.find(".popover-content")[this.options.html ? "html" : "text"](n), t.removeClass("fade top bottom left right in"), t.find(".popover-title").html() || t.find(".popover-title").hide()
    }, e.prototype.hasContent = function () {
        return this.getTitle() || this.getContent()
    }, e.prototype.getContent = function () {
        var t = this.$element, e = this.options;
        return t.attr("data-content") || ("function" == typeof e.content ? e.content.call(t[0]) : e.content)
    }, e.prototype.arrow = function () {
        return this.$arrow = this.$arrow || this.tip().find(".arrow")
    }, e.prototype.tip = function () {
        return this.$tip || (this.$tip = t(this.options.template)), this.$tip
    };
    var n = t.fn.popover;
    t.fn.popover = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.popover"), a = "object" == typeof n && n;
            o || i.data("bs.popover", o = new e(this, a)), "string" == typeof n && o[n]()
        })
    }, t.fn.popover.Constructor = e, t.fn.popover.noConflict = function () {
        return t.fn.popover = n, this
    }
}(window.jQuery), +function (t) {
    "use strict";
    function e(n, i) {
        var o, a = t.proxy(this.process, this);
        this.$element = t(t(n).is("body") ? window : n), this.$body = t("body"), this.$scrollElement = this.$element.on("scroll.bs.scroll-spy.data-api", a), this.options = t.extend({}, e.DEFAULTS, i), this.selector = (this.options.target || (o = t(n).attr("href")) && o.replace(/.*(?=#[^\s]+$)/, "") || "") + " .nav li > a", this.offsets = t([]), this.targets = t([]), this.activeTarget = null, this.refresh(), this.process()
    }

    e.DEFAULTS = {offset: 10}, e.prototype.refresh = function () {
        var e = this.$element[0] == window ? "offset" : "position";
        this.offsets = t([]), this.targets = t([]);
        var n = this;
        this.$body.find(this.selector).map(function () {
            var i = t(this), o = i.data("target") || i.attr("href"), a = /^#\w/.test(o) && t(o);
            return a && a.length && [[a[e]().top + (!t.isWindow(n.$scrollElement.get(0)) && n.$scrollElement.scrollTop()), o]] || null
        }).sort(function (t, e) {
            return t[0] - e[0]
        }).each(function () {
            n.offsets.push(this[0]), n.targets.push(this[1])
        })
    }, e.prototype.process = function () {
        var t, e = this.$scrollElement.scrollTop() + this.options.offset, n = this.$scrollElement[0].scrollHeight || this.$body[0].scrollHeight, i = n - this.$scrollElement.height(), o = this.offsets, a = this.targets, r = this.activeTarget;
        if (e >= i)return r != (t = a.last()[0]) && this.activate(t);
        for (t = o.length; t--;)r != a[t] && e >= o[t] && (!o[t + 1] || e <= o[t + 1]) && this.activate(a[t])
    }, e.prototype.activate = function (e) {
        this.activeTarget = e, t(this.selector).parents(".active").removeClass("active");
        var n = this.selector + '[data-target="' + e + '"],' + this.selector + '[href="' + e + '"]', i = t(n).parents("li").addClass("active");
        i.parent(".dropdown-menu").length && (i = i.closest("li.dropdown").addClass("active")), i.trigger("activate")
    };
    var n = t.fn.scrollspy;
    t.fn.scrollspy = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.scrollspy"), a = "object" == typeof n && n;
            o || i.data("bs.scrollspy", o = new e(this, a)), "string" == typeof n && o[n]()
        })
    }, t.fn.scrollspy.Constructor = e, t.fn.scrollspy.noConflict = function () {
        return t.fn.scrollspy = n, this
    }, t(window).on("load", function () {
        t('[data-spy="scroll"]').each(function () {
            var e = t(this);
            e.scrollspy(e.data())
        })
    })
}(window.jQuery), +function (t) {
    "use strict";
    var e = function (e) {
        this.element = t(e)
    };
    e.prototype.show = function () {
        var e = this.element, n = e.closest("ul:not(.dropdown-menu)"), i = e.attr("data-target");
        if (i || (i = e.attr("href"), i = i && i.replace(/.*(?=#[^\s]*$)/, "")), !e.parent("li").hasClass("active")) {
            var o = n.find(".active:last a")[0], a = t.Event("show.bs.tab", {relatedTarget: o});
            if (e.trigger(a), !a.isDefaultPrevented()) {
                var r = t(i);
                this.activate(e.parent("li"), n), this.activate(r, r.parent(), function () {
                    e.trigger({type: "shown.bs.tab", relatedTarget: o})
                })
            }
        }
    }, e.prototype.activate = function (e, n, i) {
        function o() {
            a.removeClass("active").find("> .dropdown-menu > .active").removeClass("active"), e.addClass("active"), r ? (e[0].offsetWidth, e.addClass("in")) : e.removeClass("fade"), e.parent(".dropdown-menu") && e.closest("li.dropdown").addClass("active"), i && i()
        }

        var a = n.find("> .active"), r = i && t.support.transition && a.hasClass("fade");
        r ? a.one(t.support.transition.end, o).emulateTransitionEnd(150) : o(), a.removeClass("in")
    };
    var n = t.fn.tab;
    t.fn.tab = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.tab");
            o || i.data("bs.tab", o = new e(this)), "string" == typeof n && o[n]()
        })
    }, t.fn.tab.Constructor = e, t.fn.tab.noConflict = function () {
        return t.fn.tab = n, this
    }, t(document).on("click.bs.tab.data-api", '[data-toggle="tab"], [data-toggle="pill"]', function (e) {
        e.preventDefault(), t(this).tab("show")
    })
}(window.jQuery), +function (t) {
    "use strict";
    var e = function (n, i) {
        this.options = t.extend({}, e.DEFAULTS, i), this.$window = t(window).on("scroll.bs.affix.data-api", t.proxy(this.checkPosition, this)).on("click.bs.affix.data-api", t.proxy(this.checkPositionWithEventLoop, this)), this.$element = t(n), this.affixed = this.unpin = null, this.checkPosition()
    };
    e.RESET = "affix affix-top affix-bottom", e.DEFAULTS = {offset: 0}, e.prototype.checkPositionWithEventLoop = function () {
        setTimeout(t.proxy(this.checkPosition, this), 1)
    }, e.prototype.checkPosition = function () {
        if (this.$element.is(":visible")) {
            var n = t(document).height(), i = this.$window.scrollTop(), o = this.$element.offset(), a = this.options.offset, r = a.top, s = a.bottom;
            "object" != typeof a && (s = r = a), "function" == typeof r && (r = a.top()), "function" == typeof s && (s = a.bottom());
            var l = null != this.unpin && i + this.unpin <= o.top ? !1 : null != s && o.top + this.$element.height() >= n - s ? "bottom" : null != r && r >= i ? "top" : !1;
            this.affixed !== l && (this.unpin && this.$element.css("top", ""), this.affixed = l, this.unpin = "bottom" == l ? o.top - i : null, this.$element.removeClass(e.RESET).addClass("affix" + (l ? "-" + l : "")), "bottom" == l && this.$element.offset({top: document.body.offsetHeight - s - this.$element.height()}))
        }
    };
    var n = t.fn.affix;
    t.fn.affix = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("bs.affix"), a = "object" == typeof n && n;
            o || i.data("bs.affix", o = new e(this, a)), "string" == typeof n && o[n]()
        })
    }, t.fn.affix.Constructor = e, t.fn.affix.noConflict = function () {
        return t.fn.affix = n, this
    }, t(window).on("load", function () {
        t('[data-spy="affix"]').each(function () {
            var e = t(this), n = e.data();
            n.offset = n.offset || {}, n.offsetBottom && (n.offset.bottom = n.offsetBottom), n.offsetTop && (n.offset.top = n.offsetTop), e.affix(n)
        })
    })
}(window.jQuery), !function (t) {
    var e = function (n, i, o) {
        o && (o.stopPropagation(), o.preventDefault()), this.$element = t(n), this.$newElement = null, this.button = null, this.options = t.extend({}, t.fn.selectpicker.defaults, this.$element.data(), "object" == typeof i && i), null == this.options.title && (this.options.title = this.$element.attr("title")), this.val = e.prototype.val, this.render = e.prototype.render, this.init()
    };
    e.prototype = {
        constructor: e, init: function () {
            function e() {
                var e = c - t(window).scrollTop(), n = t(window).innerHeight, i = p + parseInt(r.css("margin-top")) + parseInt(r.css("margin-bottom")) + 2, o = n - e - h - i;
                d = o, a.hasClass("dropup") && (d = e - i), r.css({
                    "max-height": d + "px",
                    "overflow-y": "auto",
                    "min-height": 3 * l + "px"
                })
            }

            var n = this;
            this.$element.hide(), this.multiple = this.$element.prop("multiple");
            var i = void 0 !== this.$element.attr("class") ? this.$element.attr("class").split(/\s+/) : "", o = this.$element.attr("id");
            this.$element.after(this.createView()), this.$newElement = this.$element.next(".select");
            var a = this.$newElement, r = this.$newElement.find(".dropdown-menu"), s = this.$newElement.find(".dropdown-arrow"), l = (r.find("li > a"), a.addClass("open").find(".dropdown-menu li > a").outerHeight());
            a.removeClass("open");
            var u = r.find("li .divider").outerHeight(!0), c = this.$newElement.offset().top, d = 0, h = this.$newElement.outerHeight();
            this.button = this.$newElement.find("> button"), void 0 !== o && (this.button.attr("id", o), t('label[for="' + o + '"]').click(function () {
                a.find("button#" + o).focus()
            }));
            for (var f = 0; f < i.length; f++)"selectpicker" != i[f] && this.$newElement.addClass(i[f]);
            this.multiple && this.$newElement.addClass("select-multiple"), this.button.addClass(this.options.style), r.addClass(this.options.menuStyle), s.addClass(function () {
                return n.options.menuStyle ? n.options.menuStyle.replace("dropdown-", "dropdown-arrow-") : void 0
            }), this.checkDisabled(), this.checkTabIndex(), this.clickListener();
            var p = parseInt(r.css("padding-top")) + parseInt(r.css("padding-bottom")) + parseInt(r.css("border-top-width")) + parseInt(r.css("border-bottom-width"));
            if ("auto" == this.options.size)e(), t(window).resize(e), t(window).scroll(e), this.$element.bind("DOMNodeInserted", e); else if (this.options.size && "auto" != this.options.size && r.find("li").length > this.options.size) {
                var m = r.find("li > *").filter(":not(.divider)").slice(0, this.options.size).last().parent().index(), g = r.find("li").slice(0, m + 1).find(".divider").length;
                d = l * this.options.size + g * u + p, r.css({"max-height": d + "px", "overflow-y": "scroll"})
            }
            this.$element.bind("DOMNodeInserted", t.proxy(this.reloadLi, this)), this.render()
        }, createDropdown: function () {
            var e = "<div class='btn-group select'><button class='btn dropdown-toggle clearfix' data-toggle='dropdown'><span class='filter-option pull-left'></span>&nbsp;<span class='caret'></span></button><span class='dropdown-arrow'></span><ul class='dropdown-menu' role='menu'></ul></div>";
            return t(e)
        }, createView: function () {
            var t = this.createDropdown(), e = this.createLi();
            return t.find("ul").append(e), t
        }, reloadLi: function () {
            this.destroyLi(), $li = this.createLi(), this.$newElement.find("ul").append($li), this.render()
        }, destroyLi: function () {
            this.$newElement.find("li").remove()
        }, createLi: function () {
            var e = this, n = [], i = [], o = "";
            if (this.$element.find("option").each(function () {
                    n.push(t(this).text())
                }), this.$element.find("option").each(function () {
                    var n = void 0 !== t(this).attr("class") ? t(this).attr("class") : "", o = t(this).text(), a = void 0 !== t(this).data("subtext") ? '<small class="muted">' + t(this).data("subtext") + "</small>" : "";
                    if (o += a, t(this).parent().is("optgroup") && 1 != t(this).data("divider"))if (0 == t(this).index()) {
                        var r = t(this).parent().attr("label"), s = void 0 !== t(this).parent().data("subtext") ? '<small class="muted">' + t(this).parent().data("subtext") + "</small>" : "";
                        r += s, i.push(0 != t(this)[0].index ? '<div class="divider"></div><dt>' + r + "</dt>" + e.createA(o, "opt " + n) : "<dt>" + r + "</dt>" + e.createA(o, "opt " + n))
                    } else i.push(e.createA(o, "opt " + n)); else i.push(1 == t(this).data("divider") ? '<div class="divider"></div>' : e.createA(o, n))
                }), n.length > 0)for (var a = 0; a < n.length; a++) {
                {
                    this.$element.find("option").eq(a)
                }
                o += "<li rel=" + a + ">" + i[a] + "</li>"
            }
            return 0 != this.$element.find("option:selected").length || e.options.title || this.$element.find("option").eq(0).prop("selected", !0).attr("selected", "selected"), t(o)
        }, createA: function (t, e) {
            return '<a tabindex="-1" href="#" class="' + e + '"><span class="pull-left">' + t + "</span></a>"
        }, render: function () {
            var e = this;
            if ("auto" == this.options.width) {
                var n = this.$newElement.find(".dropdown-menu").css("width");
                this.$newElement.css("width", n)
            } else this.options.width && "auto" != this.options.width && this.$newElement.css("width", this.options.width);
            this.$element.find("option").each(function (n) {
                e.setDisabled(n, t(this).is(":disabled") || t(this).parent().is(":disabled")), e.setSelected(n, t(this).is(":selected"))
            });
            var i = this.$element.find("option:selected").map(function () {
                return void 0 != t(this).attr("title") ? t(this).attr("title") : t(this).text()
            }).toArray(), o = i.join(", ");
            if (e.multiple && e.options.selectedTextFormat.indexOf("count") > -1) {
                var a = e.options.selectedTextFormat.split(">");
                (a.length > 1 && i.length > a[1] || 1 == a.length && i.length >= 2) && (o = i.length + " of " + this.$element.find("option").length + " selected")
            }
            o || (o = void 0 != e.options.title ? e.options.title : e.options.noneSelectedText), this.$element.next(".select").find(".filter-option").html(o)
        }, setSelected: function (t, e) {
            e ? this.$newElement.find("li").eq(t).addClass("selected") : this.$newElement.find("li").eq(t).removeClass("selected")
        }, setDisabled: function (t, e) {
            e ? this.$newElement.find("li").eq(t).addClass("disabled") : this.$newElement.find("li").eq(t).removeClass("disabled")
        }, checkDisabled: function () {
            this.$element.is(":disabled") && (this.button.addClass("disabled"), this.button.click(function (t) {
                t.preventDefault()
            }))
        }, checkTabIndex: function () {
            if (this.$element.is("[tabindex]")) {
                var t = this.$element.attr("tabindex");
                this.button.attr("tabindex", t)
            }
        }, clickListener: function () {
            var e = this;
            t("body").on("touchstart.dropdown", ".dropdown-menu", function (t) {
                t.stopPropagation()
            }), this.$newElement.on("click", "li a", function (n) {
                var i = t(this).parent().index(), o = t(this).parent(), a = o.parents(".select");
                if (e.multiple && n.stopPropagation(), n.preventDefault(), a.prev("select").not(":disabled") && !t(this).parent().hasClass("disabled")) {
                    if (e.multiple) {
                        var r = a.prev("select").find("option").eq(i).prop("selected");
                        r ? a.prev("select").find("option").eq(i).removeAttr("selected") : a.prev("select").find("option").eq(i).prop("selected", !0).attr("selected", "selected")
                    } else a.prev("select").find("option").removeAttr("selected"), a.prev("select").find("option").eq(i).prop("selected", !0).attr("selected", "selected");
                    a.find(".filter-option").html(o.text()), a.find("button").focus(), a.prev("select").trigger("change")
                }
            }), this.$newElement.on("click", "li.disabled a, li dt, li .divider", function (e) {
                e.preventDefault(), e.stopPropagation(), $select = t(this).parent().parents(".select"), $select.find("button").focus()
            }), this.$element.on("change", function () {
                e.render()
            })
        }, val: function (t) {
            return void 0 != t ? (this.$element.val(t), this.$element.trigger("change"), this.$element) : this.$element.val()
        }
    }, t.fn.selectpicker = function (n, i) {
        var o, a = arguments, r = this.each(function () {
            var r = t(this), s = r.data("selectpicker"), l = "object" == typeof n && n;
            if (s)for (var u in n)s[u] = n[u]; else r.data("selectpicker", s = new e(this, l, i));
            "string" == typeof n && (property = n, s[property] instanceof Function ? ([].shift.apply(a), o = s[property].apply(s, a)) : o = s[property])
        });
        return void 0 != o ? o : r
    }, t.fn.selectpicker.defaults = {
        style: null,
        size: "auto",
        title: null,
        selectedTextFormat: "values",
        noneSelectedText: "Nothing selected",
        width: null,
        menuStyle: null,
        toggleSize: null
    }
}(window.jQuery), !function (t) {
    "use strict";
    t.fn.bootstrapSwitch = function (e) {
        var n = {
            init: function () {
                return this.each(function () {
                    var e, n, i, o, a, r, s = t(this), l = "", u = s.attr("class"), c = "ON", d = "OFF", h = !1;
                    t.each(["switch-mini", "switch-small", "switch-large"], function (t, e) {
                        u.indexOf(e) >= 0 && (l = e)
                    }), s.addClass("has-switch"), void 0 !== s.data("on") && (a = "switch-" + s.data("on")), void 0 !== s.data("on-label") && (c = s.data("on-label")), void 0 !== s.data("off-label") && (d = s.data("off-label")), void 0 !== s.data("icon") && (h = s.data("icon")), n = t("<span>").addClass("switch-left").addClass(l).addClass(a).html(c), a = "", void 0 !== s.data("off") && (a = "switch-" + s.data("off")), i = t("<span>").addClass("switch-right").addClass(l).addClass(a).html(d), o = t("<label>").html("&nbsp;").addClass(l).attr("for", s.find("input").attr("id")), h && o.html('<i class="' + h + '"></i>'), e = s.find(":checkbox").wrap(t("<div>")).parent().data("animated", !1), s.data("animated") !== !1 && e.addClass("switch-animate").data("animated", !0), e.append(n).append(o).append(i), s.find(">div").addClass(s.find("input").is(":checked") ? "switch-on" : "switch-off"), s.find("input").is(":disabled") && t(this).addClass("deactivate");
                    var f = function (t) {
                        t.siblings("label").trigger("mousedown").trigger("mouseup").trigger("click")
                    };
                    s.on("keydown", function (e) {
                        32 === e.keyCode && (e.stopImmediatePropagation(), e.preventDefault(), f(t(e.target).find("span:first")))
                    }), n.on("click", function () {
                        f(t(this))
                    }), i.on("click", function () {
                        f(t(this))
                    }), s.find("input").on("change", function (e) {
                        var n = t(this), i = n.parent(), o = n.is(":checked"), a = i.is(".switch-off");
                        e.preventDefault(), i.css("left", ""), a === o && (o ? i.removeClass("switch-off").addClass("switch-on") : i.removeClass("switch-on").addClass("switch-off"), i.data("animated") !== !1 && i.addClass("switch-animate"), i.parent().trigger("switch-change", {
                            el: n,
                            value: o
                        }))
                    }), s.find("label").on("mousedown touchstart", function (e) {
                        var n = t(this);
                        r = !1, e.preventDefault(), e.stopImmediatePropagation(), n.closest("div").removeClass("switch-animate"), n.closest(".has-switch").is(".deactivate") ? n.unbind("click") : (n.on("mousemove touchmove", function (e) {
                            var n = t(this).closest(".switch"), i = (e.pageX || e.originalEvent.targetTouches[0].pageX) - n.offset().left, o = i / n.width() * 100, a = 25, s = 75;
                            r = !0, a > o ? o = a : o > s && (o = s), n.find(">div").css("left", o - s + "%")
                        }), n.on("click touchend", function (e) {
                            var n = t(this), i = t(e.target), o = i.siblings("input");
                            e.stopImmediatePropagation(), e.preventDefault(), n.unbind("mouseleave"), r ? o.prop("checked", !(parseInt(n.parent().css("left")) < -25)) : o.prop("checked", !o.is(":checked")), r = !1, o.trigger("change")
                        }), n.on("mouseleave", function (e) {
                            var n = t(this), i = n.siblings("input");
                            e.preventDefault(), e.stopImmediatePropagation(), n.unbind("mouseleave"), n.trigger("mouseup"), i.prop("checked", !(parseInt(n.parent().css("left")) < -25)).trigger("change")
                        }), n.on("mouseup", function (e) {
                            e.stopImmediatePropagation(), e.preventDefault(), t(this).unbind("mousemove")
                        }))
                    })
                })
            }, toggleActivation: function () {
                t(this).toggleClass("deactivate")
            }, isActive: function () {
                return !t(this).hasClass("deactivate")
            }, setActive: function (e) {
                e ? t(this).removeClass("deactivate") : t(this).addClass("deactivate")
            }, toggleState: function (e) {
                var n = t(this).find("input:checkbox");
                n.prop("checked", !n.is(":checked")).trigger("change", e)
            }, setState: function (e, n) {
                t(this).find("input:checkbox").prop("checked", e).trigger("change", n)
            }, status: function () {
                return t(this).find("input:checkbox").is(":checked")
            }, destroy: function () {
                var e, n = t(this).find("div");
                return n.find(":not(input:checkbox)").remove(), e = n.children(), e.unwrap().unwrap(), e.unbind("change"), e
            }
        };
        return n[e] ? n[e].apply(this, Array.prototype.slice.call(arguments, 1)) : "object" != typeof e && e ? void t.error("Method " + e + " does not exist!") : n.init.apply(this, arguments)
    }
}(jQuery), $(function () {
    $(".switch").bootstrapSwitch()
}), !function (t) {
    "use strict";
    var e = function (e, n) {
        this.$element = t(e), this.options = t.extend({}, t.fn.typeahead.defaults, n), this.matcher = this.options.matcher || this.matcher, this.sorter = this.options.sorter || this.sorter, this.highlighter = this.options.highlighter || this.highlighter, this.updater = this.options.updater || this.updater, this.source = this.options.source, this.$menu = t(this.options.menu), this.shown = !1, this.listen()
    };
    e.prototype = {
        constructor: e, select: function () {
            var t = this.$menu.find(".active").attr("data-value");
            return this.$element.val(this.updater(t)).change(), this.hide()
        }, updater: function (t) {
            return t
        }, show: function () {
            var e = t.extend({}, this.$element.position(), {height: this.$element[0].offsetHeight});
            return this.$menu.insertAfter(this.$element).css({
                top: e.top + e.height,
                left: e.left
            }).show(), this.shown = !0, this
        }, hide: function () {
            return this.$menu.hide(), this.shown = !1, this
        }, lookup: function () {
            var e;
            return this.query = this.$element.val(), !this.query || this.query.length < this.options.minLength ? this.shown ? this.hide() : this : (e = t.isFunction(this.source) ? this.source(this.query, t.proxy(this.process, this)) : this.source, e ? this.process(e) : this)
        }, process: function (e) {
            var n = this;
            return e = t.grep(e, function (t) {
                return n.matcher(t)
            }), e = this.sorter(e), e.length ? this.render(e.slice(0, this.options.items)).show() : this.shown ? this.hide() : this
        }, matcher: function (t) {
            return ~t.toLowerCase().indexOf(this.query.toLowerCase())
        }, sorter: function (t) {
            for (var e, n = [], i = [], o = []; e = t.shift();)e.toLowerCase().indexOf(this.query.toLowerCase()) ? ~e.indexOf(this.query) ? i.push(e) : o.push(e) : n.push(e);
            return n.concat(i, o)
        }, highlighter: function (t) {
            var e = this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&");
            return t.replace(new RegExp("(" + e + ")", "ig"), function (t, e) {
                return "<strong>" + e + "</strong>"
            })
        }, render: function (e) {
            var n = this;
            return e = t(e).map(function (e, i) {
                return e = t(n.options.item).attr("data-value", i), e.find("a").html(n.highlighter(i)), e[0]
            }), e.first().addClass("active"), this.$menu.html(e), this
        }, next: function () {
            var e = this.$menu.find(".active").removeClass("active"), n = e.next();
            n.length || (n = t(this.$menu.find("li")[0])), n.addClass("active")
        }, prev: function () {
            var t = this.$menu.find(".active").removeClass("active"), e = t.prev();
            e.length || (e = this.$menu.find("li").last()), e.addClass("active")
        }, listen: function () {
            this.$element.on("focus", t.proxy(this.focus, this)).on("blur", t.proxy(this.blur, this)).on("keypress", t.proxy(this.keypress, this)).on("keyup", t.proxy(this.keyup, this)), this.eventSupported("keydown") && this.$element.on("keydown", t.proxy(this.keydown, this)), this.$menu.on("click", t.proxy(this.click, this)).on("mouseenter", "li", t.proxy(this.mouseenter, this)).on("mouseleave", "li", t.proxy(this.mouseleave, this))
        }, eventSupported: function (t) {
            var e = t in this.$element;
            return e || (this.$element.setAttribute(t, "return;"), e = "function" == typeof this.$element[t]), e
        }, move: function (t) {
            if (this.shown) {
                switch (t.keyCode) {
                    case 9:
                    case 13:
                    case 27:
                        t.preventDefault();
                        break;
                    case 38:
                        t.preventDefault(), this.prev();
                        break;
                    case 40:
                        t.preventDefault(), this.next()
                }
                t.stopPropagation()
            }
        }, keydown: function (e) {
            this.suppressKeyPressRepeat = ~t.inArray(e.keyCode, [40, 38, 9, 13, 27]), this.move(e)
        }, keypress: function (t) {
            this.suppressKeyPressRepeat || this.move(t)
        }, keyup: function (t) {
            switch (t.keyCode) {
                case 40:
                case 38:
                case 16:
                case 17:
                case 18:
                    break;
                case 9:
                case 13:
                    if (!this.shown)return;
                    this.select();
                    break;
                case 27:
                    if (!this.shown)return;
                    this.hide();
                    break;
                default:
                    this.lookup()
            }
            t.stopPropagation(), t.preventDefault()
        }, focus: function () {
            this.focused = !0
        }, blur: function () {
            this.focused = !1, !this.mousedover && this.shown && this.hide()
        }, click: function (t) {
            t.stopPropagation(), t.preventDefault(), this.select(), this.$element.focus()
        }, mouseenter: function (e) {
            this.mousedover = !0, this.$menu.find(".active").removeClass("active"), t(e.currentTarget).addClass("active")
        }, mouseleave: function () {
            this.mousedover = !1, !this.focused && this.shown && this.hide()
        }
    };
    var n = t.fn.typeahead;
    t.fn.typeahead = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("typeahead"), a = "object" == typeof n && n;
            o || i.data("typeahead", o = new e(this, a)), "string" == typeof n && o[n]()
        })
    }, t.fn.typeahead.defaults = {
        source: [],
        items: 8,
        menu: '<ul class="typeahead dropdown-menu"></ul>',
        item: '<li><a href="#"></a></li>',
        minLength: 1
    }, t.fn.typeahead.Constructor = e, t.fn.typeahead.noConflict = function () {
        return t.fn.typeahead = n, this
    }, t(document).on("focus.typeahead.data-api", '[data-provide="typeahead"]', function () {
        var e = t(this);
        e.data("typeahead") || e.typeahead(e.data())
    })
}(window.jQuery), !function (t) {
    "use strict";
    var e = function (e, n) {
        this.options = t.extend({}, t.fn.affix.defaults, n), this.$window = t(window).on("scroll.affix.data-api", t.proxy(this.checkPosition, this)).on("resize.affix.data-api", t.proxy(this.refresh, this)), this.$element = t(e), this.refresh()
    };
    e.prototype.refresh = function () {
        this.position = this.$element.offset()
    }, e.prototype.checkPosition = function () {
        if (this.$element.is(":visible")) {
            var t, e = this.$window.scrollLeft(), n = this.$window.scrollTop(), i = this.position, o = this.options.offset;
            "object" != typeof o && (o = {
                x: o,
                y: o
            }), t = (null == o.x || i.left - e <= o.x) && (null == o.y || i.top - n <= o.y), t != this.affixed && (this.affixed = t, this.$element[t ? "addClass" : "removeClass"]("affix"))
        }
    }, t.fn.affix = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("affix"), a = "object" == typeof n && n;
            o || i.data("affix", o = new e(this, a)), "string" == typeof n && o[n]()
        })
    }, t.fn.affix.Constructor = e, t.fn.affix.defaults = {offset: 0}, t(function () {
        t('[data-spy="affix"]').each(function () {
            var e = t(this), n = e.data();
            n.offset = n.offset || {}, n.offsetX && (n.offset.x = n.offsetX), n.offsetY && (n.offset.y = n.offsetY), e.affix(n)
        })
    })
}(window.jQuery), !function (t) {
    var e = function (t, e) {
        this.init(t, e)
    };
    e.prototype = {
        constructor: e, init: function (e, n) {
            var i = this.$element = t(e);
            this.options = t.extend({}, t.fn.checkbox.defaults, n), i.before(this.options.template), this.setState()
        }, setState: function () {
            var t = this.$element, e = t.closest(".checkbox");
            t.prop("disabled") && e.addClass("disabled"), t.prop("checked") && e.addClass("checked")
        }, toggle: function () {
            var e = "checked", n = this.$element, i = n.closest(".checkbox"), o = n.prop(e), a = t.Event("toggle");
            0 == n.prop("disabled") && (i.toggleClass(e) && o ? n.removeAttr(e) : n.prop(e, e), n.trigger(a).trigger("change"))
        }, setCheck: function (e) {
            var n = "checked", i = this.$element, o = i.closest(".checkbox"), a = "check" == e ? !0 : !1, r = t.Event(e);
            o[a ? "addClass" : "removeClass"](n) && a ? i.prop(n, n) : i.removeAttr(n), i.trigger(r).trigger("change")
        }
    };
    var n = t.fn.checkbox;
    t.fn.checkbox = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("checkbox"), a = t.extend({}, t.fn.checkbox.defaults, i.data(), "object" == typeof n && n);
            o || i.data("checkbox", o = new e(this, a)), "toggle" == n && o.toggle(), "check" == n || "uncheck" == n ? o.setCheck(n) : n && o.setState()
        })
    }, t.fn.checkbox.defaults = {template: '<span class="icons"><span class="first-icon fui-checkbox-unchecked"></span><span class="second-icon fui-checkbox-checked"></span></span>'}, t.fn.checkbox.noConflict = function () {
        return t.fn.checkbox = n, this
    }, t(document).on("click.checkbox.data-api", "[data-toggle^=checkbox], .checkbox", function (e) {
        var n = t(e.target);
        "A" != e.target.tagName && (e && e.preventDefault() && e.stopPropagation(), n.hasClass("checkbox") || (n = n.closest(".checkbox")), n.find(":checkbox").checkbox("toggle"))
    }), t(function () {
        t('[data-toggle="checkbox"]').each(function () {
            var e = t(this);
            e.checkbox()
        })
    })
}(window.jQuery), !function (t) {
    var e = function (t, e) {
        this.init(t, e)
    };
    e.prototype = {
        constructor: e, init: function (e, n) {
            var i = this.$element = t(e);
            this.options = t.extend({}, t.fn.radio.defaults, n), i.before(this.options.template), this.setState()
        }, setState: function () {
            var t = this.$element, e = t.closest(".radio");
            t.prop("disabled") && e.addClass("disabled"), t.prop("checked") && e.addClass("checked")
        }, toggle: function () {
            var e = "disabled", n = "checked", i = this.$element, o = i.prop(n), a = i.closest(".radio"), r = i.closest(i.closest("form").length ? "form" : "body"), s = r.find(':radio[name="' + i.attr("name") + '"]'), l = t.Event("toggle");
            s.not(i).each(function () {
                var i = t(this), o = t(this).closest(".radio");
                0 == i.prop(e) && o.removeClass(n) && i.removeAttr(n).trigger("change")
            }), 0 == i.prop(e) && (0 == o && a.addClass(n) && i.attr(n, !0), i.trigger(l), o !== i.prop(n) && i.trigger("change"))
        }, setCheck: function (e) {
            var n = "checked", i = this.$element, o = i.closest(".radio"), a = "check" == e ? !0 : !1, r = i.prop(n), s = i.closest(i.closest("form").length ? "form" : "body"), l = s.find(':radio[name="' + i.attr("name") + '"]'), u = t.Event(e);
            l.not(i).each(function () {
                var e = t(this), i = t(this).closest(".radio");
                i.removeClass(n) && e.removeAttr(n)
            }), o[a ? "addClass" : "removeClass"](n) && a ? i.prop(n, n) : i.removeAttr(n), i.trigger(u), r !== i.prop(n) && i.trigger("change")
        }
    };
    var n = t.fn.radio;
    t.fn.radio = function (n) {
        return this.each(function () {
            var i = t(this), o = i.data("radio"), a = t.extend({}, t.fn.radio.defaults, i.data(), "object" == typeof n && n);
            o || i.data("radio", o = new e(this, a)), "toggle" == n && o.toggle(), "check" == n || "uncheck" == n ? o.setCheck(n) : n && o.setState()
        })
    }, t.fn.radio.defaults = {template: '<span class="icons"><span class="first-icon fui-radio-unchecked"></span><span class="second-icon fui-radio-checked"></span></span>'}, t.fn.radio.noConflict = function () {
        return t.fn.radio = n, this
    }, t(document).on("click.radio.data-api", "[data-toggle^=radio], .radio", function (e) {
        var n = t(e.target);
        "A" != e.target.tagName && (e && e.preventDefault() && e.stopPropagation(), n.hasClass("radio") || (n = n.closest(".radio")), n.find(":radio").radio("toggle"))
    }), t(function () {
        t('[data-toggle="radio"]').each(function () {
            var e = t(this);
            e.radio()
        })
    })
}(window.jQuery), function (t) {
    var e = new Array, n = new Array;
    t.fn.doAutosize = function (e) {
        var n = t(this).data("minwidth"), i = t(this).data("maxwidth"), o = "", a = t(this), r = t("#" + t(this).data("tester_id"));
        if (o !== (o = a.val())) {
            var s = o.replace(/&/g, "&amp;").replace(/\s/g, " ").replace(/</g, "&lt;").replace(/>/g, "&gt;");
            r.html(s);
            var l = r.width(), u = l + e.comfortZone >= n ? l + e.comfortZone : n, c = a.width(), d = c > u && u >= n || u > n && i > u;
            d && a.width(u)
        }
    }, t.fn.resetAutosize = function (e) {
        var n = t(this).data("minwidth") || e.minInputWidth || t(this).width(), i = t(this).data("maxwidth") || e.maxInputWidth || t(this).closest(".tagsinput").width() - e.inputPadding, o = t(this), a = t("<tester/>").css({
            position: "absolute",
            top: -9999,
            left: -9999,
            width: "auto",
            fontSize: o.css("fontSize"),
            fontFamily: o.css("fontFamily"),
            fontWeight: o.css("fontWeight"),
            letterSpacing: o.css("letterSpacing"),
            whiteSpace: "nowrap"
        }), r = t(this).attr("id") + "_autosize_tester";
        !t("#" + r).length > 0 && (a.attr("id", r), a.appendTo("body")), o.data("minwidth", n), o.data("maxwidth", i), o.data("tester_id", r), o.css("width", n)
    }, t.fn.addTag = function (i, o) {
        return o = jQuery.extend({focus: !1, callback: !0}, o), this.each(function () {
            var a = t(this).attr("id"), r = t(this).val().split(e[a]);
            if ("" == r[0] && (r = new Array), i = jQuery.trim(i), o.unique) {
                var s = t(this).tagExist(i);
                1 == s && t("#" + a + "_tag").addClass("not_valid")
            } else var s = !1;
            if ("" != i && 1 != s) {
                if (t("<span>").addClass("tag").append(t("<span>").text(i).append("&nbsp;&nbsp;"), t('<a class="tagsinput-remove-link">', {
                        href: "#",
                        title: "Remove tag",
                        text: ""
                    }).click(function () {
                        return t("#" + a).removeTag(escape(i))
                    })).insertBefore("#" + a + "_addTag"), r.push(i), t("#" + a + "_tag").val(""), o.focus ? t("#" + a + "_tag").focus() : t("#" + a + "_tag").blur(), t.fn.tagsInput.updateTagsField(this, r), o.callback && n[a] && n[a].onAddTag) {
                    var l = n[a].onAddTag;
                    l.call(this, i)
                }
                if (n[a] && n[a].onChange) {
                    var u = r.length, l = n[a].onChange;
                    l.call(this, t(this), r[u - 1])
                }
            }
        }), !1
    }, t.fn.removeTag = function (o) {
        return o = unescape(o), this.each(function () {
            var a = t(this).attr("id"), r = t(this).val().split(e[a]);
            for (t("#" + a + "_tagsinput .tag").remove(), str = "", i = 0; i < r.length; i++)r[i] != o && (str = str + e[a] + r[i]);
            if (t.fn.tagsInput.importTags(this, str), n[a] && n[a].onRemoveTag) {
                var s = n[a].onRemoveTag;
                s.call(this, o)
            }
        }), !1
    }, t.fn.tagExist = function (n) {
        var i = t(this).attr("id"), o = t(this).val().split(e[i]);
        return jQuery.inArray(n, o) >= 0
    }, t.fn.importTags = function (e) {
        id = t(this).attr("id"), t("#" + id + "_tagsinput .tag").remove(), t.fn.tagsInput.importTags(this, e)
    }, t.fn.tagsInput = function (i) {
        var o = jQuery.extend({
            interactive: !0,
            defaultText: "",
            minChars: 0,
            width: "",
            height: "",
            autocomplete: {selectFirst: !1},
            hide: !0,
            delimiter: ",",
            unique: !0,
            removeWithBackspace: !0,
            placeholderColor: "#666666",
            autosize: !0,
            comfortZone: 20,
            inputPadding: 12
        }, i);
        return this.each(function () {
            o.hide && t(this).hide();
            var i = t(this).attr("id");
            (!i || e[t(this).attr("id")]) && (i = t(this).attr("id", "tags" + (new Date).getTime()).attr("id"));
            var a = jQuery.extend({
                pid: i,
                real_input: "#" + i,
                holder: "#" + i + "_tagsinput",
                input_wrapper: "#" + i + "_addTag",
                fake_input: "#" + i + "_tag"
            }, o);
            e[i] = a.delimiter, (o.onAddTag || o.onRemoveTag || o.onChange) && (n[i] = new Array, n[i].onAddTag = o.onAddTag, n[i].onRemoveTag = o.onRemoveTag, n[i].onChange = o.onChange);
            var r = t("#" + i).attr("class").replace("tagsinput", ""), s = '<div id="' + i + '_tagsinput" class="tagsinput ' + r + '"><div class="tagsinput-add-container" id="' + i + '_addTag"><div class="tagsinput-add"></div>';
            if (o.interactive && (s = s + '<input id="' + i + '_tag" value="" data-default="' + o.defaultText + '" />'), s += "</div></div>", t(s).insertAfter(this), t(a.holder).css("width", o.width), t(a.holder).css("min-height", o.height), t(a.holder).css("height", "100%"), "" != t(a.real_input).val() && t.fn.tagsInput.importTags(t(a.real_input), t(a.real_input).val()), o.interactive) {
                if (t(a.fake_input).val(t(a.fake_input).attr("data-default")), t(a.fake_input).css("color", o.placeholderColor), t(a.fake_input).resetAutosize(o), t(a.holder).bind("click", a, function (e) {
                        t(e.data.fake_input).focus()
                    }), t(a.fake_input).bind("focus", a, function (e) {
                        t(e.data.fake_input).val() == t(e.data.fake_input).attr("data-default") && t(e.data.fake_input).val(""), t(e.data.fake_input).css("color", "#000000")
                    }), void 0 != o.autocomplete_url) {
                    autocomplete_options = {source: o.autocomplete_url};
                    for (attrname in o.autocomplete)autocomplete_options[attrname] = o.autocomplete[attrname];
                    void 0 !== jQuery.Autocompleter ? (t(a.fake_input).autocomplete(o.autocomplete_url, o.autocomplete), t(a.fake_input).bind("result", a, function (e, n) {
                        n && t("#" + i).addTag(n[0] + "", {focus: !0, unique: o.unique})
                    })) : void 0 !== jQuery.ui.autocomplete && (t(a.fake_input).autocomplete(autocomplete_options), t(a.fake_input).bind("autocompleteselect", a, function (e, n) {
                        return t(e.data.real_input).addTag(n.item.value, {focus: !0, unique: o.unique}), !1
                    }))
                } else t(a.fake_input).bind("blur", a, function (e) {
                    var n = t(this).attr("data-default");
                    return "" != t(e.data.fake_input).val() && t(e.data.fake_input).val() != n ? e.data.minChars <= t(e.data.fake_input).val().length && (!e.data.maxChars || e.data.maxChars >= t(e.data.fake_input).val().length) && t(e.data.real_input).addTag(t(e.data.fake_input).val(), {
                        focus: !0,
                        unique: o.unique
                    }) : (t(e.data.fake_input).val(t(e.data.fake_input).attr("data-default")), t(e.data.fake_input).css("color", o.placeholderColor)), !1
                });
                t(a.fake_input).bind("keypress", a, function (e) {
                    return e.which == e.data.delimiter.charCodeAt(0) || 13 == e.which ? (e.preventDefault(), e.data.minChars <= t(e.data.fake_input).val().length && (!e.data.maxChars || e.data.maxChars >= t(e.data.fake_input).val().length) && t(e.data.real_input).addTag(t(e.data.fake_input).val(), {
                        focus: !0,
                        unique: o.unique
                    }), t(e.data.fake_input).resetAutosize(o), !1) : void(e.data.autosize && t(e.data.fake_input).doAutosize(o))
                }), a.removeWithBackspace && t(a.fake_input).bind("keydown", function (e) {
                    if (8 == e.keyCode && "" == t(this).val()) {
                        e.preventDefault();
                        var n = t(this).closest(".tagsinput").find(".tag:last").text(), i = t(this).attr("id").replace(/_tag$/, "");
                        n = n.replace(/[\s\u00a0]+x$/, ""), t("#" + i).removeTag(escape(n)), t(this).trigger("focus")
                    }
                }), t(a.fake_input).blur(), a.unique && t(a.fake_input).keydown(function (e) {
                    (8 == e.keyCode || String.fromCharCode(e.which).match(/\w+|[\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\xf1\xd1,/]+/)) && t(this).removeClass("not_valid")
                })
            }
        }), this
    }, t.fn.tagsInput.updateTagsField = function (n, i) {
        var o = t(n).attr("id");
        t(n).val(i.join(e[o]))
    }, t.fn.tagsInput.importTags = function (o, a) {
        t(o).val("");
        var r = t(o).attr("id"), s = a.split(e[r]);
        for (i = 0; i < s.length; i++)t(o).addTag(s[i], {focus: !1, callback: !1});
        if (n[r] && n[r].onChange) {
            var l = n[r].onChange;
            l.call(o, o, s[i])
        }
    }
}(jQuery), function (t, e, n) {
    function i(t) {
        var e = {}, i = /^jQuery\d+$/;
        return n.each(t.attributes, function (t, n) {
            n.specified && !i.test(n.name) && (e[n.name] = n.value)
        }), e
    }

    function o(t, i) {
        var o = this, a = n(o);
        if (o.value == a.attr("placeholder") && a.hasClass("placeholder"))if (a.data("placeholder-password")) {
            if (a = a.hide().next().show().attr("id", a.removeAttr("id").data("placeholder-id")), t === !0)return a[0].value = i;
            a.focus()
        } else o.value = "", a.removeClass("placeholder"), o == e.activeElement && o.select()
    }

    function a() {
        var t, e = this, a = n(e), r = this.id;
        if ("" == e.value) {
            if ("password" == e.type) {
                if (!a.data("placeholder-textinput")) {
                    try {
                        t = a.clone().attr({type: "text"})
                    } catch (s) {
                        t = n("<input>").attr(n.extend(i(this), {type: "text"}))
                    }
                    t.removeAttr("name").data({
                        "placeholder-password": !0,
                        "placeholder-id": r
                    }).bind("focus.placeholder", o), a.data({"placeholder-textinput": t, "placeholder-id": r}).before(t)
                }
                a = a.removeAttr("id").hide().prev().attr("id", r).show()
            }
            a.addClass("placeholder"), a[0].value = a.attr("placeholder")
        } else a.removeClass("placeholder")
    }

    var r, s, l = "placeholder" in e.createElement("input"), u = "placeholder" in e.createElement("textarea"), c = n.fn, d = n.valHooks;
    l && u ? (s = c.placeholder = function () {
        return this
    }, s.input = s.textarea = !0) : (s = c.placeholder = function () {
        var t = this;
        return t.filter((l ? "textarea" : ":input") + "[placeholder]").not(".placeholder").bind({
            "focus.placeholder": o,
            "blur.placeholder": a
        }).data("placeholder-enabled", !0).trigger("blur.placeholder"), t
    }, s.input = l, s.textarea = u, r = {
        get: function (t) {
            var e = n(t);
            return e.data("placeholder-enabled") && e.hasClass("placeholder") ? "" : t.value
        }, set: function (t, i) {
            var r = n(t);
            return r.data("placeholder-enabled") ? ("" == i ? (t.value = i, t != e.activeElement && a.call(t)) : r.hasClass("placeholder") ? o.call(t, !0, i) || (t.value = i) : t.value = i, r) : t.value = i
        }
    }, l || (d.input = r), u || (d.textarea = r), n(function () {
        n(e).delegate("form", "submit.placeholder", function () {
            var t = n(".placeholder", this).each(o);
            setTimeout(function () {
                t.each(a)
            }, 10)
        })
    }), n(t).bind("beforeunload.placeholder", function () {
        n(".placeholder").each(function () {
            this.value = ""
        })
    }))
}(this, document, jQuery), function (t) {
    t.fn.stacktable = function (e) {
        var n = this, i = {id: "stacktable", hideOriginal: !1}, o = t.extend({}, i, e);
        return n.each(function () {
            var e = t('<table class="' + o.id + '"><tbody></tbody></table>');
            void 0 !== typeof o.myClass && e.addClass(o.myClass);
            var n = "";
            $table = t(this), $topRow = $table.find("tr").eq(0), $table.find("tr").each(function (e) {
                var i = "";
                i = e % 2 === 0 ? "even" : "odd", n += '<tr class="' + i + '">', t(this).find("td").each(function (e) {
                    "" !== t(this).html() && (n += '<tr class="' + i + '">', n += $topRow.find("td,th").eq(e).html() ? "<td>" + $topRow.find("td,th").eq(e).html() + "</td>" : "<td></td>", n += "<td>" + t(this).html() + "</td>", n += "</tr>")
                })
            }), e.append(t(n)), $table.before(e), o.hideOriginal && $table.hide()
        })
    }
}(jQuery), $(function () {
    function t() {
        return n++, n > 100 ? (clearInterval(e), !0) : void $("#counter").html(n + "%")
    }

    var e = setInterval(t, 2e3), n = 0
}), GetRTXUserInfo = function () {
    var t = {UserName: "", Sign: ""};
    if (window.ActiveXObject)try {
        var e = new ActiveXObject("RTXClient.RTXAPI"), n = e.GetObject("KernalRoot");
        t.UserName = n.Account;
        var i = n.Sign;
        return t.Sign = i.GetString("Sign"), t
    } catch (o) {
        return alert("\u63d0\u793a\uff1a\u8bf7\u4f7f\u7528IE\u6d4f\u89c8\u5668\u5e76\u4e14\u786e\u4fdd\u5b89\u88c5\u4e86RTX\u8f6f\u4ef6\uff01 "), !1
    }
    return !0
}, CallIMToChat = function (t) {
    if (null == t || "" == t)return alert("\u63d0\u793a\uff1a\u63a5\u6536\u4eba\u4e0d\u80fd\u4e3a\u7a7a\uff01"), !1;
    try {
        var e = new ActiveXObject("RTXClient.RTXAPI"), n = e.GetObject("KernalRoot");
        if (t == n.Account)return alert("\u63d0\u793a\uff1a\u4e0d\u80fd\u7ed9\u81ea\u5df1\u53d1RTX\u6d88\u606f\uff01"), !1;
        var i = e.GetObject("AppRoot"), o = i.GetAppObject("RTXPlugin.IM");
        return o.SendIM(t, "", ""), !0
    } catch (a) {
        return alert("\u63d0\u793a\uff1a\u672a\u80fd\u542f\u52a8RTX\u5bf9\u8bdd\u7a97\u53e3\uff01\u8bf7\u4f7f\u7528IE\u6d4f\u89c8\u5668\u5e76\u4e14\u786e\u4fdd\u5b89\u88c5\u4e86RTX\u8f6f\u4ef6\uff01 "), !1
    }
}, String.prototype.repeat = function (t) {
    return new Array(t + 1).join(this)
}, function (t) {
    t.fn.addSliderSegments = function (e) {
        return this.each(function () {
            var n = 100 / (e - 1) + "%", i = "<div class='ui-slider-segment' style='margin-left: " + n + ";'></div>";
            t(this).prepend(i.repeat(e - 2))
        })
    }, t(function () {
        t(".todo li").click(function () {
            t(this).toggleClass("todo-done")
        }), t("select[name='huge']").selectpicker({
            style: "btn-hg btn-primary",
            menuStyle: "dropdown-inverse"
        }), t("select[name='herolist']").selectpicker({
            style: "btn-primary",
            menuStyle: "dropdown-inverse"
        }), t("select[name='info']").selectpicker({style: "btn-info"}), t("[data-toggle=tooltip]").tooltip("show"), t(".tagsinput").tagsInput();
        var e = t("#slider");
        e.length && e.slider({
            min: 1,
            max: 5,
            value: 2,
            orientation: "horizontal",
            range: "min"
        }).addSliderSegments(e.slider("option").max), t("input, textarea").placeholder(), t(".pagination a").on("click", function () {
            t(this).parent().siblings("li").removeClass("active").end().addClass("active")
        }), t(".btn-group a").on("click", function () {
            t(this).siblings().removeClass("active").end().addClass("active")
        }), t('a[href="#fakelink"]').on("click", function (t) {
            t.preventDefault()
        }), t("[data-toggle='switch']").wrap('<div class="switch" />').parent().bootstrapSwitch()
    })
}(jQuery), function (t, e) {
    function n() {
        var t = m.elements;
        return "string" == typeof t ? t.split(" ") : t
    }

    function i(t) {
        var e = p[t[h]];
        return e || (e = {}, f++, t[h] = f, p[f] = e), e
    }

    function o(t, n, o) {
        return n || (n = e), l ? n.createElement(t) : (o || (o = i(n)), n = o.cache[t] ? o.cache[t].cloneNode() : d.test(t) ? (o.cache[t] = o.createElem(t)).cloneNode() : o.createElem(t), n.canHaveChildren && !c.test(t) ? o.frag.appendChild(n) : n)
    }

    function a(t, e) {
        e.cache || (e.cache = {}, e.createElem = t.createElement, e.createFrag = t.createDocumentFragment, e.frag = e.createFrag()), t.createElement = function (n) {
            return m.shivMethods ? o(n, t, e) : e.createElem(n)
        }, t.createDocumentFragment = Function("h,f", "return function(){var n=f.cloneNode(),c=n.createElement;h.shivMethods&&(" + n().join().replace(/\w+/g, function (t) {
                return e.createElem(t), e.frag.createElement(t), 'c("' + t + '")'
            }) + ");return n}")(m, e.frag)
    }

    function r(t) {
        t || (t = e);
        var n = i(t);
        if (m.shivCSS && !s && !n.hasCSS) {
            var o, r = t;
            o = r.createElement("p"), r = r.getElementsByTagName("head")[0] || r.documentElement, o.innerHTML = "x<style>article,aside,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}mark{background:#FF0;color:#000}</style>", o = r.insertBefore(o.lastChild, r.firstChild), n.hasCSS = !!o
        }
        return l || a(t, n), t
    }

    var s, l, u = t.html5 || {}, c = /^<|^(?:button|map|select|textarea|object|iframe|option|optgroup)$/i, d = /^(?:a|b|code|div|fieldset|h1|h2|h3|h4|h5|h6|i|label|li|ol|p|q|span|strong|style|table|tbody|td|th|tr|ul)$/i, h = "_html5shiv", f = 0, p = {};
    !function () {
        try {
            var t = e.createElement("a");
            t.innerHTML = "<xyz></xyz>", s = "hidden" in t;
            var n;
            if (!(n = 1 == t.childNodes.length)) {
                e.createElement("a");
                var i = e.createDocumentFragment();
                n = "undefined" == typeof i.cloneNode || "undefined" == typeof i.createDocumentFragment || "undefined" == typeof i.createElement
            }
            l = n
        } catch (o) {
            l = s = !0
        }
    }();
    var m = {
        elements: u.elements || "abbr article aside audio bdi canvas data datalist details figcaption figure footer header hgroup main mark meter nav output progress section summary time video",
        version: "3.6.2",
        shivCSS: !1 !== u.shivCSS,
        supportsUnknownElements: l,
        shivMethods: !1 !== u.shivMethods,
        type: "default",
        shivDocument: r,
        createElement: o,
        createDocumentFragment: function (t, o) {
            if (t || (t = e), l)return t.createDocumentFragment();
            for (var o = o || i(t), a = o.frag.cloneNode(), r = 0, s = n(), u = s.length; u > r; r++)a.createElement(s[r]);
            return a
        }
    };
    t.html5 = m, r(e)
}(this, document), function (t) {
    "function" == typeof define && define.amd ? define(["jquery"], t) : t(jQuery)
}(function (t, e) {
    var n = 0, i = Array.prototype.slice, o = t.cleanData;
    t.cleanData = function (e) {
        for (var n, i = 0; null != (n = e[i]); i++)try {
            t(n).triggerHandler("remove")
        } catch (a) {
        }
        o(e)
    }, t.widget = function (e, n, i) {
        var o, a, r, s, l = {}, u = e.split(".")[0];
        e = e.split(".")[1], o = u + "-" + e, i || (i = n, n = t.Widget), t.expr[":"][o.toLowerCase()] = function (e) {
            return !!t.data(e, o)
        }, t[u] = t[u] || {}, a = t[u][e], r = t[u][e] = function (t, e) {
            return this._createWidget ? void(arguments.length && this._createWidget(t, e)) : new r(t, e)
        }, t.extend(r, a, {
            version: i.version,
            _proto: t.extend({}, i),
            _childConstructors: []
        }), s = new n, s.options = t.widget.extend({}, s.options), t.each(i, function (e, i) {
            return t.isFunction(i) ? void(l[e] = function () {
                var t = function () {
                    return n.prototype[e].apply(this, arguments)
                }, o = function (t) {
                    return n.prototype[e].apply(this, t)
                };
                return function () {
                    var e, n = this._super, a = this._superApply;
                    return this._super = t, this._superApply = o, e = i.apply(this, arguments), this._super = n, this._superApply = a, e
                }
            }()) : void(l[e] = i)
        }), r.prototype = t.widget.extend(s, {widgetEventPrefix: a ? s.widgetEventPrefix : e}, l, {
            constructor: r,
            namespace: u,
            widgetName: e,
            widgetFullName: o
        }), a ? (t.each(a._childConstructors, function (e, n) {
            var i = n.prototype;
            t.widget(i.namespace + "." + i.widgetName, r, n._proto)
        }), delete a._childConstructors) : n._childConstructors.push(r), t.widget.bridge(e, r)
    }, t.widget.extend = function (n) {
        for (var o, a, r = i.call(arguments, 1), s = 0, l = r.length; l > s; s++)for (o in r[s])a = r[s][o], r[s].hasOwnProperty(o) && a !== e && (n[o] = t.isPlainObject(a) ? t.isPlainObject(n[o]) ? t.widget.extend({}, n[o], a) : t.widget.extend({}, a) : a);
        return n
    }, t.widget.bridge = function (n, o) {
        var a = o.prototype.widgetFullName || n;
        t.fn[n] = function (r) {
            var s = "string" == typeof r, l = i.call(arguments, 1), u = this;
            return r = !s && l.length ? t.widget.extend.apply(null, [r].concat(l)) : r, this.each(s ? function () {
                var i, o = t.data(this, a);
                return o ? t.isFunction(o[r]) && "_" !== r.charAt(0) ? (i = o[r].apply(o, l), i !== o && i !== e ? (u = i && i.jquery ? u.pushStack(i.get()) : i, !1) : void 0) : t.error("no such method '" + r + "' for " + n + " widget instance") : t.error("cannot call methods on " + n + " prior to initialization; attempted to call method '" + r + "'")
            } : function () {
                var e = t.data(this, a);
                e ? e.option(r || {})._init() : t.data(this, a, new o(r, this))
            }), u
        }
    }, t.Widget = function () {
    }, t.Widget._childConstructors = [], t.Widget.prototype = {
        widgetName: "widget",
        widgetEventPrefix: "",
        defaultElement: "<div>",
        options: {disabled: !1, create: null},
        _createWidget: function (e, i) {
            i = t(i || this.defaultElement || this)[0], this.element = t(i), this.uuid = n++, this.eventNamespace = "." + this.widgetName + this.uuid, this.options = t.widget.extend({}, this.options, this._getCreateOptions(), e), this.bindings = t(), this.hoverable = t(), this.focusable = t(), i !== this && (t.data(i, this.widgetFullName, this), this._on(!0, this.element, {
                remove: function (t) {
                    t.target === i && this.destroy()
                }
            }), this.document = t(i.style ? i.ownerDocument : i.document || i), this.window = t(this.document[0].defaultView || this.document[0].parentWindow)), this._create(), this._trigger("create", null, this._getCreateEventData()), this._init()
        },
        _getCreateOptions: t.noop,
        _getCreateEventData: t.noop,
        _create: t.noop,
        _init: t.noop,
        destroy: function () {
            this._destroy(), this.element.unbind(this.eventNamespace).removeData(this.widgetName).removeData(this.widgetFullName).removeData(t.camelCase(this.widgetFullName)), this.widget().unbind(this.eventNamespace).removeAttr("aria-disabled").removeClass(this.widgetFullName + "-disabled ui-state-disabled"), this.bindings.unbind(this.eventNamespace), this.hoverable.removeClass("ui-state-hover"), this.focusable.removeClass("ui-state-focus")
        },
        _destroy: t.noop,
        widget: function () {
            return this.element
        },
        option: function (n, i) {
            var o, a, r, s = n;
            if (0 === arguments.length)return t.widget.extend({}, this.options);
            if ("string" == typeof n)if (s = {}, o = n.split("."), n = o.shift(), o.length) {
                for (a = s[n] = t.widget.extend({}, this.options[n]), r = 0; r < o.length - 1; r++)a[o[r]] = a[o[r]] || {}, a = a[o[r]];
                if (n = o.pop(), i === e)return a[n] === e ? null : a[n];
                a[n] = i
            } else {
                if (i === e)return this.options[n] === e ? null : this.options[n];
                s[n] = i
            }
            return this._setOptions(s), this
        },
        _setOptions: function (t) {
            var e;
            for (e in t)this._setOption(e, t[e]);
            return this
        },
        _setOption: function (t, e) {
            return this.options[t] = e, "disabled" === t && (this.widget().toggleClass(this.widgetFullName + "-disabled ui-state-disabled", !!e).attr("aria-disabled", e), this.hoverable.removeClass("ui-state-hover"), this.focusable.removeClass("ui-state-focus")), this
        },
        enable: function () {
            return this._setOption("disabled", !1)
        },
        disable: function () {
            return this._setOption("disabled", !0)
        },
        _on: function (e, n, i) {
            var o, a = this;
            "boolean" != typeof e && (i = n, n = e, e = !1), i ? (n = o = t(n), this.bindings = this.bindings.add(n)) : (i = n, n = this.element, o = this.widget()), t.each(i, function (i, r) {
                function s() {
                    return e || a.options.disabled !== !0 && !t(this).hasClass("ui-state-disabled") ? ("string" == typeof r ? a[r] : r).apply(a, arguments) : void 0
                }

                "string" != typeof r && (s.guid = r.guid = r.guid || s.guid || t.guid++);
                var l = i.match(/^(\w+)\s*(.*)$/), u = l[1] + a.eventNamespace, c = l[2];
                c ? o.delegate(c, u, s) : n.bind(u, s)
            })
        },
        _off: function (t, e) {
            e = (e || "").split(" ").join(this.eventNamespace + " ") + this.eventNamespace, t.unbind(e).undelegate(e)
        },
        _delay: function (t, e) {
            function n() {
                return ("string" == typeof t ? i[t] : t).apply(i, arguments)
            }

            var i = this;
            return setTimeout(n, e || 0)
        },
        _hoverable: function (e) {
            this.hoverable = this.hoverable.add(e), this._on(e, {
                mouseenter: function (e) {
                    t(e.currentTarget).addClass("ui-state-hover")
                }, mouseleave: function (e) {
                    t(e.currentTarget).removeClass("ui-state-hover")
                }
            })
        },
        _focusable: function (e) {
            this.focusable = this.focusable.add(e), this._on(e, {
                focusin: function (e) {
                    t(e.currentTarget).addClass("ui-state-focus")
                }, focusout: function (e) {
                    t(e.currentTarget).removeClass("ui-state-focus")
                }
            })
        },
        _trigger: function (e, n, i) {
            var o, a, r = this.options[e];
            if (i = i || {}, n = t.Event(n), n.type = (e === this.widgetEventPrefix ? e : this.widgetEventPrefix + e).toLowerCase(), n.target = this.element[0], a = n.originalEvent)for (o in a)o in n || (n[o] = a[o]);
            return this.element.trigger(n, i), !(t.isFunction(r) && r.apply(this.element[0], [n].concat(i)) === !1 || n.isDefaultPrevented())
        }
    }, t.each({show: "fadeIn", hide: "fadeOut"}, function (e, n) {
        t.Widget.prototype["_" + e] = function (i, o, a) {
            "string" == typeof o && (o = {effect: o});
            var r, s = o ? o === !0 || "number" == typeof o ? n : o.effect || n : e;
            o = o || {}, "number" == typeof o && (o = {duration: o}), r = !t.isEmptyObject(o), o.complete = a, o.delay && i.delay(o.delay), r && t.effects && t.effects.effect[s] ? i[e](o) : s !== e && i[s] ? i[s](o.duration, o.easing, a) : i.queue(function (n) {
                t(this)[e](), a && a.call(i[0]), n()
            })
        }
    })
}), function (t) {
    "use strict";
    "function" == typeof define && define.amd ? define(["jquery"], t) : t(window.jQuery)
}(function (t) {
    "use strict";
    var e = 0;
    t.ajaxTransport("iframe", function (n) {
        if (n.async) {
            var i, o, a;
            return {
                send: function (r, s) {
                    i = t('<form style="display:none;"></form>'), i.attr("accept-charset", n.formAcceptCharset), a = /\?/.test(n.url) ? "&" : "?", "DELETE" === n.type ? (n.url = n.url + a + "_method=DELETE", n.type = "POST") : "PUT" === n.type ? (n.url = n.url + a + "_method=PUT", n.type = "POST") : "PATCH" === n.type && (n.url = n.url + a + "_method=PATCH", n.type = "POST"), o = t('<iframe src="javascript:false;" name="iframe-transport-' + (e += 1) + '"></iframe>').bind("load", function () {
                        var e, a = t.isArray(n.paramName) ? n.paramName : [n.paramName];
                        o.unbind("load").bind("load", function () {
                            var e;
                            try {
                                if (e = o.contents(), !e.length || !e[0].firstChild)throw new Error
                            } catch (n) {
                                e = void 0
                            }
                            s(200, "success", {iframe: e}), t('<iframe src="javascript:false;"></iframe>').appendTo(i), i.remove()
                        }), i.prop("target", o.prop("name")).prop("action", n.url).prop("method", n.type), n.formData && t.each(n.formData, function (e, n) {
                            t('<input type="hidden"/>').prop("name", n.name).val(n.value).appendTo(i)
                        }), n.fileInput && n.fileInput.length && "POST" === n.type && (e = n.fileInput.clone(), n.fileInput.after(function (t) {
                            return e[t]
                        }), n.paramName && n.fileInput.each(function (e) {
                            t(this).prop("name", a[e] || n.paramName)
                        }), i.append(n.fileInput).prop("enctype", "multipart/form-data").prop("encoding", "multipart/form-data")), i.submit(), e && e.length && n.fileInput.each(function (n, i) {
                            var o = t(e[n]);
                            t(i).prop("name", o.prop("name")), o.replaceWith(i)
                        })
                    }), i.append(o).appendTo(document.body)
                }, abort: function () {
                    o && o.unbind("load").prop("src", "javascript".concat(":false;")), i && i.remove()
                }
            }
        }
    }), t.ajaxSetup({
        converters: {
            "iframe text": function (e) {
                return e && t(e[0].body).text()
            }, "iframe json": function (e) {
                return e && t.parseJSON(t(e[0].body).text())
            }, "iframe html": function (e) {
                return e && t(e[0].body).html()
            }, "iframe script": function (e) {
                return e && t.globalEval(t(e[0].body).text())
            }
        }
    })
}), function (t) {
    "use strict";
    "function" == typeof define && define.amd ? define(["jquery", "jquery.ui.widget"], t) : t(window.jQuery)
}(function (t) {
    "use strict";
    t.support.xhrFileUpload = !(!window.XMLHttpRequestUpload || !window.FileReader), t.support.xhrFormDataFileUpload = !!window.FormData, t.propHooks.elements = {
        get: function (e) {
            return t.nodeName(e, "form") ? t.grep(e.elements, function (e) {
                return !t.nodeName(e, "input") || "file" !== e.type
            }) : null
        }
    }, t.widget("blueimp.fileupload", {
        options: {
            dropZone: t(document),
            pasteZone: t(document),
            fileInput: void 0,
            replaceFileInput: !0,
            paramName: void 0,
            singleFileUploads: !0,
            limitMultiFileUploads: void 0,
            sequentialUploads: !1,
            limitConcurrentUploads: void 0,
            forceIframeTransport: !1,
            redirect: void 0,
            redirectParamName: void 0,
            postMessage: void 0,
            multipart: !0,
            maxChunkSize: void 0,
            uploadedBytes: void 0,
            recalculateProgress: !0,
            progressInterval: 100,
            bitrateInterval: 500,
            formData: function (t) {
                return t.serializeArray()
            },
            add: function (t, e) {
                e.submit()
            },
            processData: !1,
            contentType: !1,
            cache: !1
        },
        _refreshOptionsList: ["fileInput", "dropZone", "pasteZone", "multipart", "forceIframeTransport"],
        _BitrateTimer: function () {
            this.timestamp = +new Date, this.loaded = 0, this.bitrate = 0, this.getBitrate = function (t, e, n) {
                var i = t - this.timestamp;
                return (!this.bitrate || !n || i > n) && (this.bitrate = (e - this.loaded) * (1e3 / i) * 8, this.loaded = e, this.timestamp = t), this.bitrate
            }
        },
        _isXHRUpload: function (e) {
            return !e.forceIframeTransport && (!e.multipart && t.support.xhrFileUpload || t.support.xhrFormDataFileUpload)
        },
        _getFormData: function (e) {
            var n;
            return "function" == typeof e.formData ? e.formData(e.form) : t.isArray(e.formData) ? e.formData : e.formData ? (n = [], t.each(e.formData, function (t, e) {
                n.push({name: t, value: e})
            }), n) : []
        },
        _getTotal: function (e) {
            var n = 0;
            return t.each(e, function (t, e) {
                n += e.size || 1
            }), n
        },
        _onProgress: function (t, e) {
            if (t.lengthComputable) {
                var n, i, o = +new Date;
                if (e._time && e.progressInterval && o - e._time < e.progressInterval && t.loaded !== t.total)return;
                e._time = o, n = e.total || this._getTotal(e.files), i = parseInt(t.loaded / t.total * (e.chunkSize || n), 10) + (e.uploadedBytes || 0), this._loaded += i - (e.loaded || e.uploadedBytes || 0), e.lengthComputable = !0, e.loaded = i, e.total = n, e.bitrate = e._bitrateTimer.getBitrate(o, i, e.bitrateInterval), this._trigger("progress", t, e), this._trigger("progressall", t, {
                    lengthComputable: !0,
                    loaded: this._loaded,
                    total: this._total,
                    bitrate: this._bitrateTimer.getBitrate(o, this._loaded, e.bitrateInterval)
                })
            }
        },
        _initProgressListener: function (e) {
            var n = this, i = e.xhr ? e.xhr() : t.ajaxSettings.xhr();
            i.upload && (t(i.upload).bind("progress", function (t) {
                var i = t.originalEvent;
                t.lengthComputable = i.lengthComputable, t.loaded = i.loaded, t.total = i.total, n._onProgress(t, e)
            }), e.xhr = function () {
                return i
            })
        },
        _initXHRData: function (e) {
            var n, i = e.files[0], o = e.multipart || !t.support.xhrFileUpload, a = e.paramName[0];
            e.headers = e.headers || {}, e.contentRange && (e.headers["Content-Range"] = e.contentRange), o ? t.support.xhrFormDataFileUpload && (e.postMessage ? (n = this._getFormData(e), e.blob ? n.push({
                name: a,
                value: e.blob
            }) : t.each(e.files, function (t, i) {
                n.push({name: e.paramName[t] || a, value: i})
            })) : (e.formData instanceof FormData ? n = e.formData : (n = new FormData, t.each(this._getFormData(e), function (t, e) {
                n.append(e.name, e.value)
            })), e.blob ? (e.headers["Content-Disposition"] = 'attachment; filename="' + encodeURI(i.name) + '"', n.append(a, e.blob, i.name)) : t.each(e.files, function (t, i) {
                (window.Blob && i instanceof Blob || window.File && i instanceof File) && n.append(e.paramName[t] || a, i, i.name)
            })), e.data = n) : (e.headers["Content-Disposition"] = 'attachment; filename="' + encodeURI(i.name) + '"', e.contentType = i.type, e.data = e.blob || i), e.blob = null
        },
        _initIframeSettings: function (e) {
            e.dataType = "iframe " + (e.dataType || ""), e.formData = this._getFormData(e), e.redirect && t("<a></a>").prop("href", e.url).prop("host") !== location.host && e.formData.push({
                name: e.redirectParamName || "redirect",
                value: e.redirect
            })
        },
        _initDataSettings: function (t) {
            this._isXHRUpload(t) ? (this._chunkedUpload(t, !0) || (t.data || this._initXHRData(t), this._initProgressListener(t)), t.postMessage && (t.dataType = "postmessage " + (t.dataType || ""))) : this._initIframeSettings(t, "iframe")
        },
        _getParamName: function (e) {
            var n = t(e.fileInput), i = e.paramName;
            return i ? t.isArray(i) || (i = [i]) : (i = [], n.each(function () {
                for (var e = t(this), n = e.prop("name") || "files[]", o = (e.prop("files") || [1]).length; o;)i.push(n), o -= 1
            }), i.length || (i = [n.prop("name") || "files[]"])), i
        },
        _initFormSettings: function (e) {
            e.form && e.form.length || (e.form = t(e.fileInput.prop("form")), e.form.length || (e.form = t(this.options.fileInput.prop("form")))), e.paramName = this._getParamName(e), e.url || (e.url = e.form.prop("action") || location.href), e.type = (e.type || e.form.prop("method") || "").toUpperCase(), "POST" !== e.type && "PUT" !== e.type && "PATCH" !== e.type && (e.type = "POST"), e.formAcceptCharset || (e.formAcceptCharset = e.form.attr("accept-charset"))
        },
        _getAJAXSettings: function (e) {
            var n = t.extend({}, this.options, e);
            return this._initFormSettings(n), this._initDataSettings(n), n
        },
        _enhancePromise: function (t) {
            return t.success = t.done, t.error = t.fail, t.complete = t.always, t
        },
        _getXHRPromise: function (e, n, i) {
            var o = t.Deferred(), a = o.promise();
            return n = n || this.options.context || a, e === !0 ? o.resolveWith(n, i) : e === !1 && o.rejectWith(n, i), a.abort = o.promise, this._enhancePromise(a)
        },
        _getUploadedBytes: function (t) {
            var e = t.getResponseHeader("Range"), n = e && e.split("-"), i = n && n.length > 1 && parseInt(n[1], 10);
            return i && i + 1
        },
        _chunkedUpload: function (e, n) {
            var i, o, a = this, r = e.files[0], s = r.size, l = e.uploadedBytes = e.uploadedBytes || 0, u = e.maxChunkSize || s, c = r.slice || r.webkitSlice || r.mozSlice, d = t.Deferred(), h = d.promise();
            return this._isXHRUpload(e) && c && (l || s > u) && !e.data ? n ? !0 : l >= s ? (r.error = "Uploaded bytes exceed file size", this._getXHRPromise(!1, e.context, [null, "error", r.error])) : (o = function () {
                var n = t.extend({}, e);
                n.blob = c.call(r, l, l + u, r.type), n.chunkSize = n.blob.size, n.contentRange = "bytes " + l + "-" + (l + n.chunkSize - 1) + "/" + s, a._initXHRData(n), a._initProgressListener(n), i = (a._trigger("chunksend", null, n) !== !1 && t.ajax(n) || a._getXHRPromise(!1, n.context)).done(function (i, r, u) {
                    l = a._getUploadedBytes(u) || l + n.chunkSize, (!n.loaded || n.loaded < n.total) && a._onProgress(t.Event("progress", {
                        lengthComputable: !0,
                        loaded: l - n.uploadedBytes,
                        total: l - n.uploadedBytes
                    }), n), e.uploadedBytes = n.uploadedBytes = l, n.result = i, n.textStatus = r, n.jqXHR = u, a._trigger("chunkdone", null, n), a._trigger("chunkalways", null, n), s > l ? o() : d.resolveWith(n.context, [i, r, u])
                }).fail(function (t, e, i) {
                    n.jqXHR = t, n.textStatus = e, n.errorThrown = i, a._trigger("chunkfail", null, n), a._trigger("chunkalways", null, n), d.rejectWith(n.context, [t, e, i])
                })
            }, this._enhancePromise(h), h.abort = function () {
                return i.abort()
            }, o(), h) : !1
        },
        _beforeSend: function (t, e) {
            0 === this._active && (this._trigger("start"), this._bitrateTimer = new this._BitrateTimer), this._active += 1, this._loaded += e.uploadedBytes || 0, this._total += this._getTotal(e.files)
        },
        _onDone: function (e, n, i, o) {
            if (!this._isXHRUpload(o) || !o.loaded || o.loaded < o.total) {
                var a = this._getTotal(o.files) || 1;
                this._onProgress(t.Event("progress", {lengthComputable: !0, loaded: a, total: a}), o)
            }
            o.result = e, o.textStatus = n, o.jqXHR = i, this._trigger("done", null, o)
        },
        _onFail: function (t, e, n, i) {
            i.jqXHR = t, i.textStatus = e, i.errorThrown = n, this._trigger("fail", null, i), i.recalculateProgress && (this._loaded -= i.loaded || i.uploadedBytes || 0, this._total -= i.total || this._getTotal(i.files))
        },
        _onAlways: function (t, e, n, i) {
            this._active -= 1, this._trigger("always", null, i), 0 === this._active && (this._trigger("stop"), this._loaded = this._total = 0, this._bitrateTimer = null)
        },
        _onSend: function (e, n) {
            var i, o, a, r, s = this, l = s._getAJAXSettings(n), u = function () {
                return s._sending += 1, l._bitrateTimer = new s._BitrateTimer, i = i || ((o || s._trigger("send", e, l) === !1) && s._getXHRPromise(!1, l.context, o) || s._chunkedUpload(l) || t.ajax(l)).done(function (t, e, n) {
                        s._onDone(t, e, n, l)
                    }).fail(function (t, e, n) {
                        s._onFail(t, e, n, l)
                    }).always(function (t, e, n) {
                        if (s._sending -= 1, s._onAlways(t, e, n, l), l.limitConcurrentUploads && l.limitConcurrentUploads > s._sending)for (var i, o = s._slots.shift(); o;) {
                            if (i = o.state ? "pending" === o.state() : !o.isRejected()) {
                                o.resolve();
                                break
                            }
                            o = s._slots.shift()
                        }
                    })
            };
            return this._beforeSend(e, l), this.options.sequentialUploads || this.options.limitConcurrentUploads && this.options.limitConcurrentUploads <= this._sending ? (this.options.limitConcurrentUploads > 1 ? (a = t.Deferred(), this._slots.push(a), r = a.pipe(u)) : r = this._sequence = this._sequence.pipe(u, u), r.abort = function () {
                return o = [void 0, "abort", "abort"], i ? i.abort() : (a && a.rejectWith(l.context, o), u())
            }, this._enhancePromise(r)) : u()
        },
        _onAdd: function (e, n) {
            var i, o, a, r, s = this, l = !0, u = t.extend({}, this.options, n), c = u.limitMultiFileUploads, d = this._getParamName(u);
            if ((u.singleFileUploads || c) && this._isXHRUpload(u))if (!u.singleFileUploads && c)for (a = [], i = [], r = 0; r < n.files.length; r += c)a.push(n.files.slice(r, r + c)), o = d.slice(r, r + c), o.length || (o = d), i.push(o); else i = d; else a = [n.files], i = [d];
            return n.originalFiles = n.files, t.each(a || n.files, function (o, r) {
                var u = t.extend({}, n);
                return u.files = a ? r : [r], u.paramName = i[o], u.submit = function () {
                    return u.jqXHR = this.jqXHR = s._trigger("submit", e, this) !== !1 && s._onSend(e, this), this.jqXHR
                }, l = s._trigger("add", e, u)
            }), l
        },
        _replaceFileInput: function (e) {
            var n = e.clone(!0);
            t("<form></form>").append(n)[0].reset(), e.after(n).detach(), t.cleanData(e.unbind("remove")), this.options.fileInput = this.options.fileInput.map(function (t, i) {
                return i === e[0] ? n[0] : i
            }), e[0] === this.element[0] && (this.element = n)
        },
        _handleFileTreeEntry: function (e, n) {
            var i, o = this, a = t.Deferred(), r = function (t) {
                t && !t.entry && (t.entry = e), a.resolve([t])
            };
            return n = n || "", e.isFile ? e._file ? (e._file.relativePath = n, a.resolve(e._file)) : e.file(function (t) {
                t.relativePath = n, a.resolve(t)
            }, r) : e.isDirectory ? (i = e.createReader(), i.readEntries(function (t) {
                o._handleFileTreeEntries(t, n + e.name + "/").done(function (t) {
                    a.resolve(t)
                }).fail(r)
            }, r)) : a.resolve([]), a.promise()
        },
        _handleFileTreeEntries: function (e, n) {
            var i = this;
            return t.when.apply(t, t.map(e, function (t) {
                return i._handleFileTreeEntry(t, n)
            })).pipe(function () {
                return Array.prototype.concat.apply([], arguments)
            })
        },
        _getDroppedFiles: function (e) {
            e = e || {};
            var n = e.items;
            return n && n.length && (n[0].webkitGetAsEntry || n[0].getAsEntry) ? this._handleFileTreeEntries(t.map(n, function (t) {
                var e;
                return t.webkitGetAsEntry ? (e = t.webkitGetAsEntry(), e && (e._file = t.getAsFile()), e) : t.getAsEntry()
            })) : t.Deferred().resolve(t.makeArray(e.files)).promise()
        },
        _getSingleFileInputFiles: function (e) {
            e = t(e);
            var n, i, o = e.prop("webkitEntries") || e.prop("entries");
            if (o && o.length)return this._handleFileTreeEntries(o);
            if (n = t.makeArray(e.prop("files")), n.length)void 0 === n[0].name && n[0].fileName && t.each(n, function (t, e) {
                e.name = e.fileName, e.size = e.fileSize
            }); else {
                if (i = e.prop("value"), !i)return t.Deferred().resolve([]).promise();
                n = [{name: i.replace(/^.*\\/, "")}]
            }
            return t.Deferred().resolve(n).promise()
        },
        _getFileInputFiles: function (e) {
            return e instanceof t && 1 !== e.length ? t.when.apply(t, t.map(e, this._getSingleFileInputFiles)).pipe(function () {
                return Array.prototype.concat.apply([], arguments)
            }) : this._getSingleFileInputFiles(e)
        },
        _onChange: function (e) {
            var n = this, i = {fileInput: t(e.target), form: t(e.target.form)};
            this._getFileInputFiles(i.fileInput).always(function (t) {
                i.files = t, n.options.replaceFileInput && n._replaceFileInput(i.fileInput), n._trigger("change", e, i) !== !1 && n._onAdd(e, i)
            })
        },
        _onPaste: function (e) {
            var n = e.originalEvent.clipboardData, i = n && n.items || [], o = {files: []};
            return t.each(i, function (t, e) {
                var n = e.getAsFile && e.getAsFile();
                n && o.files.push(n)
            }), this._trigger("paste", e, o) === !1 || this._onAdd(e, o) === !1 ? !1 : void 0
        },
        _onDrop: function (t) {
            var e = this, n = t.dataTransfer = t.originalEvent.dataTransfer, i = {};
            n && n.files && n.files.length && t.preventDefault(), this._getDroppedFiles(n).always(function (n) {
                i.files = n, e._trigger("drop", t, i) !== !1 && e._onAdd(t, i)
            })
        },
        _onDragOver: function (e) {
            var n = e.dataTransfer = e.originalEvent.dataTransfer;
            return this._trigger("dragover", e) === !1 ? !1 : void(n && -1 !== t.inArray("Files", n.types) && (n.dropEffect = "copy", e.preventDefault()))
        },
        _initEventHandlers: function () {
            this._isXHRUpload(this.options) && (this._on(this.options.dropZone, {
                dragover: this._onDragOver,
                drop: this._onDrop
            }), this._on(this.options.pasteZone, {paste: this._onPaste})), this._on(this.options.fileInput, {change: this._onChange})
        },
        _destroyEventHandlers: function () {
            this._off(this.options.dropZone, "dragover drop"), this._off(this.options.pasteZone, "paste"), this._off(this.options.fileInput, "change")
        },
        _setOption: function (e, n) {
            var i = -1 !== t.inArray(e, this._refreshOptionsList);
            i && this._destroyEventHandlers(), this._super(e, n), i && (this._initSpecialOptions(), this._initEventHandlers())
        },
        _initSpecialOptions: function () {
            var e = this.options;
            void 0 === e.fileInput ? e.fileInput = this.element.is('input[type="file"]') ? this.element : this.element.find('input[type="file"]') : e.fileInput instanceof t || (e.fileInput = t(e.fileInput)), e.dropZone instanceof t || (e.dropZone = t(e.dropZone)), e.pasteZone instanceof t || (e.pasteZone = t(e.pasteZone))
        },
        _create: function () {
            var e = this.options;
            t.extend(e, t(this.element[0].cloneNode(!1)).data()), this._initSpecialOptions(), this._slots = [], this._sequence = this._getXHRPromise(!0), this._sending = this._active = this._loaded = this._total = 0, this._initEventHandlers()
        },
        _destroy: function () {
            this._destroyEventHandlers()
        },
        add: function (e) {
            var n = this;
            e && !this.options.disabled && (e.fileInput && !e.files ? this._getFileInputFiles(e.fileInput).always(function (t) {
                e.files = t, n._onAdd(null, e)
            }) : (e.files = t.makeArray(e.files), this._onAdd(null, e)))
        },
        send: function (e) {
            if (e && !this.options.disabled) {
                if (e.fileInput && !e.files) {
                    var n, i, o = this, a = t.Deferred(), r = a.promise();
                    return r.abort = function () {
                        return i = !0, n ? n.abort() : (a.reject(null, "abort", "abort"), r)
                    }, this._getFileInputFiles(e.fileInput).always(function (t) {
                        i || (e.files = t, n = o._onSend(null, e).then(function (t, e, n) {
                            a.resolve(t, e, n)
                        }, function (t, e, n) {
                            a.reject(t, e, n)
                        }))
                    }), this._enhancePromise(r)
                }
                if (e.files = t.makeArray(e.files), e.files.length)return this._onSend(null, e)
            }
            return this._getXHRPromise(!1, e && e.context)
        }
    })
}), !function (t) {
    var e = function () {
        return !1 === t.support.boxModel && t.support.objectAll && t.support.leadingWhitespace
    }();
    t.jGrowl = function (e, n) {
        0 === t("#jGrowl").size() && t('<div id="jGrowl"></div>').addClass(n && n.position ? n.position : t.jGrowl.defaults.position).appendTo("body"), t("#jGrowl").jGrowl(e, n)
    }, t.fn.jGrowl = function (e, n) {
        if (t.isFunction(this.each)) {
            var i = arguments;
            return this.each(function () {
                void 0 === t(this).data("jGrowl.instance") && (t(this).data("jGrowl.instance", t.extend(new t.fn.jGrowl, {
                    notifications: [],
                    element: null,
                    interval: null
                })), t(this).data("jGrowl.instance").startup(this)), t.isFunction(t(this).data("jGrowl.instance")[e]) ? t(this).data("jGrowl.instance")[e].apply(t(this).data("jGrowl.instance"), t.makeArray(i).slice(1)) : t(this).data("jGrowl.instance").create(e, n)
            })
        }
    }, t.extend(t.fn.jGrowl.prototype, {
        defaults: {
            pool: 0,
            header: "",
            group: "",
            sticky: !1,
            position: "top-right",
            glue: "after",
            theme: "default",
            themeState: "highlight",
            corners: "10px",
            check: 250,
            life: 3e3,
            closeDuration: "normal",
            openDuration: "normal",
            easing: "swing",
            closer: !0,
            closeTemplate: "&times;",
            closerTemplate: "<div>[\u5173\u95ed\u6240\u6709]</div>",
            log: function () {
            },
            beforeOpen: function () {
            },
            afterOpen: function () {
            },
            open: function () {
            },
            beforeClose: function () {
            },
            close: function () {
            },
            animateOpen: {opacity: "show"},
            animateClose: {opacity: "hide"}
        }, notifications: [], element: null, interval: null, create: function (e, n) {
            var i = t.extend({}, this.defaults, n);
            "undefined" != typeof i.speed && (i.openDuration = i.speed, i.closeDuration = i.speed), this.notifications.push({
                message: e,
                options: i
            }), i.log.apply(this.element, [this.element, e, i])
        }, render: function (e) {
            var n = this, i = e.message, o = e.options;
            o.themeState = "" === o.themeState ? "" : "ui-state-" + o.themeState;
            var a = t("<div/>").addClass("jGrowl-notification " + o.themeState + " ui-corner-all" + (void 0 !== o.group && "" !== o.group ? " " + o.group : "")).append(t("<div/>").addClass("jGrowl-close").html(o.closeTemplate)).append(t("<div/>").addClass("jGrowl-header").html(o.header)).append(t("<div/>").addClass("jGrowl-message").html(i)).data("jGrowl", o).addClass(o.theme).children("div.jGrowl-close").bind("click.jGrowl", function () {
                t(this).parent().trigger("jGrowl.beforeClose")
            }).parent();
            t(a).bind("mouseover.jGrowl", function () {
                t("div.jGrowl-notification", n.element).data("jGrowl.pause", !0)
            }).bind("mouseout.jGrowl", function () {
                t("div.jGrowl-notification", n.element).data("jGrowl.pause", !1)
            }).bind("jGrowl.beforeOpen", function () {
                o.beforeOpen.apply(a, [a, i, o, n.element]) !== !1 && t(this).trigger("jGrowl.open")
            }).bind("jGrowl.open", function () {
                o.open.apply(a, [a, i, o, n.element]) !== !1 && ("after" == o.glue ? t("div.jGrowl-notification:last", n.element).after(a) : t("div.jGrowl-notification:first", n.element).before(a), t(this).animate(o.animateOpen, o.openDuration, o.easing, function () {
                    t.support.opacity === !1 && this.style.removeAttribute("filter"), null !== t(this).data("jGrowl") && (t(this).data("jGrowl").created = new Date), t(this).trigger("jGrowl.afterOpen")
                }))
            }).bind("jGrowl.afterOpen", function () {
                o.afterOpen.apply(a, [a, i, o, n.element])
            }).bind("jGrowl.beforeClose", function () {
                o.beforeClose.apply(a, [a, i, o, n.element]) !== !1 && t(this).trigger("jGrowl.close")
            }).bind("jGrowl.close", function () {
                t(this).data("jGrowl.pause", !0), t(this).animate(o.animateClose, o.closeDuration, o.easing, function () {
                    t.isFunction(o.close) ? o.close.apply(a, [a, i, o, n.element]) !== !1 && t(this).remove() : t(this).remove()
                })
            }).trigger("jGrowl.beforeOpen"), "" !== o.corners && void 0 !== t.fn.corner && t(a).corner(o.corners), t("div.jGrowl-notification:parent", n.element).size() > 1 && 0 === t("div.jGrowl-closer", n.element).size() && this.defaults.closer !== !1 && t(this.defaults.closerTemplate).addClass("jGrowl-closer " + this.defaults.themeState + " ui-corner-all").addClass(this.defaults.theme).appendTo(n.element).animate(this.defaults.animateOpen, this.defaults.speed, this.defaults.easing).bind("click.jGrowl", function () {
                t(this).siblings().trigger("jGrowl.beforeClose"), t.isFunction(n.defaults.closer) && n.defaults.closer.apply(t(this).parent()[0], [t(this).parent()[0]])
            })
        }, update: function () {
            t(this.element).find("div.jGrowl-notification:parent").each(function () {
                void 0 !== t(this).data("jGrowl") && void 0 !== t(this).data("jGrowl").created && t(this).data("jGrowl").created.getTime() + parseInt(t(this).data("jGrowl").life, 10) < (new Date).getTime() && t(this).data("jGrowl").sticky !== !0 && (void 0 === t(this).data("jGrowl.pause") || t(this).data("jGrowl.pause") !== !0) && t(this).trigger("jGrowl.beforeClose")
            }), this.notifications.length > 0 && (0 === this.defaults.pool || t(this.element).find("div.jGrowl-notification:parent").size() < this.defaults.pool) && this.render(this.notifications.shift()), t(this.element).find("div.jGrowl-notification:parent").size() < 2 && t(this.element).find("div.jGrowl-closer").animate(this.defaults.animateClose, this.defaults.speed, this.defaults.easing, function () {
                t(this).remove()
            })
        }, startup: function (n) {
            this.element = t(n).addClass("jGrowl").append('<div class="jGrowl-notification"></div>'), this.interval = setInterval(function () {
                t(n).data("jGrowl.instance").update()
            }, parseInt(this.defaults.check, 10)), e && t(this.element).addClass("ie6")
        }, shutdown: function () {
            t(this.element).removeClass("jGrowl").find("div.jGrowl-notification").trigger("jGrowl.close").parent().empty(), clearInterval(this.interval)
        }, close: function () {
            t(this.element).find("div.jGrowl-notification").each(function () {
                t(this).trigger("jGrowl.beforeClose")
            })
        }
    }), t.jGrowl.defaults = t.fn.jGrowl.prototype.defaults
}(jQuery);