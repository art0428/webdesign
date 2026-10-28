/* ══ 管理者工作室 設計系統 30.0.0 ══ theme.js
   色系切換（規範 3.8、4.2）與深淺模式（規範 8.8）。由 emit_css.py 產生，THEMES 表取自元件庫。
   用法：
     <html data-style="s1">                         本系統選定的風格（建置時決定，全站只有一套）
     <script src="theme.js"></script>
     DS.applyTheme('c1')                            切換色系；不合法組合退回 c1 並回傳實際套用的 key
     DS.setColorScheme('dark'|'light'|'system')     只有 S3、S5、S6 有深色（DARK_STYLES）；其他風格呼叫無效果
     DS.setDarkTint('follow'|'neutral')             S6 深色底跟隨色系（預設）或中性石墨；其他風格呼叫無效果；DS.darkTint() 回目前生效的值
     DS.setDensity('comfortable'|'normal'|'compact') 密度三檔；不在本風格可選範圍的檔退回該套預設（DENSITY 矩陣）
     DS.labelTables()                               依表頭替表格每格補 data-l（手機卡片列的欄名）；載入時自動跑，動態新增列後再呼叫
     跟隨系統時會監聽 prefers-color-scheme 的變化並重套品牌色
   色系、深淺、深色底偏好以 localStorage 記住（鍵 ds.theme、ds.scheme、ds.darkTint、ds.density），網址參數 ?theme=c3、?tint=neutral 優先。 */
(function(){
const THEMES={
 c1:{"id":"C1","name":"深海藍","acc":"#2B5FB8","accSoft":"#EDF1F9","acc2":"#C2377B","acc2Soft":"#FAEEF4","acc2Deep":"#BA3576","accDeep":"#2B5FB8","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c2:{"id":"C2","name":"深湖青","acc":"#0F5C63","accSoft":"#EBF1F2","acc2":"#C4663A","acc2Soft":"#FAF2EE","acc2Deep":"#A15430","accDeep":"#0F5C63","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c3:{"id":"C3","name":"深靛","acc":"#2C2A72","accSoft":"#EDEDF3","acc2":"#8C7AE6","acc2Soft":"#F5F4FD","acc2Deep":"#6A5DAF","accDeep":"#2C2A72","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c4:{"id":"C4","name":"電光紫","acc":"#6D28D9","accSoft":"#F3EDFC","acc2":"#0F8A99","acc2Soft":"#EBF5F6","acc2Deep":"#0D7481","accDeep":"#6D28D9","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c5:{"id":"C5","name":"森林綠","acc":"#1F5E3D","accSoft":"#ECF1EF","acc2":"#A16207","acc2Soft":"#F7F2EA","acc2Deep":"#975C07","accDeep":"#1F5E3D","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c6:{"id":"C6","name":"胡桃棕","acc":"#6B4A33","accSoft":"#F2F0EE","acc2":"#4A6B55","acc2Soft":"#F0F2F1","acc2Deep":"#4A6B55","accDeep":"#6B4A33","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c7:{"id":"C7","name":"焦糖磚橘","acc":"#A8481F","accSoft":"#F8EFEC","acc2":"#2B2B2B","acc2Soft":"#EDEDED","acc2Deep":"#2B2B2B","accDeep":"#A8481F","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c8:{"id":"C8","name":"暖墨","acc":"#23201E","accSoft":"#ECECEC","acc2":"#D95F1E","acc2Soft":"#FCF1EC","acc2Deep":"#AE4C18","accDeep":"#23201E","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c9:{"id":"C9","name":"唇膏紅","acc":"#9F2436","accSoft":"#F7EDEF","acc2":"#2A5C6A","acc2Soft":"#EEF2F3","acc2Deep":"#2A5C6A","accDeep":"#9F2436","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c10:{"id":"C10","name":"節慶桃紅","acc":"#9E2C6A","accSoft":"#F7EEF3","acc2":"#5C97CB","acc2Soft":"#F2F7FB","acc2Deep":"#336DA0","accDeep":"#9E2C6A","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c11:{"id":"C11","name":"燒橄欖","acc":"#646049","accSoft":"#F3F2F0","acc2":"#C65D52","acc2Soft":"#FAF2F1","acc2Deep":"#B2463B","accDeep":"#646049","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c12:{"id":"C12","name":"玫瑰棕","acc":"#80565B","accSoft":"#F5F1F2","acc2":"#BA797D","acc2Soft":"#F9F4F5","acc2Deep":"#9F5257","accDeep":"#80565B","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 sc1:{"id":"SC1","name":"深綠 × 相思黃","acc":"#35463D","accSoft":"#EFF0EF","acc2":"#DACD65","acc2Soft":"#FCFBF3","acc2Deep":"#6F6519","acc2Type":"light","styles":["s1","s3","s5","s6","s7"],"adjust":["s4"],"series":"SC","accDeep":"#35463D"},
 sc2:{"id":"SC2","name":"鈷藍 × 亮橘","acc":"#2449E8","accSoft":"#EEF1FD","acc2":"#FF7A1A","acc2Soft":"#FFF3EA","acc2Deep":"#B0490A","acc2Type":"light","styles":["s1","s3","s5","s6","s7"],"adjust":["s4"],"series":"SC","accDeep":"#2449E8"},
 sc3:{"id":"SC3","name":"石板藍 × 冰川青","acc":"#3D4C5E","accSoft":"#EFF1F3","acc2":"#5FB4C9","acc2Soft":"#F0F8FA","acc2Deep":"#296778","acc2Type":"light","styles":["s1","s3","s4","s5","s6","s7"],"adjust":["s2"],"series":"SC","accDeep":"#3D4C5E"}
};
/* 深色模式的品牌色（規範 8.8：OKLab 只加明度、填色上一律深色字），依風格分表：各套深色的面板底不同，
   主色要提亮到的程度也不同 */
const DARK={s3:{"c1":{"acc":"#76A9FF","accSoft":"#2D3954","accDeep":"#76A9FF","acc2":"#C2377B","acc2Soft":"#39273F","acc2Deep":"#FF7EB6","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c2":{"acc":"#6FB3BB","accSoft":"#2C3B49","accDeep":"#6FB3BB","acc2":"#C4663A","acc2Soft":"#392F34","acc2Deep":"#E7936E","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c3":{"acc":"#9AA2F5","accSoft":"#333852","accDeep":"#9AA2F5","acc2":"#8C7AE6","acc2Soft":"#303250","acc2Deep":"#A89DF5","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c4":{"acc":"#B09AFF","accSoft":"#363754","accDeep":"#B09AFF","acc2":"#0F8A99","acc2Soft":"#1C3443","acc2Deep":"#60B6C4","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c5":{"acc":"#77B690","accSoft":"#2D3B42","accDeep":"#77B690","acc2":"#A16207","acc2Soft":"#342E2C","acc2Deep":"#DB9C56","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c6":{"acc":"#C6A087","accSoft":"#3A3840","accDeep":"#C6A087","acc2":"#54755F","acc2Soft":"#27313A","acc2Deep":"#8DB098","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c7":{"acc":"#F18A62","accSoft":"#41343B","accDeep":"#F18A62","acc2":"#6E6E6E","acc2Soft":"#2C303C","acc2Deep":"#A9A9A9","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c8":{"acc":"#ABA7A4","accSoft":"#353945","accDeep":"#ABA7A4","acc2":"#D95F1E","acc2Soft":"#3D2D30","acc2Deep":"#F68D5E","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c9":{"acc":"#FF7D84","accSoft":"#433240","accDeep":"#FF7D84","acc2":"#447684","acc2Soft":"#253140","acc2Deep":"#7DB0BF","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c10":{"acc":"#F67DB7","accSoft":"#413248","accDeep":"#F67DB7","acc2":"#5C97CB","acc2Soft":"#29364B","acc2Deep":"#72ADE4","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c11":{"acc":"#ADA990","accSoft":"#363942","accDeep":"#ADA990","acc2":"#C65D52","acc2Soft":"#3A2D38","acc2Deep":"#FB8778","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c12":{"acc":"#CA9BA0","accSoft":"#3A3744","accDeep":"#CA9BA0","acc2":"#BA797D","acc2Soft":"#38323F","acc2Deep":"#E59194","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc1":{"acc":"#9AAEA3","accSoft":"#333A45","accDeep":"#9AAEA3","acc2":"#DACD65","acc2Soft":"#3D3F3B","acc2Deep":"#B4AA62","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc2":{"acc":"#82A6FF","accSoft":"#2F3954","accDeep":"#82A6FF","acc2":"#FF7A1A","acc2Soft":"#43322F","acc2Deep":"#FA8C59","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc3":{"acc":"#99AABF","accSoft":"#333949","accDeep":"#99AABF","acc2":"#5FB4C9","acc2Soft":"#293B4B","acc2Deep":"#74B1C4","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"}},
 s5:{"c1":{"acc":"#81B0FF","accSoft":"#353F56","accDeep":"#81B0FF","acc2":"#C93E81","acc2Soft":"#402D42","acc2Deep":"#FF8BBB","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c2":{"acc":"#77BBC3","accSoft":"#33414D","accDeep":"#77BBC3","acc2":"#C4663A","acc2Soft":"#3F3437","acc2Deep":"#EF9B76","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c3":{"acc":"#A2AAFE","accSoft":"#3A3E56","accDeep":"#A2AAFE","acc2":"#8C7AE6","acc2Soft":"#363752","acc2Deep":"#B1A6FF","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c4":{"acc":"#B7A4FF","accSoft":"#3D3E56","accDeep":"#B7A4FF","acc2":"#0F8A99","acc2Soft":"#223946","acc2Deep":"#68BECC","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c5":{"acc":"#7FBE98","accSoft":"#344246","accDeep":"#7FBE98","acc2":"#A4650E","acc2Soft":"#3A3330","acc2Deep":"#E3A35E","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c6":{"acc":"#CEA88F","accSoft":"#413E44","accDeep":"#CEA88F","acc2":"#597B64","acc2Soft":"#2E373D","acc2Deep":"#96BAA1","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c7":{"acc":"#FC936B","accSoft":"#483B3E","accDeep":"#FC936B","acc2":"#737373","acc2Soft":"#323640","acc2Deep":"#B1B1B1","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c8":{"acc":"#B3AFAC","accSoft":"#3D3F49","accDeep":"#B3AFAC","acc2":"#D95F1E","acc2Soft":"#433232","acc2Deep":"#FF9565","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c9":{"acc":"#FF8F93","accSoft":"#493A45","accDeep":"#FF8F93","acc2":"#497A89","acc2Soft":"#2C3743","acc2Deep":"#85B8C7","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c10":{"acc":"#FF87C1","accSoft":"#49394C","accDeep":"#FF87C1","acc2":"#5C97CB","acc2Soft":"#2F3B4E","acc2Deep":"#7AB5ED","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c11":{"acc":"#B5B197","accSoft":"#3D4046","accDeep":"#B5B197","acc2":"#C65D52","acc2Soft":"#40323A","acc2Deep":"#FF9587","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c12":{"acc":"#D4A5A9","accSoft":"#423E48","accDeep":"#D4A5A9","acc2":"#BA797D","acc2Soft":"#3E3741","acc2Deep":"#EF9A9E","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc1":{"acc":"#A2B6AB","accSoft":"#3A4049","accDeep":"#A2B6AB","acc2":"#DACD65","acc2Soft":"#43443E","acc2Deep":"#BCB26A","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc2":{"acc":"#8CAEFF","accSoft":"#363F56","accDeep":"#8CAEFF","acc2":"#FF7A1A","acc2Soft":"#493732","acc2Deep":"#FF9666","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc3":{"acc":"#A2B3C8","accSoft":"#3A404D","accDeep":"#A2B3C8","acc2":"#5FB4C9","acc2Soft":"#2F404E","acc2Deep":"#7DBBCD","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"}},
 s6:{"c1":{"acc":"#629AF8","accSoft":"#262E3E","accDeep":"#629AF8","acc2":"#C2377B","acc2Soft":"#351F2A","acc2Deep":"#F46BA8","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c2":{"acc":"#61A5AC","accSoft":"#253031","accDeep":"#61A5AC","acc2":"#C4663A","acc2Soft":"#35261F","acc2Deep":"#D88561","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c3":{"acc":"#8D94E6","accSoft":"#2C2E3B","accDeep":"#8D94E6","acc2":"#8C7AE6","acc2Soft":"#2C293B","acc2Deep":"#9C90E7","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c4":{"acc":"#A486FF","accSoft":"#302B3F","accDeep":"#A486FF","acc2":"#0F8A99","acc2Soft":"#182C2E","acc2Deep":"#4FA6B4","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c5":{"acc":"#6BA984","accSoft":"#27312B","accDeep":"#6BA984","acc2":"#A16207","acc2Soft":"#302617","acc2Deep":"#CC8E48","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c6":{"acc":"#B9947B","accSoft":"#332E2A","accDeep":"#B9947B","acc2":"#4D6E58","acc2Soft":"#222724","acc2Deep":"#81A48C","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c7":{"acc":"#E57F57","accSoft":"#3A2A24","accDeep":"#E57F57","acc2":"#666666","acc2Soft":"#262626","acc2Deep":"#9B9B9B","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c8":{"acc":"#9F9B98","accSoft":"#2F2F2E","accDeep":"#9F9B98","acc2":"#D95F1E","acc2Soft":"#39251B","acc2Deep":"#E88051","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c9":{"acc":"#F17178","accSoft":"#3C2829","accDeep":"#F17178","acc2":"#3C6D7C","acc2Soft":"#1F272A","acc2Deep":"#71A3B3","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c10":{"acc":"#E972AC","accSoft":"#3B2831","accDeep":"#E972AC","acc2":"#5C97CB","acc2Soft":"#252E36","acc2Deep":"#659FD5","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c11":{"acc":"#A19D84","accSoft":"#302F2B","accDeep":"#A19D84","acc2":"#C65D52","acc2Soft":"#362523","acc2Deep":"#ED7B6C","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c12":{"acc":"#BD8F94","accSoft":"#342D2E","accDeep":"#BD8F94","acc2":"#BA797D","acc2Soft":"#34292A","acc2Deep":"#D78588","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc1":{"acc":"#8CA095","accSoft":"#2C2F2E","accDeep":"#8CA095","acc2":"#DACD65","acc2Soft":"#393726","acc2Deep":"#A69C55","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc2":{"acc":"#6D96FF","accSoft":"#272E3F","accDeep":"#6D96FF","acc2":"#FF7A1A","acc2Soft":"#3F291A","acc2Deep":"#EA7E4B","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc3":{"acc":"#8C9DB2","accSoft":"#2C2F32","accDeep":"#8C9DB2","acc2":"#5FB4C9","acc2Soft":"#253336","acc2Deep":"#68A5B7","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"}}};
const DARK_STYLES=["s3", "s5", "s6"];
/* 深色底「跟隨色系」（規範 8.8，v29）：S6 深色的六個面與淡底帶目前色系主色的色調（明度不動、OKLCH 彩度 ≤0.015），
   品牌色依新的卡片色重算淡底（C2、C3 主色補一階明度）。由 build_dark.py 呼叫 derive_dark_tint.py 推導，不要手改。
   <html data-dark-tint="neutral"> 或 DS.setDarkTint('neutral') 切回中性石墨；沒有 JS 時是中性石墨（CSS 只寫中性值）。 */
const TINT_STYLES=["s6"];
const DARK_TINT={"c1":{"s":{"page":"#0F1217","card":"#171A20","paperc":"#1D2026","sel":"#23262C","line":"#2B2E34","line-2":"#373A41","err-soft":"#3A2C30","wrn-soft":"#373225","ok-soft":"#263530","info-soft":"#273341"},"b":{"acc":"#629AF8","accSoft":"#232E43","accDeep":"#629AF8","acc2Soft":"#321F2F","acc2Deep":"#F46BA8"}},"c2":{"s":{"page":"#0C1415","card":"#141C1D","paperc":"#1A2223","sel":"#1F2829","line":"#273031","line-2":"#333C3D","err-soft":"#382E2D","wrn-soft":"#353423","ok-soft":"#23372D","info-soft":"#25353E"},"b":{"acc":"#62A6AD","accSoft":"#203234","accDeep":"#62A6AD","acc2Soft":"#302822","acc2Deep":"#D88561"}},"c3":{"s":{"page":"#111217","card":"#191A20","paperc":"#1F2026","sel":"#25262C","line":"#2D2E34","line-2":"#393A40","err-soft":"#3C2C30","wrn-soft":"#393225","ok-soft":"#283530","info-soft":"#293341"},"b":{"acc":"#8E95E7","accSoft":"#2C2E40","accDeep":"#8E95E7","acc2Soft":"#2B2940","acc2Deep":"#9C90E7"}},"c4":{"s":{"page":"#121117","card":"#1A191F","paperc":"#201F25","sel":"#26252C","line":"#2E2D34","line-2":"#3A3940","err-soft":"#3D2B2F","wrn-soft":"#3A3224","ok-soft":"#28342F","info-soft":"#2A3240"},"b":{"acc":"#A486FF","accSoft":"#302A43","accDeep":"#A486FF","acc2Soft":"#182B33","acc2Deep":"#4FA6B4"}},"c5":{"s":{"page":"#0E1410","card":"#161C18","paperc":"#1C221E","sel":"#212824","line":"#29302C","line-2":"#353C38","err-soft":"#392E29","wrn-soft":"#37341F","ok-soft":"#253729","info-soft":"#26353A"},"b":{"acc":"#6BA984","accSoft":"#243329","accDeep":"#6BA984","acc2Soft":"#2C2715","acc2Deep":"#CC8E48"}},"c6":{"s":{"page":"#16110D","card":"#1F1915","paperc":"#251F1B","sel":"#2B2521","line":"#332D28","line-2":"#3F3934","err-soft":"#412B26","wrn-soft":"#3E321C","ok-soft":"#2D3427","info-soft":"#2E3238"},"b":{"acc":"#B9947B","accSoft":"#382D25","accDeep":"#B9947B","acc2Soft":"#262720","acc2Deep":"#81A48C"}},"c7":{"s":{"page":"#17100E","card":"#1F1816","paperc":"#251E1C","sel":"#2B2422","line":"#342C29","line-2":"#403835","err-soft":"#412A27","wrn-soft":"#3E311D","ok-soft":"#2D3427","info-soft":"#2E3139"},"b":{"acc":"#E57F57","accSoft":"#3F2820","accDeep":"#E57F57","acc2Soft":"#2A2423","acc2Deep":"#9B9B9B"}},"c8":{"s":{"page":"#141110","card":"#1C1917","paperc":"#221F1D","sel":"#282523","line":"#312D2B","line-2":"#3D3937","err-soft":"#3E2B28","wrn-soft":"#3C321E","ok-soft":"#2A3428","info-soft":"#2C3239"},"b":{"acc":"#9F9B98","accSoft":"#312E2C","accDeep":"#9F9B98","acc2Soft":"#3A2418","acc2Deep":"#E88051"}},"c9":{"s":{"page":"#171010","card":"#1F1818","paperc":"#261E1E","sel":"#2C2424","line":"#342C2C","line-2":"#403838","err-soft":"#412A29","wrn-soft":"#3E311F","ok-soft":"#2D3429","info-soft":"#2E313A"},"b":{"acc":"#F17178","accSoft":"#412627","accDeep":"#F17178","acc2Soft":"#242628","acc2Deep":"#71A3B3"}},"c10":{"s":{"page":"#161013","card":"#1F181B","paperc":"#251E21","sel":"#2B2427","line":"#332C2F","line-2":"#3F383B","err-soft":"#412A2B","wrn-soft":"#3E3121","ok-soft":"#2D342C","info-soft":"#2E313D"},"b":{"acc":"#E972AC","accSoft":"#3F2632","accDeep":"#E972AC","acc2Soft":"#292C37","acc2Deep":"#659FD5"}},"c11":{"s":{"page":"#13120C","card":"#1B1A14","paperc":"#21201A","sel":"#272620","line":"#2F2E27","line-2":"#3B3A33","err-soft":"#3D2C26","wrn-soft":"#3B321B","ok-soft":"#293526","info-soft":"#2B3337"},"b":{"acc":"#A19D84","accSoft":"#302F26","accDeep":"#A19D84","acc2Soft":"#36251E","acc2Deep":"#ED7B6C"}},"c12":{"s":{"page":"#171011","card":"#1F1819","paperc":"#251E1F","sel":"#2C2425","line":"#342C2C","line-2":"#403838","err-soft":"#412A2A","wrn-soft":"#3E311F","ok-soft":"#2D342A","info-soft":"#2E313B"},"b":{"acc":"#BD8F94","accSoft":"#382B2D","accDeep":"#BD8F94","acc2Soft":"#382829","acc2Deep":"#D78588"}},"sc1":{"s":{"page":"#0D1410","card":"#151C18","paperc":"#1B221E","sel":"#212824","line":"#29302C","line-2":"#353C38","err-soft":"#382E29","wrn-soft":"#36341F","ok-soft":"#243729","info-soft":"#26353A"},"b":{"acc":"#8CA095","accSoft":"#28312C","accDeep":"#8CA095","acc2Soft":"#353824","acc2Deep":"#A69C55"}},"sc2":{"s":{"page":"#101218","card":"#171A20","paperc":"#1D2026","sel":"#23262C","line":"#2B2E34","line-2":"#373A41","err-soft":"#3A2C30","wrn-soft":"#373225","ok-soft":"#263530","info-soft":"#273341"},"b":{"acc":"#6D96FF","accSoft":"#252E44","accDeep":"#6D96FF","acc2Soft":"#3C291F","acc2Deep":"#EA7E4B"}},"sc3":{"s":{"page":"#0E1217","card":"#161A20","paperc":"#1C2126","sel":"#22272C","line":"#2A2F34","line-2":"#363B40","err-soft":"#392C30","wrn-soft":"#373225","ok-soft":"#253530","info-soft":"#263341"},"b":{"acc":"#8C9DB2","accSoft":"#292F37","accDeep":"#8C9DB2","acc2Soft":"#22333B","acc2Deep":"#68A5B7"}}};
const TINT_VARS=["--page", "--card", "--paperc", "--sel", "--line", "--line-2", "--err-soft", "--wrn-soft", "--ok-soft", "--info-soft"];
const root=document.documentElement;
const STYLE=(root.dataset.style||'s1').toLowerCase();
const mq=window.matchMedia?window.matchMedia('(prefers-color-scheme: dark)'):null;
function isDark(){
  if(!DARK_STYLES.includes(STYLE)) return false;
  const a=root.getAttribute('data-theme');
  if(a==='dark') return true; if(a==='light') return false;
  return !!(mq&&mq.matches);
}
function allowed(k){const t=THEMES[k];return !!t&&(t.styles.includes(STYLE)||(t.adjust||[]).includes(STYLE));}
function applyTheme(k){
  let t=THEMES[k];
  if(!t||!allowed(k)){ if(typeof DS.onFallback==='function') DS.onFallback(k,'c1'); k='c1'; t=THEMES.c1; }
  const dark=isDark();
  if(dark&&DARK[STYLE]&&DARK[STYLE][k]) t=Object.assign({},t,DARK[STYLE][k]);
  const r=root.style;
  TINT_VARS.forEach(v=>r.removeProperty(v));
  if(dark&&darkTint()==='follow'&&DARK_TINT[k]){ t=Object.assign({},t,DARK_TINT[k].b); const s=DARK_TINT[k].s; for(const n in s) r.setProperty('--'+n,s[n]); }
  r.setProperty('--acc',t.acc); r.setProperty('--acc-soft',t.accSoft); r.setProperty('--accsoft',t.accSoft); r.setProperty('--acc-deep',t.accDeep);
  r.setProperty('--acc2',t.acc2); r.setProperty('--acc2-soft',t.acc2Soft); r.setProperty('--acc2soft',t.acc2Soft); r.setProperty('--acc2-deep',t.acc2Deep);
  const ink=(getComputedStyle(root).getPropertyValue('--ink')||'#26292E').trim();
  if(dark){ r.setProperty('--acc2-text',t.acc2Text); r.setProperty('--on-acc',t.onAcc); r.setProperty('--on-acc2',t.onAcc2); }
  else { r.setProperty('--acc2-text', t.acc2Type==='light' ? ink : '#FFFFFF'); r.removeProperty('--on-acc'); r.removeProperty('--on-acc2'); }
  root.classList.toggle('sc-light', t.acc2Type==='light');
  root.classList.toggle('sc-adjust', !!(t.adjust&&t.adjust.includes(STYLE)));
  root.dataset.theme_id=t.id;
  try{ localStorage.setItem('ds.theme',k); }catch(_){}
  return k;
}
if(mq&&mq.addEventListener) mq.addEventListener('change',()=>{ const k=root.dataset.theme_key; if(k) applyTheme(k); });
function setColorScheme(mode){
  if(mode==='system'){ root.removeAttribute('data-theme'); }
  else { root.setAttribute('data-theme', mode==='dark'?'dark':'light'); }
  try{ localStorage.setItem('ds.scheme',mode); }catch(_){}
  /* 深型／淺型副色的字色跟著 --ink 走，換模式後重算 */
  const k=root.dataset.theme_key; if(k) applyTheme(k);
}
function darkTint(){
  if(!TINT_STYLES.includes(STYLE)) return null;
  return root.getAttribute('data-dark-tint')==='neutral' ? 'neutral' : 'follow';
}
function setDarkTint(mode){
  if(!TINT_STYLES.includes(STYLE)) return darkTint();
  mode = mode==='neutral' ? 'neutral' : 'follow';
  root.setAttribute('data-dark-tint',mode);
  try{ localStorage.setItem('ds.darkTint',mode); }catch(_){}
  const k=root.dataset.theme_key; if(k) applyTheme(k);
  return darkTint();
}
/* 密度三檔（規範 5.7）：只改尺寸、不改顏色；每套風格有預設檔與可選範圍（DENSITY 矩陣），不寫 data-density 就是預設；
   不在可選範圍的檔退回該套預設並回傳；768px 以下 CSS 本身收斂成一檔（觸控下限優先） */
const DENSITY={"s1": {"default": "comfortable", "allowed": ["comfortable", "normal", "compact"]}, "s2": {"default": "comfortable", "allowed": ["comfortable", "normal"]}, "s3": {"default": "comfortable", "allowed": ["comfortable", "normal", "compact"]}, "s4": {"default": "comfortable", "allowed": ["comfortable", "normal"]}, "s5": {"default": "comfortable", "allowed": ["comfortable", "normal"]}, "s6": {"default": "normal", "allowed": ["comfortable", "normal", "compact"]}, "s7": {"default": "comfortable", "allowed": ["comfortable", "normal"]}};
const DENSE_STYLES=Object.keys(DENSITY).filter(k=>DENSITY[k].allowed.includes('compact'));
function density(){ const d=DENSITY[STYLE]||DENSITY.s1; return root.getAttribute('data-density')||d.default; }
function setDensity(mode){
  const d=DENSITY[STYLE]||DENSITY.s1;
  if(!d.allowed.includes(mode)){ if(typeof DS.onDensityFallback==='function') DS.onDensityFallback(mode,d.default); mode=d.default; }
  if(mode===d.default) root.removeAttribute('data-density'); else root.setAttribute('data-density',mode);
  try{ localStorage.setItem('ds.density',mode); }catch(_){}
  return density();
}
/* 表格手機卡片列的欄名（規範 6.3，v27）：每格沒有 data-l 時依表頭補上；動態新增的列再呼叫一次 DS.labelTables() */
function labelTables(scope){
  (scope||document).querySelectorAll('table.t').forEach(t=>{
    const hs=[...t.querySelectorAll('thead th')].map(th=>th.textContent.replace(/[↕↓↑]/g,'').trim());
    t.querySelectorAll('tbody tr').forEach(tr=>[...tr.children].forEach((td,i)=>{ if(!td.hasAttribute('data-l')&&hs[i]) td.setAttribute('data-l',hs[i]); }));
  });
}
function init(){
  labelTables();
  let k=null, mode=null, dens=null, tint=null;
  try{ const q=new URLSearchParams(location.search); k=q.get('theme'); tint=q.get('tint'); }catch(_){}
  try{ k=k||localStorage.getItem('ds.theme'); mode=localStorage.getItem('ds.scheme'); dens=localStorage.getItem('ds.density'); tint=tint||localStorage.getItem('ds.darkTint'); }catch(_){}
  if(mode&&mode!=='system') root.setAttribute('data-theme',mode);
  /* 深色底：網址 ?tint= ＞ 使用者偏好 ds.darkTint ＞ 頁面寫的 data-dark-tint ＞ 預設跟隨 */
  if(TINT_STYLES.includes(STYLE)&&(tint==='neutral'||tint==='follow')) root.setAttribute('data-dark-tint',tint);
  if(dens&&!root.hasAttribute('data-density')){ const d=DENSITY[STYLE]||DENSITY.s1; if(d.allowed.includes(dens)&&dens!==d.default) root.setAttribute('data-density',dens); }
  root.dataset.theme_key=applyTheme(k||'c1');
}
window.DS={THEMES,STYLE,DENSITY,DARK_TINT,allowed,applyTheme:function(k){root.dataset.theme_key=k;return applyTheme(k);},setColorScheme,setDarkTint,darkTint,setDensity,density,labelTables,init};
init();
})();
