#
import logging
import time
import sys
from glob import glob
import joblib
import sys

import torch
import whisper

logging.basicConfig(
    filename=f'whisper_transcribe-{time.strftime("%Y%m%d-%H:%M:%S")}.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%Y%m%d-%H:%M:%S',
    level=logging.INFO,
)


def transcribe_audio(
        model,
        fpath: str,
        base_path: str,
        results_dict: dict,
        audio_ext: str = 'mp3',
        verbose: int = 1,
    ):
    if verbose:
        logging.info(f'Transcribing audio from {fpath}')
    transcript_results = model.transcribe(
        fpath,
        word_timestamps=True,
    )
    results_dict[fpath] = transcript_results
    if verbose:
        logging.info(f'Transcribed {fpath}')
    fname = fpath.split('/')[-1].replace(f'.{audio_ext}', '')
    compressed_fpath = f'{base_path}/text-whisper-{fname}.gz'
    joblib.dump(transcript_results, compressed_fpath)
    if verbose:
        logging.info(f'Saved file to {compressed_fpath}')


if __name__ == '__main__':

    # Only use args as given
    ARG_NAMES = ('command', 'path', 'extension')
    args = dict(zip(ARG_NAMES, sys.argv))
    try:
        MAIN_PATH = args['path']
    except KeyError as err:
        logging.error(f'`{err}` param not provided in CLI args')
        print('Must give a base path to find data')
        raise KeyError(err)
    ext = args.get('extension', 'mp3')

    # Setup for GPU usage
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logging.info(f'Using {device=}')
    if device != 'cuda':
        sys.exit('Not using GPU!!! STOP!!!')

    # Whisper model setup
    # https://huggingface.co/openai/whisper-base.en
    whisper_model_checkpoint = 'large-v2'
    # whisper_model_checkpoint = 'small'

    whisper_model = whisper.load_model(whisper_model_checkpoint).to(device)

    # Transcribe (and save) each audio file (*.m4a)
    
    results = {}
    glob_str = f'{MAIN_PATH}/raw_data/*{ext}'
    print(f'{len(glob(glob_str))} files to process')
    for i,fpath in enumerate(glob(glob_str)):
        results[fpath] = transcribe_audio(
            whisper_model,
            fpath,
            results_dict=results,
            base_path=MAIN_PATH,
            audio_ext=ext,
        )
        print(f'Finished {i}: {fpath}')
