"""Create a narrated MP4 walkthrough from the verified PDF pages and local WAVs.
Requires imageio-ffmpeg only as a build-time dependency.
"""
import sys, subprocess, wave, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tmp/video-deps'))
import imageio_ffmpeg
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
segments=[];offset=0;subtitles=[]
scripts=json.loads((ROOT/'tmp/narration.json').read_text())
def timestamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
for i in range(1,8):
    wav=ROOT/f'tmp/scene-{i}.wav'
    with wave.open(str(wav)) as f:duration=f.getnframes()/f.getframerate()+1
    target=ROOT/f'tmp/video-{i}.mp4'
    cmd=[ffmpeg,'-y','-loglevel','error','-loop','1','-framerate','12','-i',str(ROOT/f'tmp/pitch-{i}.png'),'-i',str(wav),'-vf','scale=1280:720,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','128k','-af','apad','-t',str(duration),'-movflags','+faststart',str(target)]
    subprocess.run(cmd,check=True);segments.append(target)
    words=scripts[i-1].split();chunks=[' '.join(words[j:j+13]) for j in range(0,len(words),13)]
    for j,chunk in enumerate(chunks):
        start=offset+j*(duration-1)/len(chunks);end=offset+(j+1)*(duration-1)/len(chunks)
        subtitles.append(f'{len(subtitles)+1}\n{timestamp(start)} --> {timestamp(end)}\n{chunk}\n')
    offset+=duration
if offset>=180:raise ValueError(f'Demo exceeds three minutes: {offset:.2f}s')
(ROOT/'tmp/concat.txt').write_text('\n'.join("file '"+p.as_posix()+"'" for p in segments))
(ROOT/'submission/NxtGen-Demo.srt').write_text('\n'.join(subtitles),encoding='utf-8')
subprocess.run([ffmpeg,'-y','-loglevel','error','-f','concat','-safe','0','-i',str(ROOT/'tmp/concat.txt'),'-i',str(ROOT/'submission/NxtGen-Demo.srt'),'-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata','title=NxtGen Demand - narrated product walkthrough','-metadata','comment=Synthetic data and computed outputs. Not a recorded browser session.','-movflags','+faststart',str(ROOT/'submission/NxtGen-Demo.mp4')],check=True)
(ROOT/'tmp/video-info.json').write_text(json.dumps({'duration_seconds':round(offset,2),'resolution':'1280x720','narrated':True,'subtitles':'English','type':'Computed-output product walkthrough, not browser recording'},indent=2))
print(f'Created narrated demo: {offset:.2f} seconds, 1280x720, embedded subtitles.')
