# -*- coding: utf-8 -*-
"""Hebrew-first bilingual copy for the public site.

Hebrew is the default and the design language: the layout is RTL, and the
French translation rides along for the older Tunisian-Jewish audience the
logo speaks to ("Cuisine Tunisienne").

Anything wrapped in [[ ]] is a placeholder the owner still has to supply -
grep for it before going live. See CONTENT_TODO.md.
"""

LANGUAGES = {
    "he": {"name": "עברית", "dir": "rtl", "short": "HE"},
    "fr": {"name": "Français", "dir": "ltr", "short": "FR"},
}

DEFAULT_LANG = "he"

TRANSLATIONS = {
    # ── Chrome ──────────────────────────────────────────────────
    "brand_name": {"he": "נעמי", "fr": "Neomi"},
    "brand_latin": {"he": "Neomi", "fr": "נעמי"},
    "brand_tagline": {"he": "מטבח טוניסאי", "fr": "Cuisine Tunisienne"},
    "fish_tagline": {"he": "דגים מהים", "fr": "Poisson de la mer"},
    "meat_tagline": {"he": "בשרי", "fr": "Plat de viande"},
    "kosher_badge": {"he": "כשר למהדרין", "fr": "Casher Lemehadrin"},

    "nav_home": {"he": "דף הבית", "fr": "Accueil"},
    "nav_menu": {"he": "התפריט", "fr": "La carte"},
    "nav_kosher": {"he": "כשר למהדרין", "fr": "Casher Lemehadrin"},
    "nav_gallery": {"he": "גלריה", "fr": "Galerie"},
    "nav_about": {"he": "הסיפור שלנו", "fr": "Notre histoire"},
    "nav_reservations": {"he": "הזמנת שולחן", "fr": "Réserver"},
    "nav_order": {"he": "משלוחים ואיסוף", "fr": "Commander"},
    "nav_events": {"he": "אירועים", "fr": "Événements"},
    "nav_contact": {"he": "צרו קשר", "fr": "Contact"},

    "site_title_suffix": {
        "he": "מסעדה טוניסאית כשרה",
        "fr": "Restaurant tunisien casher",
    },
    "meta_description": {
        "he": "נעמי — מטבח טוניסאי אותנטי, כשר למהדרין. קומפלט פואסון, סלטים, קוסקוס ומנות שנעשות כמו בבית. בואו לטעום.",
        "fr": "Neomi — cuisine tunisienne authentique, casher lemehadrin. Complet poisson, salades, couscous. Venez goûter.",
    },

    # ── Hero ────────────────────────────────────────────────────
    "hero_eyebrow": {"he": "מטבח טוניסאי · כשר למהדרין", "fr": "Cuisine Tunisienne · Casher"},
    "hero_headline": {"he": "בואו לטעום", "fr": "Venez goûter"},
    "hero_sub": {
        "he": "אוכל טוניסאי אמיתי, כמו שהיה בבית של סבתא",
        "fr": "La vraie cuisine tunisienne, comme à la maison — et c'est nous qui faisons la vaisselle.",
    },
    "hero_cta_reserve": {"he": "הזמינו שולחן", "fr": "Réserver une table"},
    "hero_cta_call": {"he": "התקשרו אלינו", "fr": "Appelez-nous"},
    "hero_scroll": {"he": "גללו למטה", "fr": "Faites défiler"},

    # ── Trust strip ─────────────────────────────────────────────
    "trust_kosher": {"he": "כשר למהדרין", "fr": "Casher Lemehadrin"},
    "trust_authentic": {"he": "מטבח טוניסאי אותנטי", "fr": "Cuisine tunisienne authentique"},
    "trust_shabbat": {"he": "סגור בשישי ובשבת", "fr": "Fermé vendredi et Chabbat"},
    "trust_events": {"he": "אירועים ושמחות", "fr": "Événements et fêtes"},

    # ── Signature dish story ────────────────────────────────────
    "story_eyebrow": {"he": "המנה שבאים בשבילה", "fr": "Le plat signature"},
    "story_title": {"he": "הקומפלט פואסון של נעמי", "fr": "Le Complet Poisson de Neomi"},
    "story_intro": {
        "he": "מנה אחת, שש סיבות לבוא. דג שלם על הגריל, חריסה שנטחנת אצלנו, ביצה, צ'יפס — והכול מגיע לשולחן ביחד.",
        "fr": "Un seul plat, six raisons de venir. Un poisson entier grillé, notre harissa maison, un œuf, des frites — tout arrive à table ensemble.",
    },
    "story_1_alt": {"he": "קומפלט פואסון של נעמי — המנה המלאה", "fr": "Le Complet Poisson de Neomi"},
    "story_2_alt": {"he": "דג שלם צרוב על הגריל", "fr": "Poisson entier grillé"},
    "story_3_alt": {"he": "ביצת עין על גבי המנה", "fr": "Œuf au plat sur le poisson"},
    "story_4_alt": {"he": "צ'יפס טרי לצד הדג", "fr": "Frites fraîches"},
    "story_5_alt": {"he": "חריסה טוניסאית בהכנה עצמית", "fr": "Harissa tunisienne maison"},
    "story_6_alt": {"he": "המנה השלמה על מגש", "fr": "Le plat complet sur son plateau"},
    "story_cta": {"he": "הזמינו שולחן", "fr": "Réserver une table"},

    # ── Salatim / table ─────────────────────────────────────────
    "salatim_eyebrow": {"he": "לפני שמתחילים", "fr": "Pour commencer"},
    "salatim_title": {"he": "השולחן מתמלא לפני שהזמנתם", "fr": "La table se remplit avant même de commander"},
    "salatim_text": {
        "he": "מטבוחה, סלט חצילים, סלק, לפת, גזר בחריסה, תפוחי אדמה — הסלטים מתחלפים לפי מה שיש בשוק ומגיעים לשולחן בלי לשאול. ככה זה אצלנו.",
        "fr": "Matbucha, caviar d'aubergines, betteraves, navets, carottes à la harissa, pommes de terre — les salades changent selon le marché et arrivent sans qu'on les demande. C'est comme ça chez nous.",
    },
    "salatim_alt_overhead": {"he": "מגוון סלטים טוניסאיים על מפה משובצת", "fr": "Assortiment de salades tunisiennes"},
    "salatim_alt_spread": {"he": "סלטים בקערות לבנות על השולחן", "fr": "Salades en bols blancs sur la table"},
    "salatim_alt_matbucha": {"he": "מטבוחה טוניסאית", "fr": "Matbucha tunisienne"},
    "salatim_alt_eggplant": {"he": "סלט חצילים", "fr": "Caviar d'aubergines"},

    # ── Dishes photographed at the restaurant ───────────────────
    "dish_alt_complet": {
        "he": "קומפלט פואסון על השולחן, עם מגוון סלטי הבית",
        "fr": "Complet poisson servi avec les salades maison",
    },
    "dish_alt_banatagge": {
        "he": "בנטז׳ — תפוחי אדמה ממולאים בבשר, עם אורז וסלט",
        "fr": "Banatagge — pommes de terre farcies à la viande, riz et salade",
    },
    "dish_alt_pargit": {
        "he": "פרגית על הגריל עם צ׳יפס וסלט",
        "fr": "Parguit grillé, frites et salade",
    },
    "dish_alt_table_spread": {
        "he": "שולחן ערוך במסעדה — מנות הבית והסלטים ביחד",
        "fr": "Une table dressée au restaurant — les plats et les salades ensemble",
    },
    "dish_alt_spaghetti": {
        "he": "ספגטי בולונז",
        "fr": "Spaghetti bolognaise",
    },

    # ── About / story ───────────────────────────────────────────
    "about_eyebrow": {"he": "הסיפור שלנו", "fr": "Notre histoire"},
    "about_title": {"he": "המתכונים של סבתא נעמי", "fr": "Les recettes de Mamie Neomi"},
    "about_p1": {
        "he": "סבתא נעמי ז״ל גדלה בטוניס, בבית שבו האוכל היה חלק מהחיים עצמם: סירים על האש, שולחן פתוח, וטעמים שנשארים בזיכרון הרבה אחרי הארוחה. המתכונים שהשאירה עברו למשפחה, ומהם נולדה המסעדה.",
        "fr": "Mamie Neomi, de mémoire bénie, a grandi à Tunis, dans une maison où la cuisine faisait partie de la vie même : les marmites sur le feu, la table toujours ouverte, et des goûts qui restent en mémoire longtemps après le repas. Les recettes qu'elle a laissées sont passées à la famille, et le restaurant en est né.",
    },
    "about_p2": {
        "he": "אנחנו ממשיכים את המתכונים שקיבלנו ממנה, ואת האירוח החם והנדיב שבא איתם.",
        "fr": "Nous prolongeons les recettes que nous avons reçues d'elle, et l'hospitalité chaleureuse et généreuse qui va avec.",
    },
    "about_more": {"he": "כל הסיפור", "fr": "Toute l'histoire"},
    "about_portrait_alt": {"he": "תצלום של סבתא נעמי ז״ל, במטבח המסעדה", "fr": "Photo de Mamie Neomi, de mémoire bénie, dans la cuisine du restaurant"},
    "about_kitchen_alt": {"he": "ארוחה משפחתית במטבח", "fr": "Repas de famille dans la cuisine"},

    # ── About page (/about) ─────────────────────────────────────
    # The owner's own account of the place, supplied 25/08/2026 and used
    # close to verbatim in Hebrew. Neomi is the GRANDMOTHER - "סבתא נעמי" -
    # who grew up in Tunis and HAS SINCE PASSED AWAY. The recipes went to
    # her family, who cook them now.
    #
    # She is therefore written about in the past tense throughout, and the
    # first mention in each language carries the traditional honorific
    # (ז״ל in Hebrew, "de mémoire bénie" in French). Keep it that way if
    # this copy is edited: present-tense phrasing about her would be wrong,
    # not just imprecise.
    "about_page_title": {"he": "ברוכים הבאים לנעמי", "fr": "Bienvenue chez Neomi"},
    "about_page_lead": {
        "he": "מסעדה טוניסאית בנתניה שמביאה לשולחן את הטעמים של הבית, את המתכונים של סבתא נעמי ואת החום של אירוח אמיתי.",
        "fr": "Un restaurant tunisien à Netanya qui apporte à table les saveurs de la maison, les recettes de Mamie Neomi et la chaleur d'une vraie hospitalité.",
    },

    "about_ch1_eyebrow": {"he": "השורשים", "fr": "Les racines"},
    "about_ch1_title": {
        "he": "סבתא נעמי, וטוניס שנשארה בזיכרון",
        "fr": "Mamie Neomi, et la Tunis restée en mémoire",
    },
    "about_ch1_text": {
        "he": "סבתא נעמי ז״ל גדלה בטוניס, בבית שבו האוכל היה חלק מהחיים עצמם: סירים על האש, שולחן פתוח, ריחות של קוסקוס ותבשילים טוניסאיים, דגים, מרגז, סלטים, בוריקה ובנטז׳ — וטעמים שנשארים בזיכרון הרבה אחרי הארוחה.",
        "fr": "Mamie Neomi, de mémoire bénie, a grandi à Tunis, dans une maison où la cuisine faisait partie de la vie même : les marmites sur le feu, la table toujours ouverte, les odeurs de couscous et de plats tunisiens, le poisson, la merguez, les salades, la brick et le banatagge — et des goûts qui restent en mémoire longtemps après le repas.",
    },
    "about_ch1_text2": {
        "he": "מתוך הזיכרון הזה נולדה המסעדה: מקום שממשיך את המסורת שלה דרך אוכל טוניסאי אמיתי, מתכונים שעברו מדור לדור, ואהבה גדולה לאירוח חם ונדיב.",
        "fr": "C'est de ce souvenir qu'est né le restaurant : un lieu qui prolonge sa tradition par une vraie cuisine tunisienne, des recettes transmises de génération en génération, et un grand amour de l'hospitalité chaleureuse et généreuse.",
    },

    "about_ch2_eyebrow": {"he": "המטבח", "fr": "La cuisine"},
    "about_ch2_title": {
        "he": "המטבח נשאר נאמן לשורשים",
        "fr": "La cuisine est restée fidèle à ses racines",
    },
    "about_ch2_text": {
        "he": "בוריקה קריספית, מינינה, בנטז׳, פלפל ממולא, שקשוקה ביתית עם מרגז, ספגטי טוניסאי, קומפלט פואסון, דגים ובשרים — ולצידם תבשילי יום שמתחלפים לפי מה שמתבשל במטבח. אלה לא מנות שנבנו סביב תפריט — אלה המתכונים עצמם, כפי שהיא לימדה אותם.",
        "fr": "Brick croustillante, minina, banatagge, poivron farci, chakchouka maison à la merguez, spaghetti tunisien, complet poisson, poissons et viandes — et à côté, les plats du jour qui changent selon ce qui mijote en cuisine. Ce ne sont pas des plats construits autour d'une carte : ce sont ses recettes, telles qu'elle les a transmises.",
    },

    "about_ch3_eyebrow": {"he": "הכשרות", "fr": "La cacherout"},
    "about_ch3_title": {"he": "כשר למהדרין, בלי כוכביות", "fr": "Casher lemehadrin, sans astérisque"},
    "about_ch3_text": {
        "he": "המסעדה בהשגחת בד״ץ ״בהידור הכשרות״ והרבנות הראשית נתניה — בשרי, כשר למהדרין. התעודה עצמה מוצגת כאן באתר, ואפשר להגדיל ולקרוא בה כל שורה, כולל תאריך התוקף.",
        "fr": "Le restaurant est sous la supervision du Badatz « BeHidour HaKashrout » et du Grand Rabbinat de Netanya — viande, casher lemehadrin. Le certificat lui-même est affiché sur ce site : vous pouvez l'agrandir et en lire chaque ligne, date de validité comprise.",
    },
    "about_ch3_cta": {"he": "לתעודת הכשרות", "fr": "Voir le certificat"},

    "about_ch4_eyebrow": {"he": "השולחן", "fr": "La table"},
    "about_ch4_title": {
        "he": "לשבת סביב שולחן מלא",
        "fr": "S'asseoir autour d'une table bien remplie",
    },
    "about_ch4_text": {
        "he": "אנחנו מגישים אוכל טוניסאי כשר למהדרין באווירה נעימה וחמה. זה המקום להגיע אליו לארוחה טובה בנתניה, לשבת סביב שולחן מלא, לטעום מנות טוניסאיות מסורתיות — ולהרגיש שמבשלים בשבילכם כמו בבית.",
        "fr": "Nous servons une cuisine tunisienne casher lemehadrin dans une ambiance agréable et chaleureuse. C'est l'endroit où venir pour un bon repas à Netanya, s'asseoir autour d'une table bien garnie, goûter des plats tunisiens traditionnels — et sentir qu'on cuisine pour vous comme à la maison.",
    },

    # No prepared food for Friday/Shabbat: the owner confirmed on 25/08/2026
    # that it is not offered, so this chapter is about events only. Do not
    # add takeaway copy back without asking.
    "about_ch5_eyebrow": {"he": "אירועים", "fr": "Événements"},
    "about_ch5_title": {
        "he": "אירועים סביב שולחן גדול",
        "fr": "Les événements autour d'une grande table",
    },
    # Carries markup (see the events_text note above): the About chapter
    # text is rendered with |safe in about.html so the capacity can be bold,
    # matching the homepage.
    "about_ch5_text": {
        "he": "אנחנו מתאימים גם לאירועים <strong>עד 120 איש</strong>: שבת חתן, ברית, יום הולדת או ארוחה משפחתית סביב שולחן טוניסאי מלא, עם שירות אישי ותשומת לב לכל פרט.",
        "fr": "Nous recevons aussi les événements <strong>jusqu'à 120 personnes</strong> : Chabbat Hatan, brit-mila, anniversaire ou repas de famille autour d'une table tunisienne bien garnie, avec un service personnalisé et une attention à chaque détail.",
    },
    "about_ch5_cta": {"he": "דברו איתנו בוואטסאפ", "fr": "Écrivez-nous sur WhatsApp"},

    "about_quote": {
        "he": "נעמי היא הבית הטוניסאי של פעם — מסורת, אוכל טוב וטעם אמיתי.",
        "fr": "Neomi, c'est la maison tunisienne d'antan — la tradition, la bonne cuisine et le vrai goût.",
    },

    "about_close_title": {"he": "בואו לשבת איתנו", "fr": "Venez vous asseoir avec nous"},
    "about_close_text": {
        "he": "הזמינו שולחן, או פשוט התקשרו ותגידו לנו מתי אתם מגיעים.",
        "fr": "Réservez une table, ou appelez-nous simplement pour nous dire quand vous venez.",
    },

    "about_where": {"he": "אנחנו כאן", "fr": "Nous sommes ici"},
    "about_table_alt": {"he": "שולחן ערוך במסעדה, קומפלט פואסון וסלטים", "fr": "Une table dressée : complet poisson et salades"},
    "about_events_alt": {"he": "הגשת קוסקוס לשולחן", "fr": "Le couscous arrive à table"},

    # ── Atmosphere ──────────────────────────────────────────────
    "atmos_eyebrow": {"he": "האווירה", "fr": "L'ambiance"},
    "atmos_title": {"he": "שולחן שכייף לשבת מסביבו", "fr": "Une table où il fait bon s'asseoir"},
    "atmos_text": {
        "he": "מנות שמגיעות באמצע השולחן וכולם מושיטים יד. זה מקום לארוחה טעימה באווירה רגועה, נעימה ומשפחתית.",
        "fr": "Les plats arrivent au milieu de la table et tout le monde se sert. C'est un endroit pour un bon repas, dans une ambiance calme, chaleureuse et familiale.",
    },
    "atmos_family_alt": {"he": "משפחה סביב שולחן עמוס", "fr": "Une famille autour d'une table garnie"},
    "atmos_hands_alt": {"he": "ידיים מעבירות מנה חמה", "fr": "Des mains passent un plat chaud"},
    "atmos_couscous_alt": {"he": "הגשת קוסקוס לשולחן", "fr": "Le couscous arrive à table"},
    "atmos_real_alt": {"he": "שולחן אמיתי במסעדה", "fr": "Une vraie table au restaurant"},

    # ── Events ──────────────────────────────────────────────────
    "events_eyebrow": {"he": "אירועים", "fr": "Événements"},
    "events_title": {"he": "שמחות, חגים וארוחות גדולות", "fr": "Fêtes, jours de fête et grands repas"},
    # NOTE: this one value contains markup and is rendered with |safe in
    # index.html, so the capacity can be bold. It is developer-authored
    # copy, never anything a visitor typed. If you add markup to another
    # key, add the |safe at its render site too - the rest of the file is
    # escaped as normal.
    "events_text": {
        "he": "אירועים <strong>עד 120 איש</strong>: בריתות, שבת חתן, ימי הולדת, ארוחות חג וערבי חברה. אפשר לסגור אזור או את כל המסעדה, ולבנות תפריט לפי מספר האורחים.",
        "fr": "Événements <strong>jusqu'à 120 personnes</strong> : brit-mila, Chabbat Hatan, anniversaires, repas de fête et soirées entre amis. Possibilité de privatiser une salle ou tout le restaurant, avec un menu adapté au nombre d'invités.",
    },
    "events_cta": {"he": "דברו איתנו על אירוע", "fr": "Parlons de votre événement"},

    # ── Hours & location ────────────────────────────────────────
    "hours_title": {"he": "שעות פתיחה", "fr": "Horaires"},
    "hours_closed": {"he": "סגור", "fr": "Fermé"},
    "hours_shabbat_note": {
        "he": "בשישי ובשבת סגור. פתוחים ראשון–חמישי, צהריים וערב.",
        "fr": "Fermé le vendredi et le Chabbat. Ouvert du dimanche au jeudi, midi et soir.",
    },
    "open_now": {"he": "פתוח עכשיו", "fr": "Ouvert maintenant"},
    "closed_now": {"he": "סגור עכשיו", "fr": "Fermé actuellement"},

    "location_title": {"he": "איך מגיעים", "fr": "Nous trouver"},
    "nav_waze": {"he": "נווטו ב-Waze", "fr": "Ouvrir dans Waze"},
    "nav_gmaps": {"he": "פתחו ב-Google Maps", "fr": "Ouvrir dans Google Maps"},
    "call_us": {"he": "התקשרו", "fr": "Appeler"},
    "whatsapp_us": {"he": "וואטסאפ", "fr": "WhatsApp"},

    # ── Menu page ───────────────────────────────────────────────
    "menu_title": {"he": "התפריט", "fr": "La carte"},
    "menu_soon_title": {"he": "התפריט המלא בדרך", "fr": "La carte complète arrive"},
    "menu_soon_text": {
        "he": "אנחנו מסדרים את התפריט לפרטי פרטים. בינתיים — התקשרו ונשמח לספר לכם מה יש היום, או הזמינו שולחן ותגלו במקום.",
        "fr": "Nous finalisons la carte. En attendant, appelez-nous pour savoir ce qu'il y a aujourd'hui, ou réservez et découvrez sur place.",
    },
    # Section names exactly as printed on the menu card.
    "cat_appetizer": {"he": "מנות ראשונות", "fr": "Entrées"},
    "cat_main": {"he": "עיקריות", "fr": "Plats principaux"},
    "cat_grill": {"he": "בשרים", "fr": "Grillades & Viandes"},
    "cat_fish": {"he": "דגים", "fr": "Poissons & Spécialités Tunisiennes"},
    "cat_drink": {"he": "שתייה", "fr": "Boissons & Bières"},
    "cat_dessert": {"he": "קינוחים", "fr": "Desserts"},

    # The "opening the table" salatim service - a signature of the house and
    # the first thing that reaches the table.
    "table_open_title": {"he": "פותחים שולחן אצל נעמי", "fr": "On ouvre la table chez Neomi"},
    "table_open_text": {
        "he": "מבחר סלטי הבית מוגש לשולחן בתחילת הארוחה.",
        "fr": "Une sélection de salades maison est servie à table en début de repas.",
    },
    "table_open_price": {"he": "12 ₪ לסועד", "fr": "12 ₪ par personne"},

    "sides_note": {
        "he": "כל המנות מוגשות עם תוספת לבחירה: אורז | צ׳יפס | שעועית ירוקה",
        "fr": "Tous les plats sont servis avec un accompagnement au choix : Riz | Frites | Haricots verts sautés",
    },
    "service_note": {"he": "לא כולל דמי שירות 10%", "fr": "Service non compris"},
    "bsd": {"he": "בס״ד", "fr": "בס״ד"},
    "menu_intro": {
        "he": "אוכל טוניסאי אמיתי | כשר למהדרין",
        "fr": "La vraie cuisine tunisienne | Casher Lemehadrin",
    },
    "menu_download": {"he": "הורדת התפריט (PDF)", "fr": "Télécharger la carte (PDF)"},

    # ── Kashrut certificate ─────────────────────────────────────
    "kosher_title": {"he": "תעודת הכשרות", "fr": "Le certificat de cacherout"},
    "kosher_intro": {
        "he": "המסעדה מפוקחת ומאושרת כשרה למהדרין מן המהדרין. זו התעודה עצמה — אפשר להגדיל ולקרוא.",
        "fr": "Le restaurant est supervisé et certifié casher lemehadrin min hamehadrin. Voici le certificat lui-même — cliquez pour l'agrandir.",
    },
    "kosher_alt": {
        "he": "תעודת הכשרות של מסעדת נעמי מטעם הרבנות הראשית נתניה",
        "fr": "Le certificat de cacherout du restaurant Neomi, délivré par le Grand Rabbinat de Netanya",
    },
    "kosher_supervision_label": {"he": "בהשגחת", "fr": "Sous la supervision de"},
    "kosher_holder_label": {"he": "ניתנה ל", "fr": "Délivré à"},
    "kosher_type_label": {"he": "סוג", "fr": "Type"},
    "kosher_valid_label": {"he": "בתוקף עד", "fr": "Valable jusqu'au"},
    "kosher_valid_from_label": {"he": "מתאריך", "fr": "À partir du"},
    "kosher_expired": {
        "he": "התעודה שמוצגת כאן פגה. תעודה מחודשת תעלה בקרוב — עד אז, נשמח לענות בטלפון.",
        "fr": "Le certificat affiché ici a expiré. Une version renouvelée sera mise en ligne prochainement — d'ici là, appelez-nous.",
    },
    "kosher_view_full": {"he": "פתחו את התעודה בגודל מלא", "fr": "Ouvrir le certificat en grand"},
    "kosher_questions": {
        "he": "שאלות על הכשרות? התקשרו ונשמח להסביר.",
        "fr": "Des questions sur la cacherout ? Appelez-nous, nous serons ravis de vous répondre.",
    },

    # ── Reservations ────────────────────────────────────────────
    "res_title": {"he": "הזמנת שולחן", "fr": "Réserver une table"},
    "res_intro": {
        "he": "שלחו בקשה ונחזור אליכם לאישור. לאירועים ולקבוצות גדולות — עדיף בטלפון.",
        "fr": "Envoyez une demande et nous vous confirmerons. Pour les groupes et événements, préférez le téléphone.",
    },
    "res_name": {"he": "שם מלא", "fr": "Nom complet"},
    "res_phone": {"he": "טלפון", "fr": "Téléphone"},
    "res_date": {"he": "תאריך", "fr": "Date"},
    "res_time": {"he": "שעה", "fr": "Heure"},
    "res_party": {"he": "מספר סועדים", "fr": "Nombre de convives"},
    "res_notes": {"he": "הערות (כיסא תינוק, אלרגיות, אירוע)", "fr": "Remarques (chaise haute, allergies, événement)"},
    "res_submit": {"he": "שלחו בקשה", "fr": "Envoyer la demande"},
    "res_success": {"he": "הבקשה נשלחה! נחזור אליכם לאישור בהקדם.", "fr": "Demande envoyée ! Nous vous confirmerons très vite."},
    "res_error": {"he": "נא למלא את כל שדות החובה.", "fr": "Merci de remplir tous les champs obligatoires."},

    # ── After the booking form ──────────────────────────────────
    "res_sent_title": {"he": "הבקשה נקלטה", "fr": "Demande reçue"},
    "res_sent_lead": {
        "he": "הבקשה שלכם נשמרה אצלנו. נשאר שלב אחד קטן — שלחו לנו את ההודעה בוואטסאפ ונאשר לכם מיד.",
        "fr": "Votre demande a bien été enregistrée. Il reste une petite étape — envoyez-nous le message WhatsApp et nous confirmerons tout de suite.",
    },
    "res_sent_whatsapp": {"he": "שליחת ההודעה בוואטסאפ", "fr": "Envoyer le message WhatsApp"},
    "res_sent_opening": {
        "he": "פותחים וואטסאפ עם ההודעה מוכנה…",
        "fr": "Ouverture de WhatsApp avec le message prêt…",
    },
    "res_sent_manual": {
        "he": "לא נפתח? לחצו על הכפתור.",
        "fr": "Rien ne s'ouvre ? Appuyez sur le bouton.",
    },
    "res_sent_or_call": {
        "he": "מעדיפים לדבר? התקשרו אלינו ונסגור את זה בטלפון.",
        "fr": "Vous préférez parler ? Appelez-nous et nous réglons cela au téléphone.",
    },
    "res_sent_details": {"he": "פרטי הבקשה", "fr": "Détails de la demande"},

    # ── Ordering ────────────────────────────────────────────────
    "order_title": {"he": "משלוחים ואיסוף", "fr": "Livraison et à emporter"},
    "order_pickup": {"he": "איסוף עצמי", "fr": "À emporter"},
    "order_delivery": {"he": "משלוח", "fr": "Livraison"},
    "order_cart": {"he": "העגלה", "fr": "Panier"},
    "order_empty": {"he": "העגלה ריקה", "fr": "Panier vide"},
    "order_total": {"he": "סה\"כ", "fr": "Total"},
    "order_submit": {"he": "שליחת ההזמנה", "fr": "Envoyer la commande"},
    "order_add": {"he": "הוספה", "fr": "Ajouter"},
    "order_confirmed_title": {"he": "ההזמנה נקלטה", "fr": "Commande reçue"},
    "order_thanks": {"he": "תודה", "fr": "Merci"},
    "order_confirmed_text": {
        "he": "קיבלנו את ההזמנה ונתקשר אליכם לאישור.",
        "fr": "Nous avons reçu votre commande et vous appellerons pour la confirmer.",
    },
    "order_number": {"he": "מספר הזמנה", "fr": "N° de commande"},
    "order_type_label": {"he": "סוג", "fr": "Type"},
    "order_address_label": {"he": "כתובת למשלוח", "fr": "Adresse de livraison"},
    "order_items": {"he": "פריטים", "fr": "Articles"},
    "order_notes_label": {"he": "הערות", "fr": "Remarques"},
    "back_home": {"he": "חזרה לדף הבית", "fr": "Retour à l'accueil"},

    # ── Gallery ─────────────────────────────────────────────────
    "gallery_title": {"he": "גלריה", "fr": "Galerie"},
    "gallery_intro": {
        "he": "המנות, השולחנות והאווירה. הכי טוב להגיע ולראות במו עיניכם.",
        "fr": "Les plats, les tables et l'ambiance. Le mieux reste de venir voir.",
    },
    "gallery_tab_all": {"he": "הכול", "fr": "Tout"},
    "gallery_tab_dishes": {"he": "מנות", "fr": "Plats"},
    "gallery_tab_atmos": {"he": "אווירה", "fr": "Ambiance"},
    "gallery_tab_video": {"he": "וידאו", "fr": "Vidéo"},
    "gallery_close": {"he": "סגירה", "fr": "Fermer"},
    "gallery_prev": {"he": "הקודם", "fr": "Précédent"},
    "gallery_next": {"he": "הבא", "fr": "Suivant"},
    "video_play": {"he": "נגן וידאו", "fr": "Lire la vidéo"},

    # ── Footer ──────────────────────────────────────────────────
    "footer_about": {
        "he": "מטבח טוניסאי אותנטי, כשר למהדרין. מתכונים שעברו במשפחה, אוכל שמגיע לשולחן חם.",
        "fr": "Cuisine tunisienne authentique, casher lemehadrin. Des recettes de famille, servies bien chaudes.",
    },
    "footer_contact": {"he": "צרו קשר", "fr": "Contact"},
    "footer_hours": {"he": "שעות", "fr": "Horaires"},
    "footer_follow": {"he": "עקבו אחרינו", "fr": "Suivez-nous"},
    "footer_rights": {"he": "כל הזכויות שמורות", "fr": "Tous droits réservés"},

    # ── Misc ────────────────────────────────────────────────────
    "currency": {"he": "₪", "fr": "₪"},
    "skip_to_content": {"he": "דלגו לתוכן", "fr": "Aller au contenu"},
}

# Day names, indexed 0=Sunday to match BusinessHours.day_of_week.
DAY_NAMES = {
    "he": ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"],
    "fr": ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"],
}


def translate(key, lang=DEFAULT_LANG):
    """Look up a copy key. Falls back to Hebrew, then to the key itself."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    return entry.get(lang) or entry.get(DEFAULT_LANG) or key


def day_name(index, lang=DEFAULT_LANG):
    names = DAY_NAMES.get(lang, DAY_NAMES[DEFAULT_LANG])
    try:
        return names[index]
    except (IndexError, TypeError):
        return ""
