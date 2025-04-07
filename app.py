from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os
from tqdm import tqdm

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    format = data['format']

    try:
        yt = YouTube(url)
        if format == 'mp3':
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download()
            base, ext = os.path.splitext(out_file)
            new_file = base + ".mp3"
            os.rename(out_file, new_file)
            message = "Successfully Downloaded as MP3"
        elif format == 'mp4':
            # Get the highest resolution video stream
            video = yt.streams.filter(file_extension='mp4').get_highest_resolution()

            # Get the file size for progress bar
            file_size = video.filesize

            # Download with tqdm progress bar
            with tqdm(total=file_size, unit='B', unit_scale=True, desc='Downloading') as bar:
                video.download(output_path='downloads', filename='video')
                bar.update(file_size)

            message = "Successfully Downloaded as MP4 in high resolution"
        else:
            message = "Invalid format specified"

    except Exception as e:
        message = f"Error: {str(e)}"

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)
