from celery import shared_task
from .models import Video, VideoFile
from django.conf import settings
import subprocess
import os
import uuid

@shared_task
def transcode_video(video_id):
    try:
        video = Video.objects.get(id=video_id)
        original_path = video.original_file.path

        file_extension = os.path.splitext(original_path)[1]

        resolutions = {
            '1080p': ('1920x1080', '5M'),
            '720p': ('1280x720', '2M'),
            '480p': ('854x480', '1M'),
            '360p': ('640x360', '700k'),
        }

        for name, (res, bitrate) in resolutions.items():
            unique_filename = f"{uuid.uuid4()}_{name}{file_extension}"
            output_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'videos', unique_filename)
            
            # ❗️따옴표와 shell=True를 사용하도록 FFmpeg 명령어 수정
            cmd = f'ffmpeg -i "{original_path}" -vf scale={res} -c:v libx264 -b:v {bitrate} -c:a aac -b:a 128k -preset fast -y "{output_path}"'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, encoding='utf-8')

            if result.returncode != 0:
                print(f"FFmpeg Error for {name}:", result.stderr)
                continue
            
            relative_path = os.path.join('uploads', 'videos', unique_filename)
            VideoFile.objects.create(
                video=video,
                resolution=name,
                file=relative_path
            )
            
        return f"Video {video_id} transcoding completed."

    except Video.DoesNotExist:
        return f"Video with id {video_id} does not exist."
    except Exception as e:
        return f"Error transcoding video {video_id}: {str(e)}"