# VALORANT Mature Content Manager - v2.0.1

## 🔒 v2.0.1: locked while in game
- The tool now shows whether you are **in Riot Client** or **in game**.
- While VALORANT is running, the blood / corpse switches, **Save**, **Apply now** and restoring a backup are locked, and the game files are never copied. Changing them mid-game would be overwritten by the game or fail halfway.
- The game is detected from both `VALORANT.exe` and `VALORANT-Win64-Shipping.exe`.
- Auto-apply on Play still works as before: it copies the files a few seconds before the game process starts.

## 🎮 What's New in v2.0
A rewrite for **Patch 13.08**. Since VN accounts no longer show the Mature Content option in game, the tool now handles both things blood and corpses need:

- **Account settings**: turns **Show blood** / **Show corpses** on (or off) for your Riot account, the same way the crosshair tool ValorantCC saves settings. Each Save backs up your previous settings first, and you can restore any backup from the **Advanced** menu.
- **Auto-apply on Play**: watches Riot Client and copies the Mature files right after it finishes checking files, before the game starts. You no longer need to time the copy by hand.
- **New interface**: one window with three steps (Riot Client → Account settings → Game files), a banner that says what to do next, tooltips on every button, and Vietnamese / English.
- Finds the VALORANT install folder automatically and shows it, and warns when the Mature files no longer match the game patch (grey boxes in game).

## 📦 What's Included
- `VALORANT-MatureContent-Manager.exe`: the app (the Mature data files are bundled inside)
- `VALORANT-MatureContent-CLI.exe`: command-line version
- `HuongDan.docx`: step-by-step guide (Vietnamese)

## 🚀 Quick Start
1. Open Riot Client and log in.
2. Run `VALORANT-MatureContent-Manager.exe`.
3. Turn on **Show blood** / **Show corpses** and click **Save** (VALORANT must be closed).
4. Keep **Apply automatically when pressing Play** on and leave the tool open.
5. Press **Play** in Riot Client.

## ⚠️ Important Notes
- **Windows Defender warning** is normal: click "More info" → "Run anyway".
- **Use at your own risk**: modifying game files may lead to account suspension.
- The previous version is kept in `old_script/` in the repository.

**Created by:** @l1ttled1no | **Support:** [YouTube Channel](https://youtube.com/@l1ttled1no)
