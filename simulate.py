#################################################################################
#  This file is part of The AI Sandbox.
#
#  Copyright (c) 2007-2012, AiGameDev.com
#
#  Credits:         See the PEOPLE file in the base directory.
#  License:         This software may be used for your own personal research
#                   and education only.  For details, see the LICENSING file.
#################################################################################

import bootstrap
import sys

from aisbx import platform
from aisbx import callstack

from game.application import CaptureTheFlag


# By default load these commanders.
defaults = ['examples.Random', 'examples.Balanced']


def main(PreferedRunner, args, **kwargs):
    """
        Setup our custom demo application, as well as a window-mode runner,
        and launch it.  This function returns once the demo is over.
            - If RCTRL+R is pressed, the application is restarted.
            - On RCTRL+F, the game code is dynamically refreshed.
    """
    while True:
        runner = PreferedRunner()

        if not args:
            args = defaults

        app = CaptureTheFlag(args, **kwargs)
        if not runner.run(app):
            break
        r = app.reset
        del runner
        del app

        if not r:
            break
        else:
            import gc
            gc.collect()

            from reload import reset
            reset()


# This is the entry point for the whole application.  The main function is
# called only when the module is first executed.  Subsequent resetting or
# refreshing cannot automatically update this __main__ module.
if __name__ == '__main__':
    import sys

    try:
        if '--console' in sys.argv:
            sys.argv.remove('--console')
            main(platform.ConsoleRunner, sys.argv[1:], quiet = True)
        else:
            if '--windowed' in sys.argv:
                sys.argv.remove('--windowed')
            main(platform.WindowRunner, sys.argv[1:])

    except Exception as e:
        print str(e)
        tb_list = callstack.format(sys.exc_info()[2])
        for s in tb_list:
            print s
        raise
