
import os
from argparse import ArgumentParser
from multiprocessing import Pool, Process
import time


def transcode(segment):
    name = segment.split('.m2ts')[0]
    cmd = 'ffmpeg -i {segment} -c:v libx264 -tune animation -profile:v high -level 4.2 -b:v 3000k -c:a copy -threads 6 output/{output}.mp4'.format(
        segment='tmp/{}'.format(segment), output=name)
    os.system(cmd)
    open('output/{}.SUCESS'.format(name), 'w').close()


def main(source):
    cmd = 'ffmpeg -i {source} -c:a aac -b:a 320k -map 0 -f segment -segment_time 600 tmp/main_%02d.m2ts'.format(source=source)
    os.system(cmd)
    segments = [x for x in os.listdir('tmp/')]
    pool = Pool(processes=14)
    pool.map(transcode, segments)

    with open('output/ts.list', 'w') as writer:
        for segment in sorted(os.listdir('output/')):
            if '.SUCESS' in segment:
                filename = segment.replace('.SUCESS', '.mp4')
                writer.write('file \'{}\''.format(filename))
                writer.write('\n')

    cmd = 'ffmpeg -f concat -safe 0 -i output/ts.list -c copy output.mp4 '
    os.system(cmd)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', dest='source')
    args = parser.parse_args()
    os.makedirs('tmp/', exist_ok=True)
    os.makedirs('output/', exist_ok=True)
    main(args.source)
