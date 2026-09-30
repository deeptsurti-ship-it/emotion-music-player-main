import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emotion_player.settings')
django.setup()

from app.models import EmotionSong
from django.core.files import File

def add_songs_from_folder():
    """Add all downloaded songs to the database based on filename"""
    
    songs_folder = Path("downloaded_songs")
    if not songs_folder.exists():
        print("❌ Downloaded songs folder not found!")
        return
    
    # Emotion mapping (model choices use capitalized names: Happy, Sad, Angry, etc.)
    emotion_mapping = {
        'happy': 'Happy',
        'sad': 'Sad', 
        'angry': 'Angry',
        'fear': 'Fear',
        'surprise': 'Surprise',
        'disgust': 'Disgust',
        'neutral': 'Neutral'
    }
    
    # Artist mapping for better metadata
    artist_mapping = {
        'happy': 'Happy Vibes Artist',
        'sad': 'Melancholy Artist',
        'angry': 'Intense Artist', 
        'fear': 'Calming Artist',
        'surprise': 'Dynamic Artist',
        'disgust': 'Cleansing Artist',
        'neutral': 'Balanced Artist'
    }
    
    added_count = 0
    
    # Process each song file
    print("\n🎵 Adding songs to database...")
    
    for file_path in songs_folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.mp3', '.mp4', '.webm', '.wav']:
            emotion_name = file_path.stem.lower()
            
            if emotion_name in emotion_mapping:
                emotion = emotion_mapping[emotion_name]
                
                # Check if song already exists
                existing_song = EmotionSong.objects.filter(
                    emotion=emotion,
                    title__icontains=emotion_name.title()
                ).first()
                
                if existing_song:
                    print(f"⚠️  Song already exists for {emotion_name}: {existing_song.title}")
                    continue
                
                try:
                    # Create the song entry
                    song = EmotionSong.objects.create(
                        title=f"{emotion_name.title()} Vibes",
                        artist=artist_mapping.get(emotion_name, "Unknown Artist"),
                        emotion=emotion,
                    )
                    
                    # Add the file
                    with open(file_path, 'rb') as f:
                        song.song_file.save(
                            f"{emotion_name}{file_path.suffix}",
                            File(f),
                            save=True
                        )
                    
                    print(f"✅ Added {emotion_name.title()} song: {song.title}")
                    added_count += 1
                    
                except Exception as e:
                    print(f"❌ Error adding {emotion_name} song: {str(e)}")
            else:
                print(f"⚠️  Unknown emotion in filename: {file_path.name}")
    
    print(f"\n🎉 Successfully added {added_count} songs to the database!")
    
    # Show summary
    total_songs = EmotionSong.objects.count()
    print(f"📊 Total songs in database: {total_songs}")
    
    print("\n📋 Songs by emotion:")
    for key, emotion in emotion_mapping.items():
        count = EmotionSong.objects.filter(emotion=emotion).count()
        print(f"   {emotion}: {count} songs")

if __name__ == "__main__":
    print("🎵 Adding downloaded songs to database...")
    add_songs_from_folder()
    print("\n✅ Done!")

