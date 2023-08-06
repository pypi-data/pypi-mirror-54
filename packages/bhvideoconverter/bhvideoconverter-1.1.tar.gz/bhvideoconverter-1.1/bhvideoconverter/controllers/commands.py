from cement import Controller, ex
import ffmpeg
import pathlib
import os

class commands(Controller):
    class Meta:
        label = 'bhvideoconverter_commands'



    @ex(
        help='remove sound from video',
        arguments = [
            (
                ['--videopath', '-v'],
                {
                    'help': 'enter video path you want to extract'
                }
            ),
            (
                ['--outputfilepath', '-o'],
                {
                    'help': 'enter out put of file with name end format for e.g:/Desktop/test.mp4'
                }
            ),
            (
                ['--fps', '-f'],
                {
                    'help': 'frams of video'
                }
            )
        ]
    )

    def RemoveSound(self):
        if self.app.pargs.videopath is None and self.app.pargs.outputfilepath is None:
            self.app.log.error('You must add the path of file')
        else:
            if self.app.pargs.fps is None:
                self.app.log.info('Video path: %s' % self.app.pargs.videopath)
                self.app.log.info('out path: %s' % self.app.pargs.outputfilepath)
                FilePath = self.app.pargs.videopath
                OutPutPath = self.app.pargs.outputfilepath
                stream = ffmpeg.input(FilePath)
                stream = ffmpeg.hflip(stream)
                stream = ffmpeg.output(stream, OutPutPath)
                ffmpeg.run(stream)
            else:
                self.app.log.info('Video Path: %s' % self.app.pargs.videopath)
                self.app.log.info('out path: %s' % self.app.pargs.outputfilepath)
                self.app.log.info('FPS: %s' % self.app.pargs.fps)
                FilePath = self.app.pargs.videopath
                OutPutPath = self.app.pargs.outputfilepath
                FPS = self.app.pargs.fps
                stream = ffmpeg.input(FilePath)
                stream = ffmpeg.hflip(stream).filter('fps', fps=FPS)
                stream = ffmpeg.output(stream, OutPutPath)
                ffmpeg.run(stream)


    @ex(
        help='merge specific video with specific audio',
        arguments = [
            (
                ['--audiofilepath', '-a'],
                {
                    'help': 'enter audio file path'
                }
            ),
            (
                ['--videofilepath', '-v'],
                {
                    'help': 'enter video file path'
                }
            ),
            (
                ['--outputfilepath', '-o'],
                {
                    'help': 'enter out put of file with name end format for e.g:/Desktop/test.mp4'
                }
            ),
            (
                ['--fps', '-f'],
                {
                    'help': 'frames of video'
                }
            )
        ]
    )
    def MergeVideo(self):
        if self.app.pargs.videofilepath is None and self.app.pargs.audiofilepath is None and self.app.pargs.outputfilepath is None:
            self.app.log.error('you must add Video path and Output path')
        else:
            if self.app.pargs.fps is None:
                self.app.log.info('video path: %s' % self.app.pargs.videofilepath)
                self.app.log.info('audio path: %s' % self.app.pargs.audiofilepath)
                self.app.log.info('out put: %s' % self.app.pargs.outputfilepath)
                AudioPath = self.app.pargs.audiofilepath
                OutputPath = self.app.pargs.outputfilepath
                VideoPath = self.app.pargs.videofilepath
                vinput = ffmpeg.input(VideoPath)
                ainput = ffmpeg.input(AudioPath)
                v1 = vinput.video.hflip()
                a1 = ainput.audio
                output = ffmpeg.output(v1, a1, OutputPath)
                output.run()
            else:
                self.app.log.info('video path: %s' % self.app.pargs.videofilepath)
                self.app.log.info('audio path: %s' % self.app.pargs.audiofilepath)
                self.app.log.info('out put: %s' % self.app.pargs.outputfilepath)
                self.app.log.info('frams: %s' % self.app.pargs.fps)
                VideoPath = self.app.pargs.videofilepath
                AudioPath = self.app.pargs.audiofilepath
                OutputPath = self.app.pargs.outputfilepath
                FPS = int(self.app.pargs.fps)
                vinput = ffmpeg.input(VideoPath)
                ainput = ffmpeg.input(AudioPath)
                v1 = vinput.video.hflip().filter('fps', fps=FPS)
                a1 = ainput.audio
                output = ffmpeg.output(v1, a1, OutputPath)
                output.run()

    @ex(
        help='Convert specific video format to another format',
        arguments= [
            (
                ['--videopath', '-v'],
                {
                    'help': 'video file path'
                }
            ),
            (
                ['--outputpath', '-o'],
                {
                    'help': 'output file path with format e.x:/Destop/output.mov'
                }
            ),
            (
                ['--fps', '-f'],
                {
                    'help': 'frames of video'
                }
            )
        ]
    )
    def ConvertVideo(self):

        if self.app.pargs.videopath is None:
            self.app.log.error('You must add the path of file')
        else:
            if self.app.pargs.outputpath is None:
                self.app.log.error('You must add the output of file')
            else:
                if self.app.pargs.fps is None:          
                    filePath = self.app.pargs.videopath
                    output = self.app.pargs.outputpath
                    self.app.log.info('file path: %s' % filePath)
                    self.app.log.info('out put: %s' % output)

                    input1 = ffmpeg.input(filePath)
                    v1 = input1.video.hflip()
                    a1 = input1.audio
                    outputFile = ffmpeg.output(v1, a1, output)
                    outputFile.run()
                else:
                    filePath = self.app.pargs.videopath
                    output = self.app.pargs.outputpath
                    fps = int(self.app.pargs.fps)
                    self.app.log.info('file path: %s' % filePath)
                    self.app.log.info('out put: %s' % output)
                    self.app.log.info('frams: %s' % fps)
                    input1 = ffmpeg.input(filePath)
                    v1 = input1.video.hflip().filter('fps', fps=fps)
                    a1 = input1.audio
                    outputFile = ffmpeg.output(v1, a1, output)
                    outputFile.run()


    @ex(
        help='convert multiple videos from folder',
        arguments = [
            (
                ['--folderpath', '-fp'],
                {
                    'help': 'enter folder path and put all videos you want to converted'
                }
            ),
            (
                ['--outputfolderpath', '-o'],
                {
                    'help': 'enter output of folder you want put all converted videos'
                }
            ),
            (
                ['--videoformat', '-e'],
                {
                    'help': 'enter format you want to convert all videos to it'
                }
            ),
            (
                ['--fps', '-f'],
                {
                    'help': 'frames of video'
                }
            )
        ]
    )
    def ConvertVideos(self):

        if self.app.pargs.folderpath is None:
            self.app.log.error('You must add the path of folder')
        else:
            if self.app.pargs.outputfolderpath is None:
                self.app.log.error('You must add the output folder path')
            else:
                if self.app.pargs.videoformat is None:
                    self.app.log.error('You must add format to convert videos to it')
                else:
                    if self.app.pargs.fps is None:
                        FolderPath = self.app.pargs.folderpath
                        OutPutFolder = self.app.pargs.outputfolderpath
                        VideoFormat = self.app.pargs.videoformat
                        self.app.log.info('Folder path: %s' % FolderPath)
                        self.app.log.info('Output path: %s' % OutPutFolder)
                        self.app.log.info('Video format: %s' % VideoFormat)
                        arr = os.listdir(FolderPath)
                        for item in arr:
                            itemPath = FolderPath + '/' + item
                            ItemExtension = pathlib.PurePosixPath(itemPath).suffix
                            ItemWithoutExtension = item.replace(ItemExtension, '')
                            self.app.log.info('video: %s' % itemPath)
                            input1 = ffmpeg.input(itemPath)
                            v1 = input1.video.hflip()
                            a1 = input1.audio
                            output = str(OutPutFolder + '/' + ItemWithoutExtension + '.' + VideoFormat)
                            outputfile = ffmpeg.output(v1, a1, output)
                            outputfile.run()
                    else:
                        FolderPath = self.app.pargs.folderpath
                        OutPutFolder = self.app.pargs.outputfolderpath
                        VideoFormat = self.app.pargs.videoformat
                        FPS = int(self.app.pargs.fps)
                        self.app.log.info('Folder path: %s' % FolderPath)
                        self.app.log.info('Output path: %s' % OutPutFolder)
                        self.app.log.info('Video format: %s' % VideoFormat)
                        self.app.log.info('FPS: %s' % FPS)
                        arr = os.listdir(FolderPath)
                        for item in arr:
                            itemPath = FolderPath + '/' + item
                            ItemExtension = pathlib.PurePosixPath(itemPath).suffix
                            ItemWithoutExtension = item.replace(ItemExtension, '')
                            self.app.log.info('video: %s' % itemPath)
                            input1 = ffmpeg.input(itemPath)
                            v1 = input1.video.hflip().filter('fps', fps=FPS)
                            a1 = input1.audio
                            output = str(OutPutFolder + '/' + ItemWithoutExtension + '.' + VideoFormat)
                            outputfile = ffmpeg.output(v1, a1, output)
                            outputfile.run()