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

VIRAL_TAGS_BHAKTI = [
    "khatu shyam", "khatu shyam live darshan", "khatu shyam shorts", "khatu shyam status 2026",
    "jai shree shyam", "khatu shyam ji", "haare ka sahara", "shyam baba", "khatu naresh",
    "khatu dham", "morpankhi mukut", "khatu shyam darshan today", "khatu shyam shringar",
    "bhakti shorts", "shorts feed", "viral shorts", "trending shorts", "nandini vinod soni"
]

VIRAL_TAGS_MOTIVATION = [
    "learning of life", "life changing lesson", "motivational shorts", "dhyan ke fayde",
    "meditation in hindi", "mind peace status", "peace of mind", "overthinking kaise roke",
    "positive vibes status", "success motivation", "mind power", "shorts feed",
    "trending shorts", "viral shorts", "explore", "explore page", "daily motivation"
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
            json.dump(state, f, indent=2)
    except Exception:
        pass

def run_cloud_cycle():
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"\n[{now_str}] ☁️ GITHUB CLOUD SERVER RUNNING 2-MINUTE VELOCITY AUTO-BOOSTER...")
    state = load_state()
    now_ts = int(time.time())

    channels = []
    
    # 1. Nandini to Vinod
    tok_nandini_str = os.environ.get("TOKEN_NANDINI_JSON")
    if tok_nandini_str:
        try:
            channels.append({
                "name": "Nandini & Vinod Soni Official",
                "creds": Credentials.from_authorized_user_info(json.loads(tok_nandini_str)),
                "tags": VIRAL_TAGS_BHAKTI
            })
        except Exception as e:
            print(f"Error parsing Nandini token: {e}")

    # 2. Learning of life
    tok_lol_str = os.environ.get("TOKEN_LEARNING_JSON")
    if tok_lol_str:
        try:
            channels.append({
                "name": "Learning of life",
                "creds": Credentials.from_authorized_user_info(json.loads(tok_lol_str)),
                "tags": VIRAL_TAGS_MOTIVATION
            })
        except Exception as e:
            print(f"Error parsing LOL token: {e}")

    for ch in channels:
        ch_name = ch["name"]
        creds = ch["creds"]
        target_tags = ch["tags"]
        print(f"\n📡 [CLOUD] Scanning Realtime Views on: {ch_name}...")

        try:
            yt = build('youtube', 'v3', credentials=creds)
            ch_resp = yt.channels().list(part="contentDetails", mine=True).execute()
            uploads_id = ch_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            pl_resp = yt.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_id,
                maxResults=10
            ).execute()
            v_ids = [it["contentDetails"]["videoId"] for it in pl_resp.get("items", [])]

            v_resp = yt.videos().list(
                part="snippet,status,statistics,contentDetails",
                id=",".join(v_ids)
            ).execute()

            for v in v_resp.get("items", []):
                vid = v["id"]
                snip = v["snippet"]
                stat = v["status"]
                stats = v["statistics"]
                content = v["contentDetails"]

                if stat.get("privacyStatus") != "public":
                    continue

                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))

                prev = state.get(vid, {})
                prev_views = prev.get("views", views)
                prev_ts = prev.get("timestamp", now_ts)
                diff_mins = max(1, (now_ts - prev_ts) // 60)
                diff_views = views - prev_views
                velocity = diff_views / diff_mins

                print(f"  🎬 [{vid}] Views: {views:<5} (+{diff_views} in {diff_mins}m, {velocity:.1f} v/m) | {snip['title'][:40]}...")

                # Drop / 1K Stall Trigger
                if diff_mins >= 4 and diff_views <= 1:
                    print(f"     🚨 [CLOUD DETECTED SLOWDOWN on {vid}] -> Triggering Wave-2 Cloud Boost...")
                    snip["tags"] = target_tags
                    try:
                        yt.videos().update(part="snippet", body={"id": vid, "snippet": snip}).execute()
                        print(f"     🔥 [CLOUD AUTO-BOOSTED] Re-indexed search signals for {vid}")
                    except Exception as e:
                        print(f"     ⚠️ Cloud update note: {e}")

                state[vid] = {
                    "views": views,
                    "likes": likes,
                    "timestamp": now_ts
                }
        except Exception as e:
            print(f"  ⚠️ Error scanning {ch_name}: {e}")

    save_state(state)

def main():
    print("=" * 80)
    print("🚀 GITHUB 24/7 CLOUD SERVER VELOCITY AUTO-BOOSTER ACTIVE...")
    print("=" * 80)
    # Run loop for 5.5 hours on GitHub runner then self-relay
    end_time = time.time() + 19800  # 5.5 hours
    while time.time() < end_time:
        try:
            run_cloud_cycle()
        except Exception as e:
            print(f"⚠️ Exception in cycle: {e}")
        print("⏳ Sleeping 120 seconds on GitHub Cloud Server...")
        time.sleep(120)

if __name__ == "__main__":
    main()
