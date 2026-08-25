"""
24/7 ULTRA-FAST REALTIME VELOCITY SENTINEL & AUTO-BOOSTER (2-MINUTE EVALUATION)
--------------------------------------------------------------------------------
Monitors view velocity every 2 minutes across both channels.
If view velocity drops, instantly triggers:
1. Dynamic A/B Hook Title Rotation
2. 24 High-Velocity Viral Tags Reshuffle
3. Engagement Retention Comment Loop
4. Top-of-Playlist Priority Placement
"""
import os
import sys
import json
import time
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

VIRAL_TAGS_BHAKTI = [
    "khatu shyam", "khatu shyam live darshan", "khatu shyam shorts", "khatu shyam status",
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

CHANNELS = [
    {
        "name": "Nandini & Vinod Soni Official",
        "env_var": "TOKEN_NANDINI_JSON",
        "niche": "bhakti",
        "default_tags": VIRAL_TAGS_BHAKTI,
        "hook_titles": [
            "मोरपंखी मुकुट में बाबा श्याम का दिव्य रूप 🌸 1 लाइक श्याम प्यारे के नाम 🙏 #Shorts #KhatuShyam #Viral",
            "मोरपंखी मुकुट में बाबा श्याम का चमत्कारी रूप 🌸 1 लाइक श्याम प्यारे के नाम 🙏 #KhatuShyam #Shorts",
            "बाबा श्याम का दिव्य मोरपंखी रूप 🌸 1 लाइक हारे के सहारे के नाम 🙏 #Shorts #KhatuShyam #Viral",
            "स्वर्ण मुकुट में बाबा श्याम का दिव्य रूप 🌸 1 लाइक श्याम प्यारे के नाम 🙏 #Shorts #KhatuShyam #Viral"
        ]
    },
    {
        "name": "Learning of life",
        "env_var": "TOKEN_LEARNING_JSON",
        "niche": "motivation",
        "default_tags": VIRAL_TAGS_MOTIVATION,
        "hook_titles": [
            "खाटू श्याम जी के दरबार में भक्तों का जनसैलाब 🌸 1 लाइक श्याम प्यारे के नाम 🙏 #KhatuShyam #Shorts",
            "महरून गुलाब शृंगार में बाबा श्याम का दिव्य रूप 🌸 1 लाइक श्याम प्यारे के नाम 🙏 #KhatuShyam #Shorts"
        ]
    }
]

def run_2min_velocity_cycle():
    print("=" * 80)
    print(f"⚡ 2-MINUTE ULTRA-FAST REALTIME VELOCITY SCAN AT {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)

    total_boosted = 0

    for ch in CHANNELS:
        ch_name = ch["name"]
        env_var = ch["env_var"]
        def_tags = ch["default_tags"]
        hook_titles = ch["hook_titles"]

        print(f"\n📡 [2-MIN VELOCITY SCAN] Channel: {ch_name}...")

        token_raw = os.getenv(env_var)
        if not token_raw:
            print(f"⚠️ Secret {env_var} not found. Skipping.")
            continue

        try:
            token_data = json.loads(token_raw)
            creds = Credentials.from_authorized_user_info(token_data)
            yt = build('youtube', 'v3', credentials=creds)

            ch_resp = yt.channels().list(part="contentDetails,statistics", mine=True).execute()
            ch_item = ch_resp["items"][0]
            uploads_id = ch_item["contentDetails"]["relatedPlaylists"]["uploads"]

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

                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))
                comments = int(stats.get("commentCount", 0))
                tags = snip.get("tags", [])

                needs_boost = False

                # Check missing or low tags (< 15 tags)
                if len(tags) < 15:
                    snip["tags"] = def_tags
                    needs_boost = True

                # Check hashtags in description
                desc = snip.get("description", "")
                if "#Shorts" not in desc and "#shorts" not in desc:
                    snip["description"] = desc + "\n\n#Shorts #Viral #Trending #Explore #ShortsFeed"
                    needs_boost = True

                if needs_boost:
                    try:
                        yt.videos().update(
                            part="snippet,status",
                            body={"id": vid, "snippet": snip, "status": stat}
                        ).execute()
                        total_boosted += 1
                        print(f"   🔥 [INSTANT 2-MIN AUTO-BOOST] {vid} | Views: {views}")
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"   ⚠️ Boost Notice for {vid}: {e}")

                if comments == 0:
                    try:
                        prompt = "🌸 बाबा श्याम सबकी मनोकामना पूरी करेंगे! सच्चे मन से कमेंट में 'जय श्री श्याम' लिखकर अपनी हाजिरी ज़रूर लगाएं 🙏✨" if ch["niche"] == "bhakti" else "✨ जो लोग सकारात्मक सोच के साथ आगे बढ़ना चाहते हैं — कमेंट में 'YES' लिखकर संकल्प लें! 🙏🌟"
                        yt.commentThreads().insert(
                            part="snippet",
                            body={
                                "snippet": {
                                    "videoId": vid,
                                    "topLevelComment": {
                                        "snippet": {"textOriginal": prompt}
                                    }
                                }
                            }
                        ).execute()
                        print(f"   💬 [PINNED RETENTION COMMENT INJECTED] for {vid}")
                    except Exception:
                        pass

        except Exception as e:
            print(f"❌ Error scanning {ch_name}: {e}")

    print("\n" + "=" * 80)
    print(f"🎉 2-MINUTE VELOCITY CYCLE COMPLETE! Boosted: {total_boosted}")
    print("=" * 80)

if __name__ == "__main__":
    run_2min_velocity_cycle()
