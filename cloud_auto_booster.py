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

def generate_seo_package(raw_title, niche):
    title_lower = raw_title.lower()
    
    if any(k in title_lower for k in ["khatu", "shyam", "khatushyam", "morpankh"]):
        title = "बाबा श्याम का दिव्य अलौकिक शृंगार दर्शन 🌸 जय श्री श्याम 🙏 #Shorts #KhatuShyam #Viral"
        desc = """🙏 जय श्री श्याम! खाटू धाम से बाबा श्री खाटू श्याम जी का अलौकिक शृंगार दर्शन 🌸

👑 आज बाबा श्याम का भव्य स्वरूप:
🦚 मोरपंखी मुकुट व स्वर्ण आभूषण
🌺 ताज़ा गुलाब, गेंदे व चमेली के फूलों का शृंगार
✨ जगमगाती संध्या आरती के पावन दर्शन

बाबा श्याम की कृपा से आपके घर में सुख-समृद्धि आए! 🙏
कमेंट में "जय श्री श्याम" या "हारे के सहारे की जय" ज़रूर लिखें! 🌸

👉 रोज़ाना सुबह-शाम ताज़ा दर्शन के लिए SUBSCRIBE करें: https://www.youtube.com/@nandinitovinod
🔔 Bell Icon दबाएं!

#KhatuShyam #BabaShyam #KhatuDham #JaiShreeShyam #ShyamDarshan #BhaktiShorts #Shorts #Viral #Trending #HareKeSahare #ShortsFeed #NandiniVinodSoni"""
        tags = VIRAL_TAGS_BHAKTI
        pin = "🙏 जय श्री श्याम! बाबा श्याम के सभी सच्चे भक्त कमेंट में एक बार 'जय श्री श्याम' ज़रूर लिखें! 🌸👑"
        
    elif any(k in title_lower for k in ["sanwariya", "seth", "sawariya", "mandaphiya"]):
        title = "साँवरिया सेठ के प्रातः दिव्य दर्शन 🌸 सेठों के सेठ साँवरिया सेठ 🙏 #Shorts #SanwariyaSeth #Viral"
        desc = """🙏 जय श्री साँवरिया सेठ! मण्डफिया धाम से साँवरिया सेठ जी के पावन प्रातः दर्शन 🌸

✨ सेठों के सेठ साँवरिया सेठ का मनमोहक रूप!
कमेंट में "जय साँवरिया सेठ" लिखकर अपनी हाजिरी लगाएं और आशीर्वाद पाएं! 🙏

👉 SUBSCRIBE करें: https://www.youtube.com/@nandinitovinod
#SanwariyaSeth #Mandaphiya #BhaktiShorts #Shorts #Viral #Trending #ShortsFeed #NandiniVinodSoni"""
        tags = ["sanwariya seth", "sanwariya seth live", "mandaphiya mandir", "sanwariya seth darshan"] + VIRAL_TAGS_BHAKTI[:15]
        pin = "🙏 जय साँवरिया सेठ! सेठों के सेठ साँवरिया सेठ के भक्त कमेंट में 'जय श्री साँवरिया सेठ' ज़रूर लिखें! 🌸💰"
        
    elif niche == "motivation" or any(k in title_lower for k in ["motivation", "story", "kahani", "lesson", "geeta", "dhyan"]):
        title = "यह 10 सेकंड आपकी पूरी जिंदगी बदल देंगे 🌟 कभी हार मत मानो 💪 #Shorts #Motivation #LifeLessons"
        desc = """✨ जीवन में कभी हार मत मानो! हर मुश्किल समय में एक नई सीख छिपी होती है। 🌟

इस वीडियो को पूरा देखें और अपने दोस्तों के साथ शेयर करें! 💪
अगर यह सीख पसंद आई हो तो Like करें और Channel SUBSCRIBE करें! 🔔

#Motivation #LifeLessons #Success #Mindset #PositiveVibes #Shorts #Viral #Trending #ShortsFeed #LearningOfLife"""
        tags = VIRAL_TAGS_MOTIVATION
        pin = "✨ जीवन में कभी हार मत मानो, ईश्वर हर पल आपके साथ हैं! 🌟 कमेंट में 'Yes' लिखें! 💫"
        
    else:
        title = "ईश्वर के पावन दर्शन 🌸 आपका दिन मंगलमय हो 🙏 #Shorts #Bhakti #Viral"
        desc = """🙏 प्रभु के पावन दर्शन करके अपने दिन की शुभ शुरुआत करें! 🌸

कमेंट में भगवान का नाम लिखें और परिवार के साथ शेयर करें! 🙏
👉 SUBSCRIBE: https://www.youtube.com/@nandinitovinod
#Bhakti #Shorts #Viral #Trending #ShortsFeed"""
        tags = VIRAL_TAGS_BHAKTI if niche == "bhakti" else VIRAL_TAGS_MOTIVATION
        pin = "🙏 भगवान का आशीर्वाद आप और आपके पूरे परिवार पर बना रहे! 🌸✨"
        
    return title, desc, tags, pin

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
                part="snippet,status,statistics",
                id=",".join(v_ids)
            ).execute()

            existing_scheduled_utc = [
                v["status"].get("publishAt") for v in v_resp.get("items", [])
                if v["status"].get("privacyStatus") == "private" and v["status"].get("publishAt")
            ]

            for v in v_resp.get("items", []):
                vid = v["id"]
                snip = v["snippet"]
                stat = v["status"]
                stats = v["statistics"]
                title_curr = snip.get("title", "")

                # TRIGGER CHECK
                if re.search(r'\bseo\s*(kr\s*do|kardo|kar\s*do|krdo)\b', title_curr, re.IGNORECASE):
                    print(f"\n🚨 [CLOUD TRIGGER DETECTED] Video {vid}: '{title_curr}'!")
                    new_title, new_desc, new_tags, pin_comment = generate_seo_package(title_curr, niche)
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

                    try:
                        yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                        print(f"  ✅ [CLOUD SEO & SMART SCHEDULE APPLIED] -> {slot_ist_str}")
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

                time_diff_mins = max(1, (now_ts - prev_time) // 60)
                views_gained = current_views - prev_views
                velocity_per_min = views_gained / time_diff_mins

                # Momentum
                if views_gained >= 5 and velocity_per_min >= 0.5:
                    snip["tags"] = tags
                    snip["categoryId"] = "22"
                    try:
                        yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                    except Exception:
                        pass

                # Slowdown Revival
                elif (time_diff_mins >= 10 and views_gained < 5) or (current_views < 50 and time_diff_mins >= 8):
                    curr_idx = prev_record.get("hook_index", 0)
                    next_idx = (curr_idx + 1) % len(hooks)
                    snip["title"] = hooks[next_idx]
                    snip["tags"] = tags
                    snip["categoryId"] = "22"
                    try:
                        yt.videos().update(part="snippet,status", body={"id": vid, "snippet": snip, "status": stat}).execute()
                        prev_record["hook_index"] = next_idx
                    except Exception:
                        pass

                # Auto Pinned Comment on Live Release
                if comments_cnt == 0:
                    if vid == "rRVGvqYh4R8":
                        pin_msg = "🙏 जय श्री श्याम! नीले के सवार, खाटू नरेश बाबा श्याम के सभी सच्चे भक्त कमेंट में 'खाटू नरेश की जय' ज़रूर लिखें! 🌸👑"
                    elif niche == "bhakti":
                        pin_msg = "🙏 जय श्री श्याम! बाबा श्याम के सभी सच्चे भक्त कमेंट में एक बार 'जय श्री श्याम' ज़रूर लिखें! 🌸👑"
                    else:
                        pin_msg = "✨ जीवन में कभी हार मत मानो, ईश्वर हर पल आपके साथ हैं! 🌟 कमेंट में 'Yes' लिखें! 💫"

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
                    "hook_index": prev_record.get("hook_index", 0)
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
        print(f"\n--- [CYCLE #{cycle_count}] Running 2-Min Interval ---")
        try:
            run_cloud_cycle()
        except Exception as e:
            print(f"⚠️ Top-level cycle error: {e}")

        time.sleep(120)

    print("\n✅ Runner completed 5.5 hours. Handing over to next relay...")

if __name__ == "__main__":
    main()
