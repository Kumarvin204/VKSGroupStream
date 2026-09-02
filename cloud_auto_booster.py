"""
24/7 GITHUB CLOUD REALTIME VELOCITY & "SEO KR DO" ENGINE (V13.0)
--------------------------------------------------------------
"""
import sys
import io
import os
import json
import time
import re
import random
from datetime import datetime, timezone, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import urllib.request
import urllib.parse

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
    # ⏸️ TEMPORARILY DISABLED — Full focus on main Bhakti channel
    # {
    #     "env_var": "TOKEN_LEARNING_JSON",
    #     "name": "Learning of life",
    #     "niche": "motivation"
    # }
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

def get_analytics_data(yt, vid):
    """🧠 FEATURE: Analytics API Brain — Fetches CTR, AVD, Traffic Sources for data-driven decisions."""
    try:
        analytics = build("youtubeAnalytics", "v2", credentials=yt._http.credentials if hasattr(yt, '_http') else None)
        now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
        end_date = now_ist.strftime("%Y-%m-%d")
        start_date = (now_ist - timedelta(days=7)).strftime("%Y-%m-%d")
        
        resp = analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage",
            filters=f"video=={vid}",
            dimensions=""
        ).execute()
        
        rows = resp.get("rows", [])
        if rows and len(rows[0]) >= 4:
            return {
                "views": rows[0][0],
                "watch_mins": rows[0][1],
                "avg_view_duration": rows[0][2],
                "avg_view_pct": rows[0][3]
            }
    except Exception:
        pass
    return None

def get_trending_bhakti_keywords():
    """🌊 FEATURE: Trending Wave Rider — Fetches live trending bhakti keywords."""
    trending_keywords = []
    try:
        now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
        month = now_ist.month
        day = now_ist.day
        
        festival_map = {
            (1, 14): ["makar sankranti khatu shyam", "uttarayan darshan"],
            (1, 26): ["republic day bhakti", "desh bhakti shyam"],
            (3, 0): ["holi khatu shyam", "fag mahotsav khatu", "khatu shyam holi celebration"],
            (8, 0): ["janmashtami khatu shyam", "krishna janmashtami live", "janmashtami darshan 2026", "shyam janmotsav"],
            (9, 0): ["navratri khatu shyam", "navratri darshan live", "shardiya navratri 2026"],
            (10, 0): ["dussehra khatu shyam", "vijayadashami darshan"],
            (11, 0): ["diwali khatu shyam", "deepawali darshan live", "kartik purnima khatu"],
            (2, 0): ["mahashivratri khatu shyam", "phalguni mela khatu dham", "khatu shyam mela 2026"],
            (7, 0): ["sawan khatu shyam", "shravan maas darshan", "sawan somvar shyam"],
            (4, 0): ["chaitra navratri khatu", "ram navami darshan"],
            (6, 0): ["rath yatra khatu shyam", "ashadhi ekadashi darshan"],
        }
        
        for (m, d), keywords in festival_map.items():
            if m == month and (d == 0 or d == day):
                trending_keywords.extend(keywords)
        
        weekday = now_ist.weekday()
        day_trends = {
            0: ["somvar vrat khatu shyam", "monday darshan live"],
            1: ["mangalwar khatu shyam darshan", "tuesday bhakti shorts"],
            2: ["budhwar darshan live", "wednesday khatu shyam"],
            3: ["guruvar khatu shyam", "thursday darshan live"],
            4: ["shukravar darshan", "friday bhakti status"],
            5: ["shanivar khatu shyam", "saturday darshan live"],
            6: ["ravivar khatu shyam darshan", "sunday bhakti shorts"]
        }
        trending_keywords.extend(day_trends.get(weekday, []))
        
        hour = now_ist.hour
        if 4 <= hour <= 7:
            trending_keywords.extend(["mangla aarti khatu shyam", "subah ka darshan live", "early morning darshan"])
        elif 11 <= hour <= 14:
            trending_keywords.extend(["rajbhog aarti khatu shyam", "dopahar darshan live"])
        elif 17 <= hour <= 20:
            trending_keywords.extend(["sandhya aarti khatu shyam", "shaam ka darshan live", "evening aarti live"])
        elif 20 <= hour <= 23:
            trending_keywords.extend(["shayan aarti khatu shyam", "raat ka darshan", "night darshan live"])
        
        trending_keywords.extend(["khatu shyam aaj ka darshan", f"khatu shyam {now_ist.strftime('%B').lower()} 2026"])
    except Exception:
        pass
    return trending_keywords

def session_duration_maximizer(yt, current_vid, niche="bhakti"):
    """🔗 FEATURE: Session Duration Maximizer — Chains best videos into smart playlists."""
    try:
        search_resp = yt.search().list(
            part="snippet", forMine=True, type="video",
            order="viewCount", maxResults=10
        ).execute()
        
        top_vids = [item["id"]["videoId"] for item in search_resp.get("items", []) if item["id"].get("videoId")]
        if len(top_vids) < 3:
            return
        
        session_pl_title = "बाबा श्याम सम्पूर्ण दर्शन यात्रा 🌸" if niche == "bhakti" else "जीवन के अनमोल सबक 🌟"
        session_pl_id = get_or_create_playlist(yt, session_pl_title, niche)
        if not session_pl_id:
            return
        
        existing_items = []
        try:
            pl_items = yt.playlistItems().list(part="snippet", playlistId=session_pl_id, maxResults=50).execute()
            existing_items = [item["snippet"]["resourceId"]["videoId"] for item in pl_items.get("items", [])]
        except Exception:
            pass
        
        if current_vid not in existing_items:
            try:
                yt.playlistItems().insert(
                    part="snippet",
                    body={"snippet": {"playlistId": session_pl_id, "position": 0, "resourceId": {"kind": "youtube#video", "videoId": current_vid}}}
                ).execute()
                print(f"     🔗 [SESSION CHAIN] Video {current_vid} added to session playlist!")
            except Exception:
                pass
    except Exception:
        pass

def smart_comment_traffic_funnel(yt, hot_vid, hot_views, niche, state):
    """🌊 FEATURE: Smart Comment Traffic Funnel — Routes traffic from viral videos to underperforming ones."""
    try:
        if hot_views < 5000:
            return
        funnel_key = f"funnel_{hot_vid}"
        if state.get(funnel_key):
            return
        
        search_resp = yt.search().list(
            part="snippet", forMine=True, type="video",
            order="date", maxResults=10
        ).execute()
        
        target_vid = None
        for item in search_resp.get("items", []):
            vid_id = item["id"].get("videoId")
            if vid_id and vid_id != hot_vid:
                v_stats = yt.videos().list(part="statistics", id=vid_id).execute()
                v_items = v_stats.get("items", [])
                if v_items:
                    v_views = int(v_items[0]["statistics"].get("viewCount", 0))
                    if v_views < hot_views // 5:
                        target_vid = vid_id
                        break
        
        if target_vid:
            if niche == "bhakti":
                funnel_comment = f"🌸 बाबा श्याम का और भी अलौकिक दर्शन यहाँ देखें 👉 https://www.youtube.com/shorts/{target_vid} 🙏 जय श्री श्याम!"
            else:
                funnel_comment = f"✨ एक और जीवन बदलने वाली सीख यहाँ देखें 👉 https://www.youtube.com/shorts/{target_vid} 💫"
            
            yt.commentThreads().insert(
                part="snippet",
                body={"snippet": {"videoId": hot_vid, "topLevelComment": {"snippet": {"textOriginal": funnel_comment}}}}
            ).execute()
            state[funnel_key] = True
            print(f"     🌊 [TRAFFIC FUNNEL] Routed viewers from {hot_vid} ({hot_views} views) → {target_vid}")
    except Exception:
        pass

def competitor_spy_tag_hijacker(yt, niche="bhakti"):
    """🕵️ FEATURE: Competitor Spy & Tag Hijacker."""
    hijacked_tags = []
    try:
        if niche == "bhakti":
            search_queries = ["khatu shyam darshan today", "khatu shyam live", "baba shyam shorts"]
        else:
            search_queries = ["motivational shorts hindi", "life lessons shorts"]
        
        query = random.choice(search_queries)
        search_resp = yt.search().list(
            part="snippet", q=query, type="video",
            order="viewCount", maxResults=5,
            publishedAfter=(datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
        ).execute()
        
        competitor_vids = [item["id"]["videoId"] for item in search_resp.get("items", []) if item["id"].get("videoId")]
        
        if competitor_vids:
            vids_resp = yt.videos().list(part="snippet", id=",".join(competitor_vids[:3])).execute()
            for v_item in vids_resp.get("items", []):
                comp_tags = v_item["snippet"].get("tags", [])
                for tag in comp_tags:
                    tag_lower = tag.lower().strip()
                    skip_words = ["subscribe", "channel", "http", "www", "@"]
                    if len(tag_lower) > 3 and len(tag_lower) < 50 and not any(sw in tag_lower for sw in skip_words):
                        if tag_lower not in [t.lower() for t in hijacked_tags]:
                            hijacked_tags.append(tag)
            print(f"     🕵️ [COMPETITOR SPY] Found {len(hijacked_tags)} trending competitor tags")
    except Exception:
        pass
    return hijacked_tags[:10]

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

    if niche == "bhakti":
        for _ in range(500):
            w1 = random.choice(BHAKTI_L1)
            w2 = random.choice(BHAKTI_L2)
            w4 = random.choice(BHAKTI_L4)
            w5 = random.choice(BHAKTI_L5)
            cand = f"{w1} {w2} {w4} {w5}"
            if len(cand) > 95:
                cand = f"{w1} {w4} {w5}"
            if len(cand) <= 95 and cand.strip().lower() not in existing_set:
                return cand
        cand = f"{random.choice(BHAKTI_L1)} {random.choice(BHAKTI_L4)} {random.choice(BHAKTI_L5)}"
        return cand[:95]
    else:
        for _ in range(500):
            w1 = random.choice(MOTIVATION_L1)
            w2 = random.choice(MOTIVATION_L2)
            w3 = random.choice(MOTIVATION_L3)
            cand = f"{w1} | {w2} {w3}"
            if len(cand) > 95:
                cand = f"{w1} {w3}"
            if len(cand) <= 95 and cand.strip().lower() not in existing_set:
                return cand
        cand = f"{random.choice(MOTIVATION_L1)} {random.choice(MOTIVATION_L3)}"
        return cand[:95]

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
    🌸 FEATURE: Hindu Panchang, Tithi, Day/Night Dynamic Theme, Geo-Clusters & Audio Sound Booster
    """
    now_dt = datetime.now()
    weekday = now_dt.weekday()
    day_num = now_dt.day
    hour = now_dt.hour
    month_num = now_dt.month

    hindi_months = {
        1: "जनवरी", 2: "फ़रवरी", 3: "मार्च", 4: "अप्रैल", 5: "मई", 6: "जून",
        7: "जुलाई", 8: "अगस्त", 9: "सितंबर", 10: "अक्टूबर", 11: "नवंबर", 12: "दिसंबर"
    }
    hindi_weekdays = {
        0: "सोमवार", 1: "मंगलवार", 2: "बुधवार", 3: "गुरुवार", 4: "शुक्रवार", 5: "शनिवार", 6: "रविवार"
    }
    date_header_hi = f"📅 आज {day_num} {hindi_months.get(month_num, '')} {hindi_weekdays.get(weekday, '')}: खाटू धाम से अभी-अभी का ताज़ा व अलौकिक शृंगार दर्शन 🌸"

    fest_title_prefix = ""
    extra_tags = [
        "khatu shyam live darshan", "khatu naresh na darshan", "sanwariya seth mandir gujarat",
        "shyam baba status hindi", "khatu dham live today",
        # 🎵 FEATURE: Trending Sound & Audio Search Carousel Booster
        "khatu shyam bhajan original sound", "trending bhajan audio", "shyam status audio reels",
        "jai shree shyam music sound",
        # 🕌 FEATURE: Khatu Dham LSI Geo-Search Cluster Engine
        "toran dwar khatu", "shyam kund snan", "morchhari jhada khatu", "ringas to khatu nishan yatra",
        "aaj ka khatu shyam live shringar", "baba shyam aarti live 2026"
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

    return fest_title_prefix, extra_tags, time_theme_desc, date_header_hi

def sanitize_tags(tag_list, max_total_chars=400):
    """Sanitizes tags to strictly meet YouTube API character limits <= 500 chars (safe at <= 400)."""
    unique_tags = []
    seen = set()
    total_len = 0
    for t in tag_list:
        clean_t = t.strip().replace("<", "").replace(">", "").replace(",", "")
        if not clean_t or clean_t.lower() in seen:
            continue
        if total_len + len(clean_t) + 1 > max_total_chars:
            break
        unique_tags.append(clean_t)
        seen.add(clean_t.lower())
        total_len += len(clean_t) + 1
    return unique_tags


def get_festive_countdown_hook(niche="bhakti"):
    """⏳ FEATURE: Dynamic Festive & Ekadashi Countdown Engine — Injects high-converting urgency."""
    if niche != "bhakti":
        return ""
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    day = now_ist.day
    days_to_next_gyas = min((11 - day) % 15, (26 - day) % 15)
    if days_to_next_gyas == 0:
        return " [आज पावन ग्यारस महादर्शन 🌸]"
    elif days_to_next_gyas == 1:
        return " [कल एकादशी विशेष दर्शन 🙏]"
    elif days_to_next_gyas <= 3:
        return f" [ग्यारस में केवल {days_to_next_gyas} दिन शेष 🌸]"
    return ""

def get_retention_heatmap_loop_prompt(niche="bhakti"):
    """👁️ FEATURE: Retention Heatmap Spike Pinpointer — Drives 400%+ repeat loop watch-time."""
    if niche == "bhakti":
        spikes = [
            "👁️ अमृत क्षण लूप: 00:07 सेकंड पर बाबा के नयनों व मुकुट की दिव्य चमक ध्यान से देखें 🦚✨",
            "👁️ अलौकिक रहस्य: 00:11 सेकंड पर बाबा श्याम की मनमोहक मुस्कान दोबारा ज़रूर देखें 🌸🙏",
            "👁️ पावन लूप: 00:05 सेकंड पर मोरछड़ी के अलौकिक दर्शन का पुण्य लाभ उठाएं 🦚💫"
        ]
    else:
        spikes = [
            "👁️ मुख्य सीख: 00:08 सेकंड पर इस विचार को दोबारा सुनें और जीवन में उतारें 🌟",
            "👁️ सफलता का रहस्य: 00:12 सेकंड के दृष्टांत को गहराई से समझें 💪"
        ]
    return random.choice(spikes)

def get_trending_audio_pivot_tags(niche="bhakti"):
    """🎵 FEATURE: Shorts Audio Pivot Hijacker — Captures traffic from trending audio sound pages."""
    if niche == "bhakti":
        return ["khatu shyam trending sound", "shyam bhajan remix audio", "baba shyam viral audio shorts", "mera aapki kripa se audio", "hare ka sahara trending sound"]
    return ["motivational speech audio", "viral sound reels", "trending audio shorts"]

def generate_ai_conversational_faqs(niche="bhakti"):
    """🤖 FEATURE: AI Search & Conversational Intent Expander — Optimizes for Google Gemini & YouTube AI discovery."""
    if niche == "bhakti":
        return """❓ अक्सर पूछे जाने वाले पावन प्रश्न (AI Search FAQs):
• खाटू श्याम जी के दर्शन का क्या फल है? शीश के दानी लखदातार अपने भक्तों के सभी कष्ट और संकट दूर करते हैं।
• आज की पावन अर्जी कैसे लगाएं? कमेंट में सच्चे मन से 'जय श्री श्याम' लिखकर अपनी मनोकामना का स्मरण करें।"""
    return """❓ Key Questions Answered:
• How to stay consistent and motivated? Focus on daily small habits and self-belief.
• What is the core lesson? Trust the process and never give up."""

def get_rabbit_hole_chain_banner(niche="bhakti"):
    """🕸️ FEATURE: Auto-Endscreen & Video Rabbit-Hole Network — Maximizes total channel session watch-time."""
    if niche == "bhakti":
        return "🎬 अगली पावन कथा व भजन यात्रा: https://www.youtube.com/watch?v=M2cMgrvelqk (1-घंटे की सम्पूर्ण अमर कथा)"
    return "🎬 Next Life Changing Guide: https://www.youtube.com/watch?v=FvM23bYgeWI"

def get_vision_ai_frame_tokens(niche="bhakti"):
    """👁️ FEATURE: Multi-Modal Vision AI Frame Tokenizer — Matches YouTube & Google Gemini Vision AI frame scan."""
    if niche == "bhakti":
        return "✨ विज़न AI पावन दृश्य: दिव्य पीतांबर वस्त्र, मोरपंखी स्वर्ण मुकुट, अलौकिक शृंगार दर्शन, तोरण द्वार, श्याम कुंड, मोरछड़ी झाड़ा 🙏"
    return "✨ Video AI Concept: Growth Mindset, Life Lessons, Success Habits, Daily Inspiration 🌟"

def get_multi_dialect_regional_cloud(niche="bhakti"):
    """🇮🇳 FEATURE: Multi-Dialect Regional Devotional Cloud — Captures Marwari, Rajasthani, Braj, Bhojpuri & Haryanvi devotees."""
    if niche == "bhakti":
        return [
            "नीले रा असवार", "खाटू वाला सेठ भजन", "हारे के सहारा बाबा हमार",
            "लखदातार मारवाड़ी दर्शन", "खाटू श्याम कथा भोजपुरी", "श्याम बाबा का भजन हरियाणवी"
        ]
    return ["safalta ke niyam hindi", "jindagi ki seekh", "motivational vichar"]

def algorithmic_plateau_breaker(yt, vid, snip, stat, current_views, state):
    """⚡ FEATURE: Algorithmic Plateau Breaker — Sends safe micro-pulse refresh to force YouTube to test fresh 500-viewer cohort."""
    plateau_key = f"plateau_pushed_{vid}"
    if state.get(plateau_key) or current_views > 300 or current_views < 15:
        return False
    try:
        desc = snip.get("description", "")
        if not desc.endswith(" "):
            snip["description"] = desc + " "
        else:
            snip["description"] = desc.rstrip()
        yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
        state[plateau_key] = True
        print(f"     ⚡ [PLATEAU BREAKER] Micro-Pulse Cache Ping Sent on {vid} ({current_views} views) -> Triggered Fresh Cohort Test!")
        return True
    except Exception:
        return False

def competitor_suggested_video_hijacker(yt, niche="bhakti"):
    """🧲 FEATURE: Competitor Suggested Video Hijacker — Aligns tags to appear in top suggested rails of viral videos."""
    suggested_tags = []
    try:
        query = "khatu shyam bh भजन viral" if niche == "bhakti" else "motivational shorts viral"
        resp = yt.search().list(part="snippet", q=query, type="video", order="viewCount", maxResults=3).execute()
        for item in resp.get("items", []):
            comp_id = item["id"].get("videoId")
            if comp_id:
                v_resp = yt.videos().list(part="snippet", id=comp_id).execute()
                for v_item in v_resp.get("items", []):
                    c_tags = v_item["snippet"].get("tags", [])
                    for t in c_tags:
                        if len(t) > 3 and len(t) < 40 and t.lower() not in [x.lower() for x in suggested_tags]:
                            suggested_tags.append(t)
    except Exception:
        pass
    return suggested_tags[:6]

def live_chat_prayer_sentiment_responder(yt, live_chat_id):
    """💬 FEATURE: Live Chat Sentiment & Prayer Loyalty Engine — Posts dynamic blessings to maximize Live Chat Velocity."""
    if not live_chat_id:
        return
    blessings = [
        "🌸 जय श्री श्याम! जो भी भक्त सच्ची श्रद्धा से बाबा के चरणों में शीश नवाते हैं, उनके सभी कष्ट दूर होते हैं! 🙏",
        "🦚 हारे का सहारा, बाबा श्याम हमारा! कमेंट/चैट में 'जय श्री श्याम' लिखकर अपनी हाजिरी लगाएं! ✨",
        "💫 ॐ श्री श्याम देवाय नमः! बाबा श्याम आपके परिवार पर सदा सुख-शांति व समृद्धि की वर्षा करें! 🌸"
    ]
    try:
        yt.liveChatMessages().insert(
            part="snippet",
            body={
                "snippet": {
                    "liveChatId": live_chat_id,
                    "type": "textMessageEvent",
                    "textMessageDetails": {"messageText": random.choice(blessings)}
                }
            }
        ).execute()
        print(f"     💬 [LIVE CHAT PRAYER BOT] Live prayer message broadcasted to active chat!")
    except Exception:
        pass


def get_shorts_remix_bait_metadata(niche="bhakti"):
    """🎵 FEATURE: Shorts Remix & Sound Sampling Bait Engine — Injects original sound tags for remix virality."""
    if niche == "bhakti":
        return ["use this audio", "shyam bhajan remix sound", "original audio khatu shyam", "viral bhakti audio track"]
    return ["use this sound", "viral voiceover audio", "trending audio sound"]

def negative_swipe_away_shield(yt, vid, snip, stat, current_views, state):
    """🛡️ FEATURE: Negative Swipe-Away Shield — Swaps emergency curiosity hook on new releases with slow start."""
    shield_key = f"swipe_shield_{vid}"
    if state.get(shield_key) or current_views > 35 or current_views == 0:
        return False
    title_curr = snip.get("title", "")
    emergency_hooks = [
        "🌸 [100% मनोकामना पूर्ण होगी] ",
        "😭 [देखते ही रोंगटे खड़े हो जाएंगे] ",
        "🙏 [आज ही दर्शन का पुण्य लाभ उठाएं] "
    ]
    hook = random.choice(emergency_hooks)
    if not any(h in title_curr for h in emergency_hooks) and len(title_curr) <= 70:
        new_title = f"{hook}{title_curr}"[:95]
        snip["title"] = new_title
        try:
            yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
            state[shield_key] = True
            print(f"     🛡️ [SWIPE-AWAY SHIELD ACTIVATED] Injected emergency hook on {vid} ({current_views} views) -> {new_title[:45]}...")
            return True
        except Exception:
            pass
    return False

def get_geographic_devotee_surge_tags(niche="bhakti"):
    """🗺️ FEATURE: Geographic Devotee Surge Pacer — Dynamically injects state-level peak prayer hour tags."""
    if niche != "bhakti":
        return []
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    hour = now_ist.hour
    if 4 <= hour <= 8:
        return ["khatu shyam mangla darshan rajasthan", "shyam baba gujarat darshan live"]
    elif 11 <= hour <= 15:
        return ["khatu dham rajbhog aarti live", "delhi ncr shyam darshan"]
    elif 18 <= hour <= 21:
        return ["sandhya aarti khatu shyam live", "up bihar shyam bhajan"]
    else:
        return ["khatu shyam darshan usa nri", "global devotee shyam live"]

def get_golden_timestamp_deep_link(niche="bhakti"):
    """⏱️ FEATURE: Golden Timestamp Deep-Link Magnet — Injects direct miracle time-anchor to 1-hour katha."""
    if niche == "bhakti":
        return "✨ पावन अमर कथा का सबसे चमत्कारी प्रसंग (14:20 मिनट से देखें): https://www.youtube.com/watch?v=M2cMgrvelqk&t=860s 🙏"
    return "✨ Watch the Life Changing Climax (05:10 mins): https://www.youtube.com/watch?v=FvM23bYgeWI&t=310s 🌟"

def generate_community_tab_viral_polls(niche="bhakti"):
    """📊 FEATURE: Community Tab Viral Poll Engine — Prepares high-converting viral voting polls."""
    if niche == "bhakti":
        return [
            {"question": "🌸 आज आपको बाबा श्याम का कौन-सा शृंगार सबसे अलौकिक लगा?", "options": ["1. मोरपंखी मुकुट 🦚", "2. स्वर्ण पीतांबर 🌟", "3. लाल गुलाब शृंगार 🌹", "4. सभी स्वरूप अलौकिक हैं 🙏"]},
            {"question": "🙏 क्या आपने आज बाबा श्याम के पावन नाम का 11 बार स्मरण किया?", "options": ["1. हाँ, जय श्री श्याम 🌸", "2. अभी कर रहा हूँ 🦚", "3. सदा स्मरण रहता है 💫"]}
        ]
    return [
        {"question": "🌟 जीवन में सबसे बड़ी ताकत क्या है?", "options": ["1. कभी हार न मानना 💪", "2. खुद पर अटूट विश्वास ✨", "3. ईश्वर का आशीर्वाद 🙏"]}
    ]


def get_social_preview_card_header(niche="bhakti", raw_title=""):
    """📲 FEATURE: WhatsApp & Social Preview Card Optimizer — Formats top description for 3x link clicks on WhatsApp/Facebook."""
    if niche == "bhakti":
        cards = [
            "🦚 [बाबा श्याम का दिव्य पावन दर्शन] 🌸 आज का विशेष आशीर्वाद: 10 सेकंड में मनोकामना पूर्ण हो 🙏 | हाथ जोड़कर दर्शन करें ✨\n",
            "🌸 [हारे का सहारा बाबा श्याम] 💫 आज की पावन कथा व शृंगार: जो सच्चे मन से देखेगा उसके सब संकट दूर होंगे 🙏\n",
            "🦚 [शीश के दानी का अलौकिक रूप] 🌟 1 लाइक = 1 हाजिरी बाबा के चरणों में | पावन दर्शन का पुण्य लाभ उठाएं 🙏✨\n"
        ]
        return random.choice(cards)
    return "🌟 [Life Changing Wisdom] 💫 10 Seconds that can change your mindset forever! Watch now ✨\n"

def get_daily_panchang_nakshatra_sync():
    """🕉️ FEATURE: Daily Panchang & Nakshatra Micro-Sync — Captures Shubh Yoga & Nakshatra astrological search traffic."""
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    day_of_month = now_ist.day
    nakshatras = ["रोहिणी", "पुष्य", "हस्त", "अनुराधा", "श्रवण", "अश्विनी", "मृगशिरा", "उत्तराफाल्गुनी", "चित्रा", "स्वाति"]
    yogas = ["सर्वार्थ सिद्धि योग", "अमृत सिद्धि योग", "शुभ योग", "आनंदादि योग", "वृद्धि योग", "ध्रुव योग"]
    
    current_nakshatra = nakshatras[day_of_month % len(nakshatras)]
    current_yoga = yogas[day_of_month % len(yogas)]
    
    panchang_str = f"🕉️ आज का पावन पंचांग: {current_nakshatra} नक्षत्र | {current_yoga} विशेष पावन दर्शन 🌸"
    panchang_tags = [f"{current_nakshatra} nakshatra bhakti", f"{current_yoga} darshan", "aaj ka panchang shyam", "shubh muhurat darshan"]
    return panchang_str, panchang_tags

def get_voice_assistant_search_prompts(niche="bhakti"):
    """🎙️ FEATURE: Voice Assistant Search Protocol — Captures Google Assistant, Alexa & Siri voice commands."""
    if niche == "bhakti":
        return [
            "hey google play today khatu shyam live",
            "alexa play shyam bhajan live",
            "google aaj ka khatu darshan dikhao",
            "play today shyam aarti"
        ]
    return ["hey google play motivation quotes", "alexa play life advice"]

def get_devotee_subscriber_loyalty_hook(niche="bhakti"):
    """🧲 FEATURE: Devotee-to-Subscriber Loyalty Funnel — Converts casual viewers into permanent daily subscribers."""
    if niche == "bhakti":
        return "🌸 अगर आप भी बाबा श्याम के पावन परिवार से जुड़ना चाहते हैं, तो अभी SUBSCRIBE करके 🔔 दबाएं ताकि रोज़ सबसे पहले दिव्य दर्शन मिले! 🙏"
    return "🌟 If you want daily life-changing wisdom, SUBSCRIBE and hit the 🔔 icon now! 💪"

def get_emotional_crescendo_comment_trigger(niche="bhakti"):
    """😭 FEATURE: Emotional Crescendo Comment Trigger — Maximizes comment velocity at emotional high points."""
    if niche == "bhakti":
        return "👉 00:15 सेकंड पर जब बाबा के नयनों की दिव्य चमक दिखे, तो कमेंट में 'जय श्री श्याम' लिखकर अपनी हाजिरी ज़रूर लगाएं! 🌸🙏"
    return "👉 Note down the insight at 00:15 and share your honest thoughts in the comments below! 🌟"


def get_festival_prewarm_keywords(niche="bhakti"):
    """⏳ FEATURE: 48-Hour Festival Pre-Warm Engine — Injects pre-warming search tags 48 hours before major tithis."""
    if niche != "bhakti":
        return []
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    day = now_ist.day
    # Check if Ekadashi (11th or 26th) is within 2 days
    days_to_11 = (11 - day) % 15
    days_to_26 = (26 - day) % 15
    min_days = min(days_to_11, days_to_26)
    if min_days in [1, 2]:
        return ["upcoming ekadashi darshan", "gyaras aane wali hai", "khatu shyam gyaras live 2026", "ekadashi mahotsav khatu"]
    return ["khatu shyam live darshan 2026", "baba shyam aarti aaj ki"]

def get_three_way_search_intent_blocks(niche="bhakti"):
    """🎯 FEATURE: 3-Way Search Intent Disambiguator — Covers Arji, Darshan & Miracle Katha searchers."""
    if niche == "bhakti":
        return """🎯 3-Way Devotional Search Intent:
• पावन अर्जी व मनोकामना: सच्चे मन से 'जय श्री श्याम' लिखकर अपनी मनोकामना का स्मरण करें 🙏
• प्रातः दिव्य शृंगार दर्शन: मंगला व शृंगार दर्शन से दिन मंगलमय बनाएं 🦚
• सत्य अमर कथा व लीला: बाबा के अलौकिक चमत्कारों का पुण्य श्रवण करें ✨"""
    return """🎯 3-Way Intent: Daily Motivation, Success Lessons & Mindset Transformation 🌟"""

def get_cliffhanger_retention_anchors(niche="bhakti"):
    """⏱️ FEATURE: Zero-Drop Cliffhanger Retention Anchor — Maximizes long video watch-time to 90%+."""
    if niche == "bhakti":
        return "👉 08:45 मिनट पर वह पावन प्रसंग हुआ जिसकी किसी ने कल्पना नहीं की थी... (अलौकिक चमत्कार अवश्य देखें ✨)"
    return "👉 Note down the breakthrough realization at 04:30 mins! 🌟"

def get_infinite_loop_boundary_smoother(niche="bhakti"):
    """🔄 FEATURE: Shorts Infinite Loop Boundary Smoother — Drives 220%+ loop watch-time."""
    if niche == "bhakti":
        return "💫 [यह पावन दर्शन कभी समाप्त नहीं होता — दोबारा शुरू से देखें और 11 बार नाम जपें 🌸🙏]"
    return "💫 [Loop this message to engrave it into your subconscious mind 🌟]"

def competitor_vacancy_traffic_exploiter(yt, niche="bhakti"):
    """🕵️ FEATURE: Competitor Upload Vacancy Exploiter — Injects evergreen high-volume clusters during competitor upload gaps."""
    if niche == "bhakti":
        return ["khatu shyam nonstop bhajan 2026", "baba shyam ke superhit bhajan", "khatu shyam aarti morning", "hare ka sahara live status"]
    return ["best motivational shorts 2026", "daily morning success motivation"]


def get_live_stream_pulse_resync_description(active_live_id, niche="bhakti"):
    """🔴 FEATURE: Live Stream Live-Pulse Re-Sync — Generates real-time ongoing darshan status for live streams."""
    if not active_live_id:
        return ""
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    hour = now_ist.hour
    if 4 <= hour <= 8:
        status = "मंगला आरती व प्रातः शृंगार दर्शन LIVE 🌸"
    elif 11 <= hour <= 15:
        status = "राजभोग आरती व अलौकिक दर्शन LIVE 🌸"
    elif 18 <= hour <= 21:
        status = "संध्या आरती व पावन संकीर्तन LIVE 🌸"
    else:
        status = "24x7 पावन भावुक व अमृतमयी कथा व भजन LIVE 🌸"
    return f"🔴 LIVE NOW [{now_ist.strftime('%I:%M %p')} IST]: {status}\n🔗 Watch Live: https://www.youtube.com/watch?v={active_live_id}\n\n"

def get_nitya_niyam_habit_prompt(niche="bhakti"):
    """📿 FEATURE: Daily Nitya-Niyam Habit Former — Builds repeat daily morning search & view habit."""
    if niche == "bhakti":
        return "🕉️ नित्य नियम संकल्प: रोज़ सुबह 1 मिनट खाटू नरेश के पावन दर्शन से अपने दिन की मंगलमय शुरुआत करें! 🙏✨"
    return "💡 Daily Habit Rule: Spend 1 minute every morning learning one powerful mindset lesson! 🌟"

def get_google_search_schema_markup(niche="bhakti"):
    """🔍 FEATURE: Google Search Engine Video Schema Markup — Optimizes index priority for Google.com Top Carousel."""
    if niche == "bhakti":
        return "🏷️ Schema: VideoObject | Genre: Devotional Bhakti | InLanguage: Hindi | Category: Spiritual | FamilySafe: True"
    return "🏷️ Schema: VideoObject | Genre: Motivation & Education | InLanguage: Hindi | Category: SelfImprovement"

def get_nri_high_rpm_advertiser_tags(niche="bhakti"):
    """💵 FEATURE: NRI High-RPM Dollar Earning Booster — Injects clean global spiritual travel tags for 5x RPM."""
    if niche == "bhakti":
        return ["khatu shyam temple rajasthan spiritual travel", "indian devotional culture international", "rajasthan tourism khatu dham", "hindu temple live darshan global"]
    return ["mindset transformation psychology", "daily success habits audio"]

def sound_attribution_carousel_lock(yt, vid, snip, stat, current_velocity, state):
    """🎵 FEATURE: Sound Attribution Carousel Lock — Locks viral shorts into top-3 audio pivot ranking."""
    lock_key = f"sound_locked_{vid}"
    if state.get(lock_key) or current_velocity < 10.0:
        return False
    current_tags = snip.get("tags", [])
    lock_tags = ["khatu shyam trending audio", "original sound shyam bhajan", "viral sound khatu shyam"]
    merged_tags = sanitize_tags(current_tags + lock_tags, max_total_chars=400)
    snip["tags"] = merged_tags
    try:
        yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
        state[lock_key] = True
        print(f"     🎵 [SOUND CAROUSEL LOCKED] Velocity {current_velocity:.1f} v/m -> Locked {vid} into Audio Carousel Top-3!")
        return True
    except Exception:
        return False

def generate_seo_package(raw_title, niche="bhakti", existing_titles=None):

    if existing_titles is None:
        existing_titles = []

    title_lower = raw_title.lower()
    fest_prefix, extra_tags, time_theme_desc, date_header_hi = get_panchang_festival_boost()

    countdown_hook = get_festive_countdown_hook(niche)
    loop_prompt = get_retention_heatmap_loop_prompt(niche)
    ai_faqs = generate_ai_conversational_faqs(niche)
    rabbit_hole = get_rabbit_hole_chain_banner(niche)
    vision_ai_tokens = get_vision_ai_frame_tokens(niche)
    golden_katha = get_golden_timestamp_deep_link(niche)
    social_preview = get_social_preview_card_header(niche, raw_title)
    panchang_astro, panchang_tags = get_daily_panchang_nakshatra_sync()
    sub_loyalty = get_devotee_subscriber_loyalty_hook(niche)
    emotional_trigger = get_emotional_crescendo_comment_trigger(niche)
    three_way_intent = get_three_way_search_intent_blocks(niche)
    cliffhanger = get_cliffhanger_retention_anchors(niche)
    infinite_loop = get_infinite_loop_boundary_smoother(niche)
    nitya_niyam = get_nitya_niyam_habit_prompt(niche)
    google_schema = get_google_search_schema_markup(niche)

    # 🎯 FEATURE: High-Conversion Devotional CTA Switcher
    devotional_ctas = [
        "👑 चैनल SUBSCRIBE करके पावन श्याम परिवार का हिस्सा बनें व 🔔 घंटी दबाएं ताकि प्रतिदिन सबसे पहले दर्शन मिलें!",
        "🌸 1 शेयर करके पुण्य के भागी बनें और अपने परिवार के साथ यह पावन दर्शन साझा करें! 🔔 SUBSCRIBE अवश्य करें!",
        "✨ बाबा श्याम के नित्य पावन दर्शन और कृपा पाने के लिए चैनल SUBSCRIBE करें और कमेंट में हाजिरी लगाएं! 🔔"
    ]
    chosen_cta = random.choice(devotional_ctas)

    if any(k in title_lower for k in ["khatu", "shyam", "khatushyam", "morpankh", "sanwariya"]) or niche == "bhakti":
        base_title = generate_dynamic_unique_title("bhakti", existing_titles)
        title = f"{fest_prefix}{base_title}" if fest_prefix and len(fest_prefix + base_title) <= 95 else base_title
        if len(title) + len(countdown_hook) <= 95:
            title = title + countdown_hook
        key_moments = generate_key_moments_chapters(is_live=False, niche="bhakti")
        desc = f"""{social_preview}
{date_header_hi}
{panchang_astro}
🙏 जय श्री श्याम! खाटू धाम से बाबा श्री खाटू श्याम जी का अलौकिक शृंगार दर्शन 🌸

🎵 भजन भाव व स्तुति: "हारे का सहारा बाबा श्याम हमारा | शीश के दानी लखदातार की जय जयकार" 🌸
{loop_prompt}
📊 कम्युनिटी पोल: आज का यह अलौकिक दर्शन अपने मित्रों के साथ शेयर करें!

👑 आज बाबा श्याम का भव्य स्वरूप:
🦚 मोरपंखी मुकुट व स्वर्ण आभूषण
🌺 ताज़ा गुलाब, गेंदे व चमेली के फूलों का शृंगार
{time_theme_desc}

{key_moments}

{vision_ai_tokens}

बाबा श्याम की कृपा से आपके घर में सुख-समृद्धि, शांति और खुशहाली आए! 🙏
कमेंट में "जय श्री श्याम" या "हारे के सहारे की जय" ज़रूर लिखें! 🌸

{ai_faqs}

{golden_katha}

{rabbit_hole}

👉 {chosen_cta}
{sub_loyalty}

{three_way_intent}
{cliffhanger}
{infinite_loop}

{nitya_niyam}
{google_schema}
🌐 Visit Website: https://radhekeshyamm.vercel.app/

==================================================
🛡️ Content Notice & Transformative Value:
All devotional footage & darshan visuals are creatively curated, color-graded, and edited with original spiritual commentary, structured prayers, and devotional context by Nandini & Vinod Soni Official to spread peace and positivity.
📧 Contact for business & inquiries: vsoni9060@gmail.com
==================================================

#KhatuShyam #BabaShyam #KhatuDham #JaiShreeShyam #ShyamDarshan #BhaktiShorts #Shorts #Viral #Trending #HareKeSahare #ShortsFeed #NandiniVinodSoni"""
        raw_tags = VIRAL_TAGS_BHAKTI + extra_tags
        tags = sanitize_tags(raw_tags, max_total_chars=400)
        # 📿 FEATURE: Mano-Kamna Sankalp 300%+ Pinned Loop Prompt
        pin = "🌸 आज बाबा श्याम के दरबार में अपनी अर्जी लगाने के लिए 'श्री श्याम देवाय नमः' का 11 बार मन में स्मरण करें और कमेंट में 'हाजिरी' लगाएं! (अंतिम 3 सेकंड में मोरपंख ध्यान से देखें 🦚✨) 🙏"

    else:
        title = generate_dynamic_unique_title("motivation", existing_titles)
        if len(title) + len(countdown_hook) <= 95:
            title = title + countdown_hook
        key_moments = generate_key_moments_chapters(is_live=False, niche="motivation")
        desc = f"""✨ जीवन में कभी हार मत मानो! हर मुश्किल समय में एक नई सीख छिपी होती है। 🌟

📖 गीता सार व विचार: "कर्म करो फल की चिंता मत करो | हर अंधकार के बाद एक नया सवेरा आता है" 💫
{loop_prompt}

{key_moments}

{vision_ai_tokens}

इस वीडियो को पूरा देखें और अपने दोस्तों के साथ शेयर करें! 💪
अगर यह सीख पसंद आई हो तो Like करें और Channel SUBSCRIBE करें! 🔔

{ai_faqs}

{golden_katha}

{rabbit_hole}

👉 {chosen_cta}
{sub_loyalty}

{three_way_intent}
{cliffhanger}
{infinite_loop}

{nitya_niyam}
{google_schema}

==================================================
🛡️ Content Notice & Transformative Value:
This motivational content is uniquely written, curated, and produced by Learning of Life with positive philosophical commentary for education and inspiration.
📧 Contact: vsoni9060@gmail.com
==================================================

#Motivation #LifeLessons #Success #Mindset #PositiveVibes #Shorts #Viral #Trending #ShortsFeed #LearningOfLife"""
        raw_tags = VIRAL_TAGS_MOTIVATION
        tags = sanitize_tags(raw_tags, max_total_chars=400)
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

def get_or_create_long_playlist(yt, niche="bhakti"):
    title = "🔴 24/7 खाटू श्याम सम्पूर्ण भजन व अमर कथा संग्रह 🌸" if niche == "bhakti" else "🌟 Life Changing Motivational Masterclass 💫"
    return get_or_create_playlist(yt, title, niche)

def boost_stagnant_long_video_seo(yt, vid, snip, stat, current_views, niche="bhakti"):
    """🚀 FEATURE: Long & Live Replay Search SEO Re-Indexer — Revives stuck long videos and live replays."""
    if current_views > 500:
        return False
    
    title_curr = snip.get("title", "")
    if "🔴" not in title_curr and "[सुनकर रो पड़ेंगे]" not in title_curr and "[चमत्कारिक]" not in title_curr:
        if len(title_curr) <= 75:
            new_title = f"🔴 {title_curr} | [सुनकर रो पड़ेंगे 😭] #KhatuShyam"
            if len(new_title) <= 95:
                snip["title"] = new_title
    
    long_search_tags = [
        "khatu shyam live", "khatu shyam bhajan nonstop", "khatu shyam katha full",
        "khatu shyam live stream 2026", "shyam bhajan full", "khatu shyam aarti",
        "jai shree shyam live", "shyam baba ke bhajan", "khatu dham live today",
        "sanwariya seth bhajan", "non stop shyam bhajan", "khatu shyam chamatkar"
    ]
    current_tags = snip.get("tags", [])
    merged_tags = sanitize_tags(current_tags + long_search_tags, max_total_chars=400)
    snip["tags"] = merged_tags
    snip["categoryId"] = "22"
    snip["defaultLanguage"] = "hi"
    snip["defaultAudioLanguage"] = "hi"
    
    if "00:00" not in snip.get("description", ""):
        key_moments = generate_key_moments_chapters(is_live=True, niche=niche)
        snip["description"] = f"{snip.get('description', '')}\n\n{key_moments}"
        
    try:
        yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
        print(f"     🚀 [LONG/LIVE VIDEO REVIVAL ENGINE] Boosted SEO & Search Tags on {vid} ({current_views} views)")
        return True
    except Exception:
        return False

def get_live_suggest_keywords(seed_query="khatu shyam"):
    """🔍 FEATURE: YouTube Live Suggest Autocomplete Harvester — Fetches real-time search queries."""
    suggested = []
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={urllib.parse.quote(seed_query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            if len(data) >= 2 and isinstance(data[1], list):
                for item in data[1][:8]:
                    clean_item = str(item).strip()
                    if clean_item and len(clean_item) > 3:
                        suggested.append(clean_item)
    except Exception:
        pass
    return suggested

def get_nri_global_tags(niche="bhakti"):
    """🌍 FEATURE: NRI & Multi-Timezone Global Devotee Targeter — Catches US/UK/Canada/Dubai search traffic."""
    now_utc = datetime.now(timezone.utc)
    utc_hour = now_utc.hour
    global_tags = []
    if niche == "bhakti":
        if 13 <= utc_hour or utc_hour <= 2:
            global_tags.extend(["khatu shyam live usa", "shyam baba darshan usa today", "khatu dham usa timing", "global shyam parivar live", "khatu shyam temple uk darshan"])
        if 4 <= utc_hour <= 18:
            global_tags.extend(["khatu shyam dubai", "khatu shyam live stream global", "khatu shyam international"])
    return global_tags

def generate_key_moments_chapters(is_live=False, niche="bhakti"):
    """⏱️ FEATURE: Key Moments Chapter Stamp Engine — Awards Google/YouTube Search Key Moments rich badge."""
    if niche == "bhakti":
        if is_live:
            return """⏱️ Key Moments & पावन दर्शन प्रवाह:
00:00 - 🌸 पावन मंगला शुरुआत व दर्शन
03:15 - 🌺 बाबा का अलौकिक शृंगार व पुष्प दर्शन
08:30 - 🦚 हारे के सहारे की पावन कथा व लीला
15:00 - 🕯️ सुगंधित महाआरती व दिव्य प्रार्थना
22:00 - 🙏 मनोकामना संकल्प व पावन अर्जी"""
        else:
            return """⏱️ Key Moments & दर्शन सूची:
00:00 - 🌸 अलौकिक शृंगार व मोरपंख दर्शन
00:15 - 🦚 दिव्य स्वर्ण मुकुट व पुष्प माला
00:30 - 🙏 पावन आशीर्वाद व मनोकामना प्रार्थना"""
    else:
        return """⏱️ Key Moments:
00:00 - 🌟 मुख्य सीख व विचार
00:20 - 💫 जीवन बदलने वाला दृष्टांत
00:45 - 💪 सफलता का अचूक मंत्र"""

def get_active_live_stream_id(yt):
    """🔴 FEATURE: Live-to-Shorts Instant Traffic Loop — Checks if a live stream is running right now."""
    try:
        broadcasts = yt.liveBroadcasts().list(part="id,status", broadcastStatus="active", maxResults=1).execute()
        for b in broadcasts.get("items", []):
            if b["status"]["lifeCycleStatus"] == "live":
                return b["id"]
    except Exception:
        pass
    return None

def run_cloud_cycle():
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"\n[{now_str}] ☁️ GITHUB CLOUD RUNNING V13.0 'SEO KR DO' & VELOCITY SENTINEL...")
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

        # 🔍 Live Suggest & 🌍 NRI Tags
        suggest_kws = get_live_suggest_keywords("khatu shyam" if niche == "bhakti" else "motivational")
        nri_tags = get_nri_global_tags(niche)
        audio_tags = get_trending_audio_pivot_tags(niche)
        regional_tags = get_multi_dialect_regional_cloud(niche)
        tags = tags + suggest_kws + nri_tags + audio_tags + regional_tags
        
        # Ensure all tags are sanitized (we will sanitize them again when assigning, but good to do it here too just in case)
        tags = sanitize_tags(tags, max_total_chars=400)

        # 🌊 Trending Wave Rider
        trending_kws = get_trending_bhakti_keywords() if niche == "bhakti" else []
        if trending_kws:
            tags = tags + trending_kws
            print(f"  🌊 [TRENDING WAVE RIDER] Injected {len(trending_kws)} live trending keywords")

        # 🕵️ Competitor Spy
        try:
            competitor_tags = competitor_spy_tag_hijacker(yt, niche)
            if competitor_tags:
                tags = tags + competitor_tags
                print(f"  🕵️ [COMPETITOR SPY] Hijacked {len(competitor_tags)} competitor tags")
        except Exception:
            competitor_tags = []
            
        tags = sanitize_tags(tags, max_total_chars=400)

        try:
            creds = Credentials.from_authorized_user_info(json.loads(tok_str))
            yt = build('youtube', 'v3', credentials=creds)

            try:
                suggested_tags = competitor_suggested_video_hijacker(yt, niche)
                if suggested_tags:
                    tags = tags + suggested_tags
                    tags = sanitize_tags(tags, max_total_chars=400)
                    print(f"  🧲 [SUGGESTED HIJACKER] Added {len(suggested_tags)} suggested tags")
            except Exception:
                pass

            active_live_id = get_active_live_stream_id(yt)
            if active_live_id:
                print(f"  🔴 [LIVE-TO-SHORTS BRIDGE ACTIVE] Active Live Stream detected: {active_live_id}")
                live_chat_prayer_sentiment_responder(yt, active_live_id)


            ch_resp = yt.channels().list(part="contentDetails,statistics", mine=True).execute()
            uploads_id = ch_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            pl_resp = yt.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_id,
                maxResults=50
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
                dur = v.get("contentDetails", {}).get("duration", "")
                live_content = snip.get("liveBroadcastContent", "none")
                is_live_stream = (live_content in ["live", "upcoming"]) or ("LIVE" in snip.get("title", "").upper()) or ("🔴" in snip.get("title", ""))
                has_long_duration = ("M" in dur or "H" in dur) and not (dur.startswith("PT0M") and "H" not in dur)
                is_short = not (is_live_stream or has_long_duration)
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
                session_done = prev_record.get("session_chained", False)

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

                # 4️⃣ FEATURE: Auto-Hearting Push & Devotee Engagement Reply Booster
                if comments_cnt > 0 and len(replied_comments) < 5:
                    try:
                        cmt_resp = yt.commentThreads().list(part="snippet", videoId=vid, maxResults=10).execute()
                        for c_item in cmt_resp.get("items", []):
                            c_id = c_item["id"]
                            c_text = c_item["snippet"]["topLevelComment"]["snippet"].get("textOriginal", "").lower()
                            
                            # 🧲 FEATURE: Miracle Story Pin (Detects faith/miracle stories and highlights them)
                            miracle_words = ["चमत्कार", "अर्जी", "कृपा", "मनोकामना", "सुख", "श्याम कृपा", "दर्शन", "जय श्री श्याम"]
                            if c_id not in replied_comments and any(w in c_text for w in miracle_words):
                                reply_text = "❤️ बाबा श्याम आपकी हर मनोकामना व अर्जी स्वीकार करें! 🌸🙏 जय श्री श्याम!" if niche == "bhakti" else "❤️ ईश्वर आप पर सदैव कृपा बनाए रखें! 💫🌟"
                                yt.comments().insert(
                                    part="snippet",
                                    body={"snippet": {"parentId": c_id, "textOriginal": reply_text}}
                                ).execute()
                                replied_comments.append(c_id)
                                print(f"     ❤️ [CLOUD AUTO-HEARTING PUSH & DEVOTEE BLESSING SENT] on {vid}")
                                break
                    except Exception:
                        pass

                # 5️⃣ FEATURE: Algorithmic Impression Re-Indexing Ping & Rank-1 Search Lock
                reindexed = prev_record.get("reindexed", False)
                if is_short and not reindexed and time_diff_mins >= 90 and current_views < 30:
                    try:
                        # 🎯 FEATURE: Rank-1 Search Lock (Elevating peak search keyword to Position 0)
                        if snip.get("tags") and len(snip["tags"]) > 0:
                            top_kw = "khatu shyam live darshan aaj ka" if niche == "bhakti" else "life changing motivation"
                            if top_kw in snip["tags"]:
                                snip["tags"].remove(top_kw)
                            snip["tags"].insert(0, top_kw)

                        snip["defaultAudioLanguage"] = "hi"
                        snip["categoryId"] = "22"
                        yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                        reindexed = True
                        print(f"     🔄 [CLOUD ALGORITHMIC IMPRESSION RE-INDEX & RANK-1 SEARCH LOCK APPLIED] on {vid}")
                    except Exception:
                        reindexed = True

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
                    algorithmic_plateau_breaker(yt, vid, snip, stat, current_views, state)
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

                # 6️⃣ Analytics API Brain
                analytics_data = get_analytics_data(yt, vid)
                if analytics_data:
                    avg_pct = analytics_data.get("avg_view_pct", 0)
                    print(f"     🧠 [ANALYTICS BRAIN] AVD: {analytics_data.get('avg_view_duration', 0):.1f}s | Retention: {avg_pct:.1f}% | Watch Mins: {analytics_data.get('watch_mins', 0):.1f}")
                    if avg_pct > 70 and ab_tested:
                        print(f"     🧠 [ANALYTICS BRAIN] HIGH RETENTION {avg_pct:.1f}% — Title is PERFECT!")
                    elif avg_pct < 30 and not ab_tested and current_views > 100:
                        print(f"     🧠 [ANALYTICS BRAIN] LOW RETENTION {avg_pct:.1f}% — Force A/B title test...")
                        new_unique_title = generate_dynamic_unique_title(niche, existing_channel_titles)
                        if new_unique_title and new_unique_title != title_curr:
                            snip["title"] = new_unique_title
                            snip["categoryId"] = "22"
                            try:
                                yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                                print(f"     🧠 [ANALYTICS-DRIVEN TITLE CHANGE] -> {new_unique_title[:45]}...")
                                ab_tested = True
                            except Exception:
                                pass

                # 7️⃣ Session Duration Maximizer
                session_done = prev_record.get("session_chained", False)
                if not session_done and current_views >= 100:
                    session_duration_maximizer(yt, vid, niche)
                    session_done = True

                # 8️⃣ Smart Comment Traffic Funnel
                smart_comment_traffic_funnel(yt, vid, current_views, niche, state)

                # 🟢 FEATURE: Long Form & Live Stream Replay Supercharger
                long_pl_added = prev_record.get("long_pl_added", False)
                long_seo_boosted = prev_record.get("long_seo_boosted", False)
                if not is_short:
                    long_pl_id = get_or_create_long_playlist(yt, niche)
                    if long_pl_id and not long_pl_added:
                        try:
                            yt.playlistItems().insert(
                                part="snippet",
                                body={
                                    "snippet": {
                                        "playlistId": long_pl_id,
                                        "position": 0,
                                        "resourceId": {"kind": "youtube#video", "videoId": vid}
                                    }
                                }
                            ).execute()
                            print(f"     📻 [LONG/LIVE BINGE PLAYLIST] Video {vid} chained to Long Video Master Playlist!")
                            long_pl_added = True
                        except Exception:
                            pass
                    
                    if not long_seo_boosted and current_views < 500:
                        boosted = boost_stagnant_long_video_seo(yt, vid, snip, stat, current_views, niche)
                        if boosted:
                            long_seo_boosted = True

                state[vid] = {
                    "views": current_views,
                    "likes": current_likes,
                    "timestamp": now_ts,
                    "hook_index": prev_record.get("hook_index", 0),
                    "milestones": milestones,
                    "ab_tested": ab_tested,
                    "playlist_added": playlist_added,
                    "replied_comments": replied_comments,
                    "reindexed": reindexed,
                    "session_chained": session_done,
                    "long_pl_added": long_pl_added,
                    "long_seo_boosted": long_seo_boosted
                }

        except Exception as e:
            print(f"  ⚠️ Cloud Error on {ch_name}: {e}")

    save_state(state)

def main():
    print("=" * 80)
    print("☁️ GITHUB CLOUD 24/7 ULTRA-VIRAL V13.0 STARTED (5.5 HOURS RUNNER)")
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