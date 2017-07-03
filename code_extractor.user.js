// ==UserScript==
// @name         Nanaco Gift Code Extractor for Relo Club
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       kadoyau
// @match        https://www.fukuri.net/main/www/gift/login.jsp*
// @require      https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/6.18.2/babel.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/babel-polyfill/6.16.0/polyfill.js
// @grant        none
// ==/UserScript==

/* jshint ignore:start */
var inline_src = (<><![CDATA[
/* jshint ignore:end */
    
      // テーブルの取得
      let giftTable = document.getElementsByClassName("table_gift");

      // コードの取得
      var codeArray = [];
      // 2行目は、券種が結合されているためにセルが1つズレている
      codeArray.push(giftTable[0].rows[1].cells[1].textContent);
      // 3行目以下はループ
      for (var i = 2; i < giftTable[0].rows.length; i++) {
        codeArray.push(giftTable[0].rows[i].cells[0].textContent);
      }

     // テキストエリアを設置して描画
      let textarea = document.createElement('textarea'); textarea.id = 'textarea'; textarea.rows = 11;
      let header = document.getElementById("header"); header.appendChild(textarea);
      let t = document.getElementById('textarea'); t.value = codeArray.join('\n');

/* jshint ignore:start */
]]></>).toString();
var c = Babel.transform(inline_src, { presets: [ "es2015", "es2016" ] });
eval(c.code);
/* jshint ignore:end */
