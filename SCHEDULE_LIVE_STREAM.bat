@echo off
chcp 65001 >nul
title 🔴 YouTube Live Stream Scheduler & Controller
cd /d "%~dp0"
echo ======================================================================
echo           🔴 YOUTUBE LIVE STREAM SCHEDULER & CONTROLLER
echo ======================================================================
echo.
python schedule_live_stream.py
pause
