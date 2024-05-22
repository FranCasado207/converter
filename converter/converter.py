import sys
import os
import glob
import ffmpy
import click
import shutil
import subprocess

def get_frame_rate(input_file):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    frame_rate = result.stdout.strip()
    return frame_rate

def convert_to_gif(file, fileOutput):
    palette_file = 'palette.png'
    if os.path.isfile(palette_file):
        os.remove(palette_file)

    ff_palette = ffmpy.FFmpeg(
        inputs={file: None},
        outputs={palette_file: f'-vf "fps={get_frame_rate(file)},palettegen"'}
    )
    ff_palette.run()
    
    ff_gif = ffmpy.FFmpeg(
        inputs={file: None, palette_file: None},
        outputs={fileOutput: f'-lavfi "fps={get_frame_rate(file)}[x]; [x][1:v] paletteuse" -c:v gif'}
    )
    ff_gif.run()



@click.command()
@click.option('--path', '-p', help='Designate the path.')

def main(path):
    filesMP4 = []
    filesMP4backup = []
    ##mudar cwd
    try:
        os.chdir(path)
    except WindowsError as e:
        if e.winerror == 2:
            print('Caminho não existe')
    except Exception as e:
        print(e)
    else:
        #buscar todos os ficheiros mp4
        for file in glob.glob('*.mp4'):
            filesMP4.append(file)
    #verifica se existe
    if len(filesMP4) == 0:
        print('Não existe ficheiros neste caminho')
        return 0
    else:
        #cria path backup
        os.mkdir('backup')
        for file in filesMP4:
            #envia todos os ficheiros para a pasta backup
            shutil.move(file, 'backup')   
    #mudar cwd para backup
    os.chdir('backup')
    #buscar todos os ficheiros mp4
    for file in glob.glob('*.mp4'):
            #guarda
            filesMP4backup.append(file)
    #para cada ficheiro
    for file in filesMP4backup:
        #cria um nome para o gif
        fileOutput = os.path.basename(file)
        #output
        convert_to_gif(file, fileOutput+'.gif')
    #se a pallete existir deleta
    if os.path.isfile('palette.png'):
        os.remove('palette.png')
    #remove mp4s
    for file in filesMP4backup:
        if os.path.isfile(file):
            os.remove(file)
    #envia todos os gifs para a pasta antiga
    for file in glob.glob('*.gif'):
        shutil.move(file, '..\\')
    #muda para a pasta antiga
    os.chdir('..\\')
    #deleta a pasta backup
    os.rmdir('backup')
    print('Completo!!!')
    


if __name__ == '__main__':
    main()