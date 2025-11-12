"""
YouTube Music Player Module
Searches and plays music from YouTube
"""
import subprocess
import threading
import yt_dlp
import os


class YouTubePlayer:
    def __init__(self):
        """Initialize YouTube player"""
        self.current_process = None
        self.is_playing = False
        print("✓ YouTube Player initialized")

    def search_and_play(self, query):
        """
        Search for a song on YouTube and play it

        Args:
            query: Song name or search query

        Returns:
            tuple: (success, message)
        """
        try:
            print(f"\n🔍 Searching YouTube for: '{query}'")

            # Search YouTube for the song with better options
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': False,  # Show progress
                'no_warnings': False,  # Show warnings for debugging
                'default_search': 'ytsearch1',
                'extract_flat': False,
                'socket_timeout': 30,
                'retries': 3,
            }

            print("🌐 Connecting to YouTube...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch1:{query}"
                print(f"📝 Search query: {search_query}")

                info = ydl.extract_info(search_query, download=False)

                if info and 'entries' in info and len(info['entries']) > 0:
                    video = info['entries'][0]
                    if not video:
                        print("❌ No video found in search results")
                        return False, "No results found"

                    video_url = video.get('url')
                    video_title = video.get('title', 'Unknown')

                    if not video_url:
                        print("❌ No playable URL found")
                        return False, "Can't get video URL"

                    print(f"✅ Found: {video_title}")
                    print(f"🔗 URL obtained, starting playback...")

                    # Play the audio
                    success = self.play_audio(video_url, video_title)

                    if success:
                        return True, f"Playing {video_title}"
                    else:
                        return False, "Failed to start playback"
                else:
                    print("❌ No search results found")
                    return False, "Could not find the song on YouTube"

        except Exception as e:
            print(f"❌ Error playing YouTube: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error: {str(e)}"

    def play_audio(self, url, title):
        """
        Play audio from URL using available player

        Args:
            url: Audio URL
            title: Song title

        Returns:
            bool: True if playback started successfully
        """
        try:
            # Try mpv first (best option)
            print("🎮 Trying mpv player...")
            self.current_process = subprocess.Popen(
                ['mpv', '--no-video', '--really-quiet', url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_playing = True
            print(f"✅ Playing with mpv: {title}")
            return True

        except FileNotFoundError:
            print("⚠️  mpv not found, trying ffplay...")
            try:
                # Fallback to ffplay
                self.current_process = subprocess.Popen(
                    ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.is_playing = True
                print(f"✅ Playing with ffplay: {title}")
                return True

            except FileNotFoundError:
                print("⚠️  ffplay not found, trying vlc...")
                try:
                    # Fallback to vlc
                    self.current_process = subprocess.Popen(
                        ['cvlc', '--play-and-exit', '--quiet', url],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    self.is_playing = True
                    print(f"✅ Playing with vlc: {title}")
                    return True

                except FileNotFoundError:
                    print("❌ No media player found!")
                    print("📝 Install one with: sudo apt-get install mpv")
                    return False
        except Exception as e:
            print(f"❌ Error starting playback: {e}")
            return False

    def stop(self):
        """Stop currently playing music"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=2)
                self.is_playing = False
                print("⏹️  Music stopped")
                return True, "Music stopped"
            except Exception as e:
                try:
                    self.current_process.kill()
                    self.is_playing = False
                except:
                    pass
                return False, "Error stopping music"
        else:
            return False, "No music is playing"

    def pause(self):
        """Pause/resume playback (not supported by all players)"""
        if self.current_process:
            try:
                # Send SIGSTOP to pause (Linux only)
                os.kill(self.current_process.pid, 19)  # SIGSTOP
                return True, "Music paused"
            except:
                return False, "Pause not supported"
        return False, "No music is playing"

    def is_playing_music(self):
        """Check if music is currently playing"""
        if self.current_process:
            return self.current_process.poll() is None
        return False
