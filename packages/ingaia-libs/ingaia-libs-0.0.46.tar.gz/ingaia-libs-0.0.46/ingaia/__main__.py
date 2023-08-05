"""------------------------------
inGaia python utility library
------------------------------
Version: {__version__}
"""
import logging
from ingaia import __version__


def main(*args, **kwargs):
    print(__doc__.replace('{__version__}', __version__))


if __name__ == "__main__":
    main()

    try:
        from ingaia.request_logger.request_logger import generate_rl_token
        from ingaia.request_logger.decode import decode_token

        rl_token = generate_rl_token(f'ingaia-libs{__version__}')
        print(rl_token)
        print(decode_token(rl_token))
    except Exception as e:
        print(f'Request log token generation error: {e}')
