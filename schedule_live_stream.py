#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔴 YOUTUBE LIVE STREAM SCHEDULER & DISPATCHER
=============================================
Easily schedule and dispatch YouTube Live Streams via GitHub Actions:
- Support for 5.5 Hours (Single Leg) or 11 Hours (2-Leg Marathon with Zero-Gap Hot Handshake)
- Continuous Non-Stop Looping of recorded videos (-stream_loop -1)
- Start Immediately OR Schedule at any IST Clock Time (e.g. 18:30 IST) OR Delay in minutes
- Direct GitHub-side delay option (lets you turn off your PC!)
"""

import sys
import os
import time
import subprocess
from datetime import datetime, timedelta, timezone

# Ensure stdout handles UTF-8 on Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DEFAULT_STREAM_KEY = "bqgr-fqwk-0mdc-e0fm-5pxk"

POPULAR_VIDEOS = [
    ("ek_hi_names_hyam.mp4", "एक ही नाम श्याम (Hypnotic New Trance Bhajan)"),
    ("seth_karamsi_khatu_shyam_1hr_movie.mp4", "1-घंटा सेठ करमसी अमर कथा (Best for Marathon)"),
    ("isdrdmaikhojanedde.mp4", "इस दर्द में खो जाने दे (Top Bhajan)"),
    ("darwaja_khula_haai.mp4", "दरवाजा खुला है (Popular Bhajan)"),
    ("Akhri_khat.mp4", "आखिरी खत (Heart-Touching Katha)"),
    ("baba_bhajan_ajka.mp4", "बाबा का पावन भजन संग्रह"),
    ("BESTthreesong.mp4", "Top 3 श्याम भजन संग्रह"),
    ("palatdiya.mp4", "पलट दिया पासा (Superhit)"),
    ("shyambaba.mp4", "श्याम बाबा विशेष भजन"),
    ("anjanemodpe.mp4", "अनजाने मोड़ पे"),
    ("saramanhmamaha.mp4", "सारा मन में समाया"),
    ("dhuniyanethukraya.mp4", "दुनिया ने ठुकराया"),
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print("=" * 72)
    print("  🔴 YOUTUBE LIVE STREAM SCHEDULER & AUTOMATION ENGINE")
    print("  Safe 11-Hour & 5.5-Hour Non-Stop Looped Streaming")
    print("=" * 72)
    print()

def get_ist_now():
    return datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

def choose_video():
    print("📹 [STEP 1/4] Select Video to Stream in Continuous Loop:")
    for idx, (filename, label) in enumerate(POPULAR_VIDEOS, 1):
        print(f"  [{idx:2d}] {filename:<40} ({label})")
    print(f"  [{len(POPULAR_VIDEOS) + 1:2d}] Custom Video Name (type your own .mp4 filename)")
    print()
    
    while True:
        choice = input(f"👉 Select video [1-{len(POPULAR_VIDEOS) + 1}] (Default: 1): ").strip()
        if not choice:
            return POPULAR_VIDEOS[0][0]
        try:
            val = int(choice)
            if 1 <= val <= len(POPULAR_VIDEOS):
                return POPULAR_VIDEOS[val - 1][0]
            elif val == len(POPULAR_VIDEOS) + 1:
                custom = input("👉 Enter exact video filename (e.g. my_video.mp4): ").strip()
                if custom:
                    if not custom.endswith(".mp4"):
                        custom += ".mp4"
                    return custom
        except ValueError:
            pass
        print("❌ Invalid selection. Please try again.")

def choose_stream_key():
    print()
    print("🔑 [STEP 2/4] YouTube Stream Key:")
    print(f"  Current Default: {DEFAULT_STREAM_KEY}")
    choice = input(f"👉 Press Enter to use Default key, or paste new key: ").strip()
    if choice:
        return choice
    return DEFAULT_STREAM_KEY

def choose_duration():
    print()
    print("⏱️ [STEP 3/4] Live Stream Duration:")
    print("  [1] 11 Hours Marathon  — 2 Legs Relay with Zero-Gap Hot Handshake (~10h 40m)")
    print("  [2] 5.5 Hours Single Leg — Auto-Stops cleanly at 5 Hours 20 Minutes")
    print()
    while True:
        choice = input("👉 Select duration [1 or 2] (Default: 1): ").strip()
        if not choice or choice == "1":
            return "11h"
        elif choice == "2":
            return "5.5h"
        print("❌ Please enter 1 or 2.")

def choose_schedule():
    now_ist = get_ist_now()
    print()
    print("⏳ [STEP 4/4] When should the Live Stream Start?")
    print(f"  Current Time (IST): {now_ist.strftime('%I:%M:%S %p')} ({now_ist.strftime('%H:%M:%S')})")
    print("  -------------------------------------------------------------")
    print("  [1] Start IMMEDIATELY (Abhi shuru karein)")
    print("  [2] Schedule at specific Clock Time IST (e.g. 18:30, 21:00, 06:15)")
    print("  [3] Schedule after Delay locally (e.g. In 30 minutes, 2 hours)")
    print("  [4] Cloud Delay on GitHub (Workflow runs now but waits in cloud, PC can be turned off)")
    print()
    
    while True:
        choice = input("👉 Select option [1, 2, 3, or 4] (Default: 1): ").strip()
        if not choice or choice == "1":
            return ("immediate", 0, None)
        elif choice == "2":
            time_str = input("👉 Enter target IST time (HH:MM in 24hr format, e.g. 18:30 or 06:00): ").strip()
            try:
                parts = time_str.split(":")
                target_hour = int(parts[0])
                target_min = int(parts[1]) if len(parts) > 1 else 0
                
                target_dt = now_ist.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)
                if target_dt <= now_ist:
                    # Target is tomorrow!
                    target_dt += timedelta(days=1)
                
                diff_secs = (target_dt - now_ist).total_seconds()
                return ("local_timer", diff_secs, target_dt)
            except Exception:
                print("❌ Invalid time format! Please use HH:MM (e.g. 18:30).")
        elif choice == "3":
            mins_str = input("👉 Enter wait time in minutes (e.g. 15, 45, 120): ").strip()
            try:
                mins = float(mins_str)
                if mins <= 0:
                    return ("immediate", 0, None)
                target_dt = now_ist + timedelta(minutes=mins)
                return ("local_timer", mins * 60, target_dt)
            except Exception:
                print("❌ Invalid number.")
        elif choice == "4":
            mins_str = input("👉 Enter cloud delay in minutes (Max 120 mins, e.g. 30): ").strip()
            try:
                mins = int(mins_str)
                if mins <= 0:
                    return ("immediate", 0, None)
                return ("cloud_delay", mins, None)
            except Exception:
                print("❌ Invalid number.")
        print("❌ Please select 1, 2, 3, or 4.")

def trigger_workflow(stream_key, video_name, duration, delay_minutes=0):
    print()
    print("=" * 72)
    print("🚀 DISPATCHING LIVE STREAM WORKFLOW TO GITHUB ACTIONS...")
    print(f"  📹 Video:    {video_name}")
    print(f"  🔑 Key:      {stream_key[:6]}...{stream_key[-4:]}")
    print(f"  ⏱️ Duration: {duration}")
    print(f"  ⏳ Delay:    {delay_minutes} minutes")
    print("=" * 72)
    
    cmd = [
        "gh", "workflow", "run", "stream.yml",
        "-f", f"stream_key={stream_key}",
        "-f", f"video_name={video_name}",
        "-f", f"duration={duration}",
        "-f", f"delay_minutes={delay_minutes}",
        "-f", "relay_part=1"
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Workflow trigger command executed successfully!")
        
        # Wait 3 seconds and get latest run info
        time.sleep(3)
        info_cmd = ["gh", "run", "list", "--workflow=stream.yml", "--limit", "1"]
        run_res = subprocess.run(info_cmd, capture_output=True, text=True)
        if run_res.returncode == 0 and run_res.stdout.strip():
            print()
            print("📋 Latest GitHub Run Details:")
            print(run_res.stdout.strip())
        
        print()
        print("=" * 72)
        print("🎉 LIVE STREAM SUCCESSFULLY LAUNCHED!")
        print("👉 You can monitor progress on GitHub Actions:")
        print("   https://github.com/Kumarvin204/VKSGroupStream/actions")
        print("👉 Check your stream in YouTube Studio:")
        print("   https://studio.youtube.com/channel/UC.../livestreaming")
        print("=" * 72)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to trigger workflow: {e.stderr or e.stdout}")
        print("Tip: Make sure 'gh' CLI is authenticated ('gh auth status').")

def run_countdown(seconds, target_dt):
    print()
    print(f"⏳ COUNTDOWN ACTIVE: Scheduled for {target_dt.strftime('%d-%b %I:%M %p IST')}")
    print("   [Press Ctrl+C anytime to cancel schedule]")
    print()
    
    try:
        while seconds > 0:
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            time_str = f"{hrs:02d}h:{mins:02d}m:{secs:02d}s"
            sys.stdout.write(f"\r  ⏳ Stream starts in: \033[1;33m{time_str}\033[0m (Target: {target_dt.strftime('%I:%M %p IST')})   ")
            sys.stdout.flush()
            time.sleep(1)
            seconds -= 1
        print("\n\n⏰ Time arrived! Launching live stream now!")
        return True
    except KeyboardInterrupt:
        print("\n\n🛑 Schedule cancelled by user.")
        return False

def main():
    print_banner()
    
    # Step 1: Video
    video_name = choose_video()
    
    # Step 2: Stream Key
    stream_key = choose_stream_key()
    
    # Step 3: Duration
    duration = choose_duration()
    
    # Step 4: Schedule
    sched_type, sched_val, target_dt = choose_schedule()
    
    if sched_type == "immediate":
        trigger_workflow(stream_key, video_name, duration, delay_minutes=0)
    elif sched_type == "cloud_delay":
        trigger_workflow(stream_key, video_name, duration, delay_minutes=sched_val)
    elif sched_type == "local_timer":
        ok = run_countdown(sched_val, target_dt)
        if ok:
            trigger_workflow(stream_key, video_name, duration, delay_minutes=0)
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
