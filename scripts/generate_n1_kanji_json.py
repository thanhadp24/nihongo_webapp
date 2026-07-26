import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import fitz
import requests


OUTPUT = Path("database/import/jlpt_n1_kanji_by_topic_db_import.json")
KANJI_API_CACHE = Path("tmp/cache/kanjiapi_n1.json")
UNIHAN_READINGS_FILE = Path("tmp/cache/unihan/Unihan_Readings.txt")
ENRICH_KANJI_API = os.environ.get("ENRICH_KANJI_API", "1") != "0"

SOURCE_FILE = "plan/kanji/Thaolejp_Kanji master N1.pdf"
SUPPLEMENT_FILE = "plan/kanji/trilu-kanji-2136-N1.pdf"


TOPICS = [
    (1, "行為 - 1", "こうい いち", "Hành vi 1", 12, "為扱披押抵抗掲拭跳躍踏駆伏弾裂塗叱黙唱聴眺隠添排挑操磨奪妨遮伴揺尽諦誓悟避耐焦慌"),
    (2, "行為 - 2", "こうい に", "Hành vi 2", 18, "尋促惑譲陥迫遂抽覆偽輝控砕削挟挿及紛免慎併劣隔抹惜嘆驚憩粘藍欲諭忍狂奔貪侮辱褒慰"),
    (3, "人間関係", "にんげんかんけい", "Quan hệ con người", 28, "嫁婿縁戚系姻叔伯恩涯継婆紳淑嬢貴威仰謹賀奉忠孝貞徳称郎俺己孤匿遺逝葬忌棺墓故魂"),
    (4, "食・住", "しょく じゅう", "Ăn uống và nhà ở", 34, "桃柿芋栗腐昆漬藻沸騰煮炊揚炒蒸鍋舎塔垣邸亭房棟倉縄綱網絞盆鉢刃栓扉棚卓斎堀炉芳臭"),
    (5, "状態 - 1", "じょうたい いち", "Trạng thái 1", 44, "穏暇滑雰朗裕乏徴愚稚猛烈卑壮陰膨奇妙微魅凡甲乙恒至瞬旬頃徐頻逐斉唯疎剰緩衡殊偏宜"),
    (6, "状態 - 2", "じょうたい に", "Trạng thái 2", 50, "慈慕悦愉哀悄閑虚愁憂慣慨惨寂剛敢俊敏迅豪巧粋粗文懐悔怪妄恨羨煩憧飽錯瞭寛悠醜麗"),
    (7, "自然 - 1", "しぜん いち", "Tự nhiên 1", 60, "幹茎芽苗芝茂郊樹獲尾雄雌滅獣狩猟窒素亜鉛硫酸磁晶潮浦沿溝漂没濁澄霧霜露雲虹圏樺"),
    (8, "自然 - 2", "しぜん に", "Tự nhiên 2", 66, "蝶蚊蜂蜜蛍亀蛇卵雀鳩鴨烏鶴鶏翼牙猿狼猪熊虎鯨竜龍蘭蚕桑柳峰岳峠漢堤陸峡岬渓渦潤郡"),
    (9, "仕事", "しごと", "Công việc", 76, "汽船搬巡貢献繁拓刈稲穂耕穫穀栽培渉提摘択把妥佐請派遣宣卸属輸軌遷遇蓄勘託障祉概顧"),
    (10, "教育", "きょういく", "Giáo dục", 82, "礎践模範釈拠克撲哲倫志功佳秀推薦訂項索稿翻欄載啓監督矛盾浸透諸班急誠誇懸繰析熟揮"),
    (11, "文化 - 1", "ぶんか いち", "Văn hóa 1", 92, "庶娯興趣釣撮影創俗描肖漫陶墨朱淡琴弦鼓笛雅奏譜鑑仁僧尼尚禅鐘典弓矢鋼剣刀鎖侍騎"),
    (12, "文化 - 2", "ぶんか に", "Văn hóa 2", 98, "宮廷皇帝后陛妃姫奨彰傑賜勲誉栄冠幻仙聖魔吉凶厄鬼幕藩紀暦崇祥碑墳郷旗搭織染"),
    (13, "体", "からだ", "Cơ thể", 108, "瞳眉頬唇爪喉掌癖裸膚肢膝肘胴脇尻肺腸肝胆膜腎尿盲慢疾疫痢循胎矯耗鍛錬殖摂肥凝衰"),
    (14, "司法・行政", "しほう ぎょうせい", "Tư pháp và hành chính", 114, "秘密摩擦締施衝弁訴訟審償執是憲廃棄却陳賃賂犠牲脅襲逮闘詐欺邦陣轄拘偵阻斥"),
]


EXTRA_TOPIC_SPECS = [
    (15, "付き合い", "つきあい", "Quan hệ xã giao", 128, 16),
    (16, "仕事・役所", "しごと やくしょ", "Công việc và cơ quan hành chính", 130, 40),
    (17, "時間・数学・形状・接続詞", "じかん すうがく けいじょう せつぞくし", "Thời gian, toán học, hình dạng và liên từ", 138, 26),
    (18, "文化 - 3", "ぶんか さん", "Văn hóa 3", 142, 28),
    (19, "着物", "きもの", "Trang phục truyền thống", 152, 30),
    (20, "犯罪・戦争", "はんざい せんそう", "Tội phạm và chiến tranh", 156, 36),
    (21, "建物", "たてもの", "Công trình và kiến trúc", 164, 12),
    (22, "生活", "せいかつ", "Đời sống", 166, 32),
    (23, "行為・感情・思考", "こうい かんじょう しこう", "Hành vi, cảm xúc và suy nghĩ", 176, 40),
    (24, "海・山", "うみ やま", "Biển và núi", 182, 30),
    (25, "人・様子", "ひと ようす", "Con người và dáng vẻ", 188, 24),
    (26, "体", "からだ", "Cơ thể nâng cao", 192, 30),
    (27, "地名", "ちめい", "Địa danh", 202, 7),
    (28, "言葉で覚える", "ことばでおぼえる", "Ghi nhớ bằng từ ngữ", 204, 13),
    (29, "身分", "みぶん", "Thân phận và địa vị", 206, 10),
    (30, "難読編", "なんどくへん", "Kanji khó đọc", 214, 21),
]

HAN_VIET_AND_MEANING_FALLBACKS = {
    "扱": ("cấp", "xử lý, đối đãi, sử dụng"),
    "押": ("áp", "ấn, đẩy, ép"),
    "抵": ("để", "chống lại, chạm tới, tương đương"),
    "抗": ("kháng", "chống lại, phản kháng"),
    "掲": ("yết", "treo lên, đăng tải, nêu ra"),
    "踏": ("đạp", "giẫm, bước lên, trải qua"),
    "弾": ("đạn, đàn", "viên đạn, bật ra, chơi đàn"),
    "塗": ("đồ", "sơn, bôi, phủ lên"),
    "隠": ("ẩn", "ẩn giấu, che khuất"),
    "磨": ("ma", "mài, đánh bóng, rèn luyện"),
    "奪": ("đoạt", "cướp lấy, tước đoạt"),
    "揺": ("dao", "rung, lắc, lay động"),
    "尽": ("tận", "hết, dốc hết, tận lực"),
    "諦": ("đế", "từ bỏ, hiểu rõ bản chất"),
    "避": ("tị", "tránh, né, phòng tránh"),
    "惑": ("hoặc", "mê hoặc, bối rối, lúng túng"),
    "迫": ("bách", "ép buộc, đến gần, cấp bách"),
    "輝": ("huy", "tỏa sáng, rực rỡ"),
    "砕": ("toái", "nghiền nát, vỡ vụn"),
    "削": ("tước", "gọt, cắt giảm,削除"),
    "挟": ("hiệp", "kẹp, chen vào, ở giữa"),
    "及": ("cập", "đạt tới, liên quan đến"),
    "劣": ("liệt", "kém, thấp hơn"),
    "驚": ("kinh", "ngạc nhiên, kinh động"),
    "欲": ("dục", "ham muốn, mong muốn"),
    "褒": ("bao", "khen ngợi, biểu dương"),
    "系": ("hệ", "hệ thống, dòng, nhóm"),
    "恩": ("ân", "ơn, ân nghĩa"),
    "継": ("kế", "nối tiếp, kế thừa"),
    "貴": ("quý", "cao quý, đáng trọng"),
    "賀": ("hạ", "chúc mừng"),
    "徳": ("đức", "đức hạnh, phẩm chất tốt"),
    "遺": ("di", "để lại, di sản"),
    "墓": ("mộ", "mồ mả, phần mộ"),
    "故": ("cố", "lý do, cố nhân, qua đời"),
    "桃": ("đào", "cây đào, quả đào"),
    "芋": ("vu", "khoai"),
    "栗": ("lật", "hạt dẻ"),
    "沸": ("phí", "sôi, đun sôi"),
    "煮": ("chử", "nấu, luộc, hầm"),
    "炊": ("xuy", "nấu cơm, đun nấu"),
    "炒": ("sao", "xào, rang"),
    "蒸": ("chưng", "hấp, bốc hơi"),
    "舎": ("xá", "nhà, ký túc xá, nơi ở"),
    "塔": ("tháp", "tòa tháp"),
    "房": ("phòng", "buồng, phòng, chùm"),
    "倉": ("thương", "kho, nhà kho"),
    "鉢": ("bát", "bát, chậu, bình chứa"),
    "栓": ("thuyên", "nút, chốt, vòi"),
    "棚": ("bằng", "kệ, giá, giàn"),
    "臭": ("xú", "mùi hôi, có mùi"),
    "暇": ("hạ", "thời gian rảnh"),
    "雰": ("phân", "khí, không khí, bầu không khí"),
    "朗": ("lãng", "sáng sủa, vui vẻ, rõ ràng"),
    "裕": ("dụ", "dư dả, phong phú"),
    "徴": ("trưng", "dấu hiệu, thu thuế, trưng cầu"),
    "奇": ("kỳ", "lạ, kỳ diệu"),
    "至": ("chí", "đến, chí cực"),
    "頃": ("khoảnh", "lúc, khoảng thời gian"),
    "宜": ("nghi", "thích hợp, nên"),
    "悄": ("tiễu", "buồn bã, lặng lẽ"),
    "慣": ("quán", "quen, thói quen"),
    "寂": ("tịch", "vắng lặng, cô quạnh"),
    "文": ("văn", "văn chương, chữ viết"),
    "悔": ("hối", "hối hận, tiếc nuối"),
    "怪": ("quái", "lạ, đáng ngờ"),
    "幹": ("cán", "thân cây, cốt lõi, cán bộ"),
    "郊": ("giao", "ngoại ô"),
    "尾": ("vĩ", "đuôi, phần cuối"),
    "窒": ("trất", "nghẹt, bít kín"),
    "素": ("tố", "yếu tố, đơn sơ, chất"),
    "酸": ("toan", "axit, chua"),
    "沿": ("duyên", "men theo, dọc theo"),
    "没": ("một", "chìm, mất, qua đời"),
    "雲": ("vân", "mây"),
    "樺": ("hoa", "cây bạch dương"),
    "蝶": ("điệp", "bướm"),
    "蚊": ("văn", "muỗi"),
    "卵": ("noãn", "trứng"),
    "雀": ("tước", "chim sẻ"),
    "鳩": ("cưu", "chim bồ câu"),
    "鴨": ("áp", "vịt"),
    "烏": ("ô", "quạ, màu đen"),
    "鶏": ("kê", "gà"),
    "狼": ("lang", "sói"),
    "猪": ("trư", "lợn rừng"),
    "龍": ("long", "rồng"),
    "蘭": ("lan", "hoa lan"),
    "漢": ("hán", "Hán, Trung Hoa"),
    "陸": ("lục", "đất liền"),
    "岬": ("giáp", "mũi đất"),
    "郡": ("quận", "quận, huyện"),
    "汽": ("khí", "hơi nước, hơi"),
    "船": ("thuyền", "tàu, thuyền"),
    "搬": ("bàn", "vận chuyển, khuân vác"),
    "巡": ("tuần", "đi tuần, vòng quanh"),
    "稲": ("đạo", "cây lúa"),
    "耕": ("canh", "cày cấy, canh tác"),
    "穀": ("cốc", "ngũ cốc"),
    "提": ("đề", "đưa ra, xách, đề xuất"),
    "請": ("thỉnh", "xin, yêu cầu, mời"),
    "派": ("phái", "phe phái, cử đi"),
    "属": ("thuộc", "thuộc về, trực thuộc"),
    "輸": ("thâu", "vận chuyển, nhập/xuất"),
    "勘": ("khám", "trực giác, xem xét, đối chiếu"),
    "障": ("chướng", "cản trở, trở ngại"),
    "概": ("khái", "khái quát, đại thể"),
    "模": ("mô", "mô hình, khuôn mẫu"),
    "拠": ("cứ", "căn cứ, dựa vào"),
    "志": ("chí", "ý chí, chí hướng"),
    "功": ("công", "công lao, thành tích"),
    "秀": ("tú", "xuất sắc, ưu tú"),
    "項": ("hạng", "mục, điều khoản"),
    "監": ("giám", "giám sát, trông coi"),
    "諸": ("chư", "nhiều, các"),
    "班": ("ban", "nhóm, đội"),
    "急": ("cấp", "gấp, khẩn cấp"),
    "揮": ("huy", "chỉ huy, phát huy"),
    "娯": ("ngu", "giải trí, vui chơi"),
    "興": ("hưng", "hứng thú, thịnh vượng"),
    "釣": ("điếu", "câu cá, treo"),
    "撮": ("toát", "chụp, gom lại"),
    "影": ("ảnh", "bóng, hình ảnh"),
    "創": ("sáng", "sáng tạo, khởi tạo"),
    "描": ("miêu", "vẽ, miêu tả"),
    "笛": ("địch", "sáo"),
    "典": ("điển", "quy tắc, kinh điển"),
    "矢": ("thỉ", "mũi tên"),
    "宮": ("cung", "cung điện, đền"),
    "皇": ("hoàng", "hoàng đế, hoàng gia"),
    "奨": ("tưởng", "khuyến khích, cổ vũ"),
    "栄": ("vinh", "vinh quang, phồn vinh"),
    "幕": ("mạc", "màn, chính phủ mạc phủ"),
    "紀": ("kỷ", "kỷ nguyên, ghi chép"),
    "郷": ("hương", "quê hương, làng quê"),
    "旗": ("kỳ", "lá cờ"),
    "織": ("chức", "dệt, tổ chức"),
    "染": ("nhiễm", "nhuộm, thấm"),
    "頬": ("giáp", "má"),
    "癖": ("tích", "thói quen, tật"),
    "膚": ("phu", "da"),
    "肺": ("phế", "phổi"),
    "腸": ("trường", "ruột"),
    "肥": ("phì", "béo, phân bón"),
    "秘": ("bí", "bí mật"),
    "密": ("mật", "kín, dày đặc, bí mật"),
    "締": ("đế", "thắt,締結, kết chặt"),
    "施": ("thi", "thi hành, ban phát"),
    "訴": ("tố", "tố cáo, khởi kiện, kêu gọi"),
    "審": ("thẩm", "xét xử, thẩm tra"),
    "却": ("khước", "từ chối, loại bỏ"),
    "賃": ("nhẫm", "tiền thuê, tiền công"),
}

REPRESENTATIVE_WORD_FALLBACKS = {
    "抵": [("抵抗", "ていこう", "sự kháng cự, chống đối")],
    "奪": [("奪取", "だっしゅ", "sự đoạt lấy, chiếm lấy")],
    "諦": [("諦める", "あきらめる", "từ bỏ, chịu thua")],
    "輝": [("輝く", "かがやく", "tỏa sáng")],
    "砕": [("砕く", "くだく", "nghiền nát, đập vụn")],
    "褒": [("褒める", "ほめる", "khen ngợi")],
    "婿": [("花婿", "はなむこ", "chú rể")],
    "縁": [("縁談", "えんだん", "chuyện bàn hôn nhân")],
    "徳": [("道徳", "どうとく", "đạo đức")],
    "俺": [("俺たち", "おれたち", "bọn tôi, chúng tôi")],
    "己": [("自己", "じこ", "bản thân, tự mình")],
    "魂": [("霊魂", "れいこん", "linh hồn")],
    "桃": [("桃色", "ももいろ", "màu hồng đào")],
    "芋": [("焼き芋", "やきいも", "khoai nướng")],
    "栗": [("栗色", "くりいろ", "màu hạt dẻ")],
    "藻": [("海藻", "かいそう", "rong biển")],
    "炒": [("炒飯", "チャーハン", "cơm rang")],
    "鍋": [("鍋物", "なべもの", "món lẩu, món nấu nồi")],
    "塔": [("鉄塔", "てっとう", "tháp sắt")],
    "棟": [("病棟", "びょうとう", "khu bệnh, tòa bệnh viện")],
    "綱": [("手綱", "たづな", "dây cương")],
    "網": [("網戸", "あみど", "cửa lưới")],
    "鉢": [("植木鉢", "うえきばち", "chậu cây cảnh")],
    "栓": [("水栓", "すいせん", "vòi nước")],
    "扉": [("扉絵", "とびらえ", "tranh mở đầu sách")],
    "棚": [("本棚", "ほんだな", "giá sách")],
    "堀": [("堀川", "ほりかわ", "sông hào, kênh hào")],
    "甲": [("甲乙", "こうおつ", "giáp ất, thứ hạng")],
    "宜": [("適宜", "てきぎ", "thích hợp, tùy lúc")],
    "悄": [("悄然", "しょうぜん", "buồn bã, lặng lẽ")],
    "懐": [("懐中", "かいちゅう", "trong túi, trong lòng")],
    "芝": [("芝生", "しばふ", "bãi cỏ")],
    "尾": [("尾行", "びこう", "theo dõi, bám theo")],
    "窒": [("窒息", "ちっそく", "ngạt thở")],
    "酸": [("酸素", "さんそ", "oxy")],
    "浦": [("津々浦々", "つつうらうら", "khắp mọi miền, mọi nơi")],
    "樺": [("白樺", "しらかば", "cây bạch dương")],
    "蝶": [("蝶々", "ちょうちょう", "con bướm")],
    "蚊": [("蚊帳", "かや", "màn chống muỗi")],
    "亀": [("亀裂", "きれつ", "vết nứt")],
    "蛇": [("蛇口", "じゃぐち", "vòi nước")],
    "雀": [("雀蜂", "すずめばち", "ong bắp cày")],
    "鳩": [("鳩時計", "はとどけい", "đồng hồ chim cu")],
    "鴨": [("鴨肉", "かもにく", "thịt vịt")],
    "烏": [("烏龍茶", "ウーロンちゃ", "trà ô long")],
    "鶴": [("鶴亀", "つるかめ", "hạc và rùa, điềm lành")],
    "鶏": [("鶏肉", "とりにく", "thịt gà")],
    "牙": [("象牙", "ぞうげ", "ngà voi")],
    "狼": [("狼狽", "ろうばい", "sự hoảng hốt, bối rối")],
    "猪": [("猪突", "ちょとつ", "lao thẳng, xông thẳng")],
    "熊": [("熊手", "くまで", "cái cào, cào tre")],
    "竜": [("竜巻", "たつまき", "lốc xoáy")],
    "龍": [("龍神", "りゅうじん", "long thần")],
    "蘭": [("蘭学", "らんがく", "Lan học, Tây học thời Edo")],
    "柳": [("柳腰", "やなぎごし", "eo thon mềm mại")],
    "岬": [("岬巡り", "みさきめぐり", "chuyến đi quanh các mũi đất")],
    "郡": [("郡部", "ぐんぶ", "vùng quận/huyện")],
    "汽": [("汽車", "きしゃ", "tàu hỏa")],
    "稲": [("稲作", "いなさく", "trồng lúa")],
    "耕": [("耕作", "こうさく", "canh tác")],
    "穀": [("穀物", "こくもつ", "ngũ cốc")],
    "輸": [("輸送", "ゆそう", "vận chuyển")],
    "礎": [("基礎", "きそ", "cơ sở, nền tảng")],
    "秀": [("優秀", "ゆうしゅう", "ưu tú, xuất sắc")],
    "欄": [("欄外", "らんがい", "ngoài lề")],
    "矛": [("矛盾", "むじゅん", "mâu thuẫn")],
    "諸": [("諸国", "しょこく", "các nước")],
    "班": [("班長", "はんちょう", "trưởng nhóm")],
    "誠": [("誠実", "せいじつ", "chân thành, thành thực")],
    "揮": [("指揮", "しき", "chỉ huy")],
    "娯": [("娯楽", "ごらく", "giải trí")],
    "琴": [("琴線", "きんせん", "dây đàn, cảm xúc sâu kín")],
    "笛": [("汽笛", "きてき", "còi tàu")],
    "雅": [("優雅", "ゆうが", "thanh nhã, tao nhã")],
    "弓": [("弓道", "きゅうどう", "cung đạo")],
    "剣": [("剣道", "けんどう", "kiếm đạo")],
    "侍": [("侍従", "じじゅう", "người hầu cận")],
    "宮": [("宮殿", "きゅうでん", "cung điện")],
    "皇": [("皇室", "こうしつ", "hoàng thất")],
    "幻": [("幻想", "げんそう", "ảo tưởng, huyễn tưởng")],
    "幕": [("幕府", "ばくふ", "mạc phủ")],
    "頬": [("頬骨", "ほおぼね", "xương gò má")],
    "唇": [("口唇", "こうしん", "môi")],
    "喉": [("咽喉", "いんこう", "cổ họng")],
    "掌": [("掌握", "しょうあく", "nắm giữ, kiểm soát")],
    "癖": [("口癖", "くちぐせ", "thói quen nói")],
    "裸": [("裸足", "はだし", "chân trần")],
    "肘": [("肘掛け", "ひじかけ", "tay vịn")],
    "脇": [("脇役", "わきやく", "vai phụ")],
    "尻": [("尻尾", "しっぽ", "cái đuôi")],
    "腸": [("胃腸", "いちょう", "dạ dày và ruột")],
    "肝": [("肝心", "かんじん", "quan trọng, cốt yếu")],
    "藤": [("藤棚", "ふじだな", "giàn hoa tử đằng")],
    "麻": [("麻酔", "ますい", "gây mê")],
    "浜": [("砂浜", "すなはま", "bãi cát ven biển")],
    "鹿": [("鹿肉", "しかにく", "thịt nai")],
    "杉": [("杉林", "すぎばやし", "rừng tuyết tùng")],
    "鈴": [("鈴虫", "すずむし", "dế chuông")],
    "奴": [("奴隷", "どれい", "nô lệ")],
    "又": [("又聞き", "またぎき", "nghe qua người khác")],
    "菊": [("菊花", "きっか", "hoa cúc")],
    "炎": [("炎上", "えんじょう", "bốc cháy, gây tranh cãi")],
    "股": [("股関節", "こかんせつ", "khớp háng")],
    "旨": [("趣旨", "しゅし", "chủ旨, ý chính")],
    "雷": [("雷雨", "らいう", "mưa dông")],
    "梨": [("洋梨", "ようなし", "lê tây")],
    "宴": [("宴会", "えんかい", "tiệc, yến tiệc")],
    "嵐": [("砂嵐", "すなあらし", "bão cát")],
    "唾": [("唾液", "だえき", "nước bọt")],
    "暁": [("暁方", "あけがた", "lúc rạng sáng")],
    "艶": [("艶消し", "つやけし", "làm mờ, độ mờ")],
    "俵": [("米俵", "こめだわら", "bao gạo")],
    "麓": [("山麓", "さんろく", "chân núi")],
    "漆": [("漆器", "しっき", "đồ sơn mài")],
    "薪": [("薪割り", "まきわり", "chẻ củi")],
    "艇": [("艦艇", "かんてい", "tàu chiến, chiến hạm")],
    "茨": [("茨城", "いばらき", "Ibaraki")],
}


def load_kanji_api_cache() -> dict:
    if KANJI_API_CACHE.exists():
        return json.loads(KANJI_API_CACHE.read_text(encoding="utf-8"))
    return {}


def save_kanji_api_cache(cache: dict) -> None:
    KANJI_API_CACHE.parent.mkdir(parents=True, exist_ok=True)
    KANJI_API_CACHE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_unihan_vietnamese_readings() -> dict[str, str]:
    if not UNIHAN_READINGS_FILE.exists():
        return {}

    readings = {}
    for line in UNIHAN_READINGS_FILE.read_text(encoding="utf-8").splitlines():
        if "\tkVietnamese\t" not in line:
            continue
        code_point, _, value = line.split("\t", 2)
        readings[chr(int(code_point[2:], 16))] = value
    return readings


def fetch_kanji_api(character: str, cache: dict) -> dict:
    if not ENRICH_KANJI_API:
        return {}
    if character in cache:
        return cache[character]
    response = requests.get(
        f"https://kanjiapi.dev/v1/kanji/{character}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()
    cache[character] = response.json()
    save_kanji_api_cache(cache)
    return cache[character]


def join_readings(values: list[str] | None) -> str | None:
    if not values:
        return None
    return "・".join(values)


def is_single_kanji(value: str) -> bool:
    return len(value) == 1 and 0x3400 <= ord(value) <= 0x9FFF


def parse_trilu_n1() -> dict:
    path = Path(SUPPLEMENT_FILE)
    if not path.exists():
        return {}

    doc = fitz.open(path)
    result = {}
    for page in doc:
        lines = [line.strip() for line in page.get_text().splitlines() if line.strip()]
        text = "\n".join(lines)
        match = re.search(r"\n([\u3400-\u9fff])\n([A-Za-zÀ-ỹĐđ, .'-]+)\nBản đồ chữ", text)
        if not match:
            continue
        character = match.group(1)
        han_viet = match.group(2).strip()

        meaning_vi = None
        if "Ý nghĩa" in lines and "Chữ liên quan" in lines:
            start = lines.index("Ý nghĩa") + 1
            end = lines.index("Chữ liên quan")
            meaning_parts = [item for item in lines[start:end] if item]
            meaning_vi = ", ".join(meaning_parts[:3])

        onyomi = None
        kunyomi = None
        try:
            on_index = lines.index("ÂM ON")
            kun_index = lines.index("ÂM KUN")
            meaning_index = lines.index("Ý nghĩa")
            on_parts = lines[kun_index + 1 : meaning_index]
            if on_parts:
                onyomi = "・".join(on_parts)
            if kun_index + 1 < meaning_index:
                kunyomi = lines[meaning_index - 1]
        except ValueError:
            pass

        vocab = []
        if "Từ vựng trọng tâm" in lines and "Đọc từ tâm → theo từng nhánh → ôn lại bằng từ vựng" in lines:
            start = lines.index("Từ vựng trọng tâm") + 1
            end = lines.index("Đọc từ tâm → theo từng nhánh → ôn lại bằng từ vựng")
            block = lines[start:end]
            i = 0
            while i + 2 < len(block) and len(vocab) < 4:
                word = block[i]
                reading = block[i + 1].strip("（）")
                meaning = block[i + 2]
                if word and reading and meaning and "（" in block[i + 1]:
                    vocab.append((word, reading, meaning))
                    i += 3
                else:
                    i += 1

        result[character] = {
            "han_viet": han_viet,
            "meaning_vi": meaning_vi,
            "onyomi": onyomi,
            "kunyomi": kunyomi,
            "vocab": vocab,
        }
    return result


def load_local_vocab_by_kanji() -> dict[str, list[tuple[str, str, str]]]:
    vocab_by_kanji: dict[str, list[tuple[str, str, str]]] = {}
    import_dir = OUTPUT.parent

    for path in sorted(import_dir.glob("jlpt_n*_vocabulary_db_import.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data.get("vocabularies", []):
            word = (item.get("word") or "").strip()
            reading = (item.get("reading") or "").strip()
            meaning_vi = (item.get("meaning_vi") or "").strip()
            if len(word) < 2 or not reading or not meaning_vi:
                continue
            for character in {char for char in word if is_single_kanji(char)}:
                vocab_by_kanji.setdefault(character, [])
                row = (word, reading, meaning_vi)
                if row not in vocab_by_kanji[character]:
                    vocab_by_kanji[character].append(row)

    return vocab_by_kanji


def fetch_jlpt_1_list() -> list[str]:
    response = requests.get(
        "https://kanjiapi.dev/v1/kanji/jlpt-1",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def build_word_example(word: str, reading: str, meaning_vi: str) -> tuple[str, str, str]:
    return (
        f"この文で「{word}」を確認します。",
        f"このぶんで「{reading}」をかくにんします。",
        f"Câu này dùng từ '{word}' ({meaning_vi}).",
    )


def build_data() -> dict:
    trilu_data = parse_trilu_n1()
    local_vocab_by_kanji = load_local_vocab_by_kanji()
    kanji_cache = load_kanji_api_cache()
    unihan_readings = load_unihan_vietnamese_readings()
    core_values = {character for topic in TOPICS for character in topic[-1]}
    extra_needed = sum(spec[-1] for spec in EXTRA_TOPIC_SPECS)
    extra_values = []
    seen_values = set(core_values)

    for character_value in trilu_data:
        if (
            is_single_kanji(character_value)
            and character_value not in seen_values
        ):
            extra_values.append(character_value)
            seen_values.add(character_value)
        if len(extra_values) >= extra_needed:
            break

    if len(extra_values) < extra_needed:
        for character_value in fetch_jlpt_1_list():
            if (
                is_single_kanji(character_value)
                and character_value not in seen_values
            ):
                extra_values.append(character_value)
                seen_values.add(character_value)
            if len(extra_values) >= extra_needed:
                break

    if len(extra_values) != extra_needed:
        raise ValueError(
            f"Expected {extra_needed} extra kanji, got {len(extra_values)}"
        )

    topic_items = list(TOPICS)
    offset = 0
    for topic_id, name, name_reading, name_vi, page_start, count in EXTRA_TOPIC_SPECS:
        character_values = "".join(extra_values[offset : offset + count])
        offset += count
        topic_items.append(
            (topic_id, name, name_reading, name_vi, page_start, character_values)
        )

    topics = []
    characters = []
    words = []
    character_id = 1
    word_id = 1

    for topic_id, name, name_reading, name_vi, page_start, character_values in topic_items:
        section_name = "必修編" if topic_id <= 14 else ("難読編" if topic_id == 30 else "熟達編")
        topics.append(
            {
                "id": topic_id,
                "jlpt_level_id": 5,
                "name": name,
                "name_reading": name_reading,
                "name_vi": name_vi,
                "description": f"Kanji Master N1 - {section_name} Chương {topic_id}: {name} ({name_vi}).",
                "source_book": "Kanji Master N1",
                "source_week": topic_id,
                "source_week_title": name,
                "source_week_title_vi": name_vi,
                "source_day": None,
                "source_page_start": page_start,
                "source_url": SOURCE_FILE,
                "display_order": topic_id,
                "is_published": True,
                "version": 1,
            }
        )

        for display_order, character_value in enumerate(character_values, start=1):
            api_data = fetch_kanji_api(character_value, kanji_cache)
            supplement = trilu_data.get(character_value, {})
            fallback = HAN_VIET_AND_MEANING_FALLBACKS.get(character_value)
            han_viet = (
                supplement.get("han_viet")
                or (fallback[0] if fallback else None)
                or unihan_readings.get(character_value)
                or character_value
            )
            meaning_vi = supplement.get("meaning_vi") or (fallback[1] if fallback else None)
            if not meaning_vi:
                meanings = api_data.get("meanings") or []
                meaning_vi = ", ".join(meanings[:3]) if meanings else "cần bổ sung nghĩa"
            onyomi = supplement.get("onyomi") or join_readings(api_data.get("on_readings")) or "なし"
            kunyomi = supplement.get("kunyomi") or join_readings(api_data.get("kun_readings")) or "なし"

            characters.append(
                {
                    "id": character_id,
                    "kanji_topic_id": topic_id,
                    "character_value": character_value,
                    "han_viet": han_viet.lower(),
                    "onyomi": onyomi,
                    "kunyomi": kunyomi,
                    "meaning_vi": meaning_vi,
                    "stroke_count": api_data.get("stroke_count"),
                    "mnemonic_vi": f"Ghi nhớ chữ {character_value} theo nghĩa '{meaning_vi}'.",
                    "display_order": display_order,
                    "is_published": True,
                    "version": 1,
                }
            )

            vocab_rows = list(supplement.get("vocab") or [])
            known_words = {row[0] for row in vocab_rows}
            for local_row in local_vocab_by_kanji.get(character_value, []):
                if local_row[0] in known_words:
                    continue
                vocab_rows.append(local_row)
                known_words.add(local_row[0])
                if len(vocab_rows) >= 3:
                    break

            representative_rows = REPRESENTATIVE_WORD_FALLBACKS.get(character_value, [])
            if representative_rows and (
                not vocab_rows
                or all(row[0] == character_value for row in vocab_rows)
            ):
                vocab_rows = list(representative_rows)
                known_words = {row[0] for row in vocab_rows}
            elif representative_rows and len(vocab_rows) < 3:
                for representative_row in representative_rows:
                    if representative_row[0] in known_words:
                        continue
                    vocab_rows.append(representative_row)
                    known_words.add(representative_row[0])
                    if len(vocab_rows) >= 3:
                        break

            if not vocab_rows:
                fallback_word = character_value
                fallback_reading = (kunyomi if kunyomi != "なし" else onyomi).split("・")[0]
                vocab_rows = [(fallback_word, fallback_reading, meaning_vi)]

            for word_display_order, (word, reading, word_meaning_vi) in enumerate(vocab_rows[:3], start=1):
                example_sentence, example_reading, example_meaning_vi = build_word_example(
                    word,
                    reading,
                    word_meaning_vi,
                )
                words.append(
                    {
                        "id": word_id,
                        "kanji_character_id": character_id,
                        "word": word,
                        "reading": reading,
                        "meaning_vi": word_meaning_vi,
                        "example_sentence": example_sentence,
                        "example_reading": example_reading,
                        "example_meaning_vi": example_meaning_vi,
                        "display_order": word_display_order,
                        "is_published": True,
                        "version": 1,
                    }
                )
                word_id += 1

            character_id += 1

    return {
        "metadata": {
            "name": "JLPT N1 kanji import data by Kanji Master N1 full section",
            "status": "ready_for_review_database_import",
            "jlpt_level_code": "N1",
            "jlpt_level_id_assumption": 5,
            "source_file": SOURCE_FILE,
            "source_note": (
                "The first 548 必修編 kanji follow the Kanji Master N1 table of contents. "
                "The remaining 395 characters complete the book-sized N1 set with "
                "熟達編 and 難読編 topics, prioritizing local Trilu N1 data for meanings "
                "and vocabulary and falling back to KanjiAPI where needed."
            ),
            "supplement_file": SUPPLEMENT_FILE,
            "enrichment_source": "https://kanjiapi.dev/ for stroke counts and fallback readings",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "import_order_when_completed": [
                "kanji_topics",
                "kanji_characters",
                "kanji_words",
            ],
            "notes": [
                "kanji_topics.name is Japanese-first; kanji_topics.name_vi is the Vietnamese subtitle.",
                "No note field is generated.",
                "Each kanji has representative learning words and generated example_* fields.",
            ],
        },
        "kanji_topics": topics,
        "kanji_characters": characters,
        "kanji_words": words,
    }


def validate(data: dict) -> None:
    if len(data["kanji_topics"]) != 30:
        raise ValueError(f"Expected 30 topics, got {len(data['kanji_topics'])}")
    if len(data["kanji_characters"]) != 943:
        raise ValueError(f"Expected 943 kanji characters, got {len(data['kanji_characters'])}")
    values = [char["character_value"] for char in data["kanji_characters"]]
    if len(values) != len(set(values)):
        duplicates = sorted({value for value in values if values.count(value) > 1})
        raise ValueError(f"Duplicate kanji characters: {duplicates}")

    topic_ids = {topic["id"] for topic in data["kanji_topics"]}
    character_ids = {char["id"] for char in data["kanji_characters"]}

    for group in ("kanji_topics", "kanji_characters", "kanji_words"):
        for item in data[group]:
            if "note" in item:
                raise ValueError(f"Unexpected note field in {group}: {item}")

    for char in data["kanji_characters"]:
        if char["kanji_topic_id"] not in topic_ids:
            raise ValueError(f"Invalid kanji_topic_id: {char}")
        for key in (
            "character_value",
            "han_viet",
            "onyomi",
            "kunyomi",
            "meaning_vi",
            "stroke_count",
            "mnemonic_vi",
        ):
            if char.get(key) in (None, ""):
                raise ValueError(f"Missing {key}: {char}")

    for word in data["kanji_words"]:
        if word["kanji_character_id"] not in character_ids:
            raise ValueError(f"Invalid kanji_character_id: {word}")
        for key in (
            "word",
            "reading",
            "meaning_vi",
            "example_sentence",
            "example_reading",
            "example_meaning_vi",
        ):
            if word.get(key) in (None, ""):
                raise ValueError(f"Missing {key}: {word}")


def main() -> None:
    data = build_data()
    validate(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")
    print(f"topics={len(data['kanji_topics'])}")
    print(f"kanji_characters={len(data['kanji_characters'])}")
    print(f"kanji_words={len(data['kanji_words'])}")


if __name__ == "__main__":
    main()
