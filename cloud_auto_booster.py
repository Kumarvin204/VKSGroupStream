"""
24/7 GITHUB CLOUD REALTIME VELOCITY & "SEO KR DO" ENGINE (V4.0)
--------------------------------------------------------------
"""
import sys
import io
import os
import json
import time
import re
from datetime import datetime, timezone, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

STATE_FILE = "cloud_velocity_state.json"

PEAK_SLOTS_IST = [
    (7, 30),   # Morning Darshan Peak
    (13, 15),  # Lunch Time Peak
    (18, 30),  # Evening Prime Peak
    (20, 15)   # Night Leisure Peak
]

CHANNELS_CONFIG = [
    {
        "env_var": "TOKEN_NANDINI_JSON",
        "name": "Nandini & Vinod Soni Official",
        "niche": "bhakti"
    },
    {
        "env_var": "TOKEN_LEARNING_JSON",
        "name": "Learning of life",
        "niche": "motivation"
    }
]

VIRAL_TAGS_BHAKTI = [
    "khatu shyam", "khatu shyam live", "khatu shyam shorts", "khatu shyam status 2026",
    "jai shree shyam", "khatu shyam ji", "haare ka sahara", "shyam baba", "khatu naresh",
    "khatu dham", "morpankhi mukut", "khatu shyam darshan today", "khatu shyam shringar",
    "bhakti shorts", "tuesday darshan", "mangalwar darshan", "shorts feed", "viral shorts",
    "trending shorts", "daily darshan", "nandini vinod soni", "explore", "explore page", "viral video"
]

VIRAL_TAGS_MOTIVATION = [
    "learning of life", "life changing lesson", "motivational shorts", "dhyan ke fayde",
    "meditation in hindi", "mind peace status", "peace of mind", "overthinking kaise roke",
    "positive vibes status", "success motivation", "mind power", "shorts feed",
    "trending shorts", "viral shorts", "explore", "explore page", "daily motivation"
]

POWER_HOOKS_BHAKTI = [
    "बाबा श्याम का ऐसा अलौकिक रूप पहले कभी नहीं देखा 😭 1 लाइक श्याम के नाम 🙏 #Shorts #KhatuShyam #Viral",
    "देखते ही दिन बन जाएगा 🌸 खाटू श्याम जी का चमत्कारी दिव्य शृंगार दर्शन 🙏 #KhatuShyam #Shorts #Bhakti",
    "मोरपंखी मुकुट में बाबा श्याम का मनमोहक शृंगार 🌸 हारे के सहारे की जय 🙏 #Shorts #KhatuShyam #Trending",
    "जिसने भी सच्चे मन से दर्शन किए उसकी हर मनोकामना पूरी हुई 🌸 जय श्री श्याम 🙏 #Shorts #KhatuDham",
    "हारे के सहारे बाबा श्याम हमारे 🌸 1 सेकंड निकालकर दर्शन ज़रूर करें 🙏 #Shorts #KhatuShyam #ViralShorts"
]

POWER_HOOKS_MOTIVATION = [
    "यह 10 सेकंड आपकी पूरी जिंदगी बदल देंगे 🌟 कभी हार मत मानो 💪 #Shorts #Motivation #LifeLessons",
    "ईश्वर का यह गुप्त संकेत कभी अनदेखा मत करना ✨ गीता सार 🌟 #Shorts #Motivation #PositiveVibes",
    "जब चारों तरफ अंधेरा दिखे तो यह बात हमेशा याद रखना 🌟 #Shorts #Success #Mindset #Trending",
    "खाटू श्याम जी के दरबार में भक्तों का जनसैलाब 🌸 1 लाइक श्याम प्यारे के नाम 🙏 #KhatuShyam #Shorts",
    "काले पत्थर का सच्चा हीरा 😭 इस कहानी को सुनकर आपकी आँखें भर आएंगी 🌟 #Shorts #LifeChanging"
]

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_state(state):
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def get_next_available_slot(existing_scheduled_utc):
    now_utc = datetime.now(timezone.utc)
    ist_offset = timedelta(hours=5, minutes=30)
    now_ist = now_utc + ist_offset

    for day_offset in range(7):
        target_date = now_ist.date() + timedelta(days=day_offset)
        for hour, minute in PEAK_SLOTS_IST:
            slot_ist = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=timezone.utc)
            if slot_ist > now_ist + timedelta(minutes=30):
                slot_utc = slot_ist - ist_offset
                slot_utc_str = slot_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                
                clash = False
                for ex_utc in existing_scheduled_utc:
                    try:
                        ex_dt = datetime.strptime(ex_utc.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S.%f%z")
                    except Exception:
                        try:
                            ex_dt = datetime.strptime(ex_utc.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S%z")
                        except Exception:
                            continue
                    if abs((slot_utc - ex_dt).total_seconds()) < 3600:
                        clash = True
                        break
                
                if not clash:
                    return slot_utc_str, f"{slot_ist.strftime('%d-%b %I:%M %p')} IST"
                    
    fallback_utc = now_utc + timedelta(hours=3)
    return fallback_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "3 Hours from now"

# =============================================================================
# 👑 10.8 MILLION (10,800,000) 5-LAYER COMBINATORIAL DYNAMIC TITLE GENERATOR
# =============================================================================
BHAKTI_L1 = [
    "बाबा श्याम", "खाटू नरेश", "नीले के असवार", "शीश के दानी", "लखदातार बाबा श्याम",
    "हारे के सहारे", "कलयुग के देव", "मोरछड़ी वाले सांवरे", "श्याम बिहारी", "खाटू धाम वाले सांवरिया",
    "तीन बाण धारी", "सेठों के सेठ", "मण्डफिया वाले साँवरिया सेठ", "सांवरे सरकार", "भक्तों के रखवाले बाबा श्याम",
    "श्री खाटू वाले श्याम", "दीनदयाल बाबा श्याम", "कृपानिधान सांवरे", "अमृतमयी बाबा श्याम", "परम दयालु खाटू नरेश",
    "मनोकामना पूर्ण कर्ता श्याम", "संकटमोचन बाबा श्याम", "सर्वशक्तिमान खाटू नरेश", "कल्याणकारी सांवरे", "भक्तवत्सल श्याम बाबा",
    "आनंददाता बाबा श्याम", "अलौकिक खाटू नरेश", "भव्य रूप धारी सांवरे", "तेजस्वी बाबा श्याम", "महिमावान खाटू धाम सरकार",
    "श्याम धणी", "सच्चे दरबार वाले श्याम", "सांवरिया प्यारे", "दीनों के नाथ", "अद्भुत रूप धारी श्याम",
    "नीले घोड़े वाले बाबा", "स्वर्ण मुकुट धारी सांवरे", "पावन खाटू नरेश", "चमत्कारी बाबा श्याम", "अनंत कृपालु सांवरे"
]

BHAKTI_L2 = [
    "का दिव्य अलौकिक शृंगार दर्शन", "का प्रातः मंगल दर्शन", "की जगमगाती पावन संध्या आरती", "का मनमोहक मोरपंखी रूप", "का लाल गुलाब शृंगार दर्शन",
    "का भव्य स्वर्ण मुकुट शृंगार", "का चमत्कारी पावन दरबार", "का मनभावन चमेली पुष्प शृंगार", "का अलौकिक राजसी स्वरूप", "के मनमोहक नैना व दिव्य दर्शन",
    "का अद्भुत पंचामृत अभिषेक दर्शन", "की भव्य मंगला आरती", "का नयनाभिराम शृंगार दर्शन", "का पावन दिव्य शृंगार रूप", "की प्रातःकालीन दिव्य ज्योत आरती",
    "का पुष्प वर्षा शृंगार दर्शन", "का पावन व अलौकिक दरबार", "का तेजस्वी स्वर्ण शृंगार दर्शन", "की महाआरती व दिव्य दर्शन", "का मनमोहक इत्र सेवा शृंगार",
    "का पावन शीश दर्शन", "का मनोरम गुलाब व गेंदा शृंगार", "का अनुपम दिव्य स्वरूप", "का स्वर्णिम छत्र शृंगार", "का पावन अमृतमय दर्शन",
    "का दिव्य छप्पन भोग दर्शन", "का अद्भुत व चमत्कारी रूप", "का मनभावन प्रातः शृंगार", "की पावन संध्या शयन आरती", "का मनमोहक शृंगार व दर्शन"
]

BHAKTI_L3 = [
    "🌸 देखते ही मन को असीम शांति मिले", "🌸 1 सेकंड निकालकर दर्शन ज़रूर करें", "🌸 सांवरे के दर्शन से संवर जाएगी जिंदगी", "🌸 जिसने सच्चे मन से दर्शन किए संकट दूर हुए", "🌸 आपके घर में सुख-समृद्धि और खुशहाली आए",
    "🌸 जीवन का हर कष्ट व दुख दूर होगा", "🌸 1 लाइक श्याम प्यारे के नाम", "🌸 कमेंट में जय श्री श्याम लिखें", "🌸 यह दर्शन आपका पूरा दिन बना देगा", "🌸 सांवरे का आशीर्वाद हमेशा आपके साथ रहे",
    "🌸 सच्चे दिल से जो भी मांगा सब मिला", "🌸 आज का दिन आपके लिए मंगलमय हो", "🌸 बाबा श्याम हर विपदा से रक्षा करें", "🌸 सांवरे की कृपा आप पर सदा बनी रहे", "🌸 घर-परिवार में खुशियों की बरसात हो",
    "🌸 मन की हर अधूरी मुराद पूरी होगी", "🌸 सच्चे मन से शीश झुकाएं और कृपा पाएं", "🌸 बाबा के पावन दर्शन से हर बिगड़ा काम बने", "🌸 कलयुग में केवल श्याम नाम ही सच्चा सहारा है", "🌸 हर भक्त की झोली खुशियों से भर जाए",
    "🌸 आज का यह अलौकिक रूप दिल छू लेगा", "🌸 बाबा की दिव्य मुस्कान से मन प्रफुल्लित हो जाए", "🌸 सांवरे की पावन छवि को निहारते रह जाएंगे", "🌸 1 शेयर करके पुण्य के भागी बनें", "🌸 बाबा का यह रूप आपकी हर चिंता हर लेगा",
    "🌸 श्याम कृपा से हर अंधेरा दूर होगा", "🌸 सांवरे के चरणों में ही सच्चा सुख है", "🌸 मन में सच्चा विश्वास रखो सब अच्छा होगा", "🌸 बाबा श्याम की महिमा सबसे निराली है", "🌸 श्याम नाम लेने से ही बेड़ा पार हो जाए"
]

BHAKTI_L4 = [
    "🙏 जय श्री श्याम", "🙏 खाटू नरेश की जय", "🙏 हारे के सहारे की जय", "🙏 तीन बाण धारी की जय", "🙏 लखदातार की जय",
    "🙏 शीश के दानी की जय", "🙏 नीले घोड़े वाले की जय", "🙏 सांवरे सरकार की जय", "🙏 जय श्री खाटू धाम", "🙏 जय श्री साँवरिया सेठ",
    "🙏 ॐ श्री श्याम देवाय नमः", "🙏 श्याम प्यारे की जय", "🙏 मोरछड़ी वाले की जय", "🙏 कलयुग अवतारी की जय", "🙏 खाटू वाले की जय",
    "🙏 जय बाबा श्याम", "🙏 दीनबंधु की जय", "🙏 जय श्री श्याम बिहारी", "🙏 सांवरे की जय", "🙏 जय लखदातार"
]

BHAKTI_L5 = [
    "#Shorts #KhatuShyam #Viral", "#Shorts #Bhakti #Trending", "#Shorts #KhatuDham #HaareKaSahara", "#Shorts #ViralShorts #DailyDarshan", "#Shorts #ShyamDarshan #ShortsFeed",
    "#Shorts #KhatuNaresh #ViralVideo", "#Shorts #Explore #BhaktiShorts", "#Shorts #KhatuShyamJi #TrendingNow", "#Shorts #JaiShreeShyam #ViralStatus", "#Shorts #BhaktiStatus #ForYou",
    "#Shorts #TrendingShorts #Reels", "#Shorts #ShyamBaba #Status", "#Shorts #KhatuLive #ViralReels", "#Shorts #HaareKeSahare #ShortsIndia", "#Shorts #DivineDarshan #ExplorePage"
]

MOTIVATION_L1 = [
    "यह 10 सेकंड आपकी जिंदगी बदल देंगे 🌟", "जब चारों तरफ अंधेरा दिखे तो यह याद रखना 🌟", "काले पत्थर का सच्चा हीरा 😭", "ईश्वर का यह गुप्त संकेत कभी अनदेखा मत करना ✨", "किस्मत को दोष देना छोड़ो और आज से यह शुरू करो 💪",
    "जिंदगी में अगर बड़ा मुकाम पाना है तो यह सीखो 🌟", "सकारात्मक सोच की असीम शक्ति ✨", "मन को शांत और मजबूत बनाने के नियम 🌟", "सफलता का सबसे बड़ा गुप्त रहस्य 💡", "जो इंसान समय की कद्र करता है वही जीतता है 🌟",
    "हार मानने से पहले इस बात को ज़रूर याद रखना 💪", "कठिन समय ही एक मजबूत इंसान बनाता है 🌟", "अपनी कमजोरियों को अपनी ताकत बनाओ 💡", "लोग क्या कहेंगे यह सोचना आज ही बंद करो 🌟", "धैर्य और विश्वास से हर मंजिल मिलती है 💪",
    "जब तक सांस है तब तक प्रयास जारी रखो 🌟", "महानता कभी गिरने में नहीं बल्कि उठने में है 💡", "सपनों को सच करने का सबसे आसान तरीका 🌟", "जो अपने काम से प्यार करता है वह कभी नहीं थकता 💪", "जिंदगी आपको वही देती है जिसके आप हकदार हैं 🌟"
]

MOTIVATION_L2 = [
    "कभी हिम्मत मत हारो", "विश्वास रखो सब ठीक होगा", "हर मुश्किल में एक अवसर छिपा होता है", "अपने लक्ष्य पर अडिग रहो", "मेहनत कभी बेकार नहीं जाती",
    "खुद पर भरोसा सबसे बड़ी ताकत है", "आज की मेहनत कल का सुकून बनेगी", "सफलता का कोई शॉर्टकट नहीं होता", "अपनी सोच को हमेशा ऊंचा रखो", "जीवन का सच्चा सबक"
]

MOTIVATION_L3 = [
    "💪 #Shorts #Motivation #LifeLessons", "🌟 #Shorts #Success #Mindset #Trending", "✨ #Shorts #PositiveVibes #DailyMotivation", "💡 #Shorts #LifeChanging #Inspiration", "🔥 #Shorts #SelfImprovement #MindPower"
]

def generate_dynamic_unique_title(niche, existing_titles=None):
    if existing_titles is None:
        existing_titles = []
    existing_set = {t.strip().lower() for t in existing_titles}

    import random
    if niche == "bhakti":
        for _ in range(500):
            w1 = random.choice(BHAKTI_L1)
            w2 = random.choice(BHAKTI_L2)
            w3 = random.choice(BHAKTI_L3)
            w4 = random.choice(BHAKTI_L4)
            w5 = random.choice(BHAKTI_L5)
            cand = f"{w1} {w2} {w3} {w4} {w5}"
            if cand.strip().lower() not in existing_set:
                return cand
        return f"{random.choice(BHAKTI_L1)} {random.choice(BHAKTI_L2)} {random.choice(BHAKTI_L3)} {random.choice(BHAKTI_L4)} {random.choice(BHAKTI_L5)}"
    else:
        for _ in range(500):
            w1 = random.choice(MOTIVATION_L1)
            w2 = random.choice(MOTIVATION_L2)
            w3 = random.choice(MOTIVATION_L3)
            cand = f"{w1} | {w2} {w3}"
            if cand.strip().lower() not in existing_set:
                return cand
        return f"{random.choice(MOTIVATION_L1)} | {random.choice(MOTIVATION_L2)} {random.choice(MOTIVATION_L3)}"

def get_panchang_festival_boost():
    """
    🌸 FEATURE 2 & 3: Hindu Panchang, Tithi & Multi-State Regional Devotee Expansion
    Detects special days (Shanivar, Ravivar, Ekadashi / Gyas) and returns festive hooks and regional high-volume tags.
    """
    now_dt = datetime.now()
    weekday = now_dt.weekday()
    day_num = now_dt.day

    fest_title_prefix = ""
    extra_tags = [
        # Regional Multi-State Devotee Tags (Gujarat, Rajasthan, Maharashtra, Delhi NCR)
        "khatu shyam live darshan", "khatu naresh na darshan", "sanwariya seth mandir gujarat",
        "shyam baba status hindi", "khatu dham live today"
    ]

    # Real-Time Search Trends Hijacker (Time-of-day surge keywords)
    hour = now_dt.hour
    if 4 <= hour <= 11:
        extra_tags.extend(["khatu shyam mangla aarti", "pratah darshan khatu shyam"])
    elif 17 <= hour <= 23:
        extra_tags.extend(["khatu shyam sandhya aarti", "shyam darshan today live 2026"])

# =============================================================================
# 🌍 MULTI-LANGUAGE LOCALIZATION ENGINE (English, Gujarati, Marathi)
# =============================================================================
def get_video_localizations(base_title, niche="bhakti"):
    """
    🌍 FEATURE: Multi-Language Localization Engine
    Provides backend translations for NRI devotees & multi-state diaspora without altering the main Hindi title.
    """
    if niche == "bhakti":
        return {
            "en": {
                "title": "Khatu Shyam Ji Live Darshan Today 🌸 Divine Blessings & Aarti",
                "description": "Daily live darshan and aarti of Shri Khatu Shyam Ji from Khatu Dham Rajasthan. Subscribe for daily spiritual blessings!\n\n#KhatuShyam #JaiShreeShyam #KhatuDham #Shorts"
            },
            "gu": {
                "title": "ખાટુ શ્યામ જી ના લાઈવ દર્શન 🌸 શ્રી ખાટુ ધામ આરતી",
                "description": "રોજના પાવન શૃંગાર અને આરતી દર્શન ખાટુ ધામથી. સબસ્ક્રાઈબ કરો અને આશીર્વાદ મેળવો!\n\n#KhatuShyam #JaiShreeShyam #BhaktiShorts"
            },
            "mr": {
                "title": "खाटू श्याम जी चे थेट दर्शन 🌸 आजचा दिव्य शृंगार व आरती",
                "description": "दररोज सकाळी आणि संध्याकाळी खाटू श्याम जी चे पावन दर्शन. कृपा आणि शांती साठी सबस्क्राईબ करा!\n\n#KhatuShyam #JaiShreeShyam #Bhakti"
            }
        }
    else:
        return {
            "en": {
                "title": "10 Seconds That Will Change Your Life 🌟 Powerful Mindset Lessons",
                "description": "Daily motivation, life lessons, and Bhagavad Gita wisdom for peace, focus, and unstoppable success. Subscribe now!\n\n#Motivation #Success #LifeLessons #Shorts"
            }
        }

def get_panchang_festival_boost():
    """
    🌸 FEATURE: Hindu Panchang, Tithi, Day/Night Dynamic Theme & Audio Sound Booster
    """
    now_dt = datetime.now()
    weekday = now_dt.weekday()
    day_num = now_dt.day
    hour = now_dt.hour

    fest_title_prefix = ""
    extra_tags = [
        "khatu shyam live darshan", "khatu naresh na darshan", "sanwariya seth mandir gujarat",
        "shyam baba status hindi", "khatu dham live today",
        # 🎵 FEATURE: Trending Sound & Audio Search Carousel Booster
        "khatu shyam bhajan original sound", "trending bhajan audio", "shyam status audio reels",
        "jai shree shyam music sound"
    ]

    # 🌓 FEATURE: Day/Night 24-Hour Live Dynamic Theme Switcher
    if 4 <= hour < 12:
        time_theme_desc = "✨ जगमगाती प्रातः मंगला आरती व अमृतमय दर्शन"
        extra_tags.extend(["khatu shyam mangla aarti", "pratah darshan khatu shyam", "morning aarti khatu shyam"])
    elif 12 <= hour < 17:
        time_theme_desc = "✨ पावन दोपहर राजभोग आरती व मनमोहक दर्शन"
        extra_tags.extend(["khatu shyam bhog aarti", "dopahar darshan khatu shyam"])
    else:
        time_theme_desc = "✨ जगमगाती संध्या व शयन आरती के पावन दर्शन"
        extra_tags.extend(["khatu shyam sandhya aarti", "shyam darshan today live 2026", "shayan aarti khatu dham"])

    if day_num in [11, 12, 26, 27]:
        fest_title_prefix = "एकादशी विशेष 🌸 [अलौकिक] "
        extra_tags.extend(["khatu shyam ekadashi darshan", "gyas khatu shyam", "ekadashi bhajan live", "khatu dham ekadashi"])
    elif weekday == 5:
        fest_title_prefix = "शनिवार विशेष 🌸 [चमत्कारिक] "
        extra_tags.extend(["shanivar khatu shyam darshan", "shani shyam darshan", "shanivar live darshan"])
    elif weekday == 6:
        fest_title_prefix = "रविवार पावन 🌸 [दिव्य दर्शन] "
        extra_tags.extend(["ravivar khatu shyam", "sunday shyam darshan", "ravivar live khatu"])
    elif weekday == 3:
        fest_title_prefix = "गुरुवार दिव्य 🌸 [महाकृपा] "
        extra_tags.extend(["guruvar khatu shyam", "guruvar darshan live"])

    return fest_title_prefix, extra_tags, time_theme_desc

def generate_seo_package(raw_title, niche="bhakti", existing_titles=None):
    if existing_titles is None:
        existing_titles = []

    title_lower = raw_title.lower()
    fest_prefix, extra_tags, time_theme_desc = get_panchang_festival_boost()

    # 🎯 FEATURE: High-Conversion Devotional CTA Switcher
    devotional_ctas = [
        "👑 चैनल SUBSCRIBE करके पावन श्याम परिवार का हिस्सा बनें व 🔔 घंटी दबाएं ताकि प्रतिदिन सबसे पहले दर्शन मिलें!",
        "🌸 1 शेयर करके पुण्य के भागी बनें और अपने परिवार के साथ यह पावन दर्शन साझा करें! 🔔 SUBSCRIBE अवश्य करें!",
        "✨ बाबा श्याम के नित्य पावन दर्शन और कृपा पाने के लिए चैनल SUBSCRIBE करें और कमेंट में हाजिरी लगाएं! 🔔"
    ]
    chosen_cta = random.choice(devotional_ctas)

    if any(k in title_lower for k in ["khatu", "shyam", "khatushyam", "morpankh", "sanwariya"]) or niche == "bhakti":
        base_title = generate_dynamic_unique_title("bhakti", existing_titles)
        title = f"{fest_prefix}{base_title}" if fest_prefix and len(fest_prefix + base_title) <= 100 else base_title
        desc = f"""🙏 जय श्री श्याम! खाटू धाम से बाबा श्री खाटू श्याम जी का अलौकिक शृंगार दर्शन 🌸

🎵 भजन भाव व स्तुति: "हारे का सहारा बाबा श्याम हमारा | शीश के दानी लखदातार की जय जयकार" 🌸
👁️ लूप चैलेंज: क्या आपने अंतिम 3 सेकंड में बाबा के मुकुट पर चमकता दिव्य मोरपंख देखा? ध्यान से दोबारा देखें और कमेंट में बताएं! 🦚✨
📊 कम्युनिटी पोल: आज का यह अलौकिक दर्शन अपने मित्रों के साथ शेयर करें!

👑 आज बाबा श्याम का भव्य स्वरूप:
🦚 मोरपंखी मुकुट व स्वर्ण आभूषण
🌺 ताज़ा गुलाब, गेंदे व चमेली के फूलों का शृंगार
{time_theme_desc}

बाबा श्याम की कृपा से आपके घर में सुख-समृद्धि, शांति और खुशहाली आए! 🙏
कमेंट में "जय श्री श्याम" या "हारे के सहारे की जय" ज़रूर लिखें! 🌸

🎬 1-घंटे की खाटू श्याम सम्पूर्ण अमर कथा यहाँ देखें: https://www.youtube.com/watch?v=M2cMgrvelqk
🎬 श्री कृष्ण बाल लीला सम्पूर्ण 20 चमत्कार यहाँ देखें: https://www.youtube.com/watch?v=WbQXodCN-S8

👉 {chosen_cta}
🌐 Visit Website: https://radhekeshyamm.vercel.app/

==================================================
🛡️ Content Notice & Transformative Value:
All devotional footage & darshan visuals are creatively curated, color-graded, and edited with original spiritual commentary, structured prayers, and devotional context by Nandini & Vinod Soni Official to spread peace and positivity.
📧 Contact for business & inquiries: vsoni9060@gmail.com
==================================================

#KhatuShyam #BabaShyam #KhatuDham #JaiShreeShyam #ShyamDarshan #BhaktiShorts #Shorts #Viral #Trending #HareKeSahare #ShortsFeed #NandiniVinodSoni"""
        tags = VIRAL_TAGS_BHAKTI + extra_tags
        # 250%+ Seamless Loop & Multi-Choice Faith Comment Prompt
        pin = "👑 बाबा श्याम के पावन स्वरूप: 1. लखदातार 2. शीश के दानी 3. हारे के सहारे — अपनी मनोकामना कमेंट में लिखकर 'जय श्री श्याम' ज़रूर बोलें! (अंतिम 3 सेकंड में मोरपंख ध्यान से देखें 🦚✨)"

    else:
        title = generate_dynamic_unique_title("motivation", existing_titles)
        desc = f"""✨ जीवन में कभी हार मत मानो! हर मुश्किल समय में एक नई सीख छिपी होती है। 🌟

📖 गीता सार व विचार: "कर्म करो फल की चिंता मत करो | हर अंधकार के बाद एक नया सवेरा आता है" 💫
👁️ लूप चैलेंज: इस सीख के अंतिम 3 सेकंड को दोबारा ध्यान से सुनें और अपने जीवन में लागू करें! 🌟

इस वीडियो को पूरा देखें और अपने दोस्तों के साथ शेयर करें! 💪
अगर यह सीख पसंद आई हो तो Like करें और Channel SUBSCRIBE करें! 🔔

🎬 मन को शांत करने और तनाव दूर करने के 5 अचूक नियम यहाँ देखें: https://www.youtube.com/watch?v=FvM23bYgeWI

👉 {chosen_cta}

==================================================
🛡️ Content Notice & Transformative Value:
This motivational content is uniquely written, curated, and produced by Learning of Life with positive philosophical commentary for education and inspiration.
📧 Contact: vsoni9060@gmail.com
==================================================

#Motivation #LifeLessons #Success #Mindset #PositiveVibes #Shorts #Viral #Trending #ShortsFeed #LearningOfLife"""
        tags = VIRAL_TAGS_MOTIVATION
        pin = "🌟 जिंदगी में आगे बढ़ने का आपका #1 नियम क्या है: 1. कभी हार न मानना 2. खुद पर भरोसा 3. ईश्वर का साथ? कमेंट में लिखें! (अंतिम सीख दोबारा सुनें 💫)"

    return title, desc, tags, pin

def get_or_create_playlist(yt, title, niche="bhakti"):
    """
    🔄 FEATURE: Auto-Playlist Index-0 Syndication
    """
    try:
        pl_list = yt.playlists().list(part="snippet", mine=True, maxResults=25).execute()
        for item in pl_list.get("items", []):
            if title.lower() in item["snippet"]["title"].lower():
                return item["id"]
        
        new_pl = yt.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": f"Daily updated playlist for {niche} videos — watch continuously!"
                },
                "status": {"privacyStatus": "public"}
            }
        ).execute()
        return new_pl["id"]
    except Exception:
        return None

def run_cloud_cycle():
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"\n[{now_str}] ☁️ GITHUB CLOUD RUNNING V4.0 'SEO KR DO' & VELOCITY SENTINEL...")
    state = load_state()
    now_ts = int(time.time())

    for ch_cfg in CHANNELS_CONFIG:
        tok_str = os.environ.get(ch_cfg["env_var"])
        if not tok_str:
            continue

        ch_name = ch_cfg["name"]
        niche = ch_cfg["niche"]
        hooks = POWER_HOOKS_BHAKTI if niche == "bhakti" else POWER_HOOKS_MOTIVATION
        tags = VIRAL_TAGS_BHAKTI if niche == "bhakti" else VIRAL_TAGS_MOTIVATION

        try:
            creds = Credentials.from_authorized_user_info(json.loads(tok_str))
            yt = build('youtube', 'v3', credentials=creds)

            ch_resp = yt.channels().list(part="contentDetails,statistics", mine=True).execute()
            uploads_id = ch_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            pl_resp = yt.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_id,
                maxResults=10
            ).execute()

            v_ids = [it["contentDetails"]["videoId"] for it in pl_resp.get("items", [])]
            if not v_ids:
                continue

            v_resp = yt.videos().list(
                part="snippet,status,statistics,contentDetails,localizations",
                id=",".join(v_ids)
            ).execute()

            existing_channel_titles = [v["snippet"].get("title", "") for v in v_resp.get("items", [])]
            existing_scheduled_utc = [
                v["status"].get("publishAt") for v in v_resp.get("items", [])
                if v["status"].get("privacyStatus") == "private" and v["status"].get("publishAt")
            ]

            main_playlist_title = "श्री खाटू श्याम जी नित्य दर्शन 2026 🌸" if niche == "bhakti" else "Life Changing Motivation & Lessons 🌟"
            main_pl_id = get_or_create_playlist(yt, main_playlist_title, niche)

            for v in v_resp.get("items", []):
                vid = v["id"]
                snip = v["snippet"]
                stat = v["status"]
                stats = v["statistics"]
                dur = v.get("contentDetails", {}).get("duration", "PT15S")
                is_short = not ("M" in dur or "H" in dur)
                title_curr = snip.get("title", "")

                # TRIGGER CHECK
                if re.search(r'\bseo\s*(kr\s*do|kardo|kar\s*do|krdo|kro\s*do|krodo|kr\s*de|karde)\b', title_curr, re.IGNORECASE):
                    print(f"\n🚨 [CLOUD TRIGGER DETECTED] Video {vid}: '{title_curr}'!")
                    new_title, new_desc, new_tags, pin_comment = generate_seo_package(title_curr, niche, existing_channel_titles)
                    existing_channel_titles.append(new_title)
                    slot_utc_str, slot_ist_str = get_next_available_slot(existing_scheduled_utc)
                    existing_scheduled_utc.append(slot_utc_str)

                    snip["title"] = new_title
                    snip["description"] = new_desc
                    snip["tags"] = new_tags
                    snip["categoryId"] = "22"
                    snip["defaultLanguage"] = "hi"

                    stat["privacyStatus"] = "private"
                    stat["publishAt"] = slot_utc_str
                    stat["selfDeclaredMadeForKids"] = False

                    localizations_payload = get_video_localizations(new_title, niche)

                    try:
                        yt.videos().update(
                            part="snippet,status,localizations",
                            body={"id": vid, "snippet": snip, "status": stat, "localizations": localizations_payload}
                        ).execute()
                        print(f"  ✅ [CLOUD SEO, SMART SCHEDULE & LOCALIZATIONS APPLIED] -> {slot_ist_str}")
                    except Exception as e:
                        print(f"  ⚠️ Cloud Error applying SEO to {vid}: {e}")
                    continue

                # PUBLIC MONITORING
                if stat.get("privacyStatus") != "public":
                    continue

                current_views = int(stats.get("viewCount", 0))
                current_likes = int(stats.get("likeCount", 0))
                comments_cnt = int(stats.get("commentCount", 0))

                prev_record = state.get(vid, {})
                prev_views = prev_record.get("views", current_views)
                prev_time = prev_record.get("timestamp", now_ts)
                milestones = prev_record.get("milestones", [])
                ab_tested = prev_record.get("ab_tested", False)
                playlist_added = prev_record.get("playlist_added", False)
                replied_comments = prev_record.get("replied_comments", [])

                time_diff_mins = max(1, (now_ts - prev_time) // 60)
                views_gained = current_views - prev_views
                velocity_per_min = views_gained / time_diff_mins

                # 1️⃣ Auto-Playlist Index-0 Syndication Loop
                if main_pl_id and not playlist_added:
                    try:
                        yt.playlistItems().insert(
                            part="snippet",
                            body={
                                "snippet": {
                                    "playlistId": main_pl_id,
                                    "position": 0,
                                    "resourceId": {"kind": "youtube#video", "videoId": vid}
                                }
                            }
                        ).execute()
                        playlist_added = True
                        print(f"     🔄 [CLOUD PLAYLIST INDEX-0] Pinned {vid} to top of playlist!")
                    except Exception:
                        playlist_added = True

                # 2️⃣ Viral Milestone Momentum Booster (500, 1K, 2K Views)
                for ms in [250, 500, 1000, 2000, 5000]:
                    if current_views >= ms and ms not in milestones:
                        milestones.append(ms)
                        print(f"     🏆 [CLOUD MILESTONE {ms}+ VIEWS REACHED] Upgrading tags on {vid}...")
                        broad_tags = ["khatu shyam status 2026", "viral shorts today", "trending reels hindi", "bhakti live", "khatu dham"]
                        snip["tags"] = list(set((snip.get("tags") or []) + broad_tags))
                        try:
                            yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                            celebration_msg = f"🎉 आज {current_views}+ श्याम भक्तों ने पावन दर्शन किए! अपनी मनोकामना कमेंट में लिखकर 'जय श्री श्याम' ज़रूर बोलें! 🌸🙏" if niche == "bhakti" else f"🔥 {current_views}+ लोगों ने यह सीख देखी! आप भी कमेंट में अपना विचार ज़रूर साझा करें! 💫"
                            yt.commentThreads().insert(
                                part="snippet",
                                body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": celebration_msg}}}}
                            ).execute()
                        except Exception:
                            pass

                # 3️⃣ Auto A/B Dynamic Title Switcher (CTR Boost)
                if is_short and not ab_tested and time_diff_mins >= 15 and current_views < 40:
                    new_unique_title = generate_dynamic_unique_title(niche, existing_channel_titles)
                    if new_unique_title and new_unique_title != title_curr:
                        snip["title"] = new_unique_title
                        snip["tags"] = tags
                        snip["categoryId"] = "22"
                        try:
                            yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                            print(f"     🎯 [CLOUD A/B TITLE SWITCHED] -> {new_unique_title[:45]}...")
                            if title_curr in existing_channel_titles:
                                existing_channel_titles.remove(title_curr)
                            existing_channel_titles.append(new_unique_title)
                            ab_tested = True
                        except Exception:
                            pass

                # 4️⃣ Auto-Devotee Engagement Reply Booster
                if comments_cnt > 0 and len(replied_comments) < 3:
                    try:
                        cmt_resp = yt.commentThreads().list(part="snippet", videoId=vid, maxResults=5).execute()
                        for c_item in cmt_resp.get("items", []):
                            c_id = c_item["id"]
                            c_text = c_item["snippet"]["topLevelComment"]["snippet"].get("textOriginal", "").lower()
                            if c_id not in replied_comments and any(w in c_text for w in ["shyam", "khatu", "जय", "radhey", "krishna", "yes", "🙏", "🌸"]):
                                reply_text = "बाबा श्याम आपकी हर मनोकामना पूर्ण करें! 🌸🙏 जय श्री श्याम!" if niche == "bhakti" else "ईश्वर आप पर सदैव कृपा बनाए रखें! 💫🌟"
                                yt.comments().insert(
                                    part="snippet",
                                    body={"snippet": {"parentId": c_id, "textOriginal": reply_text}}
                                ).execute()
                                replied_comments.append(c_id)
                                print(f"     ❤️ [CLOUD DEVOTEE COMMENT REPLIED] on {vid}")
                                break
                    except Exception:
                        pass

                # Momentum Catcher
                elif views_gained >= 5 and velocity_per_min >= 0.5:
                    if is_short:
                        snip["tags"] = tags
                    snip["categoryId"] = "22"
                    try:
                        yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                    except Exception:
                        pass

                # Slowdown Revival
                elif is_short and ((time_diff_mins >= 25 and views_gained < 5) or (current_views < 50 and time_diff_mins >= 20)):
                    new_unique_title = generate_dynamic_unique_title(niche, existing_channel_titles)
                    if new_unique_title and new_unique_title != title_curr:
                        snip["title"] = new_unique_title
                        snip["tags"] = tags
                        snip["categoryId"] = "22"
                        try:
                            yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                            print(f"     🔥 [CLOUD SHORTS HOOK ROTATED] -> {snip['title'][:40]}...")
                            if title_curr in existing_channel_titles:
                                existing_channel_titles.remove(title_curr)
                            existing_channel_titles.append(new_unique_title)
                        except Exception:
                            pass

                # Auto Pinned Comment on Live Release
                if comments_cnt == 0:
                    pin_msg = "👑 बाबा श्याम के पावन स्वरूप: 1. लखदातार 2. शीश के दानी 3. हारे के सहारे — अपनी मनोकामना कमेंट में लिखकर 'जय श्री श्याम' ज़रूर बोलें! (अंतिम 3 सेकंड में मोरपंख ध्यान से देखें 🦚✨)" if niche == "bhakti" else "🌟 जिंदगी में आगे बढ़ने का आपका #1 नियम क्या है: 1. कभी हार न मानना 2. खुद पर भरोसा 3. ईश्वर का साथ? कमेंट में लिखें! (अंतिम सीख दोबारा सुनें 💫)"
                    try:
                        yt.commentThreads().insert(
                            part="snippet",
                            body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": pin_msg}}}}
                        ).execute()
                        print(f"     📌 [CLOUD AUTO-PINNED COMMENT POSTED] on {vid}")
                    except Exception:
                        pass

                state[vid] = {
                    "views": current_views,
                    "likes": current_likes,
                    "timestamp": now_ts,
                    "hook_index": prev_record.get("hook_index", 0),
                    "milestones": milestones,
                    "ab_tested": ab_tested,
                    "playlist_added": playlist_added,
                    "replied_comments": replied_comments
                }

        except Exception as e:
            print(f"  ⚠️ Cloud Error on {ch_name}: {e}")

    save_state(state)

def main():
    print("=" * 80)
    print("☁️ GITHUB CLOUD 24/7 ULTRA-VIRAL V4.0 STARTED (5.5 HOURS RUNNER)")
    print("=" * 80)

    start_time = time.time()
    max_duration_secs = 5.5 * 3600

    cycle_count = 0
    while time.time() - start_time < max_duration_secs:
        cycle_count += 1
        print(f"\n--- [CYCLE #{cycle_count}] Running 5-Min Super Best Interval ---")
        try:
            run_cloud_cycle()
        except Exception as e:
            print(f"⚠️ Top-level cycle error: {e}")

        time.sleep(300)

    print("\n✅ Runner completed 5.5 hours. Handing over to next relay...")

if __name__ == "__main__":
    main()
