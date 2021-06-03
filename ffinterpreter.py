import os
import subprocess
import json
import sys
import tempfile
import random
import time
import concurrent.futures
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('wxAgg')


def main():

    # probem()
    #
    # probe = FFInterpreter.ffprobe(('-hide_banner', '-show_format', '-show_streams', '-of', 'json'), "sample.mp4")
    # print(type(probe))
    # print(probe)
    #
    # video1 = FFInterpreter("sample-vids/sample_1")
    # # x = str(video.probe_out).replace(",", "\n")
    # # print(x)
    # print(video1.vcodec)
    # print(sys.platform)
    # video2 = FFInterpreter("sample-vids/sample_2")
    #
    # cmd = "./ffmpeg-4.4-amd64-static/ffprobe -loglevel error -skip_frame nokey" \
    #       " -select_streams v:0 -show_entries frame=pkt_pts_time -of json sample-vids/sample_6"
    # liveout(cmd)
    #
    # filem = "sample-vids/sample_" + str(9)
    # video = FFInterpreter(filem)
    # video.fix()
    # specimen = video.specimen(3, 10)
    # encode_out_0 = TempFile.out(video.filename, 0)
    # encode_out_1 = TempFile.out(video.filename, 1)
    # encode_out_2 = TempFile.out(video.filename, 2)
    # encode_out_3 = TempFile.out(video.filename, 3)
    # vid_specimen = FFInterpreter(specimen)
    # vid_specimen.h264encode(encode_out_0, 36)
    # vid_specimen.h264encode(encode_out_1, 31, size=(640, 360))
    # vid_specimen.h264encode(encode_out_2, 30, size=(640, 360))
    # vid_specimen.h264encode(encode_out_3, 29, size=(640, 360))
    # vid_encoded_0 = FFInterpreter(encode_out_0)
    # vid_encoded_1 = FFInterpreter(encode_out_1)
    # vid_encoded_2 = FFInterpreter(encode_out_2)
    # vid_encoded_3 = FFInterpreter(encode_out_3)
    # print(FFInterpreter.ssim(specimen, encode_out_0))
    # print(vid_encoded_0.size)
    # print(FFInterpreter.ssim(specimen, encode_out_1))
    # print(vid_encoded_1.size)
    # print(FFInterpreter.ssim(specimen, encode_out_2))
    # print(vid_encoded_2.size)
    # print(FFInterpreter.ssim(specimen, encode_out_3))
    # print(vid_encoded_3.size)

    ssims_all: list = []
    sizes_all: list = []

    for i in range(18, 19):
        if i == 1:
            break
        print(f'{PrintFormat.BOLD}\nVideo number ' + str(i) + f':{PrintFormat.ENDC}')
        filem = "sample-vids/sample_" + str(i)
        video = FFInterpreter(filem)
        video.fix()
        if video.isaudio:
            print('  * acodec:       ' + video.acodec)
            print('  * sample_rate:  ' + str(video.sample_rate))
        else:
            print('  * acodec:       ' + str(video.isaudio))
            print('  * sample_rate:  ' + str(video.isaudio))
        print("  * vcodec:       " + video.vcodec)
        print("  * framerate:   ", video.frame_rate)
        print("  * size:        ", video.size)
        if video.duration:
            print("  * duration:     " + TimeConvert.standard(video.duration))
        # print(video.keyframes())
        specimen = video.specimen(1, 10)
        vid_specimen = FFInterpreter(specimen)
        heights = [144, 240, 360, 480, 720, 1080]
        presets = ["medium", "fast", "faster", "veryfast", "superfast", "ultrafast"]
        crfs = list(range(17, 50, 30))
        # num_encode = len(crfs)
        # num_encode = 1
        # encode_out = [TempFile.out(video.filename, j) for j in range(num_encode)]
        ssims: dict = {}
        sizes: dict = {}
        for height in heights:
            ssims[height]: list = []
            sizes[height]: list = []
        for preset in presets:
            ssims[preset]: list = []
            sizes[preset]: list = []

        fig = plt.figure()
        axes_1 = fig.add_axes([0.15, 0.15, 0.75, 0.75])
        axes_1.set_xlabel('CRF')
        axes_1.set_ylabel('SSIM')
        axes_1.set_title('Quality over CRFs')

        # for height in heights:
        #     if vid_specimen.calc_width(height):
        #         for crf in crfs:
        #             encode_out = TempFile.out(video.filename, crf + height)
        #             vid_specimen.h264encode(encode_out, crf, size=vid_specimen.calc_width(height))
        #             ssims[height].append(FFInterpreter.ssim(specimen, encode_out))
        #             vid_encoded = FFInterpreter(encode_out)
        #             sizes[height].append(vid_encoded.size)
        #         label = str(height) + 'p'
        #         axes_1.plot(crfs, ssims[height], label=label)

        for preset in presets:
            for crf in crfs:
                encode_out = TempFile.out(video.filename + preset, crf)
                vid_specimen.h264encode(encode_out, crf, preset=preset)
                ssims[preset].append(FFInterpreter.ssim(specimen, encode_out))
                vid_encoded = FFInterpreter(encode_out)
                sizes[preset].append(vid_encoded.size)
            label = preset
            axes_1.plot(crfs, ssims[preset], label=label)

        axes_1.set_xlim(xmin=crfs[0])
        axes_1.legend(loc=0)
        plt.grid(True, 'both', 'both')
        plt.savefig(TempFile.pltout("plot", 0))

        plt.show()


        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     proc = {executor.submit(encode_mp, out, vid_specimen) for out in encode_out}
        #     for done in concurrent.futures.as_completed(proc):
        #         print("encode successful")
        #         print("\n".join(done.result()))

        # encode_out = TempFile.out(video.filename)
        # video.h264encode(encode_out, 50)
        # vid_encoded = FFInterpreter(encode_out)
        # print(FFInterpreter.ssim(specimen, encode_out))
        # print(vid_encoded.size)
        # if FFConsts.VERBOSE:
        #     print('importing successfull')


def encode_mp(out, vid_specimen):
    vid_specimen.h264encode(out, 30)
    vid_encoded = FFInterpreter(out)
    return [str(FFInterpreter.ssim(vid_specimen.file, out)), str(vid_encoded.size)]

    # vid8 = FFInterpreter("sample-vids/sample_8")

    # vid0.h264encode(TempFile.out(0), 50)
    # vid8.specimen()

    # with tempfile.TemporaryDirectory() as tmp:
    #     print(tmp)
    # print(random.randint(0, 1))




'''
    def probem():
    cmd = "./ffmpeg-4.4-amd64-static/ffprobe -show_format -hide_banner -show_streams -of json sample.mp4"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    rc = sp.wait()
    out, err = sp.communicate()
    print(out)
'''


class CmdRun:
    """
    this just recieves a command and passes it to the OS and returns the output :)
    """
    @staticmethod
    def run(cmd: str = ""):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = []
        for c in iter(lambda: process.stdout.read(1), b''):
            out.append(c.decode('utf-8'))
        err = []
        for c in iter(lambda: process.stderr.read(1), b''):
            err.append(c.decode('utf-8'))
        return "".join(out), "".join(err)


class TempFile:
    """
    addresses and file names auto generated just to be tidier
    """
    @staticmethod
    def randhex():
        return str(hex(random.randint(1, 999999)))

    @staticmethod
    def out(name, i):
        return FFConsts.CACHE + "Temp_out_" + name + "_" + TempFile.randhex() + f"_{str(i)}_" + ".mkv"

    @staticmethod
    def pltout(name, i):
        return FFConsts.CACHE + "Temp_pltout_" + name + "_" + TempFile.randhex() + f"_{str(i)}_" + ".png"

    @staticmethod
    def specimen(name: str = ""):
        return FFConsts.CACHE + "specimen_" + name + "_" + TempFile.randhex() + '.mkv'

    @staticmethod
    def fix(name: str = ""):
        return FFConsts.CACHE + "fix_" + name + "_" + TempFile.randhex() + '.mkv'



class TimeConvert:
    """
    didn't check if a library for this exists or not but here it is anyways
    it recieves seconds and converts it to hh:mm:ss
    """
    @staticmethod
    def standard(seconds):
        hour = int(seconds / 3600)
        minute = int((seconds % 3600) / 60)
        second = int((seconds % 3600) % 60)
        standardt = []
        if hour < 10:
            standardt.append("0" + str(hour))
        elif 100 > hour > 9:
            standardt.append(str(hour))
        else:
            print("Error")  # write error
            exit(1)
        if minute < 10:
            standardt.append("0" + str(minute))
        elif 60 > minute > 9:
            standardt.append(str(minute))
        else:
            print("Error")  # write error
            exit(1)
        if second < 10:
            standardt.append("0" + str(second))
        elif 60 > second > 9:
            standardt.append(str(second))
        else:
            print("Error")  # write error
            exit(1)
        return ":".join(standardt)


class PrintFormat:
    """
    colored text codes for print()
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class FFConsts:
    """
    constants so the can be accesible from outside the file
    """
    FF_DIR = './ffmpeg-4.4-amd64-static/'
    CACHE = '.cache/'
    VERBOSE = True
    FFPROBE_ARGS = ('-hide_banner', '-show_format', '-show_streams', '-v', 'quiet', '-of', 'json')
    VQA_comparison = 0


class FFInterpreter:
    """
    the main guy is here it handles all of the core funcions
    when creating an FFInterpreter object always run
    self.fix() right after to avoid issues with corrupted files
    """

    def __init__(self, file):
        """
        this guy recieves the addres to the file and gets the charachteristics of the video using ffprobe and
        initiates a class instance

        """
        self.file = file
        self.filename = os.path.basename(self.file)
        probe_out = FFInterpreter.ffprobe(FFConsts.FFPROBE_ARGS, file)
        if FFConsts.VERBOSE:
            print('setting ffprobe values')
        try:
            # extract and sort data
            self.probe_out = probe_out
            self.streams = probe_out['streams']
            self.format = probe_out['format']
            '''
            if len(self.streams) > 2:
                print(f'{PrintFormat.FAIL}Error: File contains more than two streams.{PrintFormat.ENDC}')
                exit(1)
            '''
            self.isvideo = False
            self.isaudio = False
            for i in self.streams:
                if i["codec_type"] == "video":
                    self.video = i
                    self.isvideo = True
                elif i["codec_type"] == "audio":
                    self.audio = i
                    self.isaudio = True
            # add audio and video bitrates                          # important
            if not self.isvideo:
                print(f'{PrintFormat.FAIL}Error: File does not contain any video streams.{PrintFormat.ENDC}')
                exit(1)

            # video stream
            if self.isvideo:
                self.vcodec = self.video['codec_name']
                self.width = int(self.video['width'])
                self.height = int(self.video['height'])
                if 'pic_fmt' in self.video:
                    self.pix_fmt = self.video['pix_fmt']
                else:
                    self.pix_fmt = False
                if 'profile' in self.video:
                    self.profile = self.video['profile']
                else:
                    self.profile = False
                if 'r_frame_rate' in self.video:
                    framerate_raw = self.video['r_frame_rate'].split('/')
                    self.frame_rate = round(int(framerate_raw[0])/int(framerate_raw[1]), 3)
                else:
                    self.frame_rate = False
            # audio stream
            if self.isaudio:
                self.acodec = self.audio['codec_name']
                self.sample_rate = int(self.audio['sample_rate'])
            # format
            if 'duration' in self.format:
                self.duration = float(self.format["duration"])
            else:
                self.duration = False
            if 'size' in self.format:
                self.size = int(self.format['size'])
            else:
                self.size = False

            if 'bit_rate' in self.format:
                self.bitrate = int(self.format['bit_rate'])
            else:
                self.bitrate = False

            self.specimen_out = False

        except KeyError as keyerr:
            print(f'{PrintFormat.FAIL}Property not found:', keyerr, f'{sys.exc_info()}{PrintFormat.ENDC}')
            raise KeyError

        if FFConsts.VERBOSE:
            print('importing video was successful')

    def fix(self):
        # fix the file if needed
        fixed = self.try_fix()
        if fixed:
            self.__init__(fixed)
        if self.duration is False or self.frame_rate is False:
            print(f'{PrintFormat.FAIL}Error: File does is corrupted.{PrintFormat.ENDC}')
            exit(1)

    def h264encode(self, out: str = "",
                   crf: int = 24,
                   framerate: float = 23.976,
                   preset: str = "veryfast",
                   size: tuple = (0, 0),
                   tune: str = "",
                   start: int = 0,
                   duration: int = 0):

        """
        h264 encoding for self
        """
        infile: list = [self.file, ]
        outfile: str = out
        outoptions: list = [
            "-c:a", "copy",
            "-c:v", "h264",
            "-movflags", "+faststart",
            "-crf", str(crf),
            "-y",
            "-v", "quiet"
        ]

        if self.frame_rate > (int(framerate) + 1):
            outoptions.append("-r")
            outoptions.append(str(framerate))

        if duration != 0:
            outoptions.append("-t")
            outoptions.append(TimeConvert.standard(duration))

        if tune != "":
            outoptions.append("-tune")
            outoptions.append(tune)

        if preset != "veryfast":
            outoptions.append("-preset")
            outoptions.append(preset)

        if size != (0, 0):
            size_ls = list(size)
            size_str = [
                str(size_ls[0]), str(size_ls[1])
            ]
            outoptions.append("-s")
            outoptions.append("x".join(size_str))

        if start != 0:
            inoptions: list = ["-ss", start]
        else:
            inoptions: list = []
        FFInterpreter.ffmpeg(tuple(infile), outfile, tuple(outoptions), tuple(inoptions))

    def try_fix(self):
        """
        makes sure the file has the important parameters
        for our program to funcion correctly

        """
        if self.duration is False\
                or self.frame_rate is False:
            infile = [self.file]
            outfile = TempFile.fix(self.filename)
            outoptions = ["-c", "copy", "-movflags", "+faststart", "-pix_fmt", "yuv420p"]
            inoptions = []
            FFInterpreter.ffmpeg(tuple(infile), outfile,
                                 tuple(outoptions), tuple(inoptions))
            return outfile
        else:
            return False

    def calc_width(self, height):
        if height < self.height:
            cwidth = (self.width / self.height) * height
            cwidth = int(cwidth)
            if cwidth % 2 != 0:
                cwidth = cwidth + 1
            size: tuple = (cwidth, height)
            return size
        else:
            return False

    def keyframes(self):
        """
        gets the keyframes of a video and stores them in a list
        it could be pretty useful but takes too much time to run and takes up memory

        """
        cmd = "-loglevel error -skip_frame nokey -select_streams v:0 -show_entries frame=pkt_pts_time -of json".split()
        ffout = FFInterpreter.ffprobe(tuple(cmd), self.file)
        frames = ffout['frames']
        keyframes: list = []
        for i in frames:
            keyframes.append(float(i['pkt_pts_time']))
        return keyframes

    def specimen(self, samples: int = 10, duration: float = 1):
        """
        now this guy takes the video and makes a smaller sample out of it
        it could take multiple samples of a set duration and merge them into a new file
        the new file will be identical in terms of codecs and streams to the original one
        """

        if self.duration and self.duration > (samples * duration):
            outfile = TempFile.specimen(self.filename)
            with tempfile.TemporaryDirectory() as tmpdir:
                outoptions = ["-c:a", "copy", "-c:v", "copy", "-y", "-avoid_negative_ts", "1"]
                if FFConsts.VERBOSE:
                    print(tmpdir)
                # keyframes = self.keyframes()
                for i in range(samples):
                    temp_outfile = str(tmpdir) + "/" + str(i) + ".mkv"
                    # keyframe = keyframes[random.randint(0, int(len(keyframes) - 1))]
                    time = random.randint(0, int(self.duration))
                    inoptions: list = ["-ss", str(time)]
                    outoptions_t: list = outoptions + ["-t", str(duration)]
                    FFInterpreter.ffmpeg(tuple([self.file]), temp_outfile,
                                         tuple(outoptions_t), tuple(inoptions))
                    with open(tmpdir + '/concatlist', 'a') as lis:
                        lis.write("file '" + temp_outfile + "'\n")
                    # cut = FFInterpreter(temp_outfile)
                    # print("keyframes", cut.keyframes())

                FFInterpreter.ffmpeg(tuple([tmpdir + '/concatlist']),
                                     outfile,
                                     tuple(['-c', 'copy', '-y']),
                                     tuple(['-f', 'concat', '-safe', '0']))

                # print(self.keyframes())
        elif self.duration:
            outfile = self.file
        else:
            outfile = "0"
        self.specimen_out = outfile
        return outfile

    def tune_h264(self, specimen: str = ""):
        """
        tune encoding parameters

        """
        if specimen != "0":
            pass
        else:
            print(f'{PrintFormat.FAIL}Error: File is corrupted.{PrintFormat.ENDC}')
            exit(1)

    @staticmethod
    def ssim_err(target_ssim: float = 0, ssim: float = 0):
        """
        compare the desired ssim to a given one and return the
        difference

        """
        return target_ssim - ssim

    @staticmethod
    def ssim(ref: str = "", dist: str = ""):
        filter_pre = [
            "[1][0]scale2ref=flags=bicubic[dist][ref]",
            "[dist]setpts=PTS-STARTPTS[distpts]",
            "[ref]setpts=PTS-STARTPTS[refpts]",
            "[distpts][refpts]ssim"
        ]
        filter_complex = '"' + ";".join(filter_pre) + '"'
        infile = (ref, dist)
        outfile = "-"
        outoptions = [
            "-filter_complex", filter_complex,
            "-an",
            "-f", "null"
        ]
        inoptions = ["-hide_banner"]
        raw_ssim = FFInterpreter.ffmpeg(infile, outfile, tuple(outoptions), tuple(inoptions))
        ssim = raw_ssim.splitlines()[-1]
        ssim_1 = ssim.split(":")[-1]
        ssim_all = ssim_1.split(" ")[0]
        return float(ssim_all)



    @staticmethod
    def ffprobe(cmd_tp: tuple = (),
                file: str = "",
                ffprobe_dir=FFConsts.FF_DIR + "ffprobe"):
        """
        this is just a wrapper for the ffprobe command
        """
        cmd_ls = list(cmd_tp)
        cmd_ls.insert(0, ffprobe_dir)
        cmd_ls.append(file)
        cmd = " ".join(cmd_ls)
        if FFConsts.VERBOSE:
            print(cmd)
        '''
        sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print("popen end")
        rc = sp.wait()
        print("wait end")
        out, err = sp.communicate()
        print("communicate end")
        '''
        out, err = CmdRun.run(cmd)
        # print(out)
        # print(err)
        if FFConsts.VERBOSE:
            print('returning ffprobe')
        return json.loads(out)

    @staticmethod
    def ffmpeg(infile_tp: tuple = (),
               outfile: str = "",
               outoptions_tp: tuple = (),
               inoptions_tp: tuple = (),
               ffmpeg_dir=FFConsts.FF_DIR + "ffmpeg"):
        """
        just a wrapper for the ffmpeg command

        """
        infile_ls = list(infile_tp)
        outoptions_ls = list(outoptions_tp)
        inoptions_ls = list(inoptions_tp)
        cmd: list = outoptions_ls
        for i in reversed(range(len(infile_ls))):
            cmd.insert(0, infile_ls[i])
            cmd.insert(0, "-i")

        if inoptions_ls:
            for i in reversed(range(len(inoptions_ls))):
                cmd.insert(0, inoptions_ls[i])

        cmd.insert(0, ffmpeg_dir)
        cmd.append(outfile)
        # print(cmd)
        cmds = " ".join(cmd)
        if FFConsts.VERBOSE:
            print(cmds)
        '''
        sp = subprocess.Popen(cmds, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print("popen end")
        rc = sp.wait()
        print("wait end")
        out, err = sp.communicate()
        print("communicate end")
        '''
        out, err = CmdRun.run(cmds)
        # print(out)
        # print(err)
        if FFConsts.VERBOSE:
            print('ffmpeg done')
        return err


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    time = end_time - start_time
    print(f'{PrintFormat.BOLD}{PrintFormat.OKGREEN}Time: {round(time, 3)}{PrintFormat.ENDC}')