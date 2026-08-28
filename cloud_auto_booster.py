import sys
import io
import os
import json
import time
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

STATE_FILE = "cloud_velocity_state.json"

CHANNELS_CONFIG = [
    {
        "env_var": "TOKEN_NANDINI_JSON",
        "name": "Nandini & Vinod Soni Official",
        "niche": "bhakti",
        "power_hooks": [
            "बाबा श्याम का ऐसा अलौकिक रूप पहले कभी नहीं देखा 😭 1 लाइक श्याम के नाम 🙏 #Shorts #KhatuShyam #Viral",
            "देखते ही दिन बन जाएगा 🌸 खाटू श्याम जी का चमत्कारी दिव्य शृंगार दर्शन 🙏 #KhatuShyam #Shorts #Bhakti",
            "मोरपंखी मुकुट में बाबा श्याम का मनमोहक शृंगार 🌸 हारे के सहारे की जय 🙏 #Shorts #KhatuShyam #Trending",
            "जिसने भी सच्चे मन से दर्शन किए उसकी हर मनोकामना पूरी हुई 🌸 जय श्री श्याम 🙏 #Shorts #KhatuDham",
            "हारे के सहारे बाबा श्याम हमारे 🌸 1 सेकंड निकालकर दर्शन ज़रूर करें 🙏 #Shorts #KhatuShyam #ViralShorts"
        ],
        "viral_tags": [
            "khatu shyam", "khatu shyam live", "khatu shyam shorts", "khatu shyam status 2026",
            "jai shree shyam", "khatu shyam ji", "haare ka sahara", "shyam baba", "khatu naresh",
            "khatu dham", "morpankhi mukut", "khatu shyam darshan today", "khatu shyam shringar",
            "bhakti shorts", "tuesday darshan", "mangalwar darshan", "shorts feed", "viral shorts",
            "trending shorts", "daily darshan", "nandini vinod soni", "explore", "explore page", "viral video"
        ]
    },
    {
        "env_var": "TOKEN_LEARNING_JSON",
        "name": "Learning of life",
        "niche": "motivation",
        "power_hooks": [
            "यह 10 सेकंड आपकी पूरी जिंदगी बदल देंगे 🌟 कभी हार मत मानो 💪 #Shorts #Motivation #LifeLessons",
            "ईश्वर का यह गुप्त संकेत कभी अनदेखा मत करना ✨ गीता सार 🌟 #Shorts #Motivation #PositiveVibes",
            "जब चारों तरफ अंधेरा दिखे तो यह बात हमेशा याद रखना 🌟 #Shorts #Success #Mindset #Trending",
            "खाटू श्याम जी के दरबार में भक्तों का जनसैलाब 🌸 1 लाइक श्याम प्यारे के नाम 🙏 #KhatuShyam #Shorts",
            "काले पत्थर का सच्चा हीरा 😭 इस कहानी को सुनकर आपकी आँखें भर आएंगी 🌟 #Shorts #LifeChanging"
        ],
        "viral_tags": [
            "learning of life", "life changing lesson", "motivational shorts", "dhyan ke fayde",
            "meditation in hindi", "mind peace status", "peace of mind", "overthinking kaise roke",
            "positive vibes status", "success motivation", "mind power", "shorts feed",
            "trending shorts", "viral shorts", "explore", "explore page", "daily motivation"
        ]
    }
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

def run_cloud_cycle():
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"\n[{now_str}] ☁️ GITHUB CLOUD SERVER RUNNING 2-MINUTE VELOCITY AUTO-BOOSTER V3.0...")
    state = load_state()
    now_ts = int(time.time())

    for ch_cfg in CHANNELS_CONFIG:
        tok_str = os.environ.get(ch_cfg["env_var"])
        if not tok_str:
            continue

        ch_name = ch_cfg["name"]
        hooks = ch_cfg["power_hooks"]
        tags = ch_cfg["viral_tags"]

        try:
            creds = Credentials.from_authorized_user_info(json.loads(tok_str))
            yt = build('youtube', 'v3', credentials=creds)

            ch_resp = yt.channels().list(part="contentDetails,statistics", mine=True).execute()
            uploads_id = ch_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            pl_resp = yt.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_id,
                maxResults=8
            ).execute()

            v_ids = [it["contentDetails"]["videoId"] for it in pl_resp.get("items", [])]

            v_resp = yt.videos().list(
                part="snippet,status,statistics",
                id=",".join(v_ids)
            ).execute()

            for v in v_resp.get("items", []):
                vid = v["id"]
                snip = v["snippet"]
                stat = v["status"]
                stats = v["statistics"]

                if stat.get("privacyStatus") != "public":
                    continue

                current_views = int(stats.get("viewCount", 0))
                current_likes = int(stats.get("likeCount", 0))

                prev_record = state.get(vid, {})
                prev_views = prev_record.get("views", current_views)
                prev_time = prev_record.get("timestamp", now_ts)

                time_diff_mins = max(1, (now_ts - prev_time) // 60)
                views_gained = current_views - prev_views
                velocity_per_min = views_gained / time_diff_mins

                print(f"  🎬 [{vid}] Views: {current_views:<5} (+{views_gained} in {time_diff_mins}m, ~{velocity_per_min:.1f} v/m) | Likes: {current_likes:<3} | {snip['title'][:32]}...")

                # 1. Momentum Spike Multiplier
                if views_gained >= 5 and velocity_per_min >= 0.5:
                    print(f"     🚀 [VIRAL MOMENTUM DETECTED] Cloud Reinforcing #ShortsFeed Clusters...")
                    snip["tags"] = tags
                    snip["categoryId"] = "22"
                    try:
                        yt.videos().update(
                            part="snippet,status",
                            body={"id": vid, "snippet": snip, "status": stat}
                        ).execute()
                    except Exception:
                        pass

                # 2. Slowdown Revival & Power Hook Rotation
                elif (time_diff_mins >= 10 and views_gained < 5) or (current_views < 50 and time_diff_mins >= 8):
                    print(f"     ⚡ [REVIVAL TRIGGERED] Cloud Rotating High-CTR Power Hook...")
                    curr_idx = prev_record.get("hook_index", 0)
                    next_idx = (curr_idx + 1) % len(hooks)

                    snip["title"] = hooks[next_idx]
                    snip["tags"] = tags
                    snip["categoryId"] = "22"
                    snip["defaultLanguage"] = "hi"

                    desc = snip.get("description", "")
                    if "#ShortsFeed" not in desc:
                        desc += "\n\n#Shorts #ShortsFeed #Viral #Trending #Bhakti"
                        snip["description"] = desc

                    try:
                        yt.videos().update(
                            part="snippet,status",
                            body={"id": vid, "snippet": snip, "status": stat}
                        ).execute()
                        print(f"     🔥 [CLOUD NEW HOOK APPLIED] -> {snip['title'][:45]}...")
                        prev_record["hook_index"] = next_idx
                    except Exception as e:
                        print(f"     ⚠️ Update note: {e}")

                # 3. Auto-Pinned Engagement Comment on Live Release
                comments_cnt = int(stats.get("commentCount", 0))
                if comments_cnt == 0:
                    if vid == "rRVGvqYh4R8":
                        pin_msg = "🙏 जय श्री श्याम! नीले के सवार, खाटू नरेश बाबा श्याम के सभी सच्चे भक्त कमेंट में 'खाटू नरेश की जय' ज़रूर लिखें! 🌸👑"
                    elif ch_cfg["niche"] == "bhakti":
                        pin_msg = "🙏 जय श्री श्याम! बाबा श्याम के सभी सच्चे भक्त कमेंट में एक बार 'जय श्री श्याम' ज़रूर लिखें! 🌸👑"
                    else:
                        pin_msg = "✨ जीवन में कभी हार मत मानो, ईश्वर हर पल आपके साथ हैं! 🌟 कमेंट में 'Yes' लिखें! 💫"

                    try:
                        yt.commentThreads().insert(
                            part="snippet",
                            body={
                                "snippet": {
                                    "videoId": vid,
                                    "topLevelComment": {
                                        "snippet": {
                                            "textOriginal": pin_msg
                                        }
                                    }
                                }
                            }
                        ).execute()
                        print(f"     📌 [CLOUD AUTO-PINNED COMMENT POSTED] on {vid}")
                    except Exception as e:
                        pass

                state[vid] = {
                    "views": current_views,
                    "likes": current_likes,
                    "timestamp": now_ts,
                    "hook_index": prev_record.get("hook_index", 0)
                }

        except Exception as e:
            print(f"  ⚠️ Error processing {ch_name}: {e}")

    save_state(state)

def main():
    print("=" * 80)
    print("☁️ GITHUB CLOUD 24/7 ULTRA-VIRAL BOOSTER SERVICE STARTED (5.5 HOURS RUNNER)")
    print("=" * 80)

    start_time = time.time()
    max_duration_secs = 5.5 * 3600  # 5.5 hours

    cycle_count = 0
    while time.time() - start_time < max_duration_secs:
        cycle_count += 1
        print(f"\n--- [CYCLE #{cycle_count}] Running 2-Min Interval ---")
        try:
            run_cloud_cycle()
        except Exception as e:
            print(f"⚠️ Top-level cycle error: {e}")

        # Sleep for 2 minutes
        time.sleep(120)

    print("\n✅ Runner completed 5.5 hours. Handing over to next cloud runner relay...")

if __name__ == "__main__":
    main()
