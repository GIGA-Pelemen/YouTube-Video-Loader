import os
from pathlib import Path
import yt_dlp
from yt_dlp.extractor import get_info_extractor
import sys

def get_video_formats(url):
    """
    Получает доступные форматы видео
    
    Args:
        url: Ссылка на видео YouTube
    Returns:
        list: Список форматов видео, отсортированный по качеству
    """
    try:
        # Используем базовый экстрактор вместо автоматического определения
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'no_warnings': True # Отключаем предупреждения
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info['formats']:
                if f.get('resolution') != 'audio only':
                    formats.append({
                        'format_id': f['format_id'],
                        'ext': f.get('ext','?'),
                        'resolution': f.get('resolution','?')
                    })
            formats.sort(key=lambda x: x['resolution'], reverse=True)
            return formats
    except Exception as e:
        print(f"Ошибка при получении форматов: {str(e)}")
        return []

def download_youtube_video(url, output_path=".", quality_index=0):
    """
    Скачивает видео с YouTube используя yt-dlp
    
    Args:
        url: Ссылка на видео YouTube
        output_path: Путь для сохранения видео
        quality_index: Индекс качества (0 - самое высокое)
    """
    try:
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        formats = get_video_formats(url)
        if not formats:
            raise Exception("Не удалось получить форматы видео")
            
        if quality_index >= len(formats):
            quality_index = len(formats) - 1
            
        selected_format = formats[quality_index]
        
        ydl_opts = {
            'format': f"{selected_format['format_id']}+bestaudio[ext=m4a]/best",
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'merge_output_format': 'mp4'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print(f"\nВидео успешно скачано в качестве {selected_format['resolution']}!")
            
    except Exception as e:
        print(f"\nПроизошла ошибка при скачивании: {str(e)}")
        print("\nДоступные форматы видео:")
        formats = get_video_formats(url)
        for i, f in enumerate(formats):
            print(f"{i}: {f['resolution']} ({f['ext']})")

def main():
    print("=== YouTube Video Downloader ===")
    while True:
        video_url = input("\nВведите ссылку на видео YouTube (или 'q' для выхода): ")
        
        if video_url.lower() == 'q':
            break
            
        formats = get_video_formats(video_url)
        if formats:
            print("\nДоступные форматы видео:")
            for i, f in enumerate(formats):
                print(f"{i}: {f['resolution']} ({f['ext']})")
            
            while True:
                try:
                    quality = int(input("\nВыберите качество (0 - самое высокое): "))
                    if quality >= 0:
                        break
                    print("Пожалуйста, введите число >= 0")
                except ValueError:
                    print("Пожалуйста, введите корректное число")
                
            # Получаем текущую директорию, где запущен скрипт
            current_dir = os.getcwd()
                
            download_youtube_video(video_url, current_dir, quality)
            
            if input("\nХотите скачать еще видео? (y/n): ").lower() != 'y':
                break
        else:
            print("Не удалось получить информацию о форматах видео")
    
    print("\nВыход...")

if __name__ == "__main__":
    main()
