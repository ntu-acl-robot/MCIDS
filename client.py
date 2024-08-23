# -*- coding: UTF-8 -*- 

import requests
import time
import numpy as np
import json
import wave


def send_post_message(msg,url):

    file_name = '<filename>'
    output_name = '<filename>'

    if '.wav' in file_name:
        headers = {"Content-Type":"audio/wav"}  ## 定義請求頭
        with wave.open(file_name, "rb") as wav_in:
            ### check channelNum
            if wav_in.getnchannels() == 2:
                with wave.open(output_name, "wb") as wav_out:
                    ### Set New Channel = 1
                    wav_out.setparams(wav_in.getparams())
                    wav_out.setnchannels(1)

                    frames = wav_in.readframes(wav_in.getnframes())

                    ### Convert to Monochannel
                    mono_frames = b""
                    for i in range(0, len(frames), wav_in.getsampwidth() * 2):
                        mono_frames += frames[i:i + wav_in.getsampwidth()]

                    wav_out.writeframes(mono_frames)

            else:
                print("not MonoFile")
    else:
        print("file with wrong type")
        return

    with open(output_name, 'rb') as file:
        files = {'file':file}
        req = requests.post(url, files=files)   
 
    print(req.status_code)
    if req.status_code == requests.codes.ok:  ## 如果請求正常並收到回復
        print('Sending ok')

        if '.wav' in file_name:
            result = req.json()['PREDICTION']  ##讀取回復
            for k, v in result.items():
                print("%s: %s" % (k, v))


if __name__ == '__main__':
    send_post_message('Web_client_template_test','<server_url>')
